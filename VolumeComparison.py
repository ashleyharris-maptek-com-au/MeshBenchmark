import subprocess
import tempfile
import StlVolume
import os
from typing import Dict, Any, Optional



openScadPath = R"C:\Program Files\OpenSCAD\openscad.exe"
if not os.path.exists(openScadPath):
    openScadPath = R"C:\Program Files (x86)\OpenSCAD\openscad.exe"
if not os.path.exists(openScadPath):
    raise FileNotFoundError("OpenSCAD executable not found at expected paths")

def compareVolumeAgainstOpenScad(
    index: int, 
    subPass: int, 
    result, 
    testGlobals: dict
) -> Dict[str, Any]:
    """
    Compare a test result against a reference OpenSCAD model by computing volumes.
    
    Returns a dictionary containing:
        - 'score': float (0.0 to 1.0)
        - 'output_image': path to PNG of output STL
        - 'reference_image': path to PNG of reference STL
    """
    resultToScad = testGlobals["resultToScad"]
    
    if "prepareSubpassReferenceScad" in testGlobals:
        referenceScad = testGlobals["prepareSubpassReferenceScad"](subPass)
    else:
        referenceScad = testGlobals["referenceScad"]

    resultAsScad = resultToScad(result)

    # Create a temp directory for this test
    temp_dir = os.path.join(tempfile.gettempdir(), f"mesh_benchmark_{index}_{subPass}")
    os.makedirs(temp_dir, exist_ok=True)

    # Define all file paths
    result_scad = os.path.join(temp_dir, "result.scad")
    reference_scad = os.path.join(temp_dir, "reference.scad")
    compare1_scad = os.path.join(temp_dir, "compare1.scad")
    compare2_scad = os.path.join(temp_dir, "compare2.scad")
    
    output_stl = os.path.join(temp_dir, "output.stl")
    reference_stl = os.path.join(temp_dir, "reference.stl")
    intersection_stl = os.path.join(temp_dir, "intersection.stl")
    difference_stl = os.path.join(temp_dir, "difference.stl")
    
    output_png = os.path.join(temp_dir, "output.png")
    reference_png = os.path.join(temp_dir, "reference.png")

    # Write SCAD files
    _write_scad_file(
        result_scad, 
        resultAsScad, 
        testGlobals.get("scadModules"), 
        "minkowski(){cube(0.001);result();}"
    )
    
    _write_scad_file(
        reference_scad, 
        referenceScad, 
        testGlobals.get("scadModules"), 
        "minkowski(){cube(0.001);reference();}"
    )

    # Write comparison SCAD files
    with open(compare1_scad, "w") as f:
        f.write(f"use <result.scad>;\n")
        f.write(f"use <reference.scad>;\n")
        if "scadModules" in testGlobals:
            f.write(testGlobals["scadModules"])
        f.write("""
minkowski(){
    cube(0.001);
    intersection() {
        result();
        reference();
    }
}""")

    with open(compare2_scad, "w") as f:
        f.write(f"use <result.scad>;\n")
        f.write(f"use <reference.scad>;\n")
        if "scadModules" in testGlobals:
            f.write(testGlobals["scadModules"])
        f.write("""
minkowski(){
    cube(0.001);
    difference() {
        union() {
            result();   
            reference();
        }   
        intersection() {
            result();
            reference();
        }        
    }
}""")

    # Generate STL files
    print(f"Generating STL files in {temp_dir}...")
    if not os.path.exists(reference_stl):
      _run_openscad(reference_scad, reference_stl)
    _run_openscad(result_scad, output_stl)
    _run_openscad(compare1_scad, intersection_stl)
    _run_openscad(compare2_scad, difference_stl)
    
    # Generate PNG images with off-axis camera
    print(f"Rendering PNG images...")
    _render_stl_to_png(output_stl, output_png)

    if not os.path.exists(reference_png):
        _render_stl_to_png(reference_stl, reference_png)

    # Calculate volumes
    resultVolume = StlVolume.calculate_stl_volume(output_stl)
    referenceVolume = StlVolume.calculate_stl_volume(reference_stl)
    intersectionVolume = StlVolume.calculate_stl_volume(intersection_stl)
    differenceVolume = StlVolume.calculate_stl_volume(difference_stl)
    
    print(f"Result Volume: {resultVolume}")
    print(f"Reference Volume: {referenceVolume}")
    print(f"Intersection Volume: {intersectionVolume}")
    print(f"Difference Volume: {differenceVolume}")

    # Calculate score
    if referenceVolume == 0:
        score = 0.0
    else:
        score = intersectionVolume / referenceVolume

        if "volumeValidateDelta" in testGlobals:
            score += testGlobals["volumeValidateDelta"](
                result, resultVolume, referenceVolume, 
                intersectionVolume, differenceVolume
            )

        score -= (differenceVolume / referenceVolume) * 0.5
        score = max(0, score)

    return {
        "score": score,
        "output_image": output_png,
        "reference_image": reference_png,
        "temp_dir": temp_dir
    }


def _write_scad_file(
    filepath: str, 
    content: str, 
    modules: Optional[str], 
    suffix: str
) -> None:
    """Write a SCAD file with optional modules and suffix."""
    with open(filepath, "w") as f:
        if modules:
            f.write(modules)
        f.write(content)
        f.write(suffix)


def _run_openscad(input_scad: str, output_file: str) -> None:
    """Run OpenSCAD to generate output file from SCAD input."""
    result = subprocess.run(
        [openScadPath, "-o", output_file, input_scad],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Warning: OpenSCAD returned non-zero exit code for {input_scad}")
        if result.stderr:
            print(f"Error output: {result.stderr}")


def _render_stl_to_png(stl_path: str, png_path: str) -> None:
    """Render an STL file to PNG using OpenSCAD with an off-axis camera."""
    # Create a temporary SCAD file that imports the STL
    temp_scad = stl_path.replace(".stl", "_render.scad")
    render_scadText_to_png(
        f'import("{os.path.basename(stl_path)}");',
        png_path
    )
    
    # Clean up the temporary SCAD file
    try:
        os.remove(temp_scad)
    except OSError:
        pass


def render_scadText_to_png(scad_content: str, png_path: str, cameraArg: str = "--camera=10,10,10,55,0,25,100") -> None:
    """Render SCAD content to PNG using OpenSCAD with an off-axis camera."""
    # Create a temporary SCAD file with the provided content
    temp_scad = png_path.replace(".png", "temp.scad")
    with open(temp_scad, "w") as f:
        f.write(scad_content)
    
    # Use off-axis camera: positioned at (10, 10, 10) looking at origin
    # Format: --camera=x,y,z,rot_x,rot_y,rot_z,distance
    # We'll use auto-center and a good viewing angle
    result = subprocess.run(
        [
            openScadPath,
            "--autocenter",
            "--viewall",
            cameraArg,
            "--imgsize=800,600",
            "--colorscheme=Starnight",
            "-o", os.path.basename(png_path),
            os.path.basename(temp_scad)
        ],
        capture_output=True,
        text=True,
        cwd=os.path.dirname(png_path)
    )
    if result.returncode != 0:
        print(f"Warning: OpenSCAD PNG rendering returned non-zero exit code")
        if result.stderr:
            print(f"Error output: {result.stderr}")

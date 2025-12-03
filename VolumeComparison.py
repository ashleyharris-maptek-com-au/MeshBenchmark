import subprocess
import tempfile
import StlVolume
import os
import hashlib
import json
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

    if resultAsScad == "":
        return {
            "score": 0,
            "output_image": None,
            "output_mouseover_image": None,
            "output_hyperlink": resultAsScad,
            "reference_image": None,
            "temp_dir": None,
            "scoreExplantion": "Result was empty",
            "resultVolume": 0,
            "referenceVolume": 0,
            "intersectionVolume": 0,
            "differenceVolume": 0
        }

    scadModules = testGlobals.get("scadModules", "")

    # Generate cache key from inputs
    cache_key = _compute_cache_key(resultAsScad, referenceScad, scadModules)
    cache_dir = os.path.join(tempfile.gettempdir(), "mesh_benchmark_cache", cache_key)
    cache_meta_path = os.path.join(cache_dir, "cache_meta.json")

    # Check for cache hit
    if os.path.exists(cache_meta_path):
        cached = _load_cache(cache_meta_path)
        if cached is not None:
            print(f"Cache hit for {cache_key[:12]}...")
            cached["scoreExplantion"] += "Results were <a href='" + cache_meta_path + "'>cached</a>."
            return cached

    # Create cache directory for this comparison
    os.makedirs(cache_dir, exist_ok=True)
    temp_dir = cache_dir

    # Define all file paths
    result_scad = os.path.join(temp_dir, "result.scad")
    resultWithReference_scad = os.path.join(temp_dir, "resultWithReference.scad")
    reference_scad = os.path.join(temp_dir, "reference.scad")
    compare1_scad = os.path.join(temp_dir, "compare1.scad")
    compare2_scad = os.path.join(temp_dir, "compare2.scad")
    
    output_stl = os.path.join(temp_dir, "output.stl")
    reference_stl = os.path.join(temp_dir, "reference.stl")
    intersection_stl = os.path.join(temp_dir, "intersection.stl")
    difference_stl = os.path.join(temp_dir, "difference.stl")
    
    output_png = os.path.join(temp_dir, "output.png")
    output2_png = os.path.join(temp_dir, "output2.png")
    reference_png = os.path.join(temp_dir, "reference.png")

    # Write SCAD files
    _write_scad_file(
        result_scad, 
        resultAsScad, 
        testGlobals.get("scadModules"), 
        "minkowski(){cube(0.001);result();}"
    )

    _write_scad_file(
        resultWithReference_scad, 
        resultAsScad + "\n" + referenceScad, 
        testGlobals.get("scadModules"), 
        "minkowski(){cube(0.001);result();}\n" + 
        """
color([1,0,0,0.8])
minkowski(){
    cube(0.001);
    difference() {
        union() {
            result();   
            reference();
        }   
        result();
    }
}"""
    )
    
    _write_scad_file(
        reference_scad, 
        referenceScad, 
        testGlobals.get("scadModules"), 
        "minkowski(){cube(0.001);reference();}"
    )

    # Write comparison SCAD files
    with open(compare1_scad, "w", encoding="utf-8") as f:
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

    with open(compare2_scad, "w", encoding="utf-8") as f:
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
    openscad_errors = []
    if not os.path.exists(reference_stl):
        err = _run_openscad(reference_scad, reference_stl)
        if err:
            openscad_errors.append(err)
    
    # Run result SCAD with 10min timeout - complex/infinite renders get aborted
    try:
        err = _run_openscad(result_scad, output_stl, timeout=600)
        if err:
            openscad_errors.append(err)
    except TimeoutError as e:
        return {
            "score": 0,
            "output_image": None,
            "output_mouseover_image": None,
            "output_hyperlink": result_scad,
            "reference_image": reference_png if os.path.exists(reference_png) else None,
            "temp_dir": temp_dir,
            "scoreExplantion": f"<div style='color:red;'>Render timeout: {e}</div>",
            "resultVolume": 0,
            "referenceVolume": 0,
            "intersectionVolume": 0,
            "differenceVolume": 0
        }
    
    err = _run_openscad(compare1_scad, intersection_stl)
    if err:
        openscad_errors.append(err)
    err = _run_openscad(compare2_scad, difference_stl)
    if err:
        openscad_errors.append(err)
    
    # Generate PNG images with off-axis camera
    print(f"Rendering PNG images...")
    _render_stl_to_png(output_stl, output_png)
    render_scadText_to_png(f"include <{os.path.basename(resultWithReference_scad)}>;", output2_png)

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

    scoreExplantion = f"""
    <table>
    <tr><td>Result Volume:</td><td>{resultVolume:.2f}</td></tr>
    <tr><td>Reference Volume:</td><td>{referenceVolume:.2f}</td></tr>
    <tr><td>Intersection Volume:</td><td>{intersectionVolume:.2f}</td></tr>
    <tr><td>Difference Volume:</td><td>{differenceVolume:.2f}</td></tr>
    </table>
    """
    
    if openscad_errors:
        scoreExplantion += "<div style='color:red;white-space:pre-wrap;'>" + "\n".join(openscad_errors).replace('<', '&lt;').replace('>', '&gt;') + "</div>"

    # Calculate score
    if referenceVolume == 0:
        score = 0.0
    else:
        score = intersectionVolume / referenceVolume

        if "volumeValidateDelta" in testGlobals:
            scoreDelta = testGlobals["volumeValidateDelta"](
                result, resultVolume, referenceVolume, 
                intersectionVolume, differenceVolume
            )

            if scoreDelta != 0:
                scoreExplantion += f"Score was weighted from raw volume similarity, +: {scoreDelta:.2f}\n"
                score += scoreDelta

        score -= (differenceVolume / referenceVolume) * 0.5

        if "postProcessScore" in testGlobals:
            oldScore = score
            score = testGlobals["postProcessScore"](score)
            if oldScore != score:
                scoreExplantion += f"Score was renormalised: {oldScore:.2f} -> {score:.2f}\n"

        score = max(0, score)

    if openscad_errors:
        score = 0

    result_dict = {
        "score": score,
        "output_image": output_png,
        "output_mouseover_image": output2_png,
        "output_hyperlink":result_scad,
        "reference_image": reference_png,
        "temp_dir": temp_dir,
        "scoreExplantion": scoreExplantion,
        "resultVolume": resultVolume,
        "referenceVolume": referenceVolume,
        "intersectionVolume": intersectionVolume,
        "differenceVolume": differenceVolume
    }

    # Save to cache
    _save_cache(cache_meta_path, result_dict)

    return result_dict


def _compute_cache_key(resultAsScad: str, referenceScad: str, scadModules: str) -> str:
    """Compute a hash key from the input SCAD texts."""
    combined = f"{resultAsScad}\n---REFERENCE---\n{referenceScad}\n---MODULES---\n{scadModules}"
    return hashlib.sha256(combined.encode('utf-8')).hexdigest()


def _load_cache(cache_meta_path: str) -> Optional[Dict[str, Any]]:
    """Load cached result if all files still exist."""
    try:
        with open(cache_meta_path, 'r', encoding='utf-8') as f:
            cached = json.load(f)
        # Verify all referenced files still exist
        for key in ['output_image', 'reference_image']:
            if key in cached and not os.path.exists(cached[key]):
                return None
        return cached
    except (json.JSONDecodeError, IOError):
        return None


def _save_cache(cache_meta_path: str, result: Dict[str, Any]) -> None:
    """Save result to cache."""
    try:
        with open(cache_meta_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
    except IOError as e:
        print(f"Warning: Failed to save cache: {e}")


def _write_scad_file(
    filepath: str, 
    content: str, 
    modules: Optional[str], 
    suffix: str
) -> None:
    """Write a SCAD file with optional modules and suffix."""
    with open(filepath, "w",encoding="utf-8") as f:
        if modules:
            f.write(modules)
        f.write(content)
        f.write(suffix)


class TimeoutError(Exception):
    """Raised when OpenSCAD times out."""
    pass


def _run_openscad(input_scad: str, output_file: str, timeout: Optional[float] = None) -> Optional[str]:
    """Run OpenSCAD to generate output file from SCAD input.
    
    Returns error message string if there was an error, None otherwise.
    Raises TimeoutError if timeout is specified and exceeded.
    """
    try:
        result = subprocess.run(
            [openScadPath, "-o", output_file, input_scad],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        print(f"OpenSCAD timed out after {timeout}s for {input_scad}")
        raise TimeoutError(f"OpenSCAD render timed out after {timeout} seconds")
    if result.returncode != 0:
        print(f"Warning: OpenSCAD returned non-zero exit code for {input_scad}")
        error_msg = f"OpenSCAD error for {os.path.basename(input_scad)}:\n"
        if result.stdout:
            error_msg += f"stdout: {result.stdout}\n"
        if result.stderr:
            error_msg += f"stderr: {result.stderr}"
            print(f"Error output: {result.stderr}")
        return error_msg
    return None


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
    with open(temp_scad, "w", encoding="utf-8") as f:
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
        encoding="utf-8",
        errors="replace",
        cwd=os.path.dirname(png_path)
    )
    if result.returncode != 0:
        print(f"Warning: OpenSCAD PNG rendering returned non-zero exit code")
        if result.stderr:
            print(f"Error output: {result.stderr}")

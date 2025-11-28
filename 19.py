import math

title = "Tetrahedron Packing in 3D"

prompt = """
Here is the points and faces of a regular tetrahedron with all sides equal 1, resting on the Z=0 plane and with an edge along the X=0 plane:

polyhedron(
    points = [
        [0, 0, 0],                               // 0
        [1, 0, 0],                               // 1
        [0.5, sqrt(3)/2, 0],                     // 2
        [0.5, sqrt(3)/6, sqrt(2/3)]              // 3 (apex)
    ],
    faces = [
        [0, 2, 1],   // base (oriented outward)
        [0, 1, 3],
        [1, 2, 3],
        [2, 0, 3]
    ],
    convexity = 4
);

We define a 7-part rigid transform of (x,y,z,q0,q1,q2,q3), where q0,q1,q2,q3 is a normalised quaternion, and x, y, z are the translation.
Rotation is defined around the 0,0,0 point (Which is NOT THE CENTRE), and is performed before translation.

We create a scene with multiple tetrahedra, each with a different transform. Now we can pack them in as tightly as possible
in order to create a 3D shape, trying to maximize packing density and recreate the target shape.

Return the transform array of tetrahedra in order to create a:
"""

structure = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "x": { "type": "number" },
            "y": { "type": "number" },
            "z": { "type": "number" },
            "q0": { "type": "number" },
            "q1": { "type": "number" },
            "q2": { "type": "number" },
            "q3": { "type": "number" }
        }
    }
}

subpassParamSummary = [
    "Create a sphere of radius 4",
    "Create a torus with major radius 8 and minor radius 2",
    "Create a set of dumbbells with spheres of radius 2 and a connecting cylinder of diameter 1",
    "Create an axially aligned square based pyramid with base side 4 and height 4, sitting on the Z=0 plane, centered at origin",
    "Create a cylinder with radius 3 and height 6, centered at origin and aligned along the Z-axis",
    "Create a cube of side length 4, centered at origin",
    "Create an octahedron with edge length 4, centered at origin, with faces on the x, y, and z plane",
    "Itself, but scaled up by a factor of 10 "
]

def prepareSubpassPrompt(index: int) -> str:
    if index == 0: 
        return prompt + "Sphere of radius 4, with the center at origin."
    if index == 1: 
        return prompt + "Torus of major radius 8, and minor radius 2, with the center at origin."
    if index == 2: 
        return prompt + "Set of dumbbells. 2 spheres of radius 2, with centers x = +/-4, and a cylinder of diameter 1 connecting them."
    if index == 3: 
        return prompt + "Axially aligned square based pyramid with base side 4 and height 4, sitting on the Z=0 plane, centered at origin."
    if index == 4: 
        return prompt + "Cylinder of radius 3 and height 6, centered at origin and aligned along the Z-axis."
    if index == 5: 
        return prompt + "Cube of side length 4, centered at origin."
    if index == 6: 
        return prompt + "Octahedron with edge length 4, hieght 2, centered at origin, with faces on the x, y, and z plane."
    if index == 7:
        return prompt + "Tetrahedron of side length 10, with vertices at 0,0,0 and 10,0,0."
    raise StopIteration

referenceScad = """
module reference(){
    translate([0,0,0.5]) cube([4,4,1], center=true);
}
"""

def prepareSubpassReferenceScad(index: int) -> str:
    if index == 0: return """
module reference(){
    sphere(r=4, $fn=20);
}
"""
    if index == 1: return """
module reference(){
    rotate_extrude()
        translate([8, 0, 0])
            circle(r = 2, $fn = 16);
}
"""
    if index == 2: return """
module reference(){
  union() {
    translate([-4,0,0]) sphere(r=2);
    translate([ 4,0,0]) sphere(r=2);
    translate([0,0,0]) rotate([0,90,0]) cylinder(r=0.5, h=8, center=true, $fn=30);
  }
}
"""
    if index == 3: return """
module reference(){
    rotate([0,0,45]) cylinder(r1=2, r2=0,h=4, $fn=4);
}
"""

    if index == 4: return """
module reference(){
    cylinder(r=3, h=6, center=true, $fn=50);
}
"""

    if index == 5: return """
module reference(){
    cube([4,4,4], center=true);
}
"""

    if index == 6: return """
module reference(){
    cylinder(r=4, h=2, center=true, $fn=8);
}
"""

    if index == 7: return """
module reference(){
    scale([10,10,10]) tetrahedron();
}
"""

def quaternionToPitchRollYawInDegrees(q0, q1, q2, q3):
    return [math.degrees(math.atan2(2 * (q0 * q1 + q2 * q3), 1 - 2 * (q1 * q1 + q2 * q2))), 
            math.degrees(math.asin(2 * (q0 * q2 - q1 * q3))), 
            math.degrees(math.atan2(2 * (q0 * q3 + q1 * q2), 1 - 2 * (q2 * q2 + q3 * q3)))]

scadModules = """
module tetrahedron(){
    polyhedron(
        points = [
            [0, 0, 0],                               // 0
            [1, 0, 0],                               // 1
            [0.5, sqrt(3)/2, 0],                     // 2
            [0.5, sqrt(3)/6, sqrt(2/3)]              // 3 (apex)
        ],
        faces = [
            [0, 2, 1],   // base (oriented outward)
            [0, 1, 3],
            [1, 2, 3],
            [2, 0, 3]
        ],
        convexity = 4
    );
  
}
"""

def resultToScad(result):
    scad = "module result(){ " 
    scad += "minkowski(){cube(0.001); union() { "
    for transform in result:
        scad += "translate([" + str(transform["x"]) + "," + \
            str(transform["y"]) + "," + str(transform["z"]) + "]) rotate(" + \
            str(quaternionToPitchRollYawInDegrees(transform["q0"], transform["q1"], transform["q2"], transform["q3"])) + ") tetrahedron();\n"
    return scad + "}}}\n\n"

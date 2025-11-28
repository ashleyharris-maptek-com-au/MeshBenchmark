hull(){
    translate([0.0, 0.0]) sphere(0.01);
    translate([1.0, 0.0]) sphere(0.01);
}
hull(){
    translate([1.0, 0.0]) sphere(0.01);
    translate([0.5, 0.8660254038]) sphere(0.01);
}
hull(){
    translate([0.5, 0.8660254038]) sphere(0.01);
    translate([0.0, 0.0]) sphere(0.01);
}
hull(){
    translate([0.0, 0.0]) sphere(0.01);
    translate([0.0, 0.0]) sphere(0.01);
}
translate([0,0,-0.01]) color([0.1,0.1,0.1]) cube([3,3,0.01]);
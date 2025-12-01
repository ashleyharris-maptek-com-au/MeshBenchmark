hull(){
    translate([6, 4]) sphere(0.01);
    translate([5, 4]) sphere(0.01);
}
hull(){
    translate([5, 4]) sphere(0.01);
    translate([5, 5]) sphere(0.01);
}
translate([0,0,-0.01]) color([0.1,0.1,0.1]) cube([10,10,0.01]);
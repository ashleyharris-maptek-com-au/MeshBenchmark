union() {
    translate([0, 0, 4.5]) color([1, 0, 0]) cube([1, 1, 1], center=true);
    translate([0, 1, 2.5]) cube([1, 1, 5], center=true);
    translate([0, 3, 2.5]) cube([1, 1, 5], center=true);
    translate([0, 4, 2.5]) cube([1, 1, 5], center=true);
    translate([1, 0, 4.5]) cube([1, 1, 9], center=true);
    translate([1, 1, 4.5]) cube([1, 1, 9], center=true);
    translate([1, 2, 4.5]) cube([1, 1, 9], center=true);
    translate([1, 3, 4.5]) cube([1, 1, 9], center=true);
    translate([1, 4, 2.0]) cube([1, 1, 4], center=true);
    translate([2, 0, 3.5]) cube([1, 1, 7], center=true);
    translate([2, 1, 3.5]) cube([1, 1, 7], center=true);
    translate([2, 2, 3.5]) cube([1, 1, 7], center=true);
    translate([2, 3, 3.5]) cube([1, 1, 7], center=true);
    translate([2, 4, 1.5]) cube([1, 1, 3], center=true);
    translate([3, 0, 0.5]) cube([1, 1, 1], center=true);
    translate([3, 1, 0.5]) cube([1, 1, 1], center=true);
    translate([3, 2, 1.0]) cube([1, 1, 2], center=true);
    translate([3, 4, 1.0]) cube([1, 1, 2], center=true);
    translate([4, 0, 1.5]) cube([1, 1, 3], center=true);
    translate([4, 1, 1.5]) cube([1, 1, 3], center=true);
    translate([4, 2, 0.5]) cube([1, 1, 1], center=true);
    translate([4, 3, -0.5]) color([0, 0, 1]) cube([1, 1, 1], center=true);
}

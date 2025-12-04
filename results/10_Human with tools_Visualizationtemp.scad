
    
    for (i = [0:4]) {
        union() {
            // Draw each cube as a 3D object
            translate([5 * sin(i * 72), 5 * cos(i * 72), 0.5]) cube([1, 1, 1],center=true);
        }
    }

     
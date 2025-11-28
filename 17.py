title = "Sand pile simulator / metric imperial and wall impact"

prompt = """
A very fine sand is dribbling from a 25NB pipe whose opening sits 200ft above the floor of a silo.

5 cubic yards are sitting in the silo at the start.
1500 cubic feet of sand is piped in from trucks.
Then a 100 cubic meters train is unloaded.
Then 20 drums of sand are emptied, each 44-gallons.

The grain size and moisture content results in an angle of repose of 33 degrees.

The silo is 10 yards in dimeter, and negligible internal wind / air current.

Return an OpenSCAD file containing the shape of the sand pile: Use metric within OpenSCAD. 1 unit = 1 meter."""

structure = None

referenceScad = """
module reference()
{
    cylinder(r=4.572, h=1.299, $fn=50);
    translate([0, 0, 1.299])
        cylinder(r1=4.572, r2=0.033, h=2.969, $fn=50);
}
"""

def resultToScad(result):
  if "```" in result:
    result = result.split("```")[1]
    result = result.partition("\n")[2] # Drop the first line as it might be "```openscad"

  return "module result(){ union(){" + result + "}}"

title = "Sand pile simulator / metric imperial and wall impact"

prompt = """
A very fine sand is dribbling from a 25NB pipe whose opening sits 200ft above the floor of a silo.

5 cubic yards are sitting in the silo at the start.
1500 cubic feet of sand is piped in from trucks.
Then a 100 cubic meters train is unloaded.
Then 20 drums of sand are emptied, each 44-gallons.

The grain size and moisture content results in an angle of repose of 33 degrees.

The silo is 10 yards in dimeter, and negligible internal wind / air current.

Return an OpenSCAD file containing the shape of the sand pile: Use metric within OpenSCAD. 1 unit = 1 meter.

Keep the OpenSCAD file as simple as possible, using the fewest number of lines possible. 

Do not output anything else than the OpenSCAD file, as commentary doesn't compile.
"""

structure = None

subpassParamSummary = [
  """
  Some things to watch out for:<ul>
    <li>The nozzle opening is 25NB, or 33.7mm internal diameter. The cone's top wont be a pin-prick.</li>
    <li>33. degrees is pretty flat, so you can visually fail most output from this.</li>
    <li>The walls of the silo require this to be a cylinder with a cone on top.</li>
  </ul>

  LLM provided curves and reference geometry is both normalised to 9 degree segments
  """
]

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

  import re
  result = re.sub(r"\$fn\s*=\s*\d+", "$fn=50", result)

  return "module result(){ union(){" + result + "}}"

def postProcessScore(score):
  # Dumb solutions like a single cone do intersect the reference geometry a decent amount,
  # so we penalise scores far below 1.
  return score ** 5
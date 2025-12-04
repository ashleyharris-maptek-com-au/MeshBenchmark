title = "Pyamid construction - more bricks than token limits"

prompt = """
A pharoh is building a pyramyd to rest on top of his tomb and protect him for the afterlife. 
He has an army of 100,000 men who are honour bound to assist him in the project.

Pyramids must face north, which is +y, and is centred over the future tomb.

Pharoh has PARAM_A cut large stones, each a 50cm side-length cube.
Each stone needs 10 men to move.

When placed on top of other stones, each stone must have all 4 base
corners sitting in the middle of another stone. Any other arrangements will result in collapse. 
The pyramid does not have any internal voids for this reason.

The final facade will be done with wedges of marble, and the local stonemason requires precise plans to cut 
marble such that each external large stone is covered and the resulting pyamid is smooth.

Generate an OpenSCAD plan showing the tallest pyramid the pharoh can build with his budget
of stone. This plan must be precise with its volume accurate to the milimeter including every step
yet optimised enough to be viewable on the stonemason's CAD software.

Use Metric SI units in all working and in the final OpenSCAD file.

Do not output anything else than the OpenSCAD file, as that will cause compilation errors.
"""

def prepareSubpassPrompt(index):
  if index == 0: return prompt.replace("PARAM_A", "20,000")
  if index == 1: return prompt.replace("PARAM_A", "150,000")
  if index == 2: return prompt.replace("PARAM_A", "600,000")
  if index == 3: return prompt.replace("PARAM_A", "2,500,000")
  raise StopIteration

structure = None

promptChangeSummary = """
Hundreds of thousands of stones, then millions. 
The AI needs to merge adjacent stones and work with merged
layers in order to solve this.<br><br>

If it attempts to bruteforce a solution by rendering millions of bricks as individual cubes, 
OpenSCAD will either crash from std::bad_alloc or timeout after 600 seconds, both causing failure.
"""

subpassParamSummary = [
  "20,000 stones (~20m high)",
  "150,000 stones (~39m high)",
  "600,000 stones",
  "2,500,000 stones (~100m high / ~200 layers)"
]

referenceScad = ""

def prepareSubpassReferenceScad(index):
  stoneCount = 20000 if index == 0 else 150000 if index == 1 else 600000 if index == 2 else 2500000
  scad = ""
  level = 0
  while True:
    level += 1
    stones = level * level
    if stones < stoneCount:
        scad += f"translate([0,0,-{level * 0.5}])  cube([{level * 0.5},{level * 0.5}, 0.5], center=true);\n"
        stoneCount -= stones
    else: break

  scad = f"translate([0,0,{level * 0.5}])" + "{\n" + scad + "}\n"

  return "module reference()\n{\n" + scad + "\n}\n"


def resultToScad(result):
  import re
  
  if "```" in result:
    result = result.split("```")[1]
    result = result.partition("\n")[2] # Drop the first line as it might be "```openscad"

  # We need to extract things that can't be nested inside module result():
  # 1. Module definitions: module name(...) { ... }
  # 2. Function definitions: function name(...) = ...;
  # 3. Top-level variable assignments: name = value; (not inside braces)
  
  extracted = []
  remaining = result
  
  # Extract module definitions by matching balanced braces
  module_pattern = re.compile(r'module\s+\w+\s*\([^)]*\)\s*\{')
  
  while True:
    match = module_pattern.search(remaining)
    if not match:
      break
    
    start = match.start()
    brace_start = match.end() - 1
    depth = 1
    pos = brace_start + 1
    
    while pos < len(remaining) and depth > 0:
      if remaining[pos] == '{':
        depth += 1
      elif remaining[pos] == '}':
        depth -= 1
      pos += 1
    
    if depth == 0:
      extracted.append(remaining[start:pos])
      remaining = remaining[:start] + remaining[pos:]
    else:
      break
  
  # Extract function definitions: function name(...) = ...;
  func_pattern = re.compile(r'function\s+\w+\s*\([^)]*\)\s*=[^;]*;')
  for match in func_pattern.finditer(remaining):
    extracted.append(match.group())
  remaining = func_pattern.sub('', remaining)
  
  # Extract top-level variable assignments (not inside braces)
  # Process line by line, tracking brace depth
  lines = remaining.split('\n')
  top_level_lines = []
  inside_lines = []
  brace_depth = 0
  
  var_assign_pattern = re.compile(r'^\s*(\w+)\s*=\s*[^;]+;\s*(//.*)?$')
  
  for line in lines:
    # Count braces to track depth (simple approach - doesn't handle strings/comments perfectly)
    open_braces = line.count('{')
    close_braces = line.count('}')
    
    # If we're at top level and this looks like a variable assignment, extract it
    if brace_depth == 0 and var_assign_pattern.match(line):
      top_level_lines.append(line)
    else:
      inside_lines.append(line)
    
    brace_depth += open_braces - close_braces
    if brace_depth < 0:
      brace_depth = 0
  
  # Combine extracted items
  preamble = "\n".join(extracted) + "\n" + "\n".join(top_level_lines)
  body = "\n".join(inside_lines)
  
  return preamble + "\nmodule result(){ union(){\n" + body + "\n}}"

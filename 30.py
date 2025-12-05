title = "Stackable 3D printed primes"

skip = True

prompt = """
2 3D shapes can be said to be stackable if there exists an orientation in which:
- they can be stacked on top of each other without any overhang
- all lowest points on the top model touch the highest points of the lower model.
- the top shapes center of gravity is within the bottom shape.
- the entire stacks center of gravity is within the footprint of the bottom shape.
- they can be 3D printed without supports - ie no cantilevers or bridges.

For example, this sequence is stackable:
- Unit cube.
- Unit cylinder (of d = 1, h = 1)
- 3 legged stool, with a seat diameter of 1.
- 3 fair dice, with a size smaller than any seat leg.

The unit cube can rest in any stable orientation. The cylinder can sit on top with a flat face down.
The stool can be flipped upsidedown and sit on top of the cylinder. The dice can sit on top
of the legs (either one per leg, or stacked on top of each other on a single leg).

Side view of a stack:

      o
      o
      o   Dice

     | |     | |       | |
     | |     | |       | |
     | |     | |       | | Stool. Legs facing up, seat facing down.
     | |     | |       | |
     =====================

     X-------------------X
     |||||||||||||||||||||
     |||||||||||||||||||||
     ||||||||||||||||||||| Cylinder (flat facing up and down)
     |||||||||||||||||||||
     |||||||||||||||||||||
     X-------------------X

     =====================
     =====================
     ===================== Unit cube
     =====================
     =====================
     =====================
     =====================
     =====================
------------------------------- Build plate / ground / Z = 0

So now you understand the concept. Lets try something more advanced!

Using: 
- A 7 segment display font, 
- Fixed diget sizes
- Reading from the ground up,

what is the largest prime number that can be 3D printed in a stack?

Clarifications:
- A ban on repeating any sequence of 3 more than once. 
  - So 888 and 6969 substrings are allowed, but 888888 or 696969 are not allowed.
- Only a single diget can be printed at any one z level. So you can't print "138" by printing
  the 1 and 3 concurrently and then use that to support the 8.
- You can rotate in all 3 direction, so you can print a 3 on a 7 by rotating it upwards, but
  you can't then print another rotated 3 on top of it, becasuse between the points of the 3
  it would overhang.

"""

structure = {
    "type": "object",
    "properties": {
        "reasoning": {"type": "string"},
        "numberSequence": {"type": "array", "items": {
            "type": "object", "properties": {
            "digit": {"type": "integer"}, "orientation": {"type": "string", "enum": 
            ["flat", "flippedX", "flippedY",    
             "rotate90X",
             "rotate90Y",
             "rotate180Z"],
             "description" : "flat = as is. Flipped X turns a 3 into an E. Flipped Y turns a 5 into a 2. Rotate 90 X makes 7 have a short spike facing up in Z. Rotate 90 Y makes 7 have a long spike facing up in Z. Rotate 180Z turns a 6 into a 9. All other rotations do not produce anything printable. "}}
             },
             "propertyOrdering": [
                "digit",
                "orientation"
             ],
             "required": [
                "digit",
                "orientation"
             ],
             "additionalProperties": False
            }
    },
    "required": ["numberSequence","reasoning"],
    "additionalProperties": False
}

def canPrintOnTop(num):
    "Returns flat prints, and then side prints"
    if num == 0: return [0, 1,7], [1,3,7]
    if num == 1: return [1], [1,3,7]
    if num == 2: return [2,5], []
    if num == 3: return [1,3,7],[1,3,7]
    if num == 4: return [1,4],[1,3,7]
    if num == 5: return [2,5],[]
    if num == 6: return [1,3,6,7,9,4],[1,3,7]
    if num == 7: return [1,7],[1,3,7]
    if num == 8: return [0,1,2,3,4,5,6,7,8,9],[1,3,7]
    if num == 9: return [1,3,6,7,9],[1,3,7]

def gradeAnswer(answer : dict, subPassIndex : int, aiEngineName : str):
    numberSequence = answer["numberSequence"]
    
    # Build the number from the digit sequence
    number_str = ""
    for item in numberSequence:
        number_str += str(item["digit"])
    
    number = int(number_str)
    
    # Check if it's prime
    if not isPrime(number):
        return 0, str(number) + " is not prime"
    
    # Check for repeated 3-tuples
    if containsAny3TupleMoreThanOnce(number_str):
        return 0, str(number) + " contains a sequence of 3 digits repeated more than once"
    
    i = 0
    while i < len(numberSequence):
        current_digit = numberSequence[i]["digit"]
        current_orientation = numberSequence[i]["orientation"]
        next_digit = numberSequence[i + 1]["digit"]
        next_orientation = numberSequence[i + 1]["orientation"]

        flatOrientations = ["flat", "flippedX", "flippedY", "rotate180Z"]

        if current_orientation in flatOrientations and \
            next_orientation in flatOrientations:
            # we're staying flat!
            allowed_digits = canPrintOnTop(current_digit)[0]
            # Check if the next digit can be printed on top
            if next_digit not in allowed_digits:
                return 0, f"Digit {next_digit} (orientation: {next_orientation}) cannot be printed on top of digit {current_digit} (orientation: {current_orientation})<br>Stack is not printable."

            continue

        if current_orientation not in flatOrientations and current_digit not in [1,3,7]:
            return 0, f"Digit {current_digit} (orientation: {current_orientation}) cannot be printed as it has bridges or cantilevers"

        if next_orientation not in flatOrientations and next_digit not in [1,3,7]:
            return 0, f"Digit {next_digit} (orientation: {next_orientation}) cannot be printed as it has bridges or cantilevers"

        if current_orientation not in flatOrientations and current_orientation != "rotate90X" and current_digit in [3,7]:
            return 0, f"Digit {current_digit} (orientation: {current_orientation}) cannot be printed as it has overhangs"

        if next_orientation not in flatOrientations and next_orientation != "rotate90X" and next_digit in [3,7]:
            return 0, f"Digit {next_digit} (orientation: {next_orientation}) cannot be printed as it has overhangs"

        if next_orientation in flatOrientations:
            # We can only go back to flat if we're printing a 1 on top of a 1 
            if current_digit != 1 or next_digit != 1 or current_orientation == "rotate90Y":
                return 0, f"Digit {next_digit} (orientation: {next_orientation}) cannot be printed on top of digit {current_digit} (orientation: {current_orientation})<br>Stack is not printable."

            continue

        if current_orientation == "rotate90Y":
            # After anything sticking up, we can only print 1s in rotate90y
            if next_digit != 1 or next_orientation != "rotate90Y":
                return 0, f"Digit {next_digit} (orientation: {next_orientation}) cannot be printed on top of digit {current_digit} (orientation: {current_orientation})<br>Stack is not printable."

            continue       

    
    # Solution I found by exhaustive search was 6669696633377117111
    solution = 6669696633377117111
    solution_len = len(str(solution))
    
    if number > solution:
        return 100, "Test needs updating. Well done!"
    
    return len(number_str) / solution_len, f"Answer given was of length {len(number_str)} while the largest printable prime (I know of) is of length {solution_len}"

endingSuffixExplainer ="""

Once you vary off flat printing, there's only a 3 printable digits, 1, 3, and 7.
1 is indefinetly printable in all orientations.
7 can be printed on it's head or side, and then only a 1 can be printed.
3 can be printed on it's side, and then only a 1 can be printed.

So once we figure out the optimal legnth of the flat sitting digets, the largest suffix is 117111, printed as shown:
<pre>
          X---X
          |   |
          |   |
          |   |
          |   |
          |   |
          |   |
          X---X

          X---X
          |   |
          |   |
          |   |
          |   |
          |   |
          |   |
          X---X

          X---X
          |   |
          |   |
X---------X---X
|             |
X-------------X

X-------------X
|             |
X-------------X

X-------------X
|             |
X-------------X
<pre>

11311 is also printable, and so are it's substrings. It can only be printed on a flat 1, 3, 4, 6, 7, 8, 9, or 0.

711 can also be printed on anything, including a 5 and 2, since when on it's head it

"""

subpassParamSummary = [endingSuffixExplainer]

def isPrime(num : int) -> bool:
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def containsAny3TupleMoreThanOnce(s : str) -> bool:
    for i in range(0, len(s) - 2):
      for j in range(i + 1, len(s) - 2):
        if s[i] == s[i + 1] == s[i + 2] == s[j] == s[j + 1] == s[j + 2]:
            return True
    return False

printableFlats = []
longestPrintablePrime = 7


def finalAllFlatSequences(num : str):
    lastDiget = num[-1]

    suffixes = canPrintOnTop(int(lastDiget))[0]
    for suffix in suffixes:
        newNumber = num  + str(suffix)

        if len(newNumber) >= 3:
          last3Digets = str(newNumber)[-3:]
          if newNumber.count(last3Digets) > 1:
            continue

        printableFlats.append(newNumber)
        finalAllFlatSequences(newNumber)

if False and __name__ == "__main__":
  for base in range(1,10):
    finalAllFlatSequences(str(base))
    for n in printableFlats:
      for suffix in [111711, 117111, 111311, 11311, 17111, 13111, 11711, 11311, 1711, 1311,711, 311, 71, 31, 11,1]:
        num = str(n) + str(suffix)
        if int(num) < longestPrintablePrime:
          continue
        if not containsAny3TupleMoreThanOnce(num) and isPrime(int(num)):
            longestPrintablePrime = int(num)
            print(longestPrintablePrime)

  # Solution I found: 6669696633377117111

if __name__ == "__main__":
    print(gradeAnswer({
        "numberSequence": [
            {"digit": 6, "orientation": "flat"},
            {"digit": 6, "orientation": "flat"},
            {"digit": 9, "orientation": "flat"},
            {"digit": 6, "orientation": "flat"},
            {"digit": 6, "orientation": "flat"},
            {"digit": 3, "orientation": "flat"},
            {"digit": 3, "orientation": "flat"},
            {"digit": 7, "orientation": "flat"},
            {"digit": 7, "orientation": "flat"},
            {"digit": 1, "orientation": "flat"},
            {"digit": 1, "orientation": "flat"},
            {"digit": 7, "orientation": "rotate90X"},
            {"digit": 1, "orientation": "rotate90Y"},
            {"digit": 1, "orientation": "rotate90Y"},
            {"digit": 1, "orientation": "rotate90Y"},
        ]
    }, 0, "AnthropicClaude"))
skip = True

title = "AI controlling explosives, what could possibly go wrong?"

prompt = """

You are responsible for levelling terrian in preperation for the construction of a new city.

Here is the terrain as modelled by a height map



You can place blasting charges to fracture the terrain, causing it to collapse and flow
down hill.

Prepare a blast plan specifying 
- Where to place the charges (X/Y)
- How deep to drill down (Z)
- Order of the blasts.

Such that the terrain collapses into as much flat plane as possible.

"""
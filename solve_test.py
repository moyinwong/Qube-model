import pycuber as pc
from utils import gen_sample
from solve import solve
from pycuber.solver import CFOPSolver

# Create a new Cube and take actions
cube1 = pc.Cube()
cube1(["R"])
print([cube1])


# Create cubies for copy cude
cubies1 = set()

#"L", "R", "U", "D", "F", "B"

cubies1.add(pc.cube.Centre(**{"L": pc.Square("red")}))
cubies1.add(pc.cube.Centre(**{"R": pc.Square("orange")}))
cubies1.add(pc.cube.Centre(**{"U": pc.Square("yellow")}))
cubies1.add(pc.cube.Centre(**{"D": pc.Square("white")}))
cubies1.add(pc.cube.Centre(**{"F": pc.Square("green")}))
cubies1.add(pc.cube.Centre(**{"B": pc.Square("blue")}))

#"LB", "LF", "LU", "LD", "DB", "DF", "UB", "UF", "RB", "RF", "RU", "RD"

cubies1.add(pc.cube.Edge(**{"L": pc.Square("red"),"B": pc.Square("blue")}))
cubies1.add(pc.cube.Edge(**{"L": pc.Square("red"),"F": pc.Square("green")}))
cubies1.add(pc.cube.Edge(**{"L": pc.Square("red"),"U": pc.Square("yellow")}))
cubies1.add(pc.cube.Edge(**{"L": pc.Square("red"),"D": pc.Square("white")}))
cubies1.add(pc.cube.Edge(**{"D": pc.Square("white"),"B": pc.Square("blue")}))
cubies1.add(pc.cube.Edge(**{"D": pc.Square("white"),"F": pc.Square("green")}))
cubies1.add(pc.cube.Edge(**{"U": pc.Square("yellow"),"B": pc.Square("blue")}))
cubies1.add(pc.cube.Edge(**{"U": pc.Square("yellow"),"F": pc.Square("green")}))
cubies1.add(pc.cube.Edge(**{"R": pc.Square("orange"),"B": pc.Square("yellow")}))
cubies1.add(pc.cube.Edge(**{"R": pc.Square("orange"),"F": pc.Square("white")}))
cubies1.add(pc.cube.Edge(**{"R": pc.Square("orange"),"U": pc.Square("green")}))
cubies1.add(pc.cube.Edge(**{"R": pc.Square("orange"),"D": pc.Square("blue")}))

#"LDB", "LDF", "LUB", "LUF", "RDB", "RDF", "RUB", "RUF"

cubies1.add(pc.cube.Corner(**{"L": pc.Square("red"),"D": pc.Square("white"),"B": pc.Square("blue")}))
cubies1.add(pc.cube.Corner(**{"L": pc.Square("red"),"D": pc.Square("white"),"F": pc.Square("green")}))
cubies1.add(pc.cube.Corner(**{"L": pc.Square("red"),"U": pc.Square("yellow"),"B": pc.Square("blue")}))
cubies1.add(pc.cube.Corner(**{"L": pc.Square("red"),"U": pc.Square("yellow"),"F": pc.Square("green")}))
cubies1.add(pc.cube.Corner(**{"R": pc.Square("orange"),"D": pc.Square("blue"),"B": pc.Square("yellow")}))
cubies1.add(pc.cube.Corner(**{"R": pc.Square("orange"),"D": pc.Square("blue"),"F": pc.Square("white")}))
cubies1.add(pc.cube.Corner(**{"R": pc.Square("orange"),"U": pc.Square("green"),"B": pc.Square("yellow")}))
cubies1.add(pc.cube.Corner(**{"R": pc.Square("orange"),"U": pc.Square("green"),"F": pc.Square("white")}))

# Create a new testing cube
cube2 = pc.Cube(cubies1)
print([cube2])

# to see if a new cube is valid
print(cube2.is_valid())


# predict action for a new testing cube
success, actions = solve(cube2)
print(success, actions)

cube2(actions)

print([cube2])

#solver = CFOPSolver(cube2)

#solution = solver.solve(suppress_progress_messages=True)

#print(solution)

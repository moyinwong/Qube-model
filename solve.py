import tensorflow.keras.backend as K
from utils import action_map, flatten_1d_b, perc_solved_cube
import numpy as np
from autodidactic_decode_p import get_model
import pycuber as pc

def acc(y_true, y_pred):
    return K.cast(K.equal(K.max(y_true, axis=-1),
                          K.cast(K.argmax(y_pred, axis=-1), K.floatx())),
                  K.floatx())

def solve(Cube):

    file_path = "auto.h5"

    model = get_model()

    model.load_weights(file_path)

    cube = Cube
    cube.score = 0

    list_sequences = [[cube]]

    existing_cubes = set()

    action_list = []

    success = False

    for j in range(50):

        X = [flatten_1d_b(x[-1]) for x in list_sequences]

        value, policy = model.predict(np.array(X), batch_size=1024)

        new_list_sequences = []

        for x, policy in zip(list_sequences, policy):

            new_sequences = [x + [x[-1].copy()(action)] for action in action_map]

            pred = np.argsort(policy)

            take_action = list(action_map.keys())[pred[-1]]

            # append action
            action_list.append(take_action)

            cube_1 = x[-1].copy()(list(action_map.keys())[pred[-1]])

            new_list_sequences.append(x + [cube_1])


        # print("new_list_sequences", len(new_list_sequences))
        last_states_flat = [flatten_1d_b(x[-1]) for x in new_list_sequences]
        value, _ = model.predict(np.array(last_states_flat), batch_size=1024)
        value = value.ravel().tolist()

        for x, v in zip(new_list_sequences, value):
                    x[-1].score = v if str(x[-1]) not in existing_cubes else -1

        new_list_sequences.sort(key=lambda x: x[-1].score , reverse=True)

        new_list_sequences = new_list_sequences[:100]

        existing_cubes.update(set([str(x[-1]) for x in new_list_sequences]))

        list_sequences = new_list_sequences

        list_sequences.sort(key=lambda x: perc_solved_cube(x[-1]), reverse=True)

        prec = perc_solved_cube((list_sequences[0][-1]))

        if prec == 1:
            success = True
            break

    return success, action_list

def turn(content):
    new_cubies = set()
    #print(content)

    #Create cubies for copy cude


    for faces in content:
        #print(faces)
        #print(content[faces])
        new_dict = {}
        for i in range(len(faces)):
            #print(faces[i])
            new_dict[faces[i]] = pc.Square(content[faces][faces[i]])
        print(new_dict)
        if len(new_dict) == 1:
            new_cubies.add(pc.cube.Centre(**new_dict))
        elif len(new_dict) == 2:
            new_cubies.add(pc.cube.Edge(**new_dict))
        elif len(new_dict) == 3:
            new_cubies.add(pc.cube.Corner(**new_dict))
        else:
            return "invalid input"

    new_cube = pc.Cube(new_cubies)
    print([new_cube])
    return new_cube

    #"L", "R", "U", "D", "F", "B"

    # cubies.add(pc.cube.Centre(**{"L": pc.Square("red")}))
    # cubies.add(pc.cube.Centre(**{"R": pc.Square("orange")}))
    # cubies.add(pc.cube.Centre(**{"U": pc.Square("yellow")}))
    # cubies.add(pc.cube.Centre(**{"D": pc.Square("white")}))
    # cubies.add(pc.cube.Centre(**{"F": pc.Square("green")}))
    # cubies.add(pc.cube.Centre(**{"B": pc.Square("blue")}))

    #"LB", "LF", "LU", "LD", "DB", "DF", "UB", "UF", "RB", "RF", "RU", "RD"

    # cubies.add(pc.cube.Edge(**{"L": pc.Square("red"),"B": pc.Square("blue")}))
    # cubies.add(pc.cube.Edge(**{"L": pc.Square("red"),"F": pc.Square("green")}))
    # cubies.add(pc.cube.Edge(**{"L": pc.Square("red"),"U": pc.Square("yellow")}))
    # cubies.add(pc.cube.Edge(**{"L": pc.Square("red"),"D": pc.Square("white")}))
    # cubies.add(pc.cube.Edge(**{"D": pc.Square("white"),"B": pc.Square("blue")}))
    # cubies.add(pc.cube.Edge(**{"D": pc.Square("white"),"F": pc.Square("green")}))
    # cubies.add(pc.cube.Edge(**{"U": pc.Square("yellow"),"B": pc.Square("blue")}))
    # cubies.add(pc.cube.Edge(**{"U": pc.Square("yellow"),"F": pc.Square("green")}))
    # cubies.add(pc.cube.Edge(**{"R": pc.Square("orange"),"B": pc.Square("yellow")}))
    # cubies.add(pc.cube.Edge(**{"R": pc.Square("orange"),"F": pc.Square("white")}))
    # cubies.add(pc.cube.Edge(**{"R": pc.Square("orange"),"U": pc.Square("green")}))
    # cubies.add(pc.cube.Edge(**{"R": pc.Square("orange"),"D": pc.Square("blue")}))

    #"LDB", "LDF", "LUB", "LUF", "RDB", "RDF", "RUB", "RUF"

    # cubies.add(pc.cube.Corner(**{"L": pc.Square("red"),"D": pc.Square("white"),"B": pc.Square("blue")}))
    # cubies.add(pc.cube.Corner(**{"L": pc.Square("red"),"D": pc.Square("white"),"F": pc.Square("green")}))
    # cubies.add(pc.cube.Corner(**{"L": pc.Square("red"),"U": pc.Square("yellow"),"B": pc.Square("blue")}))
    # cubies.add(pc.cube.Corner(**{"L": pc.Square("red"),"U": pc.Square("yellow"),"F": pc.Square("green")}))
    # cubies.add(pc.cube.Corner(**{"R": pc.Square("orange"),"D": pc.Square("blue"),"B": pc.Square("yellow")}))
    # cubies.add(pc.cube.Corner(**{"R": pc.Square("orange"),"D": pc.Square("blue"),"F": pc.Square("white")}))
    # cubies.add(pc.cube.Corner(**{"R": pc.Square("orange"),"U": pc.Square("green"),"B": pc.Square("yellow")}))
    # cubies.add(pc.cube.Corner(**{"R": pc.Square("orange"),"U": pc.Square("green"),"F": pc.Square("white")}))


    #create cubies from input


    # new_cube = pc.Cube(new_cubies)
    # print([new_cube])
    # return new_cube


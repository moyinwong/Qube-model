from utils import gen_sample, action_map, flatten_1d_b, perc_solved_cube
import tensorflow.keras.backend as K
import numpy as np
from matplotlib import pyplot as plt
from autodidactic_decode_p import get_model

def acc(y_true, y_pred):
    return K.cast(K.equal(K.max(y_true, axis=-1),
                          K.cast(K.argmax(y_pred, axis=-1), K.floatx())),
                  K.floatx())


if __name__ == "__main__":
    file_path = "auto.h5"

    model = get_model()

    model.load_weights(file_path)

    x_values = [1,2,3,4,5,6,7,8,9,10]

    y_values = []

    for random_steps in x_values:

        success_time = 0

        for times in range(100):

            #generate 1 sample
            sample_X, sample_Y, cubes = gen_sample(random_steps)

            cube = cubes[0]
            cube.score = 0

            list_sequences = [[cube]]

            existing_cubes = set()

            #print(list_sequences)

            preview_cube = cube

            #show cube before solving
            #print([preview_cube])

            #print("start solve......")

            #start solving with X steps
            for j in range(50):

                #print("step: {}".format(j + 1))

                X = [flatten_1d_b(x[-1]) for x in list_sequences]

                value, policy = model.predict(np.array(X), batch_size=1024)

                new_list_sequences = []

                for x, policy in zip(list_sequences, policy):

                    new_sequences = [x + [x[-1].copy()(action)] for action in action_map]

                    pred = np.argsort(policy)

                    take_action = list(action_map.keys())[pred[-1]]

                    #print("take action : ", take_action)

                    cube_1 = x[-1].copy()(list(action_map.keys())[pred[-1]])

                    new_list_sequences.append(x + [cube_1])


                #print("new_list_sequences", len(new_list_sequences))
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

                #print(list_sequences[0])

                #to see cube in final stage
                preview_cube(take_action)
                #print([preview_cube])

                prec = perc_solved_cube((list_sequences[0][-1]))

                #print(prec)

                if prec == 1:
                    success_time += 1
                    break

        y_values.append(success_time)





            #print("final: \n", [list_sequences[0][-1]])

    print(y_values, x_values)

    plt.plot(x_values, y_values)
    plt.ylim(0,100)
    plt.ylabel("Solved within 50 steps")
    plt.xticks(np.arange(min(x_values), max(x_values) + 1, 1))
    plt.xlabel("random scramble action time")

    print("Done")
    plt.show()


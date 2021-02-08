import json
import time
import datetime
import os.path

def convertAction(action_array,actions_path,states_path):
    if action_array[0] == "DISCARD":
        a= int(action_array[1])
    elif action_array[0] == "PLACE":
        a= int(action_array[1])+5
    elif action_array[0] == "HINT_COLOR":
        a= int(action_array[1])+10
    elif action_array[0] == "HINT_VALUE":
        a= int(action_array[1])+14
    else:
        print("Invalid Player Action")
        a=-1
    
    print("Action as int is " + str(a))


    #timestr = time.strftime("%Y%m%d-%H%M%S")
    completeName = actions_path + os.path.sep + 'playeraction' + datetime.datetime.now().strftime('%Y%m%d%-H%-M-%S.%f')

    with open(completeName, 'w') as json_file:
        json.dump(a, json_file, indent=4)
        print("File " + completeName + " saved on disk")

    return a

        
    # while True:
    #     found = False
    #     _, _, filenames = next(os.walk(states_path))
    #     for f in filenames:
    #         print(f)
    #         if "botaction" in f.lower():
    #             found = True
    #             print("found action")
    #             print(f)
    #             in_file = states_path + os.path.sep + f
    #             #out_file = actions_path + os.path.sep + "action.json"
    #             with open(in_file) as j:
    #                 data = json.load(j)
    #             #print("removing state file " + in_file)
    #             #os.remove(in_file)
    #             time.sleep(1)
    #             print("state operation done. waiting for player action")
    #             print(data)
    #         if not found:
    #             print("Waiting for state")
    #             time.sleep(1)


    # print(data)
    # return data
    #TO-DO: add the botaction reading, creating action.txt, deleting botaction logic here
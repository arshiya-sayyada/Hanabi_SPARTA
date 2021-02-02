import json
import time
import os.path

def convertAction(action_array):
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
    
    #update save_path to your folder which stores actions 
    actions_path = '/Users/macbookpro/pytorch/Final_Hanabi/SpartaIntegration/actions'
    #timestr = time.strftime("%Y%m%d-%H%M%S")
    completeName = actions_path + os.path.sep + 'playeraction'         

    with open(completeName, 'w') as json_file:
        json.dump(a, json_file, indent=4)
        
    while True:
        found = False
        action_dir = os.listdir(actions_path) 
        for s in state_dir:
            if "state" in s.lower():
                found = True
                print("found state")
                print(s)
                in_file = states_path + os.path.sep + s
                #out_file = actions_path + os.path.sep + "action.json"
                with open(in_file) as j:
                    data = json.load(j)
                #print("removing state file " + in_file)
                #os.remove(in_file)
                time.sleep(1)
                print("state operation done. waiting for player action")
                return data
            if not found:
                print("Waiting for state")
                time.sleep(1)
    #TO-DO: add the botaction reading, creating action.txt, deleting botaction logic here
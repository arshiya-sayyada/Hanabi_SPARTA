#reads converted java game state from file. This is called in server2.py
from hanabi_lib import Color
import json
import time
import os.path

def convertGameState():
    '''
    save_path = '/Users/macbookpro/pytorch/Final_Hanabi/SpartaIntegration/states/'
    #print("trying to open json in state func")
    with open(save_path + 'gameState.json') as f:
        #print("successfully opened")
        data = json.load(f)
    return data
    '''
    files = []
    states_path = '/Users/rodrigocanaan/Dev/SpartaIntegrationTest/states'

    actions_path = '/Users/rodrigocanaan/Dev/SpartaIntegrationTest/actions'

    state = None

    timeout = 30

    while timeout >=0:
        found = False
        state_dir = os.listdir(states_path) 
        for s in state_dir:
            if "state" in s.lower():
                found = True
                print("found state")
                print(s)
                in_file = states_path + os.path.sep + s
                #out_file = actions_path + os.path.sep + "action.json"
                with open(in_file) as j:
                    data = json.load(j)
                print("removing state file " + in_file)
                os.remove(in_file)
                time.sleep(1)
                print("state operation done. waiting for player action")
                return data
            if not found:
                print("Waiting for state")
                timeout -= 1
                time.sleep(0.05)
    print ("timed out waiting for state")
    return None

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
    states_path = '/Users/macbookpro/pytorch/Final_Hanabi/SpartaIntegration/states'

    actions_path = '/Users/macbookpro/pytorch/Final_Hanabi/SpartaIntegration/actions'

    state = None

    while True:
        found = False
        state_dir = os.listdir(states_path) 
        for s in state_dir:
            if "state" in s.lower():
                found = True
                print("found")
                print(s)
                in_file = states_path + os.path.sep + s
                #out_file = actions_path + os.path.sep + "action.json"
                with open(in_file) as j:
                    data = json.load(j)
                
                return data
            if not found:
                print("Waiting for state")
                time.sleep(1)
from hanabi_lib import Move, MoveType, Color
import json
import time
import os.path

def convertAction(playeraction):

    #update save_path to your folder which stores actions 
    files = []
    states_path = '/Users/macbookpro/pytorch/Final_Hanabi/SpartaIntegration/states'

    actions_path = '/Users/macbookpro/pytorch/Final_Hanabi/SpartaIntegration/actions'

    state = None

    while True:
        found = False
        action_dir = os.listdir(actions_path) 
        for s in action_dir:
            if "botaction" in s.lower():
                found = True
                print("found action")
                print(s)
                in_file = actions_path + os.path.sep + s
                out_file = actions_path + os.path.sep + "playeraction.txt"
                with open(in_file) as j:
                    action = json.load(j)
                file = open(out_file, "w")
                file.write("%s\n" %(playeraction))
                print("wrote player action")
                file.close()
                print("removing file " + in_file)
                os.remove(in_file)
                #print("removing file " + out_file)
                #os.remove(out_file)
                time.sleep(1)
                return action
            if not found:
                print("Waiting for action")
                time.sleep(1)
                break
            
        #file = open("sample.txt", "w")
        #file.write("%s = %s\n" %("a_dictionary", a_dictionary))

        #file.close()

#    save_path = '/Users/macbookpro/pytorch/HLE/hanabi-ad-hoc-learning/Experiments/SPARTA_Integration/actions/'
#    print("trying to open json")
 #   with open(save_path + 'action.json') as f:
  #      print("successfully opened")
   #     data = json.load(f)

    #file1 = open('action.txt', 'w') 
    #file1.write(str(data['action']))
    #file1.close()
        
        #obs_dict["vectorized"] = self.observation_encoder.encode(observation)
    #except Exception:
     #   print("No action file yet")
           
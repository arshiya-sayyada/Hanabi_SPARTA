from flask import Flask, render_template, request, redirect
import os
import random
import re
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():  
  return render_template('form.html')

@app.route('/dir-struct/')
def dir_struct():
    ##BEFORE RUNNING: Change root_dir address to where you want to store your logging data
    root_dir = "/Users/macbookpro/pytorch/Final_Hanabi"

    logDir = root_dir + '/Logging_Directories/SESSIONS'
    if not os.path.exists(logDir):
        os.makedirs(logDir)
        print("Directory ", logDir, " Created ")
        
    id_check = request.values.get('id_val')
    exp = request.values.get('skills')
    #print(request.values)
    
    #if user already has played before and has an id
    if id_check == 'yes':
        idx = request.values.get('id_label')

    #Note: currently there's an error check on form.html so only values greater than 0 can be inputted
    elif id_check == 'no':
        sess = os.listdir(logDir)
        sessNos = []
        for i in sess:
            temp = re.findall(r'\d+', i)
            sessNos.append(list(map(int, temp)))
        sessDone = [item for sublist in sessNos for item in sublist]
        sessDone.sort()
        if len(sessDone) == 0:
            idx = 1
        else: 
            print('last id assigned: ', sessDone[-1])
            idx = sessDone[-1] + 1
        #idx = random.randint(1, 10000)
        print('New ID assigned: ', idx)
        
    sessDir = str(logDir) + '/' + 'Session' + str(idx)
    if not os.path.exists(sessDir):
        os.makedirs(sessDir)
        print("Directory ", sessDir, " Created ")
        
        user_info = {
            'experience': exp,
            'agent': 'A'
        }
        userInfoDir = str(sessDir) + '/' + 'user_info_' + str(idx)
        with open(userInfoDir, 'w') as json_file:
            json.dump(user_info, json_file, indent=4)
            print("File " + userInfoDir + " saved on disk")

        gameDir = str(sessDir) + '/' + 'Games'
        os.makedirs(gameDir)
        print("Directory ", gameDir, " Created ")
        
        gameSessDir = str(gameDir) + '/' + 'Game' + '1'
        os.makedirs(gameSessDir)
        print("Directory ", gameSessDir, " Created ")
        
        actionDir = str(gameSessDir) + '/' + 'actions'
        stateDir = str(gameSessDir) + '/' + 'states'
        os.makedirs(actionDir)
        os.makedirs(stateDir)
        print(actionDir, ' and ', stateDir, ' directories created')

    else:
        print("Directory ", sessDir, " already exists")
        gameDir = str(sessDir) + '/' + 'Games'
        #create a new gameNo folder and action and state folders within them
        games = os.listdir(gameDir)
        gameNos = []
        for i in games:
            temp = re.findall(r'\d+', i)
            gameNos.append(list(map(int, temp)))
        gamesDone = [item for sublist in gameNos for item in sublist]
        gamesDone.sort()     
        print('last game played: ', gamesDone[-1])
        nextGameNum = gamesDone[-1] + 1

        gameSessDir = str(gameDir) + '/' + 'Game' + str(nextGameNum)
        os.makedirs(gameSessDir)
        print("Directory ", gameSessDir, " Created ")
        
        actionDir = str(gameSessDir) + '/' + 'actions'
        stateDir = str(gameSessDir) + '/' + 'states'
        os.makedirs(actionDir)
        os.makedirs(stateDir)
        print(actionDir, ' and ', stateDir, ' directories created')

    #storing these state and action location values in a json so I can read it in server2.py
    curr_loc = {
        'state_dir': stateDir,
        'action_dir': actionDir
    }
    
    currentAcStJSON = './current_location.json'
    with open(currentAcStJSON, 'w') as json_file:
        json.dump(curr_loc, json_file, indent=4)
        print("Current state and action directors being used can be found at ", currentAcStJSON)
    
    #TODO: run these bash commands here:
    #cd..
    #cd webapp
    #npm run start
    #-> in a new tab
    #BOT=RandomBot python server2.py
    #-> in a new tab
    #run java process
    return redirect("http://localhost:3003/", code=302)


if __name__ == '__main__':
  app.run(debug=True)
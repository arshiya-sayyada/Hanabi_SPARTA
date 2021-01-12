from hanabi_lib import Color
import json
import time
import os.path

def convertGameState(state):
    color_dict = [ Color(i).name for i in range(5) ]
    #print(f"Colors are {color_dict}")
    
    obs_dict = {}
    if state["isPlayerTurn"] == True:
        obs_dict["current_player"] = 0
    else:
        obs_dict["current_player"] = 1
    obs_dict["current_player_offset"] = 0
    obs_dict["life_tokens"] = state["mulligansRemaining"]
    obs_dict["information_tokens"] = state["hintStonesRemaining"]
    obs_dict["num_players"] = 2
    obs_dict["deck_size"] = state["cardsRemainingInDeck"]

    #SPARTA has Orange instead of white so we use these colors interchangeably
    color_map_dict = {'R':0,'Y':2,'G':3,'W':1,'B':4}
    obs_dict["fireworks"] = {}
    for color in color_map_dict.keys():
        obs_dict["fireworks"][color] = state["piles"][color_map_dict[color]]

#     formatMove(move, player, myNumber) for player, move in bot.move_history_
    obs_dict["legal_moves"] = []
    #condition for when discard is legal-> If hits < max_hints (8) : all discard moves are legal
    if state["hintStonesRemaining"] < 8:
        for move in range(5):
            action = {}
            action["action_type"] = 'DISCARD'
            action["card_index"] = move
            obs_dict["legal_moves"].append(action)
    #play is always legal
    for move in range(5):
        action = {}
        action["action_type"] = 'PLAY'
        action["card_index"] = move
        obs_dict["legal_moves"].append(action)
    #If hints > 0: ##. All hint moves are legal
    if state["hintStonesRemaining"] > 0:
        possible_colors = set()
        possible_ranks = set()
        for player_hand in state["cheatMyCards"]:
            card_split = list(player_hand)
            possible_colors.add(card_split[1].upper())
            possible_ranks.add(card_split[0])
        #{'action_type': 'REVEAL_COLOR', 'target_offset': 1, 'color': 'R'}
        for a in possible_colors:
            action = {}
            action["action_type"] = 'REVEAL_COLOR'
            action["target_offset"] = 1
            action["color"] = a
            obs_dict["legal_moves"].append(action)
        for a in possible_ranks:
            action = {}
            action["action_type"] = 'REVEAL_RANK'
            action["target_offset"] = 1
            action["rank"] = int(a)-1
            obs_dict["legal_moves"].append(action)
#       enumerateLegalMoves(server)
    obs_dict["legal_moves_as_int"] = []
    legal_moves_dict = []
    for move in obs_dict["legal_moves"]:
        if move['action_type']=='DISCARD':
            obs_dict["legal_moves_as_int"].append(move['card_index'])
        elif move['action_type']=='PLAY':
            obs_dict["legal_moves_as_int"].append(move['card_index']+5)
        elif move['action_type']=='REVEAL_COLOR':
            if move['color']=='R':
                obs_dict["legal_moves_as_int"].append(10)
            elif move['color']=='Y':
                obs_dict["legal_moves_as_int"].append(11)
            elif move['color']=='G':
                obs_dict["legal_moves_as_int"].append(12)
            elif move['color']=='W':
                obs_dict["legal_moves_as_int"].append(13)
            elif move['color']=='B':
                obs_dict["legal_moves_as_int"].append(14)
        elif move['action_type']=='REVEAL_RANK':
            if move['rank']==0:
                obs_dict["legal_moves_as_int"].append(15)
            elif move['rank']==1:
                obs_dict["legal_moves_as_int"].append(16)
            elif move['rank']==2:
                obs_dict["legal_moves_as_int"].append(17)
            elif move['rank']==3:
                obs_dict["legal_moves_as_int"].append(18)
            elif move['rank']==4:
                obs_dict["legal_moves_as_int"].append(19)
    #obs_dict["legal_moves_as_int"].sort()
    
    obs_dict["observed_hands"] = []
    #TO DO: map O to W
    player_hand_dict = []
    for player_hand in state["cards"]:
        cards = {}
        cards["color"] = None
        cards["rank"] = -1
        player_hand_dict.append(cards)
    obs_dict["observed_hands"].append(player_hand_dict)
    player_hand_dict = []
    for player_hand in state["cards"]:
        #cards = [card.to_dict() for card in player_hand]
        cards = {}
        card_split = list(player_hand)
        cards["color"] = card_split[1]
        cards["color"] = cards["color"].upper()
        if cards["color"] == 'O':
            cards["color"]='W'
        cards["rank"] = int(card_split[0])-1
        player_hand_dict.append(cards)
    obs_dict["observed_hands"].append(player_hand_dict)
    
    obs_dict["discard_pile"] = []
    for card in state["discards"]:
        cards = {}
        card_split = list(card)
        cards["color"] = card_split[1]
        cards["color"] = cards["color"].upper()
        if cards["color"] == 'O':
            cards["color"]='W'
        cards["rank"] = int(card_split[0])-1
        obs_dict["discard_pile"].append(cards)
        
    # Return hints received. 
    #check and knowledge from predictions
    obs_dict["card_knowledge"] = []
    obs_dict["complete_card_knowledge"] = []
    player_0_dict = []
    player_1_dict = []
    string_dict_0 = []
    string_dict_1 = []
    predict_array = state["predictions"]
    #print(f"predictions: {predict_array[1]}")
    human_array = predict_array[0]
    bot_array = predict_array[1]
    for player_hand in human_array:
        str_cck_1=""
        predict_color = []
        predict_number = []
        red = player_hand[0:5]
        white = player_hand[5:10]
        yellow = player_hand[10:15]
        green = player_hand[15:20]
        blue = player_hand[20:]
        
        for x in red:
            if x==1:
                predict_color.append('R')
                break
        for x in yellow:
            if x==1:
                predict_color.append('Y')
                break
        for x in green:
            if x==1:
                predict_color.append('G')
                break
        for x in white:
            if x==1:
                predict_color.append('W')
                break
        for x in blue:
            if x==1:
                predict_color.append('B')
                break
        
        for x in player_hand[0::5]:
            if x==1:
                predict_number.append(0)
                break
        for x in player_hand[1::5]:
            if x==1:
                predict_number.append(1)
                break
        for x in player_hand[2::5]:
            if x==1:
                predict_number.append(2)
                break
        for x in player_hand[3::5]:
            if x==1:
                predict_number.append(3)
                break
        for x in player_hand[4::5]:
            if x==1:
                predict_number.append(4)
                break
        cards = {}
        if len(predict_color)==1:
            cards["color"] = predict_color[0]
        else:
            cards["color"] = None
        
        if len(predict_number)==1:
            cards["rank"] = predict_number[0]
        else:
            cards["rank"] = None                                     
        player_1_dict.append(cards)
        str_cck_1 = str_cck_1.join(predict_color)
        for digit in predict_number:
            str_cck_1 += str(digit+1)
        string_dict_1.append(str_cck_1)
    for player_hand in bot_array:
        str_cck_0=""
        predict_color = []
        predict_number = []
        red = player_hand[0:5]
        white = player_hand[5:10]
        yellow = player_hand[10:15]
        green = player_hand[15:20]
        blue = player_hand[20:]
        
        for x in red:
            if x==1:
                predict_color.append('R')
                break
        for x in yellow:
            if x==1:
                predict_color.append('Y')
                break
        for x in green:
            if x==1:
                predict_color.append('G')
                break
        for x in white:
            if x==1:
                predict_color.append('W')
                break
        for x in blue:
            if x==1:
                predict_color.append('B')
                break
        
        for x in player_hand[0::5]:
            if x==1:
                predict_number.append(0)
                break
        for x in player_hand[1::5]:
            if x==1:
                predict_number.append(1)
                break
        for x in player_hand[2::5]:
            if x==1:
                predict_number.append(2)
                break
        for x in player_hand[3::5]:
            if x==1:
                predict_number.append(3)
                break
        for x in player_hand[4::5]:
            if x==1:
                predict_number.append(4)
                break
        cards = {}
        if len(predict_color)==1:
            cards["color"] = predict_color[0]
        else:
            cards["color"] = None
        
        if len(predict_number)==1:
            cards["rank"] = predict_number[0]
        else:
            cards["rank"] = None                                     
        player_0_dict.append(cards)
        str_cck_0 = str_cck_0.join(predict_color)
        for digit in predict_number:
            str_cck_0 += str(digit+1)
        string_dict_0.append(str_cck_0)
    if state["isPlayerTurn"] == True:
        obs_dict["card_knowledge"].append(player_1_dict)
        obs_dict["card_knowledge"].append(player_0_dict)
        obs_dict["complete_card_knowledge"].append(string_dict_1)
        obs_dict["complete_card_knowledge"].append(string_dict_0)
    else:
        obs_dict["card_knowledge"].append(player_0_dict) 
        obs_dict["card_knowledge"].append(player_1_dict)
        obs_dict["complete_card_knowledge"].append(string_dict_0)
        obs_dict["complete_card_knowledge"].append(string_dict_1)
    
    #update save_path to your folder which stores states 
    save_path = '/Users/macbookpro/pytorch/HLE/hanabi-ad-hoc-learning/Experiments/SPARTA_Integration/states/'
    timestr = time.strftime("%Y%m%d-%H%M%S")
    completeName = os.path.join(save_path, timestr + 'gameState.json')         

    with open(completeName, 'w') as json_file:
        json.dump(obs_dict, json_file, indent=4)
    
    #obs_dict["vectorized"] = self.observation_encoder.encode(observation)
    #obs_dict["pyhanabi"] = observation
    return obs_dict
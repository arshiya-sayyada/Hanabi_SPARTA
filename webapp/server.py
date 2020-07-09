#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import torch  # make sure to dynamically load everything before loading hanabi_lib
import asyncio
from quart import Quart, websocket, Response
import json
import sys
import os

from hanabi_lib import start_game, end_game, Move, MoveType, Color, get_botname, get_search_thresh, set_search_thresh


sequence = []
sequence_thresh = []
sequence_names = []
cycle = False
if "CYCLE_BOTS" in os.environ:
    cycle = True
    sequence = os.getenv("CYCLE_BOTS").split(",")
if "CYCLE_NAMES" in os.environ:
    sequence_names = os.getenv("CYCLE_NAMES").split(",")
if "CYCLE_THRESH" in os.environ:
    sequence_thresh = [float(t) for t in os.getenv("CYCLE_THRESH").split(",")]
game_counter = 0

def next_game_info():
    global game_counter
    next_bot = ""
    if not cycle:
        next_bot = os.getenv("BOT")
    else:
        if (len(sequence_thresh) != 0):
            set_search_thresh(sequence_thresh[game_counter % len(sequence_thresh)])
        next_bot = sequence[game_counter % len(sequence)]

    game_counter += 1
    return next_bot

LOG_PREFIX = "[*]"


app = Quart(__name__)
server, bot, thread = start_game(next_game_info())
print(f"{LOG_PREFIX} SERVER SEED: {server.seed}")


def card_repr(card):
    return card.__str__()

def formatMove(move, for_player_id, my_player_id):

    def playerName(playerId):
        return "You" if playerId == my_player_id else "Partner"

    def playerPosession(playerId):
        return "your" if playerId == my_player_id else "their"

    cardIndex = {
        0: "earliest",
        1: "2nd earliest",
        2: "middle",
        3: "2nd most recent",
        4: "most recent"
    }

    if move.type == MoveType.HINT_COLOR:
        return f"{playerName(for_player_id)} hinted {Color(move.value).name} to {playerName(move.to).lower()}"
    elif move.type == MoveType.HINT_VALUE:
        return f"{playerName(for_player_id)} hinted {move.value} to {playerName(move.to).lower()}"
    elif move.type == MoveType.DISCARD_CARD:
        return f"{playerName(for_player_id)} discarded {playerPosession(for_player_id)} {cardIndex[move.value]} card"
    elif move.type == MoveType.PLAY_CARD:
        return f"{playerName(for_player_id)} played {playerPosession(for_player_id)} {cardIndex[move.value]} card"
    else:
        return str(move)

def convertGameState(state):
    color_dict = [ Color(i).name for i in range(5) ]
    #print(f"Colors are {color_dict}")
    
    obs_dict = {}
    obs_dict["current_player"] = 1
    if state["isPlayerTurn"] == True:
        obs_dict["current_player_offset"] = 0
    else:
        obs_dict["current_player_offset"] = 1
    obs_dict["life_tokens"] = state["mulligansRemaining"]
    obs_dict["information_tokens"] = state["hintStonesRemaining"]
    obs_dict["num_players"] = 2
    obs_dict["deck_size"] = state["cardsRemainingInDeck"]

    #SPARTA has Orange instead of white so we use these colors interchangeably
    color_map_dict = {'R':0,'Y':2,'G':3,'W':1,'B':4}
    obs_dict["fireworks"] = {}
    for color in color_map_dict.keys():
        obs_dict["fireworks"][color] = state["piles"][color_map_dict[color]]

    obs_dict["legal_moves"] = []
    #add condition for when discard is legal-> If hits < max_hints (8) : all discard moves are legal
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
    
        
    obs_dict["legal_moves_as_int"] = []
    #for move in observation.legal_moves():
    #  obs_dict["legal_moves"].append(move.to_dict())
    #  obs_dict["legal_moves_as_int"].append(self.game.get_move_uid(move))

    obs_dict["observed_hands"] = []
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
        cards["rank"] = card_split[0]
        player_hand_dict.append(cards)
    obs_dict["observed_hands"].append(player_hand_dict)
    
    obs_dict["discard_pile"] = []
    for card in state["discards"]:
        cards = {}
        card_split = list(card)
        cards["color"] = card_split[1]
        cards["color"] = cards["color"].upper()
        cards["rank"] = card_split[0]
        obs_dict["discard_pile"].append(cards)
        
    # Return hints received.
    obs_dict["card_knowledge"] = []
    #for player_hints in observation.card_knowledge():
    #  player_hints_as_dicts = []
    #  for hint in player_hints:
    #    hint_d = {}
    #    if hint.color() is not None:
    #      hint_d["color"] = pyhanabi.color_idx_to_char(hint.color())
    #    else:
    #      hint_d["color"] = None
     #   hint_d["rank"] = hint.rank()
     #   player_hints_as_dicts.append(hint_d)
    #  obs_dict["card_knowledge"].append(player_hints_as_dicts)

    #obs_dict["vectorized"] = self.observation_encoder.encode(observation)
    #obs_dict["pyhanabi"] = observation
    print(f"Converted State: {obs_dict}")
    return obs_dict

@app.route('/')
def index():
    return '<code>Websocket endpoint is at /connect</code>'

@app.websocket('/connect')
async def ws():
    global server, bot, thread

    preloaded_moves = []

    try:
        # if a file with a list of game moves is provided,
        # read it in and advance game state
        preload_url = sys.argv[1]
        with open(preload_url) as f:
            content = f.readlines()
            preloaded_moves = [x.strip() for x in content]
            print(f"Preloaded moves from {preload_url}")
    except FileNotFoundError:
        return
    except IndexError:
        pass

    partnerNumber = 1 - server.whoAmI()
    myNumber = server.whoAmI()

    await websocket.send(json.dumps({
        'type': 'INIT',
        'colors': [ Color(i).name for i in range(5) ],
        'playerNumber': partnerNumber
    }))

    # main game loop
    while True:
        hint = bot.obs()
        hintPlayer = hint.to
        hintValue = hint.value
        hintType = hint.type.name
        flash_message = ""

        deck = server.getCurrentDeckComposition(-1)
        mapped_deck = { card_repr(card): count for (card, count) in deck.items() }

        state = {
            'cardsRemainingInDeck': server.cardsRemainingInDeck(),
            'currentScore': server.currentScore(),
            'hintStonesRemaining': server.hintStonesRemaining(),
            'mulligansRemaining': server.mulligansRemaining(),
            'playerId': myNumber,
            'partnerId': partnerNumber,
            'cards': list(map(card_repr, server.handOfPlayer(partnerNumber))),
            'cheatMyCards': list(map(card_repr, server.handOfPlayer(myNumber))),
            'cardsIds': server.cardIdsOfHandOfPlayer(myNumber),
            'partnerCardsIds': server.cardIdsOfHandOfPlayer(partnerNumber),
            'piles': server.piles(),
            'discards': list(map(card_repr, server.discards())),
            'hintPlayer': hintPlayer,
            'hintValue': hintValue,
            'hintType': hintType,
            'hintIdx': bot.obs_indices(),
            'flash_message': flash_message,
            'predictions': bot.getCardKnowledge(),
            'deckComposition': mapped_deck,
            'isPlayerTurn': server.activePlayer() == myNumber,
            'gameOver': server.gameOver(),
            'botName': sequence_names[(game_counter - 1) % len(sequence)] if len(sequence) != 0 and len(sequence) == len(sequence_names) else f"Bot {chr((game_counter - 1) % len(sequence) + 65)}" if len(sequence) > 0 else get_botname(),
            'moveHistory': [formatMove(move, player, myNumber) for player, move in bot.move_history_],
            'seed': server.seed
        }


        await websocket.send(json.dumps(state))

        print(f"Old State: {state}")
        a = convertGameState(state)
        

        if not server.activePlayer() == myNumber and not server.gameOver():
            bot.wait()
            continue

        flash_message = ""
        if len(preloaded_moves) != 0:
            action = preloaded_moves.pop(0)
        else:
            action = await websocket.receive()
        tokens = action.split(" ")
        print(f"{LOG_PREFIX} ACTION: {action}")

        try:
            if not bot.ready:
                print(f"Ignoring move {MoveType} because bot not ready.")
                continue

            if tokens[0] == "DISCARD":
                bot.makeMove(Move(MoveType.DISCARD_CARD, int(tokens[1])))
            elif tokens[0] == "PLACE":
                bot.makeMove(Move(MoveType.PLAY_CARD, int(tokens[1])))
            elif tokens[0] == "HINT_COLOR":
                bot.makeMove(Move(MoveType.HINT_COLOR, int(tokens[1]), int(tokens[2])))
            elif tokens[0] == "HINT_VALUE":
                bot.makeMove(Move(MoveType.HINT_VALUE, int(tokens[1]), int(tokens[2])))
            elif tokens[0] == "REPLAY":
                print(f"{LOG_PREFIX} FINAL SCORE: {server.currentScore()}")
                end_game(server, bot, thread)

                if tokens[1] == "-":
                    server, bot, thread = start_game(next_game_info())
                else:
                    server, bot, thread = start_game(next_game_info(), int(tokens[1]))

                print(f"{LOG_PREFIX} SERVER SEED: {server.seed}")
                partnerNumber = 1 - server.whoAmI()
                myNumber = server.whoAmI()
                await websocket.send(json.dumps({
                    'type': 'INIT',
                    'colors': [ Color(i).name for i in range(5) ],
                    'playerNumber': partnerNumber
                }))
                continue
            else:
                pass

        except RuntimeError as e:
            print(e)
            flash_message = str(e)

        if not server.gameOver():
            bot.wait()

app.run(host="0.0.0.0", port=5000)

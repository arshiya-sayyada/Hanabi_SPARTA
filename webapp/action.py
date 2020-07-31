from hanabi_lib import Move, MoveType, Color

def convertAction(action_no):
    to = 0
    if (action_no>=0 and action_no<=4):
        moveType = MoveType.DISCARD_CARD
        value = action_no
        return Move(moveType, value)
    elif (action_no>=5 and action_no<=9):
        moveType = MoveType.PLAY_CARD
        if action_no==5: 
            value = 0
        elif action_no==6:
            value = 1
        elif action_no==7:
            value = 2
        elif action_no==8:
            value = 3
        elif action_no==9:
            value = 4
        return Move(moveType, value)
    elif (action_no>=10 and action_no<=14):
        moveType = MoveType.HINT_COLOR
        #mapped to correspond colors
        if action_no==10:
            #red
            value = 0
        elif action_no==11:
            #yellow
            value = 2
        elif action_no==12:
            #green
            value = 3
        elif action_no==13:
            #orange/white
            value = 1
        elif action_no==14:
            #blue
            value = 4
        return Move(moveType, value, to)
    elif (action_no>=15 and action_no<=19):
        moveType = MoveType.HINT_VALUE
        if action_no==15:
            value = 1
        elif action_no==16:
            value = 2
        elif action_no==17:
            value = 3
        elif action_no==18:
            value = 4
        elif action_no==19:
            value = 5
        return Move(moveType, value, to)
           
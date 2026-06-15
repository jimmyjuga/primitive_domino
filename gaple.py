"""
    Primitive Domino
    Written by: Jimmy Effendi jimmy.effendi@gmail.com
    for : Final Project CIP 2026

"""

import random
import time
import tkinter as tk
from tkinter import messagebox, simpledialog
from pathlib import Path
from PIL import Image,ImageTk

root = tk.Tk()
root.title("Gaple (Domino) Games")

#2 Dimensional array which card can meet
CARD_GAMEDATA = [
#0->00
[0,1,3,6,10,15,21],
#1->01
[0,1,2,3,4,7,10,11,15,16,21,22],
#2->11
[1,2,4,7,11,16,22],
#3->20
[0,1,3,4,5,6,8,10,12,15,17,21,23],
#4->21
[1,2,3,4,5,7,8,11,12,16,17,22,23],
#5->22
[4,5,8,12,17,23],
#6->30
[0,1,3,6,7,8,9,10,13,15,18,21,24],
#7->31
[1,2,4,6,7,8,9,11,13,16,18,22,24],
#8->32
[3,4,5,6,7,8,9,12,13,17,18,23,24],
#9->33
[6,7,8,9,13,18,24],
#10->40
[0,1,3,6,10,11,12,13,14,15,19,21,25],
#11->41
[1,2,4,7,10,11,12,13,14,16,19,22,25],
#12->42
[3,4,5,8,10,11,12,13,14,17,19,23,25],
#13->43
[6,7,8,9,10,11,12,13,14,18,19,24,25],
#14->44
[10,11,12,13,14,19,25],
#15->50
[0,1,3,6,10,15,16,17,18,19,20,21,26],
#16->51
[1,2,4,7,11,15,16,17,18,19,20,21,26],
#17->52
[3,4,5,8,12,15,16,17,18,19,20,23,26],
#18->53
[6,7,8,9,13,15,16,17,18,19,20,24,26],
#19->54
[10,11,12,13,14,15,16,17,18,19,20,25,26],
#20->55
[15,16,17,18,19,20,26],
#21->60
[0,1,3,6,10,15,21,22,23,24,25,26,27],
#22->61
[1,2,4,7,11,16,21,22,23,24,25,26,27],
#23->62
[3,4,5,8,12,17,21,22,23,24,25,26,27],
#24->63
[6,7,8,9,3,13,18,21,22,23,24,25,26,27],
#25->64
[10,11,12,13,14,19,21,22,23,24,25,26,27],
#26->65
[15,16,17,18,19,20,21,22,23,24,25,26,27],
#27->66
[21,22,23,24,25,27],

]

#Card value List HEAD/TAIL Card
CARD_DATA = {0:[0,0,0],1:[1,0,1],2:[1,1,2],3:[2,0,2],4:[2,1,3],5:[2,2,4],6:[3,0,3],7:[3,1,4],8:[3,2,5],9:[3,3,6],10:[4,0,4],11:[4,1,5],12:[4,2,6],13:[4,3,7],14:[4,4,8],15:[5,0,5],16:[5,1,6],17:[5,2,7],18:[5,3,8],19:[5,4,9],20:[5,5,10],21:[6,0,6],22:[6,1,7],23:[6,2,8],24:[6,3,9],25:[6,4,10],26:[6,5,11],27:[6,6,12]}

CARD_WIDTH=48
CARD_HEIGHT=2+CARD_WIDTH*2
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
CARD_BUFFER = {}
start_btn = tk.Button()
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#AAAAAA")
DRAGGED_CARD = 0
TABLECARD = {}
TABLECARD_LEFT = 0
TABLECARD_LEFTVALUE = 0
TABLECARD_RIGHT = 0
TABLECARD_RIGHTVALUE = 0
TOTAL_SESSION = 0

PLAYER_TURN = 0
ALLPLAYER_TURNS = 0
GAME_FINISHED = 0

def main():
    global canvas, start_btn
    canvas.pack(fill="both", expand=True)
    canvas.create_rectangle(CARD_HEIGHT+50, CARD_HEIGHT+50, WIDTH-CARD_HEIGHT - 50, HEIGHT - CARD_HEIGHT - 100, fill="#448888", width=2)
    #Load all required images


    #get Len Image list to prevent recounting and save processor
    CARD_IMAGES_len = len(CARD_IMAGES)
    if CARD_IMAGES_len <= 0:
        print("Image not found or incomplete")
        return
    print("Total ", CARD_IMAGES_len," Loaded.")

    #Initiating First Game
    session_cards = CARD_DATA.copy()
    start_btn = tk.Button(canvas, text="Start Game", command=lambda: start_games(canvas, session_cards))
    start_btn.place(x=int(WIDTH/2), y=int(HEIGHT/2))

    root.mainloop()

# This app using hardoded PNG Image, since it hard to manage rotation on canvas object
def load_image():
    cards = {}
    for i in range(28):
        cardnum = CARD_DATA[i]
        cardimg = Path("cards/card"+str(cardnum[0])+str(cardnum[1])+".png")
        if cardimg.is_file():
            img = Image.open("cards/card"+str(cardnum[0])+str(cardnum[1])+".png")
            img_sized = img.resize((CARD_WIDTH, CARD_HEIGHT), Image.Resampling.LANCZOS)
            cards[i] = img_sized.copy()
        else:
            print("Card image not found or incomplete")
            return {}
    backcardpath = Path("cards/backcard.png")
    if backcardpath.is_file():
        backcard_ori = Image.open("cards/backcard.png")
        backcard_img_h = backcard_ori.resize((CARD_WIDTH, CARD_HEIGHT), Image.Resampling.LANCZOS)
    else:
        print("Backside card image not found")
        return {}

    cards[28]= (backcard_img_h)
    return cards


def start_games(canvas, session_cards):
    global USER_CARD, start_btn,PLAYER_TURN, TABLECARD, TABLECARD_LEFT, TABLECARD_LEFTVALUE, TABLECARD_RIGHT, TABLECARD_RIGHTVALUE
    DRAGGED_CARD = 0
    TABLECARD = {}
    TABLECARD_LEFT = 0
    TABLECARD_LEFTVALUE = 0
    TABLECARD_RIGHT = 0
    TABLECARD_RIGHTVALUE = 0
    PLAYER_TURN = 0
    ALLPLAYER_TURNS = 0
    start_btn.destroy()
    player_cards = {1:{},2:{},3:{},4:{}}
    card_idx = 1
    CENTER_X = WIDTH/2
    CENTER_Y = HEIGHT/2
    items = list(session_cards.items())
    random.shuffle(items)
    random.shuffle(items)
    random.shuffle(items)
    mulx = 1

    for key, value  in items:
        if card_idx < 8:
            #Player 1 Bottom
            x1 = int(CENTER_X-(CARD_WIDTH*3.5)+((CARD_WIDTH+2)*mulx))
            img = CARD_IMAGES[key].copy()
            img = ImageTk.PhotoImage(img)
            tag = "card_"+str(key)
            obj = canvas.create_image(x1,HEIGHT-(CARD_HEIGHT+40), image=img, anchor="center", tags=tag)
            CARD_BUFFER[obj] = [img,obj]
            player_cards[1][key] = value

            mulx +=1
        elif card_idx >= 8 and card_idx<15:
            #Player 2 Right
            y2 = int(CENTER_Y-(CARD_WIDTH*3.5)+(mulx*(CARD_WIDTH+2)))
            img = CARD_IMAGES[28].copy()
            img = img.rotate(90,expand=True)
            img = ImageTk.PhotoImage(img)
            tag = "card_"+str(key)
            obj = canvas.create_image(WIDTH - CARD_HEIGHT + 10 ,y2, image=img, anchor="center", tags=tag)
            CARD_BUFFER[obj] = [img,obj]
            player_cards[2][key] = value
            mulx +=1
        elif card_idx >=15 and card_idx<22:
            #Player 3 Top
            x2 = CENTER_X-(CARD_WIDTH*3.5)+((CARD_WIDTH+2)*mulx)
            img = CARD_IMAGES[28].copy()
            img = img.rotate(180,expand=True)
            img = ImageTk.PhotoImage(img)
            tag = "card_"+str(key)
            obj = canvas.create_image(x2, CARD_WIDTH + 40, image=img, anchor="center", tags=tag)
            CARD_BUFFER[obj] = [img,obj]
            player_cards[3][key] = value

            mulx +=1
        elif card_idx >=22 and card_idx <=28:
            #Player 4 left
            y1 = int(CENTER_Y-(CARD_WIDTH*3.5)+(mulx*(CARD_WIDTH+2)))
            img = CARD_IMAGES[28].copy()
            img = img.rotate(-90,expand=True)
            img = ImageTk.PhotoImage(img)
            tag = "card_"+str(key)
            obj = canvas.create_image(CARD_WIDTH + 40, y1, image=img, anchor="center", tags=tag)
            CARD_BUFFER[obj] = [img,obj]
            player_cards[4][key] = value
            mulx +=1

        if mulx > 7: mulx = 1
        card_idx += 1
    print("GAMES STARTED")
    zerocard = {}
    if PLAYER_TURN == 0:
        print("Its a new game, start with zero card")
        for i in player_cards:
            zerocard = card_find(player_cards[i],0)
            if zerocard == 1:
                PLAYER_TURN = i
                # Force Throw User Card with 0/0 head and tail
                print("User",i,"with card 0,0")
                arrange_card(canvas, 0)
                player_cards[i].pop(0)
                #Keep The Player not more than 4
                PLAYER_TURN += 1
                if PLAYER_TURN > 4:
                    PLAYER_TURN = 1
                break
        games_turn(player_cards)
    """
    else:
        #games_turn() return every player 1 finished, loop it
        while len(player_cards[PLAYER_TURN]) != 0:
            games_turn(canvas, player_cards)
            print("Second Turn")
            #Flag that makes this game session is ended
            if ALLPLAYER_TURNS >= 4 or GAME_FINISHED == 1:
                break
        end_games()
    """


def games_turn(player_cards):
    global canvas, PLAYER_TURN, ALLPLAYER_TURNS, GAME_FINISHED
    #Other than Player 1 should run automaticLY
    if GAME_FINISHED ==1 or ALLPLAYER_TURNS == 4:
        end_games()
        return
    while PLAYER_TURN != 1:
        card_thrown = 0
        print("Player", PLAYER_TURN, "Turn")
        #Get all Card that can be dropped into the table
        allowedcard = get_currentcardid()
        #Find if it one in the current player cards and view it
        for value in player_cards[PLAYER_TURN]:
            if value in allowedcard:
                card_thrown = 1
                #print("Player cards:", PLAYER_TURN, player_cards[PLAYER_TURN], "POP", value)
                arrange_card(canvas, value)
                #Remove it as it already put on the table
                player_cards[PLAYER_TURN].pop(value, None)
                break

        if card_thrown == 0:
            ALLPLAYER_TURNS +=1
            print("User", PLAYER_TURN, "Pass because no match card")
        else:
            ALLPLAYER_TURNS = 0

        #Check to make sure current player still has card after removed 1 card
        if len(player_cards[PLAYER_TURN]) == 0:
            print("Player", PLAYER_TURN, "Win")
            GAME_FINISHED = 1
            return

        #Now Next player turn
        PLAYER_TURN +=1
        #Limit only 4 player
        if PLAYER_TURN >4: PLAYER_TURN =1


    if PLAYER_TURN == 1:
        #Part of Player 1 turn, we will get user drag and drop cards
        print("Player ",PLAYER_TURN," Turn")
        #Get all allowed card to play
        allowedturn = get_currentcardid()
        #print("Session Allowed Cards for ",PLAYER_TURN,":",allowedturn, player_cards[1], TABLECARD_LEFTVALUE, TABLECARD_RIGHTVALUE)
        user_has_card = 0
        for value in player_cards[PLAYER_TURN]:
            if value in allowedturn:
                #Activate click for all card that possible to throw to table
                activate_cardmove(value, player_cards)
                #print("There is one card activated", value)
                user_has_card = 1

        #Last option if no card move for user 1
        if user_has_card == 0:
            print("Player", PLAYER_TURN, "Pass because of no match card")
            ALLPLAYER_TURNS +=1
            shift_player(player_cards)
        else:
            ALLPLAYER_TURNS = 0

def shift_player(player_cards):
    global PLAYER_TURN
    PLAYER_TURN +=1
    if ALLPLAYER_TURNS == 4 or GAME_FINISHED == 1:
        end_games()
    else:
        games_turn(player_cards)

def get_currentcardid():
    # create Card Structure is big on head small on tail and compare it to CARD_GAMEDATA so we can get possible card can be throw
    result = []
    if TABLECARD_LEFTVALUE < TABLECARD_RIGHTVALUE:
        currenttablecard = [TABLECARD_RIGHTVALUE, TABLECARD_LEFTVALUE, TABLECARD_LEFTVALUE+TABLECARD_RIGHTVALUE]
    else:
        currenttablecard = [TABLECARD_LEFTVALUE, TABLECARD_RIGHTVALUE, TABLECARD_LEFTVALUE+TABLECARD_RIGHTVALUE]
    items = list(CARD_DATA.items())
    for key, value in items:
        if value == currenttablecard:
            result = CARD_GAMEDATA[key]
            break
    return result

def end_games():
    #Function that end this game session
    global canvas, start_btn, GAME_FINISHED
    CARD_BUFFER.clear()
    canvas.delete('all')
    if PLAYER_TURN != 1:
        message = "Player " + str(PLAYER_TURN) + " Win!"
    else:
        message = "Congratulation you Win!"

    messagebox.showinfo("Information", message)
    canvas.create_rectangle(CARD_HEIGHT+50, CARD_HEIGHT+50, WIDTH-CARD_HEIGHT - 50, HEIGHT - CARD_HEIGHT - 100, fill="#448888", width=2)
    #Initiating First Game
    GAME_FINISHED=0
    ALLPLAYER_TURNS = 0
    session_cards = CARD_DATA.copy()
    start_btn = tk.Button(canvas, text="Start Game", command=lambda: start_games(canvas, session_cards))
    start_btn.place(x=int(WIDTH/2), y=int(HEIGHT/2))


#This Function run when User release their hold on left button click
def drop_card(event, player_cards):
    global canvas, TABLECARD_LEFT, TABLECARD_RIGHT, TABLECARD_LEFTVALUE, TABLECARD_RIGHTVALUE, PLAYER_TURN
    if PLAYER_TURN == 1:
        item_tags = canvas.gettags(DRAGGED_CARD)
        coordcard = canvas.coords(DRAGGED_CARD)
        if item_tags[0] != "current":
            image_key = item_tags[0].split("_")
            if len(image_key) == 2:
                img_key = int(image_key[1])
                widget = event.widget
                widget._drag_start_x = event.x
                widget._drag_start_y = event.y
                canvas.delete(DRAGGED_CARD)
                arrange_card(canvas, img_key, event.x)
                tag = "card_"+str(img_key)
                player_cards[1].pop(img_key)
                TABLECARD[img_key] = CARD_DATA[img_key].copy()

    for card_id in player_cards[1]:
        #print(card_id)
        deactivate_cardmove(card_id)

    if len(player_cards[PLAYER_TURN]) == 0:
        print("Game finished, you win!")
        GAME_FINISHED = 1
        end_games()
    else:
        PLAYER_TURN += 1
        games_turn(player_cards)

#This function run when user click their card
def drag_start(event):
    global DRAGGED_CARD
    DRAGGED_CARD = canvas.find_closest(event.x, event.y)[0]
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

#This function read and move the card object
def drag_motion(event):
    widget =event.widget
    x =  event.x - widget._drag_start_x
    y = event.y - widget._drag_start_y
    widget.move(DRAGGED_CARD, x,y)
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

#Check Card match left/right/ head and tail value, may be incomplete still in development heheh
def compare_card(card):
    card_condition = {}
    rotateright = random.randint(70,110)
    rotateleft = random.randint(260,280)
    if card[0] == TABLECARD_RIGHTVALUE:
        #print("Right  head Value")
        card_condition["rotation"] = rotateright
        card_condition["position"] = "right"
        card_condition["value"] = card[1]
    elif card[1] == TABLECARD_RIGHTVALUE:
        #print("Right tail Value")
        card_condition["rotation"] = rotateleft
        card_condition["position"] = "right"
        card_condition["value"] = card[0]

    if len(card_condition) == 0:
        if card[0] == TABLECARD_LEFTVALUE:
            #print("Left head Value")
            card_condition["rotation"] = rotateleft
            card_condition["position"] = "left"
            card_condition["value"] = card[1]
        elif card[1] == TABLECARD_LEFTVALUE:
            #print("Left tail Value")
            card_condition["rotation"] = rotateright
            card_condition["position"] = "left"
            card_condition["value"] = card[0]


    if card[0] == card[1]:
        card_condition["rotation"] = 0

    return card_condition


#Find card in player given card list
def card_find(user, card_key):
    user_cards = list(user.items())
    for key, val in user_cards:
        if key == card_key: return 1
    return 0

#This function for Player 1 Activate the card bind so they can choose it
def activate_cardmove(card_id, player_cards):
    tag = "card_"+str(card_id)
    canvas.tag_bind(tag, "<Button-1>", drag_start)
    canvas.tag_bind(tag, "<B1-Motion>", drag_motion)
    canvas.tag_bind(tag, "<ButtonRelease-1>", lambda event:drop_card(event,player_cards))


#This function for Player 1 deactivate the card bind so they no longer allowed click it
def deactivate_cardmove(card_id):
    tag = "card_"+str(card_id)
    canvas.tag_unbind(tag, "<Button-1>")
    canvas.tag_unbind(tag, "<B1-Motion>")
    canvas.tag_unbind(tag, "<ButtonRelease-1>")


#This function arrange placement card in canvas, be nice this this one :)

def arrange_card(canvas, card_id, coord=None):
    global TABLECARD, TABLECARD_LEFT, TABLECARD_LEFTVALUE, TABLECARD_RIGHT, TABLECARD_RIGHTVALUE
    img = CARD_IMAGES[card_id].copy()
    cardcondition = compare_card(CARD_DATA[card_id])
    if len(cardcondition) <= 2:
        #print("Card ID:", card_id, "Not Available for Player",PLAYER_TURN)
        return

    canvas.delete("card_"+str(card_id))
    img = img.rotate(cardcondition["rotation"],expand=True)
    img = ImageTk.PhotoImage(img)
    tag = "card_"+str(card_id)
    if len(TABLECARD) == 0:
        x = int(WIDTH/2)
        y = int(HEIGHT/2)
        obj = canvas.create_image(x,y, image=img, anchor="center", tags=tag)
        canvas.image = img
        CARD_BUFFER[obj] = [img,obj]
        TABLECARD_LEFT = card_id
        TABLECARD_LEFTVALUE = cardcondition["value"]
        TABLECARD_RIGHT = card_id
        TABLECARD_RIGHTVALUE = cardcondition["value"]
        TABLECARD[card_id] = CARD_DATA[card_id]
    else:
        #Check if Coord Parameter added, then it should not None, use it to force when player1 drop at left side or right side of the TABLECARD
        if coord != None:
            if  coord < WIDTH/2 :
                if TABLECARD_LEFTVALUE == CARD_DATA[card_id][0] or TABLECARD_LEFTVALUE == CARD_DATA[card_id][1]:
                    cardcondition["position"] = "left"
            else:
                if TABLECARD_RIGHTVALUE == CARD_DATA[card_id][0] or TABLECARD_RIGHTVALUE == CARD_DATA[card_id][1]:
                    cardcondition["position"] = "right"

        #This is all placement and Variable management
        if cardcondition["position"] == "left":
            #Left
            leftcoord = canvas.coords("card_"+str(TABLECARD_LEFT))
            #print("Left Card Position Before ",leftcoord, TABLECARD_LEFT, TABLECARD_LEFTVALUE, cardcondition)
            obj = canvas.create_image(leftcoord[0] - CARD_WIDTH,leftcoord[1], image=img, anchor="center", tags=tag)
            CARD_BUFFER[obj] = [img,obj]
            TABLECARD_LEFT = card_id
            TABLECARD_LEFTVALUE = cardcondition["value"]
            TABLECARD[card_id] = CARD_DATA[card_id].copy()
            #print("Left Card Position After ",leftcoord, TABLECARD_LEFT, TABLECARD_LEFTVALUE)

        else:
            #Right
            rightcoord = canvas.coords("card_"+str(TABLECARD_RIGHT))
            #rint("Right Card Position before",rightcoord, TABLECARD_RIGHT, TABLECARD_RIGHTVALUE, cardcondition)
            obj = canvas.create_image(rightcoord[0] +CARD_WIDTH, rightcoord[1], image=img, anchor="center", tags=tag)
            CARD_BUFFER[obj] = [img,obj]
            TABLECARD_RIGHT = card_id
            TABLECARD_RIGHTVALUE = cardcondition["value"]
            TABLECARD[card_id] = CARD_DATA[card_id].copy()
            #print("Right Card Position After ",rightcoord, TABLECARD_RIGHT, TABLECARD_RIGHTVALUE)




CARD_IMAGES = load_image()

if __name__ == '__main__':
    main()


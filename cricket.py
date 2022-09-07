import cv2
from cvzone.HandTrackingModule import HandDetector as hd
import time,random , datetime as dt

global user1_choice , user2_choice , p1 , p2 , bowler , batsman , alter , flag , role , alter_count , end , result
end , alter_count , p1 , p2 = 0 , 0 , 0 , 0
role = {}
result = 'none'
user1_choice , user2_choice = 0,0
alter = 0
flag = 0
cap = cv2.VideoCapture(0)
detector = hd(maxHands=1,detectionCon=0.8)

def toss(name_1 , name_2):
    global batsman,bowler , user1_choice , user2_choice , role
    print(
        """
                Player 1  Role :
            **************************
                  1. Bowling
                  2. Batting
            **************************
        """
    )
    while True:
        p1_role = input('Enter your choice : ')
        if p1_role=='1':
            role['Bowler']  = [p1 , user1_choice ,name_1]
            role['Batsman'] = [p2, user2_choice ,name_2]
            break
        elif p1_role=='2':
            role['Bowler']  = [ p2 , user2_choice ,name_2 ]
            role['Batsman'] = [ p1 , user1_choice ,name_1 ]
            break
        else:
            print('Invalid  Choice')


def choice_lock(frame):
    global user1_choice , user2_choice , alter , role , alter_count
    finger_details = detector.fingersUp(frame)
    if finger_details != [1,0,0,0,0]:
        user1_choice = finger_details.count(1)
        role['Batsman'][1] = user1_choice
    else:
        role['Batsman'][1] = 6

    user2_choice = random.randint(0,6)
    if user1_choice==0:
        role['Batsman'][1] = user2_choice

    print(user1_choice,user2_choice)

    if user1_choice == user2_choice:
        alter = 1
        swap_role = role['Batsman']
        role['Batsman'] = role['Bowler']
        role['Bowler'] = swap_role
        alter_count+=1
    elif user1_choice != user2_choice :
        print(role , user1_choice , user2_choice , 'normal')
        role['Batsman'][0] += role['Batsman'][1]
        print(role , user1_choice , user2_choice , 'normal')
        

                        #######################  main  code  #######################

name_1 = input('Enter name (Player 1)  : ')
name_2 = input('Enter name (Player 2)  : ')

toss(name_1,name_2)
start_time = dt.datetime.now()

while True:
    if ( alter_count==1 or alter_count==2 )and role['Batsman'][0] > role['Bowler'][0]:
        result = f"{role['Batsman'][2]} is winner"
        # print(result,'case 1')
        end = 1
    elif alter_count==2 and role['Batsman'][0] < role['Bowler'][0]:
        result = f"{role['Bowler'][2]} is winner"
        # print(result,'case 2')
        end = 1
    elif alter_count==2 and role['Batsman'][0] == role['Bowler'][0]:
        result = 'Draw Match'
        # print(result,'case 3')
        end = 1

    s , frame = cap.read()
    pressed = cv2.waitKey(1)

    if not end:
        hand_found = detector.findHands(frame)
        if hand_found[0]:
            pass
        else:
            if not alter:
                x = frame.shape[0]
                y = frame.shape[1]
                msg1 = 'Hand Not Found'
                msg2 = "Press s to play a turn when you are ready"
                cv2.putText(frame,msg1,(x//2-50,y//2-50),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,250),2)
                cv2.putText(frame,msg2,(x//2-190,y//2+30),cv2.FONT_HERSHEY_DUPLEX,0.8,(199, 209, 13),2)

                            #######################  GUI  #######################

        cv2.putText(frame,str(role['Batsman'][2]+' Batting'),(50,50),cv2.FONT_HERSHEY_DUPLEX,0.6,(0,250,0),2)
        cv2.putText(frame,str(role['Bowler'][2]+' Bowling'),(x-50,50),cv2.FONT_HERSHEY_DUPLEX, 0.6,(0,0,200),2)

        cv2.putText(frame,str(role['Batsman'][0]),(110,100),cv2.FONT_HERSHEY_DUPLEX,1,(0,250,0),2)
        cv2.putText(frame,str(role['Bowler'][0]),(x-25,100),cv2.FONT_HERSHEY_DUPLEX, 1,(0,0,200),2)

        cv2.line(frame,(x//2+90,40),(x//2+70,90),(255,0,0),2)

        if alter:
            if flag == 0:
                start_time = dt.datetime.now()
            cur_time = dt.datetime.now()
            flag = 1
            cv2.putText(frame,'OUT...!',(x//2+10,y//2-50),cv2.FONT_ITALIC,2,(0,0,250),3)
            cv2.putText(frame,'Turn Altered',(x//2+10,y//2+30),cv2.FONT_HERSHEY_DUPLEX,1,(199, 209, 13),2)
            if (cur_time - start_time).total_seconds()>5:
                alter = 0
                flag = 0

        cv2.imshow('Hand Cricket',frame)

        if pressed  == ord('s') and hand_found[0] and not alter:
            choice_lock(hand_found[0][0])
    if end:
        cv2.putText(frame,role['Batsman'][2]+ "  :  ",(x//2,y//2-50),cv2.FONT_ITALIC,1,(0,250,0),3)
        cv2.putText(frame,role['Bowler'][2]+ "  :  ",(x//2,y//2-80),cv2.FONT_ITALIC,1,(0,250,0),3)

        cv2.putText(frame,str(role['Batsman'][0]),(x//2+100,y//2-50),cv2.FONT_ITALIC,1,(0,250,0),2)
        cv2.putText(frame,str(role['Bowler'][0]),(x//2+100,y//2-80),cv2.FONT_ITALIC,1,(0,250,0),2)

        cv2.putText(frame,result+' is winner',(x//2-100,y//2-120),cv2.FONT_ITALIC,1,(0,250,0),3)

        cv2.putText(frame,'Press q to quit...',(x//2-40,y//2+40),cv2.FONT_HERSHEY_DUPLEX,1,(0,250,0),2)


        cv2.imshow('Hand Cricket',frame)

    if pressed ==ord('q'):
            break
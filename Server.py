import random
import os
import sys

import pygame
from pygame.locals import *
pygame.font.init()
pygame.mixer.init()
import serial
import time
ser=0

def init_serial():
    COMNUM=0
    global ser
    ser=serial.Serial()
    ser.baudrate=9600
    ser.port='/dev/ttyS0'
    ser.timeout=0.9
    ser.open()
    if ser.isOpen():
        print('Open : '+ser.portstr)

def send_data(COMM,data1,data2):
    msg=[0xA1,0xF1]
    msg.append(int(hex(ord(str(COMM))),16))
    msg.append(int(hex(ord(str(data1))),16))
    msg.append(int(hex(ord(str(data2))),16))
    ser.flushInput()
    ser.write(msg)
    time.sleep(0.1)
    print('I send : '+str(msg))
	
def receive_data_first():
    bytes=ser.readline(3)
    #bytes=bytes[1:]
    ser.flushOutput()
    time.sleep(0.1)
    print('I sent : '+bytes)
    return bytes

def receive_data():
    bytes=ser.readline(4)
    if bytes!='':
        bytes=bytes[1:]
        temp=bytes
    ser.flushOutput()
    time.sleep(0.1)
    print('I sent : '+bytes)
    return bytes

mode="" # main 1,2 / deck 1,2 / pregame / draw / shuffle / att / def / battle

maxlengthdeck=20
screen = pygame.display.set_mode((800, 480))
clock = pygame.time.Clock()
CT=["Card_Attack.png","Card_Snipe.png","Card_Shield.png","Card_Flash.png","Card_Negate.png","Card_Hide.png","Card_Heart.png"]
TT=["Thumb_Attack.png","Thumb_Snipe.png","Thumb_Shield.png","Thumb_Flash.png","Thumb_Negate.png","Thumb_Hide.png","Thumb_Heart.png"]
PT={1:[400], 2:[325,475], 3:[250,400,550], 4:[175,325,475,625], 5:[100,250,400,550,700], 6:[75,205,335,465,595,725], 7:[76,184,292,400,528,616,724], 8:[76,168,261,354,446,539,632,724], 9:[76,157,238,319,400,481,562,643,724]}
beige=(242,234,191)
refb=(255,0,0)
wine=(208,148,130)
clock=pygame.time.Clock()

def imageLoad(name, card):              #
    if card == 1:
        fullname = os.path.join("images/cards/", name)
    else: fullname = os.path.join('images', name)
    
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', name)
        raise SystemExit
    image = image.convert()
    
    return image, image.get_rect()

def display(font, sentence):
    displayFont = pygame.font.Font.render(font, sentence, 1, (255,255,255), (0,0,0)) 
    return displayFont

def mainGame():
    
    class cardSprite(pygame.sprite.Sprite):
        """ Sprite that displays a specific card. """
        
        def __init__(self, card, position):
            pygame.sprite.Sprite.__init__(self)
            cardImage = card + ".png"
            self.image, self.rect = imageLoad(cardImage, 1)
            self.position = position
        def update(self):
            self.rect.center = self.position

    class cardAttack(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Attack.png", 1)
            self.position = (75, 120)
            
        def update(self, mX, mY, click, dek2, hsu2, gsu2):
            self.image, self.rect = imageLoad("Card_Attack.png", 1)
            self.position = (75, 120)
            self.rect.center = self.position

            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect = imageLoad("Card_Attack.png", 1)
                self.position = (75, 120)
                self.rect.center = self.position
                hsu2+=1
                gsu2+=1
                
                if CT[0] in dek2:
                    dek2[CT[0]]+=1
                else:
                    dek2[CT[0]]=1
            
            return click, dek2, hsu2, gsu2

    class cardFlash(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Flash.png", 1)
            self.position = (225, 360)
            
        def update(self, mX, mY, click, dek2, hsu2):
            self.image, self.rect =imageLoad("Card_Flash.png", 1)
            self.position = (225, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Card_Flash.png", 1)
                self.position = (225, 360)
                self.rect.center = self.position
                hsu2+=1

                if CT[3] in dek2:
                    dek2[CT[3]]+=1
                else:
                    dek2[CT[3]]=1
            
            return click, dek2, hsu2

    class cardShield(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Shield.png", 1)
            self.position = (375, 120)
            
        def update(self, mX, mY, click, dek2, hsu2):
            self.image, self.rect =imageLoad("Card_Shield.png", 1)
            self.position = (375, 120)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Card_Shield.png", 1)
                self.position = (375, 120)
                self.rect.center = self.position
                hsu2+=1

                if CT[2] in dek2:
                    dek2[CT[2]]+=1
                else:
                    dek2[CT[2]]=1
            
            return click, dek2, hsu2

    class cardNegate(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Negate.png", 1)
            self.position = (75, 360)
            
        def update(self, mX, mY, click, dek2, hsu2):
            self.image, self.rect =imageLoad("Card_Negate.png", 1)
            self.position = (75, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Card_Negate.png", 1)
                self.position = (75, 360)
                self.rect.center = self.position
                hsu2+=1

                if CT[4] in dek2:
                    dek2[CT[4]]+=1
                else:
                    dek2[CT[4]]=1
            
            return click, dek2, hsu2

    class cardSnipe(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Snipe.png", 1)
            self.position = (225, 120)
            
        def update(self, mX, mY, click, dek2, hsu2, gsu2):
            self.image, self.rect =imageLoad("Card_Snipe.png", 1)
            self.position = (225, 120)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Card_Snipe.png", 1)
                self.position = (225, 120)
                self.rect.center = self.position
                hsu2+=1
                gsu2+=1

                if CT[1] in dek2:
                    dek2[CT[1]]+=1
                else:
                    dek2[CT[1]]=1
            
            return click, dek2, hsu2, gsu2
        
    class cardHide(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Card_Hide.png", 1)
            self.position = (375, 360)
            
        def update(self, mX, mY, click, dek2, hsu2):
            self.image, self.rect = imageLoad("Card_Hide.png", 1)
            self.position = (375, 360)
            self.rect.center = self.position

            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect = imageLoad("Card_Hide.png", 1)
                self.position = (375, 360)
                self.rect.center = self.position
                hsu2+=1
                
                if CT[5] in dek2:
                    dek2[CT[5]]+=1
                else:
                    dek2[CT[5]]=1
            
            return click, dek2, hsu2

    class thumbAttack(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Attack.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2, gsu2, tw):
            self.image, self.rect =imageLoad("Thumb_Attack.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Attack.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1
                gsu2-=1

                if CT[0] in dek2:
                    if dek2[CT[0]]==1:
                        del dek2[CT[0]]
                    else:
                        dek2[CT[0]]-=1
            
            return click, dek2, hsu2, gsu2

    class thumbSnipe(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Snipe.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2, gsu2,tw):
            self.image, self.rect =imageLoad("Thumb_Snipe.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Snipe.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1
                gsu2-=1

                if CT[1] in dek2:
                    if dek2[CT[1]]==1:
                        del dek2[CT[1]]
                    else:
                        dek2[CT[1]]-=1
            
            return click, dek2, hsu2, gsu2

    class thumbShield(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Shield.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2,tw):
            self.image, self.rect =imageLoad("Thumb_Shield.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Shield.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1

                if CT[2] in dek2:
                    if dek2[CT[2]]==1:
                        del dek2[CT[2]]
                    else:
                        dek2[CT[2]]-=1
            
            return click, dek2, hsu2

    class thumbFlash(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Flash.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2,tw):
            self.image, self.rect =imageLoad("Thumb_Flash.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Flash.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1

                if CT[3] in dek2:
                    if dek2[CT[3]]==1:
                        del dek2[CT[3]]
                    else:
                        dek2[CT[3]]-=1
            
            return click, dek2, hsu2

    class thumbNegate(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Negate.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2,tw):
            self.image, self.rect =imageLoad("Thumb_Negate.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Negate.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1

                if CT[4] in dek2:
                    if dek2[CT[4]]==1:
                        del dek2[CT[4]]
                    else:
                        dek2[CT[4]]-=1
            
            return click, dek2, hsu2

    class thumbHide(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Thumb_Hide.png", 1)
            self.position = (665, -40)
            
        def update(self, mX, mY, click, dek2, hsu2,tw):
            self.image, self.rect =imageLoad("Thumb_Hide.png", 1)
            self.position = (665, tw)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect =imageLoad("Thumb_Hide.png", 1)
                self.position = (665, tw)
                self.rect.center = self.position
                hsu2-=1

                if CT[5] in dek2:
                    if dek2[CT[5]]==1:
                        del dek2[CT[5]]
                    else:
                        dek2[CT[5]]-=1
            
            return click, dek2, hsu2

    class buttenDeckOk(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Ok.png", 0)
            self.position = (627, 440)
            
        def update(self, mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2):
            self.image, self.rect =imageLoad("Ok.png", 0)
            self.position = (627, 440)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                deck=[]
                for i in dek2:
                    for j in range(dek2[i]):
                        deck.append(i)
                dek=dek2
                hsu=hsu2
                gsu=gsu2
                if hsu<maxlengthdeck:
                    mode="main1"
                else:
                    mode="main2"
                self.image, self.rect =imageLoad("Ok2.png", 0)
                self.position = (627, 440)
                self.rect.center = self.position
                print(gsu2,"/",hsu2)
                print('dek2 : ',dek2)
                print('dek : ',dek)
                print('deck : ', deck)
                
            return click, mode, deck, dek, hsu, gsu

    class buttenDeckCancel(pygame.sprite.Sprite):   #
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Cancel.png", 0)
            self.position = (742, 440)
            
        def update(self, mX, mY, click, mode):
            self.image, self.rect =imageLoad("Cancel.png", 0)
            self.position = (742, 440)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                if hsu < maxlengthdeck:
                    mode="main1"
                else:
                    mode="main2"
                click = 0
                self.image, self.rect =imageLoad("Cancel.png", 0)
                self.position = (742, 440)
                self.rect.center = self.position
                print(gsu2,"/",hsu2)
                print('dek2 : ',dek2)
                print('dek : ',dek)
                print('deck : ', deck)
            
            return click, mode
        
    class deckEdit(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("DeckEdit.png", 0)
            self.position = (600, 240)
            
        def update(self, mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2):
            self.image, self.rect = imageLoad("DeckEdit.png", 0)
            self.position = (600, 240)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="deck1"
                click = 0
                self.image, self.rect = imageLoad("GameStart.png", 0)
                self.position = (600, 240)
                self.rect.center = self.position
                deck2=deck
                dek2={}
                for i in deck:
                    if i in dek2:
                        dek2[i]+=1
                    else:
                        dek2[i]=1
                hsu2=hsu
                gsu2=gsu
            return click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2

    class gameStart(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("GameStart.png", 0)
            self.position = (200, 240)
            
        def update(self, mX, mY, click, mode, deck3, deck, pHands, sun, tuk, que):
            self.image, self.rect = imageLoad("GameStart.png", 0)
            self.position = (200, 240)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="connect" ## "connect"
                click = 0
                tuk=9
                que=[]
                sun=random.randint(0,1)
                
                self.image, self.rect = imageLoad("GameStart.png", 0)
                self.position = (200, 240)
                self.rect.center = self.position
                deck3=shuffleDeck(deck)
                pHands=[CT[6],CT[6]]+deck3[:(sun+3)]
                deck3=deck3[(sun+3):]
            
            return click, mode, deck3, deck, pHands, sun, tuk, que
        
    class buttenMainTest(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("GameTest.png", 0)
            self.position = (310, 280)
            
        def update(self, mX, mY, click, mode):
            self.image, self.rect = imageLoad("GameTest.png", 0)
            self.position = (310, 280)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="pregame" ## "connect"
                click = 0
                self.image, self.rect = imageLoad("GameTest.png", 0)
                self.position = (310, 280)
                self.rect.center = self.position
            
            return click, mode
        
    class buttenMainCancel(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Cancel2.png", 0)
            self.position = (500, 280)
            
        def update(self, mX, mY, click, mode):
            self.image, self.rect = imageLoad("Cancel2.png", 0)
            self.position = (500, 280)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="main2"
                click = 0
                self.image, self.rect = imageLoad("Cancel2.png", 0)
                self.position = (500, 280)
                self.rect.center = self.position
            
            return click, mode

    class buttenGameSurren(pygame.sprite.Sprite):   # # 
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Surren.png", 0)
            self.position = (745, 40)
            
        def update(self, mX, mY, click, mode):
            self.image, self.rect = imageLoad("Surren.png", 0)
            self.position = (745, 40)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                mode="main2"
                click = 0
                self.image, self.rect = imageLoad("Surren.png", 0)
                self.position = (745, 40)
                self.rect.center = self.position
            
            return click, mode

    class buttenGameOk(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Ok.png", 0)
            self.position = (745, 200)
            
        def update(self, mX, mY, click, mode, sun, pHands, oHands, deck3, cnt):
            self.image, self.rect = imageLoad("Ok.png", 0)
            self.position = (745, 200)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                if mode=="pregame":
                    if sun==0:
                        pHands=pHands+deck3[:2]
                        deck3=deck3[2:]
                        mode="att"
                    else:
                        mode="def"
                elif mode=="def":
                    mode='defcom'
                elif mode=="att":
                    mode='attcom'
                elif mode=="win"or mode=="los":
                    mode='main2'
                click = 0
                self.image, self.rect = imageLoad("Ok.png", 0)
                self.position = (745, 200)
                self.rect.center = self.position
            
            return click, mode, sun, pHands, oHands, deck3, cnt

    class buttenGameTurnj(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("Turnj.png", 0)
            self.position = (745, 120)
            
        def update(self, mX, mY, click, mode, que):
            self.image, self.rect = imageLoad("Turnj.png", 0)
            self.position = (745, 120)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect = imageLoad("Turnj.png", 0)
                self.position = (745, 120)
                self.rect.center = self.position
                que=['T',9,9]
                mode='attcom'
            
            return click, mode, que

    class opponentCard(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 120)
            
        def update(self, mX, mY, click, mode, gtwi, opos, que):
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (gtwi, 120)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                self.image, self.rect = imageLoad("back.png", 1)
                self.position = (gtwi, 120)
                self.rect.center = self.position

                if mode=="att" and len(que)==3:
                    if que[0]=="A":
                        que[2]=opos
            
            return click, mode, que

    class playerCard1(pygame.sprite.Sprite):   #1
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 360)
            
        def update(self, mX, mY, click, mode, ptwi, tuk, pos, pHands, que):
            self.image, self.rect = imageLoad(pHands[pos], 1)
            if tuk==pos:
                self.position = (ptwi, 330)
            else:
                self.position = (ptwi, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                if mode=="def":
                    que.append(pos)
                    if len(que)==2:
                        pHands[que[0]],pHands[que[1]]=pHands[que[1]],pHands[que[0]]
                        que=[]

                elif mode=="att":
                    pp=pHands[pos]
                    if pp in CT[:2]:
                        if pp == CT[0]:
                            que=["A",pos,9]
                        elif pp == CT[1]:
                            que=["S",pos,9]
                    elif pp == CT[5]:
                        que=["H",pos,9]
                print(pos,que)
                        
            return click, mode, que, pHands

    class playerCard2(pygame.sprite.Sprite):   #2
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 360)
            
        def update(self, mX, mY, click, mode, ptwi, tuk, pos, pHands, que):
            self.image, self.rect = imageLoad(pHands[pos], 1)
            if tuk==pos:
                self.position = (ptwi, 330)
            else:
                self.position = (ptwi, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                if mode=="def":
                    que.append(pos)
                    if len(que)==2:
                        pHands[que[0]],pHands[que[1]]=pHands[que[1]],pHands[que[0]]
                        que=[]

                elif mode=="att":
                    pp=pHands[pos]
                    if pp in CT[:2]:
                        if pp == CT[0]:
                            que=["A",pos,9]
                        elif pp == CT[1]:
                            que=["S",pos,9]
                    elif pp == CT[5]:
                        que=["H",pos,9]
                print(pos,que)
                        
            return click, mode, que, pHands

    class playerCard3(pygame.sprite.Sprite):   #3
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 360)
            
        def update(self, mX, mY, click, mode, ptwi, tuk, pos, pHands, que):
            self.image, self.rect = imageLoad(pHands[pos], 1)
            if tuk==pos:
                self.position = (ptwi, 330)
            else:
                self.position = (ptwi, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                if mode=="def":
                    que.append(pos)
                    if len(que)==2:
                        pHands[que[0]],pHands[que[1]]=pHands[que[1]],pHands[que[0]]
                        que=[]

                elif mode=="att":
                    pp=pHands[pos]
                    if pp in CT[:2]:
                        if pp == CT[0]:
                            que=["A",pos,9]
                        elif pp == CT[1]:
                            que=["S",pos,9]
                    elif pp == CT[5]:
                        que=["H",pos,9]
                print(pos,que)
                        
            return click, mode, que, pHands

    class playerCard4(pygame.sprite.Sprite):   #4
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 360)
            
        def update(self, mX, mY, click, mode, ptwi, tuk, pos, pHands, que):
            self.image, self.rect = imageLoad(pHands[pos], 1)
            if tuk==pos:
                self.position = (ptwi, 330)
            else:
                self.position = (ptwi, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                if mode=="def":
                    que.append(pos)
                    if len(que)==2:
                        pHands[que[0]],pHands[que[1]]=pHands[que[1]],pHands[que[0]]
                        que=[]

                elif mode=="att":
                    pp=pHands[pos]
                    if pp in CT[:2]:
                        if pp == CT[0]:
                            que=["A",pos,9]
                        elif pp == CT[1]:
                            que=["S",pos,9]
                    elif pp == CT[5]:
                        que=["H",pos,9]
                print(pos,que)
                        
            return click, mode, que, pHands

    class playerCard5(pygame.sprite.Sprite):   #5
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 360)
            
        def update(self, mX, mY, click, mode, ptwi, tuk, pos, pHands, que):
            self.image, self.rect = imageLoad(pHands[pos], 1)
            if tuk==pos:
                self.position = (ptwi, 330)
            else:
                self.position = (ptwi, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                if mode=="def":
                    que.append(pos)
                    if len(que)==2:
                        pHands[que[0]],pHands[que[1]]=pHands[que[1]],pHands[que[0]]
                        que=[]

                elif mode=="att":
                    pp=pHands[pos]
                    if pp in CT[:2]:
                        if pp == CT[0]:
                            que=["A",pos,9]
                        elif pp == CT[1]:
                            que=["S",pos,9]
                    elif pp == CT[5]:
                        que=["H",pos,9]
                print(pos,que)
                        
            return click, mode, que, pHands

    class playerCard6(pygame.sprite.Sprite):   #6
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 360)
            
        def update(self, mX, mY, click, mode, ptwi, tuk, pos, pHands, que):
            self.image, self.rect = imageLoad(pHands[pos], 1)
            if tuk==pos:
                self.position = (ptwi, 330)
            else:
                self.position = (ptwi, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                if mode=="def":
                    que.append(pos)
                    if len(que)==2:
                        pHands[que[0]],pHands[que[1]]=pHands[que[1]],pHands[que[0]]
                        que=[]

                elif mode=="att":
                    pp=pHands[pos]
                    if pp in CT[:2]:
                        if pp == CT[0]:
                            que=["A",pos,9]
                        elif pp == CT[1]:
                            que=["S",pos,9]
                    elif pp == CT[5]:
                        que=["H",pos,9]
                print(pos,que)
                        
            return click, mode, que, pHands

    class playerCard7(pygame.sprite.Sprite):   #7
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 360)
            
        def update(self, mX, mY, click, mode, ptwi, tuk, pos, pHands, que):
            self.image, self.rect = imageLoad(pHands[pos], 1)
            if tuk==pos:
                self.position = (ptwi, 330)
            else:
                self.position = (ptwi, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                if mode=="def":
                    que.append(pos)
                    if len(que)==2:
                        pHands[que[0]],pHands[que[1]]=pHands[que[1]],pHands[que[0]]
                        que=[]

                elif mode=="att":
                    pp=pHands[pos]
                    if pp in CT[:2]:
                        if pp == CT[0]:
                            que=["A",pos,9]
                        elif pp == CT[1]:
                            que=["S",pos,9]
                    elif pp == CT[5]:
                        que=["H",pos,9]
                print(pos,que)
                        
            return click, mode, que, pHands

    class playerCard8(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 360)
            
        def update(self, mX, mY, click, mode, ptwi, tuk, pos, pHands, que):
            self.image, self.rect = imageLoad(pHands[pos], 1)
            if tuk==pos:
                self.position = (ptwi, 330)
            else:
                self.position = (ptwi, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                if mode=="def":
                    que.append(pos)
                    if len(que)==2:
                        pHands[que[0]],pHands[que[1]]=pHands[que[1]],pHands[que[0]]
                        que=[]

                elif mode=="att":
                    pp=pHands[pos]
                    if pp in CT[:2]:
                        if pp == CT[0]:
                            que=["A",pos,9]
                        elif pp == CT[1]:
                            que=["S",pos,9]
                    elif pp == CT[5]:
                        que=["H",pos,9]
                print(pos,que)
                        
            return click, mode, que, pHands

    class playerCard9(pygame.sprite.Sprite):   #
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("back.png", 1)
            self.position = (-40, 360)
            
        def update(self, mX, mY, click, mode, ptwi, tuk, pos, pHands, que):
            self.image, self.rect = imageLoad(pHands[pos], 1)
            if tuk==pos:
                self.position = (ptwi, 330)
            else:
                self.position = (ptwi, 360)
            self.rect.center = self.position
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                click = 0
                if mode=="def":
                    que.append(pos)
                    if len(que)==2:
                        pHands[que[0]],pHands[que[1]]=pHands[que[1]],pHands[que[0]]
                        que=[]

                elif mode=="att":
                    pp=pHands[pos]
                    if pp in CT[:2]:
                        if pp == CT[0]:
                            que=["A",pos,9]
                        elif pp == CT[1]:
                            que=["S",pos,9]
                    elif pp == CT[5]:
                        que=["H",pos,9]
                print(pos,que)
                        
            return click, mode, que, pHands

    def shuffleDeck(deck):   #
        l=len(deck)
        for i in range(l-2): #0~17
            t=random.randint(i+1,l-1)
            deck[t],deck[i]=deck[i],deck[t]
        return deck

                
            
    init_serial()
    state=0
    textFont = pygame.font.Font(None,28)
    background, backgroundRect = imageLoad("bjs2.png", 0)        #D09482 / 208 148 130
    oCards = pygame.sprite.Group()
    pCards = pygame.sprite.Group()     #
    dE = deckEdit()                         #
    gS = gameStart()                        #
    cA = cardAttack()
    cF = cardFlash()
    cSh = cardShield()
    cN = cardNegate()
    cS = cardSnipe()
    cH = cardHide()
    bDO = buttenDeckOk()
    bDC = buttenDeckCancel()
    tA=thumbAttack()
    tS=thumbSnipe()
    tSh=thumbShield()
    tF=thumbFlash()
    tN=thumbNegate()
    tH=thumbHide()
    bMT=buttenMainTest()
    bMC=buttenMainCancel()
    bGS=buttenGameSurren()
    bGO=buttenGameOk()
    bGT=buttenGameTurnj()
    o1=opponentCard()
    o2=opponentCard()
    o3=opponentCard()
    o4=opponentCard()
    o5=opponentCard()
    o6=opponentCard()
    o7=opponentCard()
    o8=opponentCard()
    o9=opponentCard()
    p1=playerCard1()
    p2=playerCard2()
    p3=playerCard3()
    p4=playerCard4()
    p5=playerCard5()
    p6=playerCard6()
    p7=playerCard7()
    p8=playerCard8()
    p9=playerCard9()
            
    buttons = pygame.sprite.Group(dE, gS)
    deck=[]                 #
    deck2=[]                #
    deck3=[]                #
    que=[]
    to=0                    #timeout
    to2=0
    tuk=9
    
    dek={}
    dek2={}

    sun=0 #
    cnt=2 #
    pHands, oHands,pPos,oPos= [], [], 0, 0
    buf=0
    pHeart=2
    oHeart=2
	
    ol=6
    mX, mY = 0, 0
    click = 0
    mode="main1"
    modedp=""
    hsu=0
    gsu=0
    hsu2=0
    gsu2=0
    
    while True:
        
        while mode=="main1": #
            state=0
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)             #
            
            titleFont = pygame.font.Font.render(textFont, "Deck is Not Set", 1, (25,25,25), wine)#(208,148,130)
            screen.blit(titleFont, (10, 440))

            gs, backgroundRect = imageLoad("GameStart2.png", 0)   #
            screen.blit(gs, (60,140))                        
            
            title, backgroundRect = imageLoad("title.png", 0)  
            screen.blit(title, (230,30))                        
            buttons = pygame.sprite.Group(dE)
            click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2 = dE.update(mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2)
            buttons.draw(screen)
                
            clock.tick(60)
            pygame.display.flip() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0                   

        while mode=="main2":
            state=0
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            
            title, backgroundRect = imageLoad("title.png", 0)
            screen.blit(title, (230,30))
            buttons = pygame.sprite.Group(dE, gS)
            click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2 = dE.update(mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2)
            click, mode, deck3, deck, pHands ,sun, tuk, que = gS.update(mX, mY, click, mode, deck3, deck, pHands, sun, tuk, que)
            buttons.draw(screen)
                
            clock.tick(60)
            pygame.display.flip() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0

        while mode=="deck1": 
            if hsu2>19:
                mode="deck2"
                break
            textFont2 = pygame.font.Font(None,55)
            background, backgroundRect = imageLoad("bjs.png", 0)    #f2 ea bf / 242 234 191
            screen.blit(background, backgroundRect)
            t=1
            tn=[0,0,0,0,0,0]
            for i in range(5):
                if CT[i] in dek2:
                    tn[i]=dek2[CT[i]]
            twitch=[-33,-33,-33,-33,-33,-33]
            twi=-33
            fs0="";fs1="";fs2="";fs3="";fs4="";fs5="";
            if CT[0] in dek2:
                buttons0=pygame.sprite.Group(tA)
                twi+=66
                twitch[0]=twi
                if dek2[CT[0]] > 1:
                    fs0 = str(dek2[CT[0]])
                buttons0.draw(screen)
            if CT[1] in dek2:
                buttons1=pygame.sprite.Group(tS)
                twi+=66
                twitch[1]=twi
                if dek2[CT[1]] > 1:
                    fs1 = str(dek2[CT[1]])
                buttons1.draw(screen)
            if CT[2] in dek2:
                buttons2=pygame.sprite.Group(tSh)
                twi+=66
                twitch[2]=twi
                if dek2[CT[2]] > 1:
                    fs2 = str(dek2[CT[2]])
                buttons2.draw(screen)
            if CT[3] in dek2:
                buttons3=pygame.sprite.Group(tF)
                twi+=66
                twitch[3]=twi
                if dek2[CT[3]] > 1:
                    fs3 = str(dek2[CT[3]])
                buttons3.draw(screen)
            if CT[4] in dek2:
                buttons4=pygame.sprite.Group(tN)
                twi+=66
                twitch[4]=twi
                if dek2[CT[4]] > 1:
                    fs4 = str(dek2[CT[4]])
                buttons4.draw(screen)
            if CT[5] in dek2:
                buttons5=pygame.sprite.Group(tH)
                twi+=66
                twitch[5]=twi
                if dek2[CT[5]] > 1:
                    fs5 = str(dek2[CT[5]])
                buttons5.draw(screen)

            f0 = pygame.font.Font.render(textFont2, fs0, 1, (255,255,30), (0x8f,0x68,0x68))
            f1 = pygame.font.Font.render(textFont2, fs1, 1, (255,255,30), (0x8f,0x68,0x68))
            f2 = pygame.font.Font.render(textFont2, fs2, 1, (255,255,30), (0x29,0x29,0x29))
            f3 = pygame.font.Font.render(textFont2, fs3, 1, (255,255,30), (0x29,0x29,0x29))
            f4 = pygame.font.Font.render(textFont2, fs4, 1, (255,255,30), (0x29,0x29,0x29))
            f5 = pygame.font.Font.render(textFont2, fs5, 1, (255,255,30), (0x3b,0x6b,0xce))

            screen.blit(f0, (710, twitch[0]-20))
            screen.blit(f1, (710, twitch[1]-20))
            screen.blit(f2, (710, twitch[2]-20))
            screen.blit(f3, (710, twitch[3]-20))
            screen.blit(f4, (710, twitch[4]-20))
            screen.blit(f5, (710, twitch[5]-20))

            buttons=pygame.sprite.Group(cA,cF,cSh,cN,cH,cS,bDO,bDC)
            
            click, dek2, hsu2, gsu2 = cA.update(mX, mY, click, dek2, hsu2, gsu2)          
            click, dek2, hsu2, gsu2 = cS.update(mX, mY, click, dek2, hsu2, gsu2)
            click, dek2, hsu2 = cF.update(mX, mY, click, dek2, hsu2)
            click, dek2, hsu2 = cSh.update(mX, mY, click, dek2, hsu2)
            click, dek2, hsu2 = cN.update(mX, mY, click, dek2, hsu2)
            click, dek2, hsu2 = cH.update(mX, mY, click, dek2, hsu2)
            click, dek2, hsu2, gsu2 = tA.update(mX, mY, click, dek2, hsu2, gsu2, twitch[0])          
            click, dek2, hsu2, gsu2 = tS.update(mX, mY, click, dek2, hsu2, gsu2, twitch[1])
            click, dek2, hsu2 = tSh.update(mX, mY, click, dek2, hsu2, twitch[2])
            click, dek2, hsu2 = tF.update(mX, mY, click, dek2, hsu2, twitch[3])
            click, dek2, hsu2 = tN.update(mX, mY, click, dek2, hsu2, twitch[4])
            click, dek2, hsu2 = tH.update(mX, mY, click, dek2, hsu2, twitch[5])
            click, mode, deck, dek, hsu, gsu = bDO.update(mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2)
            click, mode = bDC.update(mX, mY, click, mode)

            hsuFont = pygame.font.Font.render(textFont, (str(hsu2)+"/20"), 1, (5,5,5), (242,234,191))
            screen.blit(hsuFont, (475, 405))
            gsuFont = pygame.font.Font.render(textFont, (str(gsu2)+"(>9)"), 1, (5,5,5), (242,234,191))
            screen.blit(gsuFont, (475, 455))
            
            buttons.draw(screen)
                
            clock.tick(60)
            pygame.display.flip() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0

        while mode=="deck2": 
            if hsu2<20:
                mode="deck1"
                break
            textFont2 = pygame.font.Font(None,55)
            background, backgroundRect = imageLoad("bjs.png", 0)    #f2 ea bf / 242 234 191
            screen.blit(background, backgroundRect)
            t=1
            tn=[0,0,0,0,0,0]
            for i in range(5):
                if CT[i] in dek2:
                    tn[i]=dek2[CT[i]]
            twitch=[-33,-33,-33,-33,-33,-33]
            twi=-33
            fs0="";fs1="";fs2="";fs3="";fs4="";fs5="";
            if CT[0] in dek2:
                buttons0=pygame.sprite.Group(tA)
                twi+=66
                twitch[0]=twi
                if dek2[CT[0]] > 1:
                    fs0 = str(dek2[CT[0]])
                buttons0.draw(screen)
            if CT[1] in dek2:
                buttons1=pygame.sprite.Group(tS)
                twi+=66
                twitch[1]=twi
                if dek2[CT[1]] > 1:
                    fs1 = str(dek2[CT[1]])
                buttons1.draw(screen)
            if CT[2] in dek2:
                buttons2=pygame.sprite.Group(tSh)
                twi+=66
                twitch[2]=twi
                if dek2[CT[2]] > 1:
                    fs2 = str(dek2[CT[2]])
                buttons2.draw(screen)
            if CT[3] in dek2:
                buttons3=pygame.sprite.Group(tF)
                twi+=66
                twitch[3]=twi
                if dek2[CT[3]] > 1:
                    fs3 = str(dek2[CT[3]])
                buttons3.draw(screen)
            if CT[4] in dek2:
                buttons4=pygame.sprite.Group(tN)
                twi+=66
                twitch[4]=twi
                if dek2[CT[4]] > 1:
                    fs4 = str(dek2[CT[4]])
                buttons4.draw(screen)
            if CT[5] in dek2:
                buttons5=pygame.sprite.Group(tH)
                twi+=66
                twitch[5]=twi
                if dek2[CT[5]] > 1:
                    fs5 = str(dek2[CT[5]])
                buttons5.draw(screen)

            f0 = pygame.font.Font.render(textFont2, fs0, 1, (255,255,30), (0x8f,0x68,0x68))
            f1 = pygame.font.Font.render(textFont2, fs1, 1, (255,255,30), (0x8f,0x68,0x68))
            f2 = pygame.font.Font.render(textFont2, fs2, 1, (255,255,30), (0x29,0x29,0x29))
            f3 = pygame.font.Font.render(textFont2, fs3, 1, (255,255,30), (0x29,0x29,0x29))
            f4 = pygame.font.Font.render(textFont2, fs4, 1, (255,255,30), (0x29,0x29,0x29))
            f5 = pygame.font.Font.render(textFont2, fs5, 1, (255,255,30), (0x3b,0x6b,0xce))

            screen.blit(f0, (710, twitch[0]-20))
            screen.blit(f1, (710, twitch[1]-20))
            screen.blit(f2, (710, twitch[2]-20))
            screen.blit(f3, (710, twitch[3]-20))
            screen.blit(f4, (710, twitch[4]-20))
            screen.blit(f5, (710, twitch[5]-20))

            if gsu2>9:      
                buttons=pygame.sprite.Group(bDO,bDC)
                click, mode, deck, dek, hsu, gsu = bDO.update(mX, mY, click, mode, deck, dek, hsu, gsu, deck2, dek2, hsu2, gsu2)
            else:    
                buttons=pygame.sprite.Group(bDC)
            buttons.draw(screen)
            
            click, dek2, hsu2, gsu2 = tA.update(mX, mY, click, dek2, hsu2, gsu2, twitch[0])          
            click, dek2, hsu2, gsu2 = tS.update(mX, mY, click, dek2, hsu2, gsu2, twitch[1])
            click, dek2, hsu2 = tSh.update(mX, mY, click, dek2, hsu2, twitch[2])
            click, dek2, hsu2 = tF.update(mX, mY, click, dek2, hsu2, twitch[3])
            click, dek2, hsu2 = tN.update(mX, mY, click, dek2, hsu2, twitch[4])
            click, dek2, hsu2 = tH.update(mX, mY, click, dek2, hsu2, twitch[5])
            click, mode = bDC.update(mX, mY, click, mode)

            hsuFont = pygame.font.Font.render(textFont, (str(hsu2)+"/20"), 1, (255,5,5), (242,234,191))
            screen.blit(hsuFont, (475, 405))
            gsuFont = pygame.font.Font.render(textFont, (str(gsu2)+"(>9)"), 1, (255,5,5), (242,234,191))
            screen.blit(gsuFont, (475, 455))
                
            clock.tick(60)
            pygame.display.flip() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0
                

        while mode=="connect":
            to+=1
            if to>=5:
                mode="main2"
                to=0
            try:
                if state==0:
                    send_data(0,0,0)
                    temp=receive_data()
                    if temp=='000':
                        to=0
                        state=1
                elif state==1:
                    send_data(1,sun,0)
                    temp=receive_data()
                    if temp=='1AC':
                        to=0
                        ol=sun+6
                        state=2
                elif state==2:
                    send_data(1,sun,0)
                    temp=receive_data()
                    if temp=='1AC':
                        oHeart, pHeart=2, 2
                        to=0
                        state=0
                        mode="pregame"
            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            title, backgroundRect = imageLoad("title.png", 0)
            screen.blit(title, (230, 30))
            gsnoti, backgroundRect = imageLoad("GSNOTI.png", 0) 
            screen.blit(gsnoti, (250, 165))
            buttons=pygame.sprite.Group(bMT, bMC)
            buttons.draw(screen)
            click, mode = bMT.update(mX, mY, click, mode)
            click, mode = bMC.update(mX, mY, click, mode)
                
            clock.tick(60)
            pygame.display.flip() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0
            
        while mode=="pregame":
            try:
                if to<5:
                    send_data(9,9,9)
                    to+=1
            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs.png", 0)
            screen.blit(background, backgroundRect)
            if sun==0:
                title, backgroundRect = imageLoad("sun.png", 0)
            else :
                title, backgroundRect = imageLoad("hu.png", 0) 
            screen.blit(title, (100, 10))
            buttons=pygame.sprite.Group(bGS, bGO)
            buttons.draw(screen)
            pPT=PT[len(pHands)]
            j=0
            c=[0]*len(pHands)
            for i in pPT:
                c[j], backgroundRect = imageLoad(pHands[j], 1)
                c[j].set_colorkey(beige)
                screen.blit(c[j], (i-75, 240))
                j+=1
            click, mode = bGS.update(mX, mY, click, mode)
            click, mode, sun, pHands, oHands, deck3, cnt = bGO.update(mX, mY, click, mode, sun, pHands, oHands, deck3, cnt)
                
            clock.tick(60)
            pygame.display.flip() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0
                    
        while mode=="att" or mode=="def":
            try:
                if to2<5:
                    modedp=mode
                    to=0
                    send_data(9,9,9)
                    to2+=1
            except:
                oo=0;
            tuk=9
            background, backgroundRect = imageLoad("bjs.png", 0)
            screen.blit(background, backgroundRect)
            if mode=="att":
                buttons=pygame.sprite.Group(bGS, bGT, bGO)
            else :
                buttons=pygame.sprite.Group(bGS, bGO)
            buttons.draw(screen)
            pPT=PT[len(pHands)]
            j=0
            c=[0]*len(pHands)
            ptwitch=[-40,-40,-40,-40,-40,-40,-40,-40,-40]
            gtwitch=[-40,-40,-40,-40,-40,-40,-40,-40,-40]
            l=len(pHands)
            gtwi=38
            ptwi=38
            for i in range(ol):
                gtwitch[i]=gtwi
                gtwi+=76
            for i in range(l):
                ptwitch[i]=pPT[i]
            buttons1=pygame.sprite.Group(o1,o2,o3,o4,o5,o6,o7,o8,o9)
            buttons1.draw(screen)
            click, mode = bGS.update(mX, mY, click, mode)
            click, mode, sun, pHands, oHands, deck3, cnt = bGO.update(mX, mY, click, mode, sun, pHands, oHands, deck3, cnt)
            click, mode, que = bGT.update(mX, mY, click, mode, que)
            click, mode, que = o1.update(mX, mY, click, mode, gtwitch[0], 0, que)
            click, mode, que = o2.update(mX, mY, click, mode, gtwitch[1], 1, que)
            click, mode, que = o3.update(mX, mY, click, mode, gtwitch[2], 2, que)
            click, mode, que = o4.update(mX, mY, click, mode, gtwitch[3], 3, que)
            click, mode, que = o5.update(mX, mY, click, mode, gtwitch[4], 4, que)
            click, mode, que = o6.update(mX, mY, click, mode, gtwitch[5], 5, que)
            click, mode, que = o7.update(mX, mY, click, mode, gtwitch[6], 6, que)
            click, mode, que = o8.update(mX, mY, click, mode, gtwitch[7], 7, que)
            click, mode, que = o9.update(mX, mY, click, mode, gtwitch[8], 8, que)
            
            if len(que)==3:
                tuk=que[1]
                if que[2]<9:
                    poi, backgroundRect = imageLoad("target.png", 0)
                    poi.set_colorkey((0,0,0))
                    screen.blit(poi, (gtwitch[que[2]]-22, 120))
                    
            pp1=pygame.sprite.Group(p1)
            pp1.draw(screen)
            click, mode, que, pHands = p1.update(mX, mY, click, mode, ptwitch[0],tuk, 0, pHands, que)
            if l>1:
                pp2=pygame.sprite.Group(p2)
                pp2.draw(screen)
                click, mode, que, pHands = p2.update(mX, mY, click, mode, ptwitch[1],tuk, 1, pHands, que)
            if l>2:
                pp3=pygame.sprite.Group(p3)
                pp3.draw(screen)
                click, mode, que, pHands = p3.update(mX, mY, click, mode, ptwitch[2],tuk, 2, pHands, que)
            if l>3:
                pp4=pygame.sprite.Group(p4)
                pp4.draw(screen)
                click, mode, que, pHands = p4.update(mX, mY, click, mode, ptwitch[3],tuk, 3, pHands, que)
            if l>4:
                pp5=pygame.sprite.Group(p5)
                pp5.draw(screen)
                click, mode, que, pHands = p5.update(mX, mY, click, mode, ptwitch[4],tuk, 4, pHands, que)
            if l>5:
                pp6=pygame.sprite.Group(p6)
                pp6.draw(screen)
                click, mode, que, pHands = p6.update(mX, mY, click, mode, ptwitch[5],tuk, 5, pHands, que)
            if l>6:
                pp7=pygame.sprite.Group(p7)
                pp7.draw(screen)
                click, mode, que, pHands = p7.update(mX, mY, click, mode, ptwitch[6],tuk, 6, pHands, que)
            if l>7:
                pp8=pygame.sprite.Group(p8)
                pp8.draw(screen)
                click, mode, que, pHands = p8.update(mX, mY, click, mode, ptwitch[7],tuk, 7, pHands, que)
            if l>8:
                pp9=pygame.sprite.Group(p9)
                pp9.draw(screen)
                click, mode, que, pHands = p9.update(mX, mY, click, mode, ptwitch[8],tuk, 8, pHands, que)
            for i in pPT:
                c[j], backgroundRect = imageLoad(pHands[j], 1)
                c[j].set_colorkey(beige)
                if tuk==j:
                    screen.blit(c[j], (i-75, 210))
                else:
                    screen.blit(c[j], (i-75, 240))
                j+=1
            if len(que)==1:
                swi, backgroundRect = imageLoad("switch.png", 0)
                swi.set_colorkey((255,255,255))
                screen.blit(swi, (pPT[que[0]]-25, 330))
                
            clock.tick(60)
            pygame.display.flip() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0
		    
        while mode=="attcom":
            print(modedp, state)
            nowcard, backgroundRect = imageLoad("back.png", 1)
            nowcard.set_colorkey(beige)
            to+=1
            if to>=10:
                mode=modedp
                to=0
                state=0
                continue
            try:
                if state==0:
                    send_data(0,0,0)
                    temp=receive_data()
                    if temp=='000' or temp=='00' or temp[1:]=='00':
                        to=0
                        state=1
                elif state==1:
                    send_data(1,que[0],que[2])
                    temp=receive_data()
                    if temp[0]=='2':
                        to=0
                        state=2
                        del pHands[que[1]]
                        if que[0]=='A':
                            nowcard, backgroundRect = imageLoad(CT[int(temp[1])], 1)
                            nowcard.set_colorkey(beige)
                            ol-=1
                            if temp[1]=='4':
                                cnt=1
                            elif temp[1]=='3':
                                ol+=2
                            elif temp[1]=='6':
                                oHeart-=1
                        elif que[0]=='S':
                            if temp[1]=='0':
                                continue
                            else:
                                nowcard, backgroundRect = imageLoad(CT[int(temp[1])], 1)
                                nowcard.set_colorkey(beige)
                                ol-=1
                        elif que[0]=='H':
                            nowcard, backgroundRect = imageLoad(CT[5], 1)
                            nowcard.set_colorkey(beige)
                            pHands=pHands+deck3[:2]
                            deck3=deck3[2:]
                        elif que[0]=='T':
                            nowcard, backgroundRect = imageLoad("back.png", 1)
                            nowcard.set_colorkey(beige)
                            cnt=1
                            
                elif state==2:
                    send_data(9,9,9)
                    temp=receive_data()
                    if temp=='999':
                        to=0
                        state=0
                        to2=0
                        que=[]
                        tuk=9
                        cnt-=1
                        if oHeart==0:
                            cnt=2
                            mode="win"
                            continue
                        if pHeart==0:
                            cnt=2
                            mode="los"
                            continue
                        if cnt==0:
                            cnt=2
                            ol+=2
                            mode="def"
                        else:
                            mode=modedp
            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            buttons=pygame.sprite.Group(bGS, bGO)
            buttons.draw(screen)
            pPT=PT[len(pHands)]
            j=0
            c=[0]*len(pHands)
            for i in pPT:
                c[j], backgroundRect = imageLoad(pHands[j], 1)
                c[j].set_colorkey(beige)
                screen.blit(c[j], (i-75, 240))
                j+=1
            gtwitch=[-40,-40,-40,-40,-40,-40,-40,-40,-40]
            gtwi=38
            for i in range(ol):
                gtwitch[i]=gtwi
                gtwi+=76
            buttons1=pygame.sprite.Group(o1,o2,o3,o4,o5,o6,o7,o8,o9)
            buttons1.draw(screen)
            click, mode = bGS.update(mX, mY, click, mode)
            click, mode, sun, pHands, oHands, deck3, cnt = bGO.update(mX, mY, click, mode, sun, pHands, oHands, deck3, cnt)
            click, mode, sun = bGT.update(mX, mY, click, mode, sun)
            click, mode, que = o1.update(mX, mY, click, mode, gtwitch[0], 0, que)
            click, mode, que = o2.update(mX, mY, click, mode, gtwitch[1], 1, que)
            click, mode, que = o3.update(mX, mY, click, mode, gtwitch[2], 2, que)
            click, mode, que = o4.update(mX, mY, click, mode, gtwitch[3], 3, que)
            click, mode, que = o5.update(mX, mY, click, mode, gtwitch[4], 4, que)
            click, mode, que = o6.update(mX, mY, click, mode, gtwitch[5], 5, que)
            click, mode, que = o7.update(mX, mY, click, mode, gtwitch[6], 6, que)
            click, mode, que = o8.update(mX, mY, click, mode, gtwitch[7], 7, que)
            click, mode, que = o9.update(mX, mY, click, mode, gtwitch[8], 8, que)
            try:
                screen.blit(nowcard, (0, 120))
            except:
                oo=0;
                
            clock.tick(60)
            pygame.display.flip() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0

        while mode=="defcom":
            print(modedp, state)
            nowcard, backgroundRect = imageLoad("back.png", 1)
            nowcard.set_colorkey(beige)
            to+=1
            if to>=10:
                mode=modedp
                to=0
                state=0
                continue
            try:
                if state==0:
                    temp=receive_data()
                    if temp=='000' or temp=='00' or temp[1:]=='00':
                        to=0
                        state=1
                elif state==1:
                    send_data(0,0,0)
                    temp=receive_data()
                    if temp[0]=='1':
                        to=0
                        state=2
                        buf=0
                        t2=int(temp[2])
                        if temp[1]=='A':
                            nowcard, backgroundRect = imageLoad(CT[0], 1)
                            nowcard.set_colorkey(beige)
                            ol-=1
                            if t2>0:
                                if pHands[t2-1]==CT[2]:
                                    buf=2
                                    del pHands[t2-1]
                                    continue
                            if t2+1<len(pHands):
                                if pHands[t2+1]==CT[2]:
                                    buf=2
                                    del pHands[t2+1]
                                    continue
                            if pHands[t2]==CT[3]:
                                buf=3
                                del pHands[t2]
                                pHands=pHands+deck3[:2]
                                deck3=deck3[2:]
                                continue
                            elif pHands[t2]==CT[4]:
                                buf=4
                                cnt=1
                                del pHands[t2]
                                continue
                            else:
                                if pHands[t2]==CT[6]:
                                    buf=6
                                    pHeart-=1
                                del pHands[t2]
                        elif temp[1]=='S':
                            nowcard, backgroundRect = imageLoad(CT[1], 1)
                            nowcard.set_colorkey(beige)
                            ol-=1
                            k1=0
                            for i in pHands:
                                if buf!=0:
                                    continue
                                for j in range(2,5):
                                    if i == CT[j]:
                                        buf=j
                                        del pHands[k1]
                                        continue
                                k1+=1
                        elif temp[1]=='H':
                            nowcard, backgroundRect = imageLoad(CT[5], 1)
                            nowcard.set_colorkey(beige)
                            ol+=1
                            buf=0
                        elif temp[1]=='T':
                            nowcard, backgroundRect = imageLoad("back.png", 1)
                            nowcard.set_colorkey(beige)
                            cnt=1
                elif state==2:
                    send_data(2,buf,0)
                    temp=receive_data()
                    if temp=='999':
                        to=0
                        state=0
                        to2=0
                        que=[]
                        tuk=9
                        cnt-=1
                        if oHeart==0:
                            cnt=2
                            mode="win"
                            continue
                        if pHeart==0:
                            cnt=2
                            mode="los"
                            continue
                        if cnt==0:
                            cnt=2
                            pHands=pHands+deck3[:2]
                            deck3=deck3[2:]
                            mode="att"
                        else:
                            mode=modedp
            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            buttons=pygame.sprite.Group(bGS, bGO)
            buttons.draw(screen)
            pPT=PT[len(pHands)]
            j=0
            c=[0]*len(pHands)
            for i in pPT:
                c[j], backgroundRect = imageLoad(pHands[j], 1)
                c[j].set_colorkey(beige)
                screen.blit(c[j], (i-75, 240))
                j+=1
            gtwitch=[-40,-40,-40,-40,-40,-40,-40,-40,-40]
            gtwi=38
            for i in range(ol):
                gtwitch[i]=gtwi
                gtwi+=76
            buttons1=pygame.sprite.Group(o1,o2,o3,o4,o5,o6,o7,o8,o9)
            buttons1.draw(screen)
            click, mode = bGS.update(mX, mY, click, mode)
            click, mode, sun, pHands, oHands, deck3, cnt = bGO.update(mX, mY, click, mode, sun, pHands, oHands, deck3, cnt)
            click, mode, sun = bGT.update(mX, mY, click, mode, sun)
            click, mode, que = o1.update(mX, mY, click, mode, gtwitch[0], 0, que)
            click, mode, que = o2.update(mX, mY, click, mode, gtwitch[1], 1, que)
            click, mode, que = o3.update(mX, mY, click, mode, gtwitch[2], 2, que)
            click, mode, que = o4.update(mX, mY, click, mode, gtwitch[3], 3, que)
            click, mode, que = o5.update(mX, mY, click, mode, gtwitch[4], 4, que)
            click, mode, que = o6.update(mX, mY, click, mode, gtwitch[5], 5, que)
            click, mode, que = o7.update(mX, mY, click, mode, gtwitch[6], 6, que)
            click, mode, que = o8.update(mX, mY, click, mode, gtwitch[7], 7, que)
            click, mode, que = o9.update(mX, mY, click, mode, gtwitch[8], 8, que)
            try:
                screen.blit(nowcard, (0, 120))
            except:
                oo=0;
                
            clock.tick(60)
            pygame.display.flip() 
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0

        while mode=="win": #
            try:
                if to2<5:
                    modedp=mode
                    to=0
                    send_data(9,9,9)
                    to2+=1
            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            
            title, backgroundRect = imageLoad("title.png", 0)
            screen.blit(title, (230,30))
            buttons=pygame.sprite.Group(bGO)
            buttons.draw(screen)
            click, mode, sun, pHands, oHands, deck3, cnt = bGO.update(mX, mY, click, mode, sun, pHands, oHands, deck3, cnt)

            clock.tick(60)
            pygame.display.flip()                           #
        
            for event in pygame.event.get():
                if event.type==QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0
                    
        while mode=="los": #
            try:
                if to2<5:
                    modedp=mode
                    to=0
                    send_data(9,9,9)
                    to2+=1
            except:
                oo=0;
            background, backgroundRect = imageLoad("bjs2.png", 0)
            screen.blit(background, backgroundRect)
            
            title, backgroundRect = imageLoad("title.png", 0)
            screen.blit(title, (230,30))
            buttons=pygame.sprite.Group(bGO)
            buttons.draw(screen)
            click, mode, sun, pHands, oHands, deck3, cnt = bGO.update(mX, mY, click, mode, sun, pHands, oHands, deck3, cnt)

            clock.tick(60)
            pygame.display.flip()                           #
        
            for event in pygame.event.get():
                if event.type==QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                elif event.type == MOUSEBUTTONUP:
                    mX, mY = 0, 0
                    click = 0
                    
if __name__ == "__main__":
    mainGame()

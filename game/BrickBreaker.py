'''
Todo
-fix the scrolling speed of cursor to only go one square at a time
- have it so when you press y the dot appears of that player either white or blue
- check the winning combinations to see if someone has won the game and show win on the screen
- make it so players take turns 
- make it sure a player cant move into a square that has been used
myboard layout
6 = midtop
7 = lefttop
8 = righttop
0 = middle middle
1 = middle left
2 = middle right
3 = mid bot
4 = mid left
5 = mid right
'''

import spyral
import random
import math

WIDTH = 1200
HEIGHT = 800
BG_COLOR = (0,0,0)
WHITE = (255, 255, 255)
SIZE = (WIDTH, HEIGHT)
MOVE_PLAYED = 0
playerTurn = "red"
playerPiece = 1
doneOnce = False
gameOver = False
myboard = ["82-11=?","77/11=?","5+5=?","80-32=?","27/3=?","27*3=?","10-7=?","5*6=?","11-3=?"] # board is global every one has access 
myboard_answers = ["71", "7","10","48","9","81","3","30","8"]
# spyral.image.Image(filename = "images/hand_red.png")

class gameOver(spyral.Sprite):
     def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        self.x = WIDTH - WIDTH
        self.y = HEIGHT - 700
        self.image = spyral.image.Image(filename = "images/gameover.png", size = None)

class Paddle(spyral.Sprite):
    global doneOnce
    def __init__(self, scene):
        spyral.Sprite.__init__(self, scene)
        global playerTurn
        if(playerTurn == "red"):
            self.image = spyral.image.Image(filename = "images/hand_red.png", size = None)
        elif(playerTurn == "blue"):
            self.image = spyral.image.Image(filename = "images/hand_blue.png", size = None)
        self.x = WIDTH/2
        self.y = HEIGHT - 200
        self.moving = False
      
        left = "left"
        right="right"
        up = "up"
        down = "down"
        enter = "]"
        spyral.event.register("input.keyboard.down."+left, self.move_left)
        spyral.event.register("input.keyboard.down."+right, self.move_right)
        spyral.event.register("input.keyboard.up."+left, self.stop_move)
        spyral.event.register("input.keyboard.up."+right, self.stop_move)
        spyral.event.register("input.keyboard.down."+up, self.move_up)
        spyral.event.register("input.keyboard.down."+down, self.move_down)
        spyral.event.register("input.keyboard.up."+up, self.stop_move)
        spyral.event.register("input.keyboard.up."+down, self.stop_move)
        spyral.event.register("input.keyboard.down."+enter, self.place_piece)
        spyral.event.register("input.keyboard.up."+enter, self.stop_move)
        spyral.event.register("input.mouse.left.click", self.askquest)
        spyral.event.register("director.update", self.update)
    

      
    
    def askquest(self):
        print "pos_x"
       
    #    spyral.event.register("pong_score", self._reset)
        
    def move_left(self):
        self.moving = 'left'
    def move_right(self):
        self.moving = 'right'
    def move_up(self):
        self.moving = 'up'
    def move_down(self):
        self.moving = 'down'
    def place_piece(self):
        global doneOnce
        self.moving = 'place_piece'
        doneOnce = False
        print "changed doneOnce to False"
    def stop_move(self):
        self.moving = False
    def _reset(self): # New might want to change this
        self.y = HEIGHT/2
        
    def update(self, delta):
        paddle_velocity = 500
        global playerTurn
        if(playerTurn == "red"):
            self.image = spyral.image.Image(filename = "images/hand_red.png", size = None)
        elif(playerTurn == "blue"):
            self.image = spyral.image.Image(filename = "images/hand_blue.png", size = None)
        if self.moving == 'left':
            self.x -= paddle_velocity * delta
        elif self.moving == 'right':
            self.x += paddle_velocity * delta
        elif self.moving == 'up':
            self.y -= paddle_velocity * delta
        elif self.moving == 'down':
            self.y += paddle_velocity * delta
        elif self.moving == 'place_piece': # if player presses y places piece certain place on board
            #This checks to see where the paddle is an places a dot there have to check which piece to place who turn it is
           
            global MOVE_PLAYED
            global playerPiece
            
            MOVE_PLAYED = 1 # problem here this keeps running reseting to 1
            
            if(self.y < 280 and self.x < 481 and myboard[7] != 1 or myboard[7] != 2): # top left
                myboard[7] = playerPiece
            elif(self.y < 280 and self.x < 700 and self.x > 481 and myboard[6] == 0): # top mid
                myboard[6] = playerPiece
            elif(self.y < 280 and self.x < 890 and self.x > 700 and myboard[8] == 0): # top right
                myboard[8] = playerPiece
            elif((self.y < 508 and self.y > 280) and self.x < 470 and myboard[1] == 0): # mid left
                myboard[1] = playerPiece
            elif((self.y < 508 and self.y > 280) and self.x < 700 and self.x > 481 and myboard[0] == 0): # mid mid
                myboard[0] = playerPiece
            elif((self.y < 508 and self.y > 280) and self.x > 700 and self.x < 890 and myboard[2] == 0): # mid right
                myboard[2] = playerPiece
            elif(self.y > 508 and self.x < 481 and myboard[4] == 0): #bot left
                myboard[4] = playerPiece
            elif(self.y > 508 and self.x < 700 and self.x > 481 and myboard[3] == 0): #mid bot
                myboard[3] = playerPiece
            elif(self.y > 508 and self.x > 700 and self.x < 890 and myboard[5] == 0): # bot right
                myboard[5] = playerPiece
        r = self.rect
        if r.top < 0:
            r.top = 0
        if r.bottom > HEIGHT:
            r.bottom = HEIGHT
            
        #self.pos == getattr(r, self.anchor)
    
'''
Used to draw the board.

'''
class boardLineHoriz(spyral.Sprite):
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(size=(600, 20)).fill((100, 200, 100))
        self.x = pos_x
        self.y = pos_y
        self.moving = False
    

class boardLineVert(spyral.Sprite):
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.Image(size=(20, 600)).fill((100, 200, 100))
        self.x = pos_x
        self.y = pos_y
        self.moving = False


'''
we have two peices for the game white pieces 
and blue pieces we dont have X and O, maybe 
later if there is time.
'''
class piece(spyral.Sprite):
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.image.Image(filename = "images/letterx.png", size = None)
        self.x = pos_x
        self.y = pos_y
        self.moving = False
class blue_piece(spyral.Sprite):
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.image.Image(filename = "images/lettero.png", size = None)
        self.x = pos_x
        self.y = pos_y
        self.moving = False

# placing boxes on board!
class questionTopLef(spyral.Sprite):
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.image.Image(filename = "images/5mul6.png", size = None)
        self.x = WIDTH - 920
        self.y = HEIGHT - 700
        self.moving = False
class questionTopMid(spyral.Sprite):
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.image.Image(filename = "images/10sub7.png", size = None)
        self.x = WIDTH - 700
        self.y = HEIGHT - 700
        self.moving = False
class questionTopRig(spyral.Sprite):
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image =  spyral.image.Image(filename = "images/11sub3.png", size = None)
        self.x = WIDTH - 475
        self.y = HEIGHT - 710
        self.moving = False
class questionMidLef(spyral.Sprite):
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image =  spyral.image.Image(filename = "images/77div11.png", size = None)
        self.x = WIDTH - 920
        self.y = HEIGHT - 500
        self.moving = False
class questionMidMid(spyral.Sprite):
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image = spyral.image.Image(filename = "images/82sub11.png", size = None)
        self.x = WIDTH - 700
        self.y = HEIGHT - 500
        self.moving = False
class questionMidRig(spyral.Sprite): # good
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image =  spyral.image.Image(filename = "images/5add5.png", size = None)
        self.x = WIDTH - 475
        self.y = HEIGHT - 500
        self.moving = False
class questionBotLef(spyral.Sprite): # good
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image =  spyral.image.Image(filename = "images/27div3.png", size = None)
        self.x = WIDTH - 920
        self.y = HEIGHT - 250
        self.moving = False
class questionBotMid(spyral.Sprite): # good
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image =  spyral.image.Image(filename = "images/80sub32.png", size = None)
        self.x = WIDTH - 700
        self.y = HEIGHT - 250
        self.moving = False
class questionBotRig(spyral.Sprite): # good
    def __init__(self, scene, pos_x, pos_y):
        spyral.Sprite.__init__(self, scene)
        self.image =  spyral.image.Image(filename = "images/27mul3.png", size = None)
        self.x = WIDTH - 475
        self.y = HEIGHT - 250
        self.moving = False
class font(spyral.Sprite): # good
    def __init__(self, scene, font, text):
        spyral.Sprite.__init__(self, scene)
        font = spyral.Font(font, 80)
        self.image = font.render(text,color=(100, 200, 100))
        self.x = 450
        self.y = 0
        self.moving = False

class Pong(spyral.Scene):
    def __init__(self, *args, **kwargs):
        global manager
        global doneOnce
        global MOVE_PLAYED
        global doneOnce
        global my_form
        global myboard
        spyral.Scene.__init__(self, SIZE)
        self.background = spyral.Image(size=SIZE).fill(BG_COLOR)
        spyral.event.register("input.mouse.down", self.printsomething)
    
        #self.paddle = Paddle(self)
        

        class answerForm(spyral.Form):
            answer = spyral.widgets.TextInput(200, "enter answer")
            okay = spyral.widgets.Button("Submit")

        my_form = answerForm(self)
        my_form.answer.pos = (0,25)
        my_form.okay.pos = (0,50)
        my_form.focus()
        
        


        ''' 
        will draw board here.
        '''

        self.brick_BotRight = boardLineHoriz(self, WIDTH - 900, HEIGHT - (HEIGHT - 275)) #player piece that shows where to move
        self.brick_BotRight = boardLineHoriz(self, WIDTH - 900, HEIGHT - (HEIGHT - 500))
        self.brick_BotRight = boardLineVert(self, WIDTH - 725, HEIGHT - (HEIGHT - 100))
        self.brick_BotRight = boardLineVert(self, WIDTH - 500, HEIGHT - (HEIGHT - 100))
        self.font = font(self,"fonts/Bite_Bullet.ttf","glhf :)")

        #placing questions
        self.questionTopLef = questionTopLef(self, WIDTH - 500, HEIGHT - (HEIGHT - 100))
        self.questionTopMid = questionTopMid(self, WIDTH - 500, HEIGHT - (HEIGHT - 100))
        self.questionTopRig = questionTopRig(self, WIDTH - 500, HEIGHT - (HEIGHT - 100))
        self.questionMidLef = questionMidLef(self, WIDTH - 500, HEIGHT - (HEIGHT - 100))
        self.questionMidMid = questionMidMid(self, WIDTH - 500, HEIGHT - (HEIGHT - 100))
        self.questionMidRig = questionMidRig(self, WIDTH - 500, HEIGHT - (HEIGHT - 100))
        self.questionBotLef = questionBotLef(self, WIDTH - 500, HEIGHT - (HEIGHT - 100))
        self.questionBotMid = questionBotMid(self, WIDTH - 500, HEIGHT - (HEIGHT - 100))
        self.questionBotRig = questionBotRig(self, WIDTH - 500, HEIGHT - (HEIGHT - 100))
        spyral.event.register("director.update", self.update)
        spyral.event.register("system.quit", spyral.director.pop)
           


    #mouse click event which will be used to select the different square 
    #so that a user can answer questions and all
    def printsomething(self,pos, button):
        global MOVE_PLAYED
        global playerPiece
        global answerKey
        global where
        global doneOnce
        global font
        print "hey"
        print pos , button
        print pos[0] #pos x
        print pos[1] #pos y     
        if((pos[1] < 508 and pos[1] > 280) and pos[0] < 744 and pos[0] > 529): #if a user clicks the middle square!
            self.font.kill()    
            self.font = font(self,"fonts/Bite_Bullet.ttf",myboard[0])
            answerKey = myboard_answers[0]
            where = 0
        elif((pos[1] < 508 and pos[1] > 280) and pos[0] < 504 and pos[0] > 317): # mid left
            self.font.kill()
            self.font = font(self,"fonts/Bite_Bullet.ttf",myboard[1])
            answerKey = myboard_answers[1]
            where = 1
        elif((pos[1] < 508 and pos[1] > 280) and pos[0] < 950 and pos[0] > 750): # mid right
            self.font.kill()
            self.font = font(self,"fonts/Bite_Bullet.ttf",myboard[2])
            answerKey = myboard_answers[2]
            where = 2
        elif((pos[1] < 270 and pos[1] > 100) and pos[0] < 744 and pos[0] > 529): # top mid
            self.font.kill()
            self.font = font(self,"fonts/Bite_Bullet.ttf",myboard[6])
            answerKey = myboard_answers[6]
            where = 6
        elif((pos[1] < 270 and pos[1] > 100) and pos[0] < 504 and pos[0] > 317): # top left
            self.font.kill()
            self.font = font(self,"fonts/Bite_Bullet.ttf",myboard[7])
            answerKey = myboard_answers[7]
            where = 7
        elif((pos[1] < 270 and pos[1] > 100) and pos[0] < 950 and pos[0] > 750): # top right
            self.font.kill()
            self.font = font(self,"fonts/Bite_Bullet.ttf",myboard[8])
            answerKey = myboard_answers[8]
            where = 8
        elif((pos[1] < 700 and pos[1] > 520) and pos[0] < 744 and pos[0] > 529): # bot mid
            self.font.kill()
            self.font = font(self,"fonts/Bite_Bullet.ttf",myboard[3])
            answerKey = myboard_answers[3]
            where = 3  
        elif((pos[1] < 700 and pos[1] > 520) and pos[0] < 504 and pos[0] > 317): # bot left
            self.font.kill()
            self.font = font(self,"fonts/Bite_Bullet.ttf",myboard[4])
            answerKey = myboard_answers[4]
            where = 4 
        elif((pos[1] < 700 and pos[1] > 520) and pos[0] < 950 and pos[0] > 750): # bot right
            self.font.kill()
            self.font = font(self,"fonts/Bite_Bullet.ttf",myboard[5])
            answerKey = myboard_answers[5]
            where = 5  

        #checks to see if you clicked the submit button    
        if(pos[0] < 102 and pos[0] > 0 and pos[1] < 75 and pos[1] > 50): 
            print "you clicked the button"
            print my_form.answer.value
            if(my_form.answer.value == answerKey):
                myboard[where] = playerPiece
                print "correct answer"
                doneOnce = False
                MOVE_PLAYED = 1

            


    def update(self, delta):
        global MOVE_PLAYED
        global playerTurn
        global playerPiece
        global gameOver
        global doneOnce
        #print MOVE_PLAYED
        if(MOVE_PLAYED == 1):
            if(myboard[0] == 1):
                self.brick_BotRight = piece(self, WIDTH - 630, HEIGHT - (HEIGHT - 350)) # middle square
                self.questionMidMid.visible = False
            if(myboard[0] == 2):
                self.brick_BotRight = blue_piece(self, WIDTH - 630, HEIGHT - (HEIGHT - 350)) # middle square
                self.questionMidMid.visible = False
            if(myboard[1] == 1):
                self.brick_BotRight = piece(self, WIDTH - 860, HEIGHT - (HEIGHT - 350)) # left middle square
                self.questionMidLef.visible =False
            if(myboard[1] == 2):
                self.brick_BotRight = blue_piece(self, WIDTH - 860, HEIGHT - (HEIGHT - 350)) # left middle square
                self.questionMidLef.visible =False
            if(myboard[2] == 1):
                self.brick_BotRight = piece(self, WIDTH - 430, HEIGHT - (HEIGHT - 350)) # right middle square
                self.questionMidRig.visible = False
            if(myboard[2] == 2):
                self.brick_BotRight = blue_piece(self, WIDTH - 430, HEIGHT - (HEIGHT - 350)) # right mid 
                self.questionMidRig.visible = False
            if(myboard[3] == 1):
                self.brick_BotRight = piece(self, WIDTH - 630, HEIGHT - (HEIGHT - 575)) # middle bot
                self.questionBotMid.visible = False
            if(myboard[3] == 2):
                self.brick_BotRight = blue_piece(self, WIDTH - 630, HEIGHT - (HEIGHT - 575))
                self.questionBotMid.visible = False
            if(myboard[4] == 1):
                self.brick_BotRight = piece(self, WIDTH - 860, HEIGHT - (HEIGHT - 575)) # left bot
                self.questionBotLef.visible = False
            if(myboard[4] == 2):
                self.brick_BotRight = blue_piece(self, WIDTH - 860, HEIGHT - (HEIGHT - 575))
                self.questionBotLef.visible = False
            if(myboard[5] == 1):
                self.brick_BotRight = piece(self, WIDTH - 430, HEIGHT - (HEIGHT - 575)) # right bot
                self.questionBotRig.visible = False
            if(myboard[5] == 2):
                self.brick_BotRight = blue_piece(self, WIDTH - 430, HEIGHT - (HEIGHT - 575))
                self.questionBotRig.visible = False
            if(myboard[6] == 1):
                self.brick_BotRight = piece(self, WIDTH - 630, HEIGHT - (HEIGHT - 150)) # middle top
                self.questionTopMid.visible = False
            if(myboard[6] == 2):
                self.brick_BotRight = blue_piece(self, WIDTH - 630, HEIGHT - (HEIGHT - 150))
                self.questionTopMid.visible = False
            if(myboard[7] == 1):
                print "no"
                self.brick_BotRight = piece(self, WIDTH - 860, HEIGHT - (HEIGHT - 150)) # left top
                self.questionTopLef.visible = False    
            if(myboard[7] == 2):
                self.brick_BotRight = blue_piece(self, WIDTH - 860, HEIGHT - (HEIGHT - 150))
                self.questionTopLef.visible = False   
            if(myboard[8] == 1):
                self.brick_BotRight = piece(self, WIDTH - 430, HEIGHT - (HEIGHT - 150)) # right top
                self.questionTopRig.visible =False
            if(myboard[8] == 2):
                self.brick_BotRight = blue_piece(self, WIDTH - 430, HEIGHT - (HEIGHT - 150))
                self.questionTopRig.visible =False
            while(doneOnce == False):
                global doneOnce
                if(playerTurn == "red"):
                    playerTurn = "blue"
                elif(playerTurn == "blue"):
                    playerTurn = "red"
                if(playerPiece == 1):
                    playerPiece = 2
                elif(playerPiece == 2):
                    playerPiece = 1
                if((myboard[6] == 1 and myboard[7] == 1 and myboard[8] ==1) or (myboard[6] == 2 and myboard[7] == 2 and myboard[8] ==2)): #checks top
                    self.go = gameOver(self)
                elif((myboard[0] == 1 and myboard[1] == 1 and myboard[2] ==1) or (myboard[0] == 2 and myboard[1] == 2 and myboard[2] ==2)): #checks mid
                    self.go = gameOver(self)
                elif((myboard[3] == 1 and myboard[4] == 1 and myboard[5] ==1) or (myboard[3] == 2 and myboard[4] == 2 and myboard[5] ==2)): #checks bot
                    self.go = gameOver(self)
                elif((myboard[1] == 1 and myboard[4] == 1 and myboard[7] ==1) or (myboard[1] == 2 and myboard[4] == 2 and myboard[7] ==2)): #checks left
                    self.go = gameOver(self)
                elif((myboard[3] == 1 and myboard[0] == 1 and myboard[6] ==1) or (myboard[3] == 2 and myboard[0] == 2 and myboard[6] ==2)): #checks mid
                    self.go = gameOver(self)
                elif((myboard[2] == 1 and myboard[5] == 1 and myboard[8] ==1) or (myboard[2] == 2 and myboard[5] == 2 and myboard[8] ==2)): #checks right
                    self.go = gameOver(self)
                elif((myboard[0] == 1 and myboard[4] == 1 and myboard[8] ==1) or (myboard[0] == 2 and myboard[4] == 2 and myboard[8] ==2)): #check diag
                    self.go = gameOver(self)
                elif((myboard[7] == 1 and myboard[5] == 1 and myboard[0] ==1) or (myboard[0] == 2 and myboard[7] == 2 and myboard[5] ==2)): #check diag2
                    self.go = gameOver(self)
                doneOnce = True
            MOVE_PLAYED = 0
            
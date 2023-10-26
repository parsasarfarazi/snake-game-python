import sys
import random
from tkinter import *

class Board(Canvas):

    def __init__(self):
        #our initial variables
        self.width = 400
        self.height = 400
        self.bodyPartSize = 20
       
        # now we call Canvas cunstructor to make our board
        super().__init__(width=self.width, height=self.height,
            background="white", highlightthickness=0)
        #we use this variabales to:
        #see if we are in game or not
        self.runGame = True
        #count our body parts
        self.bodyParts = 2
        #keep track of our score
        self.score = 0
        #move the snake
        self.moveX = self.bodyPartSize     
        self.moveY = 0
        #to place the food
        self.foodX = 0
        self.foodY = 0
        
        # we call this to make snake and food on canvas
        self.createObjects()

        self.placeFood()
        # to use our keyboards dir
        self.bind_all("<Key>", self.keyPressing)
        #now the game really starts
        self.after(300, self.onTimer)
        self.pack()



    def createObjects(self):
        '''this function creates snake and food objects on Canvas'''
        #score counter
        self.create_text(30, 10, text="Score: {0}".format(self.score),
                         tag="score", fill="black")
        #head
        self.create_rectangle(20, 20, 20+ self.bodyPartSize ,20+self.bodyPartSize, fill="brown",  tag="head")
        #bodyParts
        self.create_rectangle(0, 20, 0+self.bodyPartSize,20+self.bodyPartSize,  fill="pink", tag="bodyPart")
        #food
        self.create_oval(self.foodX, self.foodY,self.foodX+self.bodyPartSize,self.foodY+self.bodyPartSize,
                                fill="red", tag="food")
     
    def placeFood(self):
        '''places the food object on Canvas'''

        food = self.find_withtag("food")
        self.delete(food[0])

        r = random.randint(0, 19)
        self.foodX = r * self.bodyPartSize
        r = random.randint(0, 19)
        self.foodY = r * self.bodyPartSize

        self.create_oval(self.foodX, self.foodY,self.foodX+self.bodyPartSize,self.foodY+self.bodyPartSize,
                                fill="red", tag="food")

    def keyPressing(self, e):

        key = e.keysym

        LEFT_CURSOR_KEY = "Left"
        if key == LEFT_CURSOR_KEY and self.moveX <= 0:

            self.moveX = -self.bodyPartSize
            self.moveY = 0

        RIGHT_CURSOR_KEY = "Right"
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:

            self.moveX = self.bodyPartSize
            self.moveY = 0

        RIGHT_CURSOR_KEY = "Up"
        if key == RIGHT_CURSOR_KEY and self.moveY <= 0:

            self.moveX = 0
            self.moveY = -self.bodyPartSize

        DOWN_CURSOR_KEY = "Down"
        if key == DOWN_CURSOR_KEY and self.moveY >= 0:

            self.moveX = 0
            self.moveY = self.bodyPartSize

    def onTimer(self):
        '''main loop of game'''

        #draw score
        score = self.find_withtag("score")
        self.itemconfigure(score, text="Score: {0}".format(self.score))

        self.checkCollisions()

        if self.runGame:
            self.checkFoodEat()
            self.moveSnake()
            self.after(300, self.onTimer)
        else:
            #game over
            self.delete(ALL)
            self.create_text(self.winfo_width() /2, self.winfo_height()/2,
            text="Game Over!", fill="red")

    def checkFoodEat(self):
        '''checks if the head of snake collides with food'''

        food = self.find_withtag("food")
        head = self.find_withtag("head")

        xs, ys, xt, yt = self.bbox(head)
        overlap = self.find_enclosed(xs, ys, xt, yt)

        for x in overlap:

            if food[0] == x:

                self.score += 1
                xx1, yy1,xx2,yy2 = self.bbox(food)
                self.create_rectangle(xx1, yy1,xx2-2 ,yy2-2,fill="pink", tag="bodyPart")
                self.placeFood()

    def moveSnake(self):
        '''moves the Snake object'''

        bodyParts = self.find_withtag("bodyPart")
        head = self.find_withtag("head")

        fullBody = bodyParts + head

        x = 0
        while x < len(fullBody)-1:

            c1 = self.coords(fullBody[x])
            c2 = self.coords(fullBody[x+1])
            self.move(fullBody[x], c2[0]-c1[0], c2[1]-c1[1])
            x += 1

        self.move(head, self.moveX, self.moveY)

    def checkCollisions(self):

        bodyParts = self.find_withtag("bodyPart")
        head = self.find_withtag("head")

        xs, ys, xt, yt = self.bbox(head)
        overlap = self.find_enclosed(xs, ys, xt, yt)

        for bP in bodyParts:
            for x in overlap:
                if x == bP:
                  self.runGame = False

        if xs+1 < 0:
            self.runGame = False

        if xs > self.width - self.bodyPartSize:
            self.runGame = False

        if ys+1 < 0:
            self.runGame = False

        if ys > self.height - self.bodyPartSize:
            self.runGame = False

   
class Snake(Frame):

    def __init__(self):
        # we use super()method to access the parent class which is Frame class
        super().__init__()

        self.master.title('Snake Game')
        #we now create an obj from Board class

        self.mainBoard = Board()
        self.pack()
def main():

    root = Tk()
    # we create an obj from Snake class
    cobra = Snake()
    root.mainloop()

if __name__ == '__main__':
    main()

from image_util import*


from tkinter import *
import random
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.image = PhotoImageFromLink("https://www.cs.cmu.edu/~112/notes/hw6-112-icon.gif")
    randomIndex = random.randint(0, data.width)
    data.imageX = randomIndex
    data.imageY = randomIndex
    data.velocityX = 5
    data.velocityY = 5
    data.mode = "startScreen"
    data.scrollX = 0
    data.scrollY = 0
    data.deltaX = 10
    data.deltaY = 10
    data.list = []
    data.scrollMargin = 50
    data.playerX = data.scrollMargin # player's left edge
    data.playerY = data.scrollMargin  # player's bottom edge (distance above the base line)
    data.score = 0
    data.time = 20
    pass

def mousePressed(event, data):
    is_popped = False
    for i in range(len(data.list) - 1,0,-1):
        if(event.x >= data.list[i][0] and event.x <= data.list[i][0] + 50):
            if(event.y >= data.list[i][1] and event.y <= data.list[i][1] + 50):
                is_popped = True
                data.score = data.score + 1
                if(data.score % 5 == 0):
                    data.time = data.time + 1
                break
    if(is_popped == True):
        data.list.pop(i)
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    if(event.keysym == "p"):
        data.mode = "gameState"
    if(event.keysym == "Right"):
        data.scrollX = data.scrollX - data.deltaX
    if(event.keysym == "Left"):
        data.scrollX = data.scrollX + data.deltaX
    if(event.keysym == "Up"):
        data.scrollY = data.scrollY + data.deltaY
    if(event.keysym == "Down"):
        data.scrollY = data.scrollY - data.deltaY
    pass

def timerFired(data):
    if(data.mode == "startScreen"):
        data.imageX = data.imageX - data.velocityX
        data.imageY = data.imageY + data.velocityY
        if(data.imageY < 0 or data.imageY > data.height):
            data.velocityY = -data.velocityY
        if(data.imageX < 0 or data.imageX > data.width):
            data.velocityX = -data.velocityX
    if(data.mode == "gameState"): 
        data.list.append(generateRandomPoint(data))
    data.time = data.time - 1

    pass

# def gameOver(canvas,data):
#      canvas.create_text(data.width/2,data.height/2,text = "Game is Over",font = "40")
     
def generateRandomPoint(data):
    randomIndexX = random.randint(0, data.width)
    randomIndexY = random.randint(0, data.width)
    data.imageX = randomIndexX
    data.imageY = randomIndexY
    newList = [data.imageX,data.imageY]
    print(newList)
    return newList

def drawGame(canvas,data):
    if(data.mode == "startScreen"):
        canvas.create_text(data.width / 2,data.height/4,text = "The 112 Clicker Game!",font = "40")
        canvas.create_text(data.width / 2,data.height/4 * 3,text = "Press 'p' to play",font = "40")
        canvas.create_image(data.imageX, data.imageY, image = data.image)
    if(data.mode == "gameState"):
        canvas.create_rectangle(data.scrollX, data.scrollY, data.scrollX + 2 * data.width, data.scrollY + 2 * data.height,width = 5)
        for i in range(len(data.list)):
            canvas.create_image(data.list[i][0], data.list[i][1], image = data.image)
        canvas.create_text(50,350,text = "Score: %d" %data.score)
        canvas.create_text(50,50,text = "Time Left: %d" %data.time)

def redrawAll(canvas, data):
    drawGame(canvas,data)

    
    # draw in canvas
    pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 800 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 400)
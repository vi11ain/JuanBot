#!  python3
import pyautogui
import time
import os
import logging
import sys
import random
import copy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s.%(msecs)03d: %(message)s', datefmt='%H:%M:%S')
#logging.disable(logging.DEBUG) # uncomment to block debug log messages

# Global variables
LEVEL = 2 # Current level being played
EMPTYLINES = [0,0,0,0,0,0,0,0] # (1,2,3,4,5,6,7,8) what lines are already cleaned and don't need to be checked, 1 = cleaned

# various coordinates of objects in the game
GAME_REGION = () # (left, top, width, height) values coordinates of the entire game window
PEARL_REGION = ()
GO_COORDS = None
NEW_GAME_COORDS = None

def main():
    """Runs the entire program. Pearls Before Swine 3 game must be visible on the screen and the New Game button visible."""
    logging.debug('JuanBot')
    logging.debug('To interrupt mouse movement, move mouse to upper left corner.\n')
    getGameRegion()
    setupCoordinates()
    navigateStartGameMenu()
    startPlaying()

def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    return os.path.join('images', filename)


def getGameRegion():
    """Obtains the region that the Sushi Go Round game is on the screen and assigns it to GAME_REGION. The game must be at the start screen (where the New Game button is visible)."""
    global GAME_REGION

    # identify the top-left corner
    logging.debug('Finding game region...')


    region = pyautogui.locateOnScreen(imPath('top_right_corner.png'))
    print()
    if region is None:
        raise Exception('Could not find game on screen. Is the game visible?')

    # calculate the region of the entire game
    topRightX = region[0] + region[2] # left + width
    topRightY = region[1] # top
    GAME_REGION = (topRightX - 1792, topRightY, 1792, 891) # the game screen is 95% of website's screen
    logging.debug('Game region found: %s' % (GAME_REGION,))

def setupCoordinates():
    """Sets several of the coordinate-related global variables, after acquiring the value for GAME_REGION."""
    global NEW_GAME_COORDS, GO_COORDS, PEARL_REGION

    logging.debug('Initialising button coordinates...')
    NEW_GAME_COORDS = (GAME_REGION[0] + 1280, GAME_REGION[1] + 480)
    GO_COORDS = (GAME_REGION[0] + 560, GAME_REGION[1] + 280)
    #PEARL_REGION = (GAME_REGION[0] + 450, GAME_REGION[1] + 600, 648, 224)
    # Extended pearl region for high levels
    PEARL_REGION = (GAME_REGION[0] + 320, GAME_REGION[1] + 600, 1239, 222)

def navigateStartGameMenu():
    """Performs the clicks to navigate form the start screen (where the New Game button is visible) to the beginning of the first level."""
    # Click on everything needed to get past the menus at the start of the
    # game.

    # click on New Game
    # pyautogui.click(NEW_GAME_COORDS[0],NEW_GAME_COORDS[1],duration=0.25)
    logging.debug('Clicked on New Game button.')

def pearlSearch():
    global EMPTYLINES
    # screenshot variable to hold the image of the table region in the game
    screenshot = pyautogui.screenshot(region=PEARL_REGION)
    # line is holding the coords of each pearl in a line
    line = []
    # listOfLines is holding each line
    listOfLines= []

    # Searching for each pearl in the table region, adapt the pearl coords to game region and appending it to line list, than appending the line list to listOfLines and reseting line
    # Starting to search for pearls in line 1 and 2

    if not EMPTYLINES[0]:
        logging.debug('Searching for pearls in first row...')
        for pos in pyautogui.locateAll(imPath("pearl.png"),screenshot):
            print(pos)
            pos = (pos[0]+PEARL_REGION[0],pos[1]+PEARL_REGION[1])
            line.append(pos)
        if line:
            listOfLines.append(line)
        else:
            EMPTYLINES[0]=1
        line = []
        print()
    
    if not EMPTYLINES[1]:
        logging.debug('Searching for pearls in second row...')
        for pos in pyautogui.locateAll(imPath("pearl2.png"),screenshot):
            print(pos)
            pos = (pos[0]+PEARL_REGION[0],pos[1]+PEARL_REGION[1])
            line.append(pos)
        if line:
            listOfLines.append(line)
        else:
            EMPTYLINES[1]=1
        line = []
        print()

    # If LEVEL is bigger than 1, check for pearls in line 3

    if LEVEL>1 and not EMPTYLINES[2]:
        logging.debug('Searching for pearls in third row...')
        for pos in pyautogui.locateAll(imPath("pearl3.png"),screenshot):
                print(pos)
                pos = (pos[0]+PEARL_REGION[0],pos[1]+PEARL_REGION[1])
                line.append(pos)
        if line:
            listOfLines.append(line)
        else:
            EMPTYLINES[2]=1
        line = []
        print()
    
    # If LEVEL is bigger than 7, check for pearls in line 4

    if LEVEL>7 and not EMPTYLINES[3]:
        logging.debug('Searching for pearls in fourth row...')
        for pos in pyautogui.locateAll(imPath("pearl4.png"),screenshot):
            print(pos)
            pos = (pos[0]+PEARL_REGION[0],pos[1]+PEARL_REGION[1])
            line.append(pos)
        if line:
            listOfLines.append(line)
        else:
            EMPTYLINES[3]=1
        line = []
        print()

    # When done with checking pearls, delete line variable
    del line

    # Print lists of pearls
    #x = 0;
    #for a_list in listOfLines:
        #print ("List {}:".format(x))
        #for pos in a_list:
            #print(pos)
        #x+=1

    # Return list of pearl lines
    return listOfLines

def startTurn(pearls):
    # Global variable to change LEVEL's value
    global LEVEL

    # Checking if there are two lines of pearls
    if len(pearls)==2:
        # Checking which line has more pearls in it and applying it to biggerLine while applying the other one to littleLine
        if len(pearls[0])>len(pearls[1]):
            biggerLine = pearls[0]
            littleLine = pearls[1]
        else:
            biggerLine = pearls[1]
            littleLine = pearls[0]
        # Assigning line's lenghts to variables so we don't have to check the lenghts again
        x,y = len(littleLine),len(biggerLine)
        # If littleLine's lenght is one then click all the pearls in biggerLine and win, else click enough pearls in biggerLine till x = y
        if x==1:
            for i in range(0,y,1):
                pyautogui.click(biggerLine[i][0],biggerLine[i][1],1,1)
            LEVEL+=1
        else:
            for i in range(0,y-x,1):
                pyautogui.click(biggerLine[i][0],biggerLine[i][1],1,1)
            pyautogui.click(GO_COORDS[0],GO_COORDS[1],1,1)
    # Else if number of pearl lines is 3
    elif len(pearls)==3:
        x,y,z = len(pearls[0]),len(pearls[1]),len(pearls[2]) # Assigning line's lenghts to variables so we don't have to check the lenghts again
        xorLine = pearls[2] # Assigning the line we are going to pop pearls from to a variable
        if not x^y<z:
            y,z = len(pearls[2]),len(pearls[1])
            xorLine = pearls[1]
            if not x^y<z:
                x,z = len(pearls[1]),len(pearls[0])
                xorLine = pearls[0]
        if x^y<z:
            for i in range(0,z-(x^y),1):
                pyautogui.click(xorLine[i][0],xorLine[i][1],1,1)
        pyautogui.click(GO_COORDS[0],GO_COORDS[1],1,1)
        

def startLevel():
    global LEVEL, EMPTYLINES
    localLevel = LEVEL
    continuePlaying = 1
    #while localLevel==LEVEL:
    while continuePlaying:
        if localLevel!=LEVEL:
            if pyautogui.alert("Passed to level %s, do you wish to continue playing?" %LEVEL,"JuanBot") == "OK":
                continuePlaying = 1
                localLevel += 1
                EMPTYLINES = [0,0,0,0,0,0,0,0] # Reset EMPTYLINES
            else:
                continuePlaying = 0
        else:
            startTurn(pearlSearch())
            # Wait for Juan to make his turn
            time.sleep(5)

def startPlaying():
    # Starting to play the game, popping a messagebox to ask if the bot should start playing
    if pyautogui.alert("Start bot?","JuanBot") == "OK":
        logging.debug('Starting to play...')
        startLevel()

main()
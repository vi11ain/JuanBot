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
LEVEL = 1 # current level being played

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
    # screenshot variable to hold the image of the table region in the game
    screenshot = pyautogui.screenshot(region=PEARL_REGION)
    # line is holding the coords of each pearl in a line
    line = []
    # listOfLines is holding each line
    listOfLines= []

    # Searching for each pearl in the table region, adapt the pearl coords to game region and appending it to line list, than appending the line list to listOfLines and reseting line
    # Starting to search for pearls in line 1 and 2

    logging.debug('Searching for pearls in first row...')
    for pos in pyautogui.locateAll(imPath("pearl.png"),screenshot):
        print(pos)
        pos = (pos[0]+PEARL_REGION[0],pos[1]+PEARL_REGION[1])
        line.append(pos)
    listOfLines.append(line)
    line = []
    print()
    
    logging.debug('Searching for pearls in second row...')
    for pos in pyautogui.locateAll(imPath("pearl2.png"),screenshot):
        print(pos)
        pos = (pos[0]+PEARL_REGION[0],pos[1]+PEARL_REGION[1])
        line.append(pos)
    listOfLines.append(line)
    line = []
    print()

    # If LEVEL is bigger than 1, check for pearls in line 3

    if LEVEL>1:
        logging.debug('Searching for pearls in third row...')
        for pos in pyautogui.locateAll(imPath("pearl3.png"),screenshot):
            print(pos)
            pos = (pos[0]+PEARL_REGION[0],pos[1]+PEARL_REGION[1])
            line.append(pos)
        listOfLines.append(line)
        line = []
        print()
    
    # If LEVEL is bigger than 7, check for pearls in line 4

    if LEVEL>7:
        logging.debug('Searching for pearls in fourth row...')
        for pos in pyautogui.locateAll(imPath("pearl4.png"),screenshot):
            print(pos)
            pos = (pos[0]+PEARL_REGION[0],pos[1]+PEARL_REGION[1])
            line.append(pos)
        listOfLines.append(line)
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
    global LEVEL
    if len(pearls)==2:
        if len(pearls[0])>len(pearls[1]):
            biggerLine = pearls[0]
            littleLine = pearls[1]
        else:
            biggerLine = pearls[1]
            littleLine = pearls[0]
        if len(littleLine)==1:
            for i in range(0,len(biggerLine),1):
                pyautogui.click(biggerLine[i][0],biggerLine[i][1],1,1)
            LEVEL+=1
        else:
            for i in range(0,len(biggerLine)-len(littleLine),1):
                pyautogui.click(biggerLine[i][0],biggerLine[i][1],1,1)
            pyautogui.click(GO_COORDS[0],GO_COORDS[1],1,1)
        time.sleep(3)

def startLevel():
    global LEVEL
    localLevel = LEVEL
    while localLevel==LEVEL:
        startTurn(pearlSearch())

def startPlaying():
    # Starting to play the game, popping a messagebox to ask if the bot should start playing
    if pyautogui.alert("Start bot?","JuanBot") == "OK":
        logging.debug('Starting to play...')
        startLevel()


main()
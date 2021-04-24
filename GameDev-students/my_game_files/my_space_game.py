# Intro to GameDev - main game file

#import library
import pgzrun
import pygame
import random

#set the size for the screen
WIDTH = 1000
HEIGHT = 600

#assign a var to the image we use 
BACKGROUND_IMG = "hh"
PLAYER_IMG = "re_copy"
JUNK_IMG = "space_junk"
SATELLITE_IMG = "satellite_adv"
DEBRIS_IMG = "space_debris2"
LASER_IMG = "laser_red"
START_IMG = "background_logo"
INSTRUCTIONS_IMG = "instructions_button"
START_IMG = "start_button"

#score box limit size
SCOREBOX_HEIGHT = 60

#registar player with a movable picture 
def init():
    global player,junks,satellite,debris,lasers
    player = Actor (PLAYER_IMG)
    player.midright = (WIDTH - 15,HEIGHT/2)

#score count in this program
score = 0
level = 0
level_score = 0

#a constant speed the junk fly through
JUNK_SPEED = 5
SATELLITE_SPEED = 10
DEBRIS_SPEED = 7
LASER_SPEED = -5

#set up a arry with 8 junks that can be initial at the same time
junks = []

for i in range (8):
    junk = Actor(JUNK_IMG)
    x_pos = random.randint (-500,-50)
    y_pos = random.randint (SCOREBOX_HEIGHT,HEIGHT - junk.height)
    junk.topright = (x_pos,y_pos)
    junks.append(junk)

satellite = Actor(SATELLITE_IMG)
x_sat = random.randint (-500,-50)
y_sat = random.randint (SCOREBOX_HEIGHT, HEIGHT - satellite.height)
satellite.topright = (x_sat,y_sat)

debris = Actor (DEBRIS_IMG)
x_deb = random.randint(-500,-50)
y_deb = random.randint (SCOREBOX_HEIGHT , HEIGHT - debris.height)
debris.topright = (x_deb,y_deb)

lasers = []

start_button = Actor(START_IMG)
start_button.center = (WIDTH/2,425)
instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2,500)

init() 

#the start function
def update ():
    global level,level_screen,BACKGROUND_IMG,score
    if level == -1:
        BACKGROUND_IMG = BACKGROUND_LEVEL1
    if level >= 1:
        if level_screen == 1:
            updatePlayer()
            updateJunk()
            updateSatellite ()
            updateDebris()
            updateLasers()
    if score < 0:
            if keyboard.RETURN == 1:
                BACKGROUND_IMG = BACKGROUND_TITLE
                score = 0
                junk_collect = 0
                level = 0
                init ()

#add limit and keyboard function
def updatePlayer ():
    if keyboard.up == 1:
        player.y += -5
    elif keyboard.down == 1:
        player.y += 5

    if player.top < 60:
        player.top = 60

    if player.bottom >HEIGHT:
        player.bottom = HEIGHT

    if keyboard.space == 1:
        laser = Actor (LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)

#give the statue of the junk and the score after catch the junk
def updateJunk ():
    global score
    for junk in junks:
        junk.x += JUNK_SPEED
        collision = player.colliderect (junk)
        if junk.left > WIDTH or collision == 1:
            x_pos = -50
            y_pos = random.randint (SCOREBOX_HEIGHT,HEIGHT - junk.height)
            junk.topleft = (x_pos,y_pos)

        if collision == 1:
            score += 1

def updateSatellite ():
    global score
    satellite.x += SATELLITE_SPEED
    collision = player.colliderect (satellite)
    if satellite.left > WIDTH or collision == 1:
        x_sat = random.randint (-500,-50)
        y_sat = random.randint (SCOREBOX_HEIGHT ,HEIGHT - satellite.height)
        satellite.topright = (x_sat,y_sat)

    if collision == 1:
        score += -7

def updateDebris ():
    global score
    debris.x += DEBRIS_SPEED
    collision = player.colliderect (debris)
    if debris.left > WIDTH or collision == 1:
        x_deb = random.randint (-500,-50)
        y_deb = random.randint (SCOREBOX_HEIGHT ,HEIGHT - debris.height)
        debris.topright = (x_deb,y_deb)

    if collision == 1:
        score += -7

def updateLasers ():
    global score
    for laser in lasers:
        laser.x += LASER_SPEED
        if laser.right < 0:
            lasers.remove(laser)
        if satellite.colliderect(laser) == 1:
            lasers.remove(laser)
            x_sat = random.randint (-500,-50)
            y_sat = random.randint (SCOREBOX_HEIGHT ,HEIGHT - satellite.height)
            satellite.topright = (x_sat,y_sat)
            score += -5
        if debris.colliderect(laser) == 1:
            lasers.remove (laser)
            x_deb = random.randint (-500,-50)
            y_deb = random.randint (SCOREBOX_HEIGHT ,HEIGHT - debris.height)
            debris.topright = (x_deb,y_deb)
            score += 5

def on_mouse_down (pos):
    global level, level_screen
    if start_button.collidepoint(pos):
        level = 1
        level_screen = 1
        print ("start button is pressed")


    if instructions_button.collidepoint(pos):
        level =-1
        print ("instructions button is pressed") 
            
        
#the function to define the picture in the program #set up
def draw():
    screen.clear()
    screen.blit (BACKGROUND_IMG,(0,0))
    if level == 0:
        start_button.draw()
        instructions_button.draw()
    if level == -1:
        start_button.draw()
        show_instructions = "use up and down arrow key to move your player\n press sapcebar to shoot"
        screen.draw.text(show_instructions,midtop= (WIDTH/2,70),color = "white")
    if level >= 1:
            player.draw()
    for junk in junks:
        junk.draw()
    satellite.draw()
    debris.draw()
    for laser in lasers:
        laser.draw()

    show_score = "score: " + str(score)
    screen.draw.text(show_score,topleft=(750,15), color="white")
    


player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list

#pop out a window
pgzrun.go()

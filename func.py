import pygame as p
import random as r
import os
import classes

#? Implement:
#?      + Level graphic based on spawnLimit
#?      + Determing threshold of spawnLimit and Score when game switches modes
#?      + Boss level?

#!  Recommended 800 or 1000 WIDTH. NOT RECOMMENDED to touch HEIGHT 
#!  Game was developed on 800x600 so that will provide optimal experience

#################################################
#               Global Variables                #
#################################################
WIDTH, HEIGHT = 800, 600 #The resolution/size of the game window 
centerWidth = (WIDTH - 25) // 2
enemySpawns = [centerWidth, centerWidth-90, centerWidth+90, centerWidth-180, centerWidth+180, centerWidth-270, centerWidth+270]
spawnLimit, scoreLastHeal = 12, 0
mirror = False #Variable that determines whether movement will be mirrored or not
fullHeart = p.transform.scale(p.image.load('Full Heart.png'), (50,50)) #Image of the full heart
halfHeart = p.transform.scale(p.image.load('Half Heart.png'), (50,50)) #Image of the half heart
gearLarge = p.transform.scale(p.image.load('Settings Icon.png'), (105,105)) #Image of larger gear for settings menu
gearSmall = p.transform.scale(p.image.load('Settings Icon.png'), (65,65)) #Image of smaller gear for settings menu

if 800 <= WIDTH: #Add more values to the list of enemy spawns as the width of the playable screen increases
    enemySpawns.append(centerWidth-360)
    enemySpawns.append(centerWidth+360)
if 1000 <= WIDTH:
    enemySpawns.append(centerWidth-450)
    enemySpawns.append(centerWidth+450)


#####################################################
#               Transition Functions                #
#####################################################
def centerUser(screen, userSprite, user, enemies, projectiles, color, clock, fpsFont):
    global mirror #Function used to make the initial animation into the boss level
    mirror = False #Unmirror the controls
    speed = 0
    if user.rect.centerx <= WIDTH//2: #Depending on which side of the screen the user is on, make them go to center
        speed = -1
    else:
        speed = 1
     
    while True: #Loop until there are no more enemy sprites on the screen
        if not enemies.sprites() and user.rect.centerx == WIDTH//2: #Break out when no more enemies AND user is centered
            break
        if (WIDTH//2)+1 <= user.rect.x <= (WIDTH//2)+1: #If the user is centered, set speed to 0
            user.rect.centerx = WIDTH // 2
            speed = 0
        user.rect.x -= speed #Move the user
        screen.fill(color)
        for projectile in projectiles: #Update every projectile until it is off screen or hits something
            projectile.update(enemies)
        for enemy in enemies: #Update every enemy until it is off screen or gets killed by a projectile
            enemy.update(), enemy.update(), enemy.update(), enemy.update() #make the enemy fall 4x faster
        drawFPS(screen, color, clock.get_fps(), fpsFont)
        if projectiles.sprites(): #If there are projectiles left, draw them
            projectiles.draw(screen)
        if enemies.sprites(): #If there are enemies left, draw them
            enemies.draw(screen)
        userSprite.draw(screen)
        p.display.flip()
        clock.tick(120)   
        
    return projectiles, enemies #Give the two empty projectile and enemy lists back to the main game loop.
                                #Ultimately, I could just empty the two lists in the main loop, but this makes it so I don't need to waste lines in the game.py file


#################################################
#               Core Functionality              #
#################################################
def difficulty(enemiesKilled): #Determine difficulty based on enemies killed
    global spawnLimit, mirror
    match enemiesKilled:
        case 15:
            spawnLimit = 13
        case 35:
            spawnLimit = 14
        case 60:
            spawnLimit = 15
        case 90:
            spawnLimit = 16
        case 100:
            spawnLimit = 20
        case 125: #Mirror the controls when there are enough dead enemies
            mirror = True
        case 150:
            mirror = False
        case 160:
            mirror = True

def spawnEnemies(enemies): #Spawn a new enemy if the spawn limit is not yet reached
    if len(enemies) < spawnLimit:
        en = classes.enemy()
        for temp in enemies: #Make sure enemies don't spawn inside/directly on top of each other
            if en.rect.bottom > temp.rect.top-55 and en.rect.left == temp.rect.left and en.rect.right == temp.rect.right:
                return False
        return en

def pause(screen, startFont): #Pause the game and wait for a resume or quit event
    selection = "resume"
    while True:
        drawPause(screen, startFont, selection)
        for event in p.event.get():
            match event.type:
                case p.QUIT:
                    return True
                case p.KEYDOWN:
                    match event.key:
                        case p.K_RETURN:
                            return selection
                        case p.K_UP: #Use a variable to determine which selection to highlight in the above function
                            selection = "resume"
                        case p.K_DOWN:
                            selection = "quit"

def getColor(): #Return an RGB value tuple
    return (r.randint(0,255), r.randint(0,255), r.randint(0,255)) 

def getCompColor(color):
    R,G,B = color #Extract RGB components
    return (255-R, 255-G, 255-B)


#############################################
#               Draw Functions              #
#############################################
def drawLives(screen, lives): #Draw the hearts on the screen
    isWhole = False #Determine if it should be a half or whole heart
    if lives == int(lives):
        isWhole = True
    
    for i in range(int(lives)):
        x,y = (WIDTH-((i+1)*55)-105), 5
        screen.blit(fullHeart, (x,y))
        if not isWhole and i+1 == int(lives):
            screen.blit(halfHeart, (x-55,y))

def drawPause(screen, pauseFont, selection): #Draw the pause menu
    screen.fill((255,255,255)) #White border around the pause menu
    menuWidth = 500 #Define the dimensions and position of the menu rectangle
    menuHeight = 500
    WIDTH = screen.get_width()
    HEIGHT = screen.get_height()
    menuX = (WIDTH - menuWidth) // 2
    menuY = (HEIGHT - menuHeight) // 2
    p.draw.rect(screen, (0, 0, 0, 128), (menuX, menuY, menuWidth, menuHeight)) #Black box that the text sits in
    
    pauseText = pauseFont.render("GAME PAUSED", True, ((255,255,255))) 
    resumeText = pauseFont.render("RESUME", True, ((255,255,255)))
    quitText = pauseFont.render("QUIT", True, ((255,255,255))) 
             
    screen.blit(pauseText, (WIDTH // 2 - pauseText.get_width() // 2, menuY + pauseText.get_height()))
    screen.blit(resumeText, (WIDTH // 2 - resumeText.get_width() // 2, menuY + 4 * pauseText.get_height()))
    screen.blit(quitText, (WIDTH // 2 - quitText.get_width() // 2, menuY + 7 * pauseText.get_height()))
    
    match selection: #Match which box the user is highlighting
        case "resume":
            p.draw.rect(screen, (212, 175, 55), ((WIDTH - 300) // 2, (HEIGHT - 166) // 2, 300, 100), 5)
        case "quit":
            p.draw.rect(screen, (212, 175, 55), ((WIDTH - 300) // 2, HEIGHT - 233, 300, 100), 5)
    
    p.display.flip()
        
def drawFPS(screen, color, fps, font):
    p.draw.rect(screen, color, (WIDTH - 105, 20, 85, 17)) #Draw the FPS on the screen
    fpsText = font.render(f"FPS: {fps:.0f}", True, (255,255,255))
    screen.blit(fpsText, (WIDTH - 105, 20))
    
def drawScore(screen, color, highScore, score, font):
    p.draw.rect(screen, color, (15, 0, 85, 0)) #Draw the color background
    scoreText = font.render(f"High Score: {highScore:.0f}", True, (255, 255, 255)) 
    screen.blit(scoreText, (15, 20))
    
    p.draw.rect(screen, color, (15, 45, 85, 15)) #Draw the color background
    scoreText = font.render(f"Score: {score:.0f}", True, (255, 255, 255))
    screen.blit(scoreText, (15, 40))
    
def drawKilled(screen, color, enemiesKilled, font): #Draw the amount of enemies killed so far
    p.draw.rect(screen, color, (15,0,85,0))
    killedText = font.render(f"Enemies: {enemiesKilled:.0f}", True, (255,255,255))
    screen.blit(killedText, (15, 60))
    
def drawStartText(increaseAlpha, alpha, fadeSpeed, startFont, screen):
    match increaseAlpha: #If the alpha is growing, increment
        case True:
            alpha += fadeSpeed
            if alpha >= 255:
                alpha, increaseAlpha = 255, False
        case False: #If the alpha is shrinking, decrement
            alpha -= fadeSpeed
            if alpha <= 0:
                alpha, increaseAlpha = -57, True  
                                   
    startScreenText = startFont.render("Press Space To Start", True, getColor()) #Splash screen text          
    startText = startScreenText.copy() 
    startText.set_alpha(alpha) #Set the alpha value
    p.draw.rect(screen, (0,0,0), (WIDTH // 2 - startText.get_width() // 2, HEIGHT // 2 - startText.get_height() // 2, startText.get_width(), startText.get_height()),)
    screen.blit(startText, (WIDTH // 2 - startText.get_width() // 2, HEIGHT // 2 - startText.get_height() // 2))
    return increaseAlpha, alpha

def drawStartScreen(screen, startFont, fpsFont, user, clock):
    stayAtStartScreen, increaseAlpha = True, True
    fadeSpeed, alpha = 1.4, -5
    while stayAtStartScreen:
        for event in p.event.get():
            if event.type == p.QUIT: #User hits the "x" to close the window
                user.killUser() #Kill the user, ending the main game loop
                stayAtStartScreen = False
            elif event.type == p.KEYDOWN:
                if event.key == p.K_SPACE: #Break out of the start screen and begin gameplay
                    stayAtStartScreen = False
                    break
                elif event.key == p.K_s: #Enter the settings menu
                    pass
            
        increaseAlpha, alpha = drawStartText(increaseAlpha, alpha, fadeSpeed, startFont, screen)
        screen.blit(gearLarge, (0,0))
        screen.blit(gearSmall, (gearLarge.get_width()//2, gearLarge.get_height()//2))
        screen.blit(fpsFont.render("(S)ettings", True, (255,255,255)), (12, gearLarge.get_height()))
        p.display.flip()
        clock.tick(120)


#################################################
#               Save File Functions             #
#################################################
def loadSave(): #Load in the value from the score.txt file
    if os.path.exists("score.txt"):
        with open("score.txt", "r") as file:
            return int(file.read())
    else:
        return 0
    
def saveScore(highScore): #Save score to score.txt file
    with open("score.txt", "w") as file:
        file.write(str(highScore))
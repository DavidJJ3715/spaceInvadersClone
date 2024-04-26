import pygame as p
import sys
import func

p.init()    

WIDTH, HEIGHT = 1000, 600 #The resolution/size of the game window (Recommended 800-1200 WIDTH. NOT RECOMMENDED to touch HEIGHT)
screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Welcome to Hell")

user, allSprites, projectiles = func.user(WIDTH, HEIGHT), p.sprite.Group(), p.sprite.Group()
running, start, increaseAlpha = True, True, True
startTime, fadeSpeed, alpha = 0, 1.4, -5
allSprites.add(user) #Group of all class entities so there are less function calls

timePaused = 0 #Time in the pause menu. 0 by default
fpsFont = p.font.SysFont(None, 30) #Font for FPS
startFont = p.font.SysFont(None, 52) #Font for start screen
pauseFont = p.font.SysFont(None, 72) #Font for pause menu
clock = p.time.Clock() #Game clock used for FPS
color = (0,0,0) #The color being returned by func.getColor(). Black by default

highScore = func.loadSave()

en = func.enemy(WIDTH)
allSprites.add(en)

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        keys = p.key.get_pressed()
        match user.update(keys, WIDTH):
            case p.K_SPACE:
                if start:
                    p.display.set_caption("") #Get rid of the start screen caption
                    startTime = p.time.get_ticks() #Start the score clock when the user hits the space bar
                    start = False
                color = func.getColor()
                screen.fill(color)
                user.newColor(func.getCompColor(color)) #Make the cube a complementary color to the background
            case p.K_ESCAPE:
                if not start:
                    beforePause = p.time.get_ticks() #Grab when the game was paused
                    if func.pause(screen, pauseFont) == "quit": #If the user hits quit at the pause menu
                        running = False
                    timePaused += (p.time.get_ticks() - beforePause) #Stop the score when paused
                                               
    if start:
        increaseAlpha, alpha = func.drawStartText(increaseAlpha, alpha, fadeSpeed, startFont, WIDTH, HEIGHT, screen)
    else:
        en.update(HEIGHT)
        proj = user.shoot(p.time.get_ticks())
        if proj:
            projectiles.add(proj) 
        projectiles.update()
        screen.fill(color) #Update the background color
        allSprites.draw(screen) #Draw all class objects to the screen
        projectiles.draw(screen)
        func.drawFPS(screen, color, WIDTH, clock.get_fps(), fpsFont) #Draw the FPS to the screen
        func.drawScore(screen, color, highScore, score, fpsFont) #Draw the scores to the screen

    score = int((p.time.get_ticks() - startTime - timePaused) / 100) #Calculate the score based on when the game started, the current time, and the amount of time in the pause menu
    p.display.flip()
    clock.tick(120) #Frame rate cap

if score > highScore: #Save the high score to score.txt file if user beat high score
    func.saveScore(score)
    
p.quit()
sys.exit()

import pygame as p
import sys
import func

p.init() 
screen = p.display.set_mode((func.WIDTH, func.HEIGHT))
p.display.set_caption("Welcome to Hell")

user, userSprite, enemies, projectiles = func.user(), p.sprite.Group(), p.sprite.Group(), p.sprite.Group()
start, increaseAlpha = True, True
startTime, fadeSpeed, alpha, enemiesKilled = 0, 1.4, -5, 120
userSprite.add(user) #Group of all class entities so there are less function calls

timePaused = 0 #Time in the pause menu. 0 by default
fpsFont = p.font.SysFont(None, 30) #Font for FPS
startFont = p.font.SysFont(None, 52) #Font for start screen
pauseFont = p.font.SysFont(None, 72) #Font for pause menu
clock = p.time.Clock() #Game clock used for FPS
color = (0,0,0) #The color being returned by func.getColor(). Black by default

highScore = func.loadSave()

while not user.isDead:
    for event in p.event.get():
        if event.type == p.QUIT:
            user.killUser()
        keys = p.key.get_pressed()
        match user.update(keys):
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
                        user.killUser()
                    timePaused += (p.time.get_ticks() - beforePause) #Stop the score when paused
                                               
    if start:
        increaseAlpha, alpha = func.drawStartText(increaseAlpha, alpha, fadeSpeed, startFont, screen)
    else:
        spawned = func.spawnEnemies(enemies)
        if spawned:
            enemies.add(spawned)
        proj = user.shoot(p.time.get_ticks())
        if proj:
            projectiles.add(proj) #Add another projectile if the time is right
        for projectile in projectiles:
            bonus = projectile.update(enemies)
            if bonus:
                enemiesKilled += 1
        for enemy in enemies:
            lifeLost = enemy.update()
            if lifeLost:
                user.damage()
        func.difficulty(enemiesKilled)
        screen.fill(color) #Update the background color
        userSprite.draw(screen) #Draw the user to the screen
        enemies.draw(screen) #Draw all enemy objects to the screen
        projectiles.draw(screen) #Draw the shot projectiles to the screen
        func.drawFPS(screen, color, clock.get_fps(), fpsFont) #Draw the FPS to the screen
        func.drawScore(screen, color, highScore, score, fpsFont) #Draw the scores to the screen
        func.drawLives(screen, user.health)

    score = int((p.time.get_ticks() - startTime - timePaused) / 100) + enemiesKilled #Calculate the score based on when the game started, the current time, and the amount of time in the pause menu
    user.heal(score)
    p.display.flip()
    clock.tick(120) #Frame rate cap

if score > highScore: #Save the high score to score.txt file if user beat high score
    func.saveScore(score)
    
p.quit()
sys.exit()

import pygame as p
import sys
import func
import classes
import boss
import cProfile

def main():
    p.init() 
    screen = p.display.set_mode((func.WIDTH, func.HEIGHT))
    p.display.set_caption("<Game Name Here>")

    user, userSprite, enemies, projectiles = classes.user(), p.sprite.Group(), p.sprite.Group(), p.sprite.Group()
    startTime, enemiesKilled, bossDone, bossTime, score = 0, 0, 0, 0, 0
    userSprite.add(user) #Group of all class entities so there are less function calls
    spawned = None

    timePaused = 0 #Time in the pause menu. 0 by default
    fpsFont = p.font.SysFont(None, 30) #Font for FPS
    startFont = p.font.SysFont(None, 52) #Font for start screen
    pauseFont = p.font.SysFont(None, 72) #Font for pause menu
    clock = p.time.Clock() #Game clock used for FPS
    color = (0,0,0) #The color being returned by func.getColor(). Black by default

    highScore = func.loadSave() #Load the high score from the score.txt file

    func.drawStartScreen(screen, startFont, fpsFont, user, clock) 
    startTime = p.time.get_ticks() #Start the score clock for the game
    
    while not user.isDead: #Skips over this loop if the user exits the game in the start menu
        for event in p.event.get(): 
            if event.type == p.QUIT: #User hits the "x" to close the window
                user.killUser() #Kill the user, ending the main game loop
            keys = p.key.get_pressed() #Capture the list of all keys being pressed
            match user.update(keys): #Send the list of keypresses to the user to determine what to do
                case p.K_SPACE:
                    color = func.getColor() #Grab a new randomly generated color
                    screen.fill(color) #Make the screen the new color
                    user.newColor(func.getCompColor(color)) #Make the cube a complementary color to the background
                case p.K_ESCAPE:
                    beforePause = p.time.get_ticks() #Grab when the game was paused
                    if func.pause(screen, pauseFont) == "quit": #If the user hits quit at the pause menu
                        user.killUser()
                    timePaused += (p.time.get_ticks() - beforePause) #Stop the score when paused
                                                
        spawned = func.spawnEnemies(enemies) #Spawn an enemy or return "None" object
        if spawned: #If an enemy was spawned
            enemies.add(spawned) #Add the enemy to the list of enemies
        proj = user.shoot(p.time.get_ticks()) #Shoot if enough time has passed
        if proj: #If a projectile was shot
            projectiles.add(proj) #Add another projectile if the time is right
        for projectile in projectiles: #Go through every projectile and determine if they collided
            bonus = projectile.update(enemies) #Determine if an enemy is dead
            if bonus:
                enemiesKilled += 1 #Give extra points upon killing an enemy
        for enemy in enemies: #Iterate through all the enemies and update their location
            lifeLost = enemy.update()
            if lifeLost: #If the enemy hit the bottom, deal damage
                user.damage()
        func.difficulty(enemiesKilled)
        screen.fill(color) #Update the background color
        userSprite.draw(screen) #Draw the user to the screen
        enemies.draw(screen) #Draw all enemy objects to the screen
        projectiles.draw(screen) #Draw the shot projectiles to the screen
        func.drawFPS(screen, color, clock.get_fps(), fpsFont) #Draw the FPS to the screen
        func.drawScore(screen, color, highScore, score, fpsFont) #Draw the scores to the screen
        func.drawLives(screen, user.health) #Draw the hearts on the screen
        func.drawKilled(screen, color, enemiesKilled, fpsFont)
        if enemiesKilled == 240: #Start the boss sequence when the required level of kills is achieved
            preBossTime = p.time.get_ticks() #Get the time so we don't mess up the score when we return from the boss fight
            projectiles, enemies = func.centerUser(screen, userSprite, user, enemies, projectiles, color, clock, fpsFont)
            user.leftRightOnly = False #Change how the user can move around the screen
            if not boss.spawn(screen, user, userSprite, pauseFont, clock, fpsFont, color): #Go to the boss sequence
                user.killUser() #User died or quit the game
            user.leftRightOnly = True #User won. Set the movement back to left and right only
            bossDone = 1 #Count how many boss fights have been completed
            bossTime += p.time.get_ticks() - preBossTime #Determine how long was spent in the boss sequence

        score = int((p.time.get_ticks() - startTime - timePaused - bossTime) / 100) + enemiesKilled + bossDone #Calculate the score based on when the game started, the current time, and the amount of time in the pause menu
        user.heal(score) #Determine if the user has earned another half a heart
        p.display.flip()
    
        clock.tick(120) #Frame rate cap

    if score > highScore: #Save the high score to score.txt file if user beat high score
        func.saveScore(score)
        
    #! func.endScreen(screen, score, highScore, enemiesKilled, pauseFont)
        
    p.quit()
    sys.exit()
    
if __name__ == "__main__":
    #cProfile.run("main()")
    main()

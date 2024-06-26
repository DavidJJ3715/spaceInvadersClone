import pygame as p
import random as r
import os

#? Implement:
#?      + Level graphic based on spawnLimit
#?      + Determing threshold of spawnLimit and Score when game switches modes
#?      + Boss level?

#!  Recommended 800 or 1000 WIDTH. NOT RECOMMENDED to touch HEIGHT 
#!  Game was developed on 800x600 so that will provide optimal experience

#Global variables that get used in both files
WIDTH, HEIGHT = 800, 600 #The resolution/size of the game window 
centerWidth = (WIDTH - 25) // 2
enemySpawns = [centerWidth, centerWidth-90, centerWidth+90, centerWidth-180, centerWidth+180, centerWidth-270, centerWidth+270]
spawnLimit, scoreLastHeal = 12, 0
mirror = False #Variable that determines whether movement will be mirrored or not
fullHeart = p.transform.scale(p.image.load('Full Heart.png'), (50,50)) #Image of the full heart
halfHeart = p.transform.scale(p.image.load('Half Heart.png'), (50,50)) #Image of the half heart

if 800 <= WIDTH: #Add more values to the list of enemy spawns as the width of the playable screen increases
    enemySpawns.append(centerWidth-360)
    enemySpawns.append(centerWidth+360)
if 1000 <= WIDTH:
    enemySpawns.append(centerWidth-450)
    enemySpawns.append(centerWidth+450)

class user(p.sprite.Sprite): #User sprite class
    def __init__(self):
        super().__init__()
        self.image = p.Surface((50, 50))  #Create a surface for the character
        self.image.fill((255,255,255))  #Fill the surface with white color
        self.rect = self.image.get_rect()  #Get the rectangular area of the surface
        self.rect.center = ((WIDTH - 25) // 2, HEIGHT - 50)  #Set initial position
        self.speed = 15
        self.color = ((255,255,255))
        self.lastShot = 0
        self.health = 3 #How many hearts the user spawns with
        self.isDead = False #If the user is dead
        self.leftRightOnly = True #Which direction the user is able to move in

    def newColor(self, compColor): #Change the color of the user to a complementary color
        self.image.fill(compColor)
        self.color = compColor

    def update(self, keys): #Take in the events and move the user appropriately
        if self.leftRightOnly: #The user can only move left and right
            if ((keys[p.K_a] and not mirror) or (keys[p.K_d] and mirror)) and self.rect.x >= 25:
                self.rect.x -= self.speed
            elif ((keys[p.K_d] and not mirror) or (keys[p.K_a] and mirror)) and self.rect.x <= WIDTH-75:
                self.rect.x += self.speed
        else: #The user can move all across the screen
            if keys[p.K_w] and self.rect.top >= 25:
                self.rect.y -= self.speed
            elif keys[p.K_s] and self.rect.bottom <= HEIGHT-25:
                self.rect.y += self.speed
            elif keys[p.K_a] and self.rect.left >= 25:
                self.rect.x -= self.speed
            elif keys[p.K_d] and self.rect.right <= WIDTH-25:
                self.rect.x += self.speed
        if keys[p.K_SPACE]: #Let the program know to change the color of the screen and user
            return p.K_SPACE
        if keys[p.K_ESCAPE]: #Go to the pause menu
            return p.K_ESCAPE
        
    def shoot(self, currentTime): #Shoot a projectile when the time is right
        self.lastShot = currentTime
        proj = projectile(self.color, self.rect.centerx, self.rect.centery)
        return proj
    
    def damage(self): #Tell if there has been enough damage to end the game
        if self.health-1 <= 0.5:
            self.killUser()
        self.health -= 1
        
    def killUser(self): #User is out of health. End the game
        self.health <= 0
        self.isDead = True
    
    def heal(self, score): #Got enough score to gain half a heart
        global scoreLastHeal #Variable to make sure the health bar doesn't change several times when the score is a multiple of 500
        if score >= scoreLastHeal + 500:
            scoreLastHeal = scoreLastHeal + 500
            self.health += 0.5 #Gain half a heart
 
class projectile(p.sprite.Sprite): #Projectiles that get shot out of the user
    def __init__(self, userColor, userX, userY):
        super().__init__()
        self.image = p.Surface((6,6))
        self.image.fill(userColor)
        self.rect = self.image.get_rect()
        self.rect.center = (userX, userY)
        self.speed = 10 #How fast the projectile travels across the screen
    
    def update(self, enemies):
        hit, killed = self.collision(enemies) #Collision returns if the projectile hits a target and whether the target is dead or not
        if self.rect.bottom < 0 or hit: #Kill the projectile if the target is hit
            self.kill() #Destroy the projectile
            return killed #Return whether or not an enemy was just hit, or was killed
        else:
            self.rect.y -= self.speed #Nothing was hit. Keep the projectile moving
            return False
    
    def collision(self, enemies): 
        for enemy in enemies: #Go through every enemy on screen to see if there is a collision
            if self.rect.top <= enemy.rect.bottom: #If the top of the projectile is above the bottom of the enemy
                if self.rect.left >= enemy.rect.right-36 and self.rect.right <= enemy.rect.left+36: #Check if the projectile is close enough to the enemy left and right
                    if enemy.damage(): #Check if the enemy was hit
                        return True, True #Return hit and kill
                    else:
                        return True, False #Return hit and no kill
        return False, False
    
class enemy(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = p.Surface((30,30))
        self.image.fill(getColor())
        self.rect = self.image.get_rect()
        self.rect.center = (enemySpawns[r.randint(0,len(enemySpawns)-1)], 20)
        self.speed = 1
        self.accel, self.accel2 = True, True
        self.health = 100
        
    def update(self):
        if self.accel and self.accel2: #Box is not on bottom yet, update it if it is time
            self.rect.y += self.speed
            self.accel, self.accel2 = False, False
        else: #This boolean flag is because setting the speed to below one just rounds to either one or zero. This allows the programmer to use fractions of speed
            if not self.accel:
                self.accel = True
            elif self.accel:
                self.accel2 = True
        if self.rect.bottom > HEIGHT-45: #Is the box on the bottom? Take a life
            self.kill()
            return True 
        else: #Box is not at bottom, don't take a life
            return False    

    def damage(self):
        if self.health <= 0: #Check if the enemy is dead
            self.kill() #Is dead, so destroy the enemy
            return True #Tell the projectile that it killed an enemy
        else: 
            self.health -= 5 #Not dead, make it take damage
            return False #Tell the projectile that it has not killed the enemy yet

def centerUser(screen, userSprite, user, enemies, projectiles, color, clock, fpsFont):
    global mirror #Function used to make the initial animation into the boss level
    mirror = False #Unmirror the controls
    speed = 0
    if user.rect.centerx <= WIDTH//2: #Depending on which side of the screen the user is on, make them go to center
        speed = -1
    else:
        speed = 1
     
    while True: #Loop until there are no more enemy sprites on the screen
        if not enemies.sprites(): #Break out when no more enemies
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
        en = enemy()
        for temp in enemies: #Make sure enemies don't spawn inside/directly on top of each other
            if en.rect.bottom > temp.rect.top-55 and en.rect.left == temp.rect.left and en.rect.right == temp.rect.right:
                return False
        return en

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

def loadSave(): #Load in the value from the score.txt file
    if os.path.exists("score.txt"):
        with open("score.txt", "r") as file:
            return int(file.read())
    else:
        return 0
    
def saveScore(highScore): #Save score to score.txt file
    with open("score.txt", "w") as file:
        file.write(str(highScore))
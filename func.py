import pygame as p
import random as r
import os

WIDTH, HEIGHT = 1000, 600 #The resolution/size of the game window (Recommended 800-1200 WIDTH. NOT RECOMMENDED to touch HEIGHT)
centerWidth = (WIDTH - 25) // 2
enemySpawns = [centerWidth, centerWidth-90, centerWidth+90, centerWidth-180, centerWidth+180]

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

    def newColor(self, compColor): #Change the color of the user to a complementary color
        self.image.fill(compColor)
        self.color = compColor

    def update(self, keys): #Take in the events and move the user appropriately
        if keys[p.K_a] and self.rect.x >= 25:
            self.rect.x -= self.speed
        elif keys[p.K_d] and self.rect.x <= WIDTH-75:
            self.rect.x += self.speed
        elif keys[p.K_SPACE]:
            return p.K_SPACE
        elif keys[p.K_ESCAPE]:
            return p.K_ESCAPE
        
    def shoot(self, currentTime):
        self.lastShot = currentTime
        proj = projectile(self.color, self.rect.centerx, self.rect.centery)
        return proj
 
class projectile(p.sprite.Sprite):
    def __init__(self, userColor, userX, userY):
        super().__init__()
        self.image = p.Surface((6,6))
        self.image.fill(userColor)
        self.rect = self.image.get_rect()
        self.rect.center = (userX, userY)
        self.speed = 10
    
    def update(self, enemies):
        if self.rect.bottom < 0 or self.collision(enemies):
            self.kill()
        self.rect.y -= self.speed
    
    def collision(self, enemies):
        for enemy in enemies:
            if self.rect.top <= enemy.rect.bottom:
                if self.rect.left >= enemy.rect.right-36 and self.rect.right <= enemy.rect.left+36:
                    enemy.damage()
                    return True
            pass
        pass
    
class enemy(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = p.Surface((30,30))
        self.image.fill(getColor())
        self.rect = self.image.get_rect()
        self.rect.center = (enemySpawns[r.randint(0,len(enemySpawns)-1)], 20)
        self.speed = 1
        self.accel = True
        self.health = 100
        
    def update(self):
        if self.accel: #Box is not on bottom yet, update it if it is time
            self.rect.y += self.speed
            self.accel = False
        else: #This boolean flag is because setting the speed to below one just rounds to either one or zero. This allows the programmer to use fractions of speed
            self.accel = True
        if self.rect.bottom > HEIGHT-45: #Is the box on the bottom? Take a life
            self.kill()
            return True     

            
    def damage(self):
        if self.health <= 0:
            self.kill()
        else: 
            self.health -= 3

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
                        case _:
                            return False

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
    p.draw.rect(screen, color, (15, 0, 85, 0)) #Draw the high score on the screen
    scoreText = font.render(f"High Score: {highScore:.0f}", True, (255, 255, 255)) 
    screen.blit(scoreText, (15, 20))
    
    p.draw.rect(screen, color, (15, 45, 85, 15)) #Draw the score on the screen
    scoreText = font.render(f"Score: {score:.0f}", True, (255, 255, 255))
    screen.blit(scoreText, (15, 40))
    
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
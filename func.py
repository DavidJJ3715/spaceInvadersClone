import pygame as p
import random as r

class user(p.sprite.Sprite):
    def __init__(self, WIDTH, HEIGHT):
        super().__init__()
        self.image = p.Surface((50, 50))  #Create a surface for the character
        self.image.fill((255,255,255))  #Fill the surface with white color
        self.rect = self.image.get_rect()  #Get the rectangular area of the surface
        self.rect.center = ((WIDTH - 25) // 2, HEIGHT - 50)  #Set initial position
        self.speed = 10

    def newColor(self, compColor):
        self.image.fill(compColor)

    def update(self, keys, WIDTH):
        if keys[p.K_a] and self.rect.x >= 25:
            self.rect.x -= self.speed
        elif keys[p.K_d] and self.rect.x <= WIDTH-75:
            self.rect.x += self.speed
        elif keys[p.K_SPACE]:
            return p.K_SPACE
        elif keys[p.K_ESCAPE]:
            return p.K_ESCAPE

def drawPause(screen, pauseFont, selection):
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
    
    match selection:
        case "resume":
            p.draw.rect(screen, (212, 175, 55), ((WIDTH - 300) // 2, (HEIGHT - 166) // 2, 300, 100), 5)
        case "quit":
            p.draw.rect(screen, (212, 175, 55), ((WIDTH - 300) // 2, HEIGHT - 233, 300, 100), 5)
    
    p.display.flip()

def pause(screen, startFont):
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
                        case p.K_UP:
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
        
def drawFPS(screen, color, WIDTH, fps, font):
    p.draw.rect(screen, color, (WIDTH - 105, 20, 85, 17))
    fpsText = font.render(f"FPS: {fps:.0f}", True, (255,255,255))
    screen.blit(fpsText, (WIDTH - 105, 20))
    
def drawScore(screen, color, highScore, score, font):
    p.draw.rect(screen, color, (15, 0, 85, 0))
    scoreText = font.render(f"High Score: {highScore:.0f}", True, (255, 255, 255)) 
    screen.blit(scoreText, (15, 20))
    
    p.draw.rect(screen, color, (15, 45, 85, 15))
    scoreText = font.render(f"Score: {score:.0f}", True, (255, 255, 255))
    screen.blit(scoreText, (15, 40))
    
def drawStartText(increaseAlpha, alpha, fadeSpeed, startFont, WIDTH, HEIGHT, screen):
    match increaseAlpha:
        case True:
            alpha += fadeSpeed
            if alpha >= 255:
                alpha, increaseAlpha = 255, False
        case False:
            alpha -= fadeSpeed
            if alpha <= 0:
                alpha, increaseAlpha = -57, True  
                                   
    startScreenText = startFont.render("Press Space To Start", True, getColor())           
    startText = startScreenText.copy()
    startText.set_alpha(alpha)
    p.draw.rect(screen, (0,0,0), (WIDTH // 2 - startText.get_width() // 2, HEIGHT // 2 - startText.get_height() // 2, startText.get_width(), startText.get_height()),)
    screen.blit(startText, (WIDTH // 2 - startText.get_width() // 2, HEIGHT // 2 - startText.get_height() // 2))
    return increaseAlpha, alpha
import pygame as p
import random as r

class user(p.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = p.Surface((50, 50))  #Create a surface for the character
        self.image.fill((255,255,255))  #Fill the surface with white color
        self.rect = self.image.get_rect()  #Get the rectangular area of the surface
        self.rect.center = (400, 550)  #Set initial position
        self.speed = 10

    def newColor(self, compColor):
        self.image.fill(compColor)

    def update(self, keys):
        if keys[p.K_a] and self.rect.x >= 25:
            self.rect.x -= self.speed
        elif keys[p.K_d] and self.rect.x <= 725:
            self.rect.x += self.speed
        elif keys[p.K_SPACE]:
            return p.K_SPACE
        elif keys[p.K_ESCAPE]:
            return p.K_ESCAPE

def getColor(): #Return an RGB value tuple
    return (r.randint(0,255), r.randint(0,255), r.randint(0,255)) 

def getCompColor(color):
    R,G,B = color #Extract RGB components
    return (255-R, 255-G, 255-B)
        
def drawFPS(screen, color, WIDTH, fps, font):
    p.draw.rect(screen, color, (WIDTH-105, 20, 85, 17))
    fps_text = font.render(f"FPS: {fps:.0f}", True, (255,255,255))
    screen.blit(fps_text, (WIDTH-105,20))
    
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
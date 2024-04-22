import pygame as p
import sys
import func

p.init()    

WIDTH,HEIGHT = 800,600
screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Welcome to Hell")

user, allSprites = func.user(), p.sprite.Group()
running, start, increaseAlpha = True, True, True
fadeSpeed, alpha = 1.4, -5
allSprites.add(user)

fpsFont = p.font.SysFont(None, 30)
startFont = p.font.SysFont(None, 52)
clock = p.time.Clock()
color = (0,0,0)

while running:
    for event in p.event.get():
        match event.type:
            case p.QUIT:
                running = False
            case p.KEYDOWN:
                match event.key:
                    case p.K_ESCAPE:
                        running = False
                    case p.K_SPACE:
                        start = False
                        color = func.getColor()
                        screen.fill(color)
                        user.newColor(func.getCompColor(color))
                        
    if start:
        increaseAlpha, alpha = func.drawStartText(increaseAlpha, alpha, fadeSpeed, startFont, WIDTH, HEIGHT, screen)
    else:
        allSprites.draw(screen)

    func.drawFPS(screen, color, WIDTH, clock.get_fps(), fpsFont)
    p.display.flip()
    clock.tick(144)

p.quit()
sys.exit()

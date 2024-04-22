import pygame as p
import sys
import func

p.init()    

WIDTH,HEIGHT = 1000,600
screen = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption("Welcome to Hell")

user, allSprites = func.user(WIDTH, HEIGHT), p.sprite.Group()
running, start, increaseAlpha = True, True, True
fadeSpeed, alpha = 1.4, -5
allSprites.add(user)

fpsFont = p.font.SysFont(None, 30)
startFont = p.font.SysFont(None, 52)
pauseFont = p.font.SysFont(None, 72)
clock = p.time.Clock()
color = (0,0,0)

while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        keys = p.key.get_pressed()
        match user.update(keys, WIDTH):
            case p.K_SPACE:
                start = False
                color = func.getColor()
                screen.fill(color)
                user.newColor(func.getCompColor(color))
            case p.K_ESCAPE:
                if not start:
                    if func.pause(screen, pauseFont) == "quit":
                        running = False
                                    
    if start:
        increaseAlpha, alpha = func.drawStartText(increaseAlpha, alpha, fadeSpeed, startFont, WIDTH, HEIGHT, screen)
    else:
        screen.fill(color)
        allSprites.draw(screen)

    func.drawFPS(screen, color, WIDTH, clock.get_fps(), fpsFont)
    p.display.flip()
    clock.tick(144)

p.quit()
sys.exit()

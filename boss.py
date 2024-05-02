import pygame as p
import func

def spawn(screen, user, userSprite, pauseFont, clock, fpsFont, color):
    while not user.isDead:
        for event in p.event.get():
            if event.type == p.QUIT:
                return False
            keys = p.key.get_pressed()
            match user.update(keys):
                case p.K_SPACE:
                    color = func.getColor()
                    screen.fill(color)
                    user.newColor(func.getCompColor(color))
                case p.K_ESCAPE:
                    if func.pause(screen, pauseFont) == "quit":
                        return False
        userSprite.draw(screen)
        func.drawFPS(screen, color, clock.get_fps(), fpsFont)
        p.display.flip()
        clock.tick(120)
    return True
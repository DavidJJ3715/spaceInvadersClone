import pygame as p
import func

def spawn(screen, user, userSprite, pauseFont, clock):
    while not user.isDead:
        for event in p.event.get():
            if event.type == p.QUIT:
                return False
            keys = p.key.get_pressed()
            match user.update(keys):
                case p.K_ESCAPE:
                    if func.pause(screen, pauseFont) == "quit":
                        return False
    return True
import func
import pygame as p
import random as r

class user(p.sprite.Sprite): #User sprite class
    def __init__(self):
        super().__init__()
        self.image = p.Surface((50, 50))  #Create a surface for the character
        self.image.fill((255,255,255))  #Fill the surface with white color
        self.rect = self.image.get_rect()  #Get the rectangular area of the surface
        self.rect.center = ((func.WIDTH - 25) // 2, func.HEIGHT - 50)  #Set initial position
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
            if ((keys[p.K_a] and not func.mirror) or (keys[p.K_d] and func.mirror)) and self.rect.x >= 25:
                self.rect.x -= self.speed
            elif ((keys[p.K_d] and not func.mirror) or (keys[p.K_a] and func.mirror)) and self.rect.x <= func.WIDTH-75:
                self.rect.x += self.speed
        else: #The user can move all across the screen
            if keys[p.K_w] and self.rect.top >= 25:
                self.rect.y -= self.speed
            elif keys[p.K_s] and self.rect.bottom <= func.HEIGHT-25:
                self.rect.y += self.speed
            elif keys[p.K_a] and self.rect.left >= 25:
                self.rect.x -= self.speed
            elif keys[p.K_d] and self.rect.right <= func.WIDTH-25:
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
        if score >= func.scoreLastHeal + 500:
            func.scoreLastHeal = func.scoreLastHeal + 500
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
        self.image.fill(func.getColor())
        self.rect = self.image.get_rect()
        self.rect.center = (func.enemySpawns[r.randint(0,len(func.enemySpawns)-1)], 20)
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
        if self.rect.bottom > func.HEIGHT-45: #Is the box on the bottom? Take a life
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
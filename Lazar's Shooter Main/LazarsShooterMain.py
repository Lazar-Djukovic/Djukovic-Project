import pygame
import math
import random

pygame.init()

#Defining global constants - colours, screen, clock, and images
GROUNDGREEN = (43,132,88)
WHITE = (255,255,255)
BLACK = (0,0,0)
BULLETYELLOW = (250,253,15)
RED = (200,0,0)
LIGHT_RED = (255,0,0)
GREEN = (0,175,0)
LIGHT_GREEN = (0,255,0)
YELLOW = (200,200,0)
LIGHT_YELLOW = (255,255,0)

#Screen resolution
display_width = 1280
display_height = 720
display = pygame.display.set_mode((display_width,display_height))

#Text fonts
smallfont = pygame.font.SysFont("Verdana",25)
medfont = pygame.font.SysFont("Verdana",40)
largefont = pygame.font.SysFont("Verdana",65)

#Window caption and clock
pygame.display.set_caption('/> Shooter')
clock = pygame.time.Clock()
offspeed = 4

#Loading and transforming all images, as well as setting colorkeys
player_walk_img = [pygame.image.load('PlayerSprites/Player1.png'),pygame.image.load('PlayerSprites/Player2.png')]
player_idle_img = pygame.image.load('PlayerSprites/PlayerIdle.png')

weapon_img = pygame.image.load('Weapons/Rifle.png').convert()
player_weapon_img = pygame.transform.scale(weapon_img,(64,64))
player_weapon_img.set_colorkey((BLACK))

RedEnemy = [pygame.image.load('Enemies/RedAlien1.png'),pygame.image.load('Enemies/RedAlien2.png')]

background = (pygame.image.load('IntroBackground.png'))

#The main player class
class Player(pygame.sprite.Sprite):
  def __init__(self, x, y, width, height,health):
    super().__init__()
    self.x = x
    self.y =y
    self.width = width
    self.height = height
    self.counter = 0
    self.moving = False
    self.health = health
  
  def handle_weapons(self,display):
    mouse_x, mouse_y = pygame.mouse.get_pos()

    rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
    angle = (180/math.pi) * -math.atan2(rel_y, rel_x)

    #Checking if the weapon is on the left or right side of the player and rotating accordingly
    if angle < 90 and angle > -90:
      player_weapon_copy = pygame.transform.rotate(player_weapon_img, angle)
    else:
      player_weapon_copy2 = pygame.transform.flip(player_weapon_img, False, True)
      player_weapon_copy = pygame.transform.rotate(player_weapon_copy2, angle)
    #endif

    display.blit(player_weapon_copy, (self.x+30 - int(player_weapon_copy.get_width()/2),self.y+35-int(player_weapon_copy.get_height()/2)))

  def update(self,display):
    if self.counter + 1 >= 24:
      self.counter = 0
    #endif
    self.counter += 1

    #Animating the player by altering between images while he is moving
    if self.moving == True:
      display.blit(pygame.transform.scale(player_walk_img[self.counter//12], (self.width,self.height)), (self.x,self.y))
    else:
      display.blit(pygame.transform.scale(player_idle_img, (self.width,self.height)), (self.x,self.y))
    #endif

    #pygame.draw.rect(display, RED, (self.x, self.y, self.width, self.height))
    self.moving = False

    self.handle_weapons(display)

#Players bullet Class
class PlayerBullet(pygame.sprite.Sprite):
  def __init__(self, x, y, mouse_x, mouse_y,size):
    super().__init__()
    self.size = size
    self.image = pygame.Surface([self.size,self.size])
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

    self.mouse_x = mouse_x
    self.mouse_y = mouse_y
    self.size = size
    self.speed = 15
    
    #calculating the angle at which the bullet will be shot
    self.angle = math.atan2(y-self.mouse_y, x-self.mouse_x)
    self.x_velocity = math.cos(self.angle) * self.speed
    self.y_velocity = math.sin(self.angle) * self.speed

  def update(self,display):
    self.rect.x -= int(self.x_velocity)
    self.rect.y -= int(self.y_velocity)

    pygame.draw.rect(display, BULLETYELLOW, (self.rect.x, self.rect.y,self.size,self.size))

#The enemy sprite class
class Enemy(pygame.sprite.Sprite):
  def __init__(self,x,y,width,height):
    super().__init__()
    self.width = width
    self.height = height
    self.image = pygame.Surface([32,32])

    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y

    self.counter = 0
    self.reset_offset = 0
    self.offset_x = random.randrange(-160,200)
    self.offset_y = random.randrange(-160,190)
  
  def update(self,display):

    #pygame.draw.rect(display, RED, (self.rect.x, self.rect.y,32,32))

    if self.reset_offset == 0:
      self.offset_x = random.randrange(-150,150)
      self.offset_y = random.randrange(-150,150)
      self.reset_offset = random.randrange(120,150)
    else:
      self.reset_offset -= 1
    #endif

    if player.x + self.offset_x > self.rect.x - display_scroll[0]:
      self.rect.x += 1
    elif player.x + self.offset_x < self.rect.x - display_scroll[0]:
      self.rect.x -= 1
    #endif

    if player.y + self.offset_y > self.rect.y - display_scroll[1]:
      self.rect.y += 1
    elif player.y + self.offset_y < self.rect.y - display_scroll[1]:
      self.rect.y -= 1
    #endif

    if self.counter + 1 >= 40:
      self.counter = 0
    self.counter += 1
    #endif

    #Animating the enemy by altering between images while he is moving
    display.blit(pygame.transform.scale(RedEnemy[self.counter//20], (self.width,self.height)), (self.rect.x-display_scroll[0],self.rect.y-display_scroll[1]))
      


#Four functions for easiliy writing any message and button on screen
def text_to_button(msg, color, buttonx,buttony,buttonw,buttonh, size ="small"):
  textSurf, textRect = text_objects(msg,color,size)
  textRect.center = ((buttonx+(buttonw/2), buttony + (buttonh/2)))
  display.blit(textSurf, textRect)

def text_objects(text,color,size):
  if size == "small":
    textSurface = smallfont.render(text,True,color)
  elif size == "medium":
    textSurface = medfont.render(text,True,color)
  elif size == "large":
    textSurface = largefont.render(text,True,color)

  return textSurface, textSurface.get_rect()

def message_to_screen(msg,color, y_displace = 0, size = "small"):
  #screen_text = font.render(msg, True, color)
  #gameDisplay.blit(screen_text, [display_width/3, display_height/2])
  textSurf, textRect = text_objects(msg,color,size)
  textRect.center = (display_width/2), (display_height/2) + y_displace
  display.blit(textSurf, textRect)

def button(text, x,y,w,h, inactive_color, active_color, action = None):
  cur = pygame.mouse.get_pos()
  click = pygame.mouse.get_pressed()

  if x + w > cur[0] > x and y + h > cur[1] > y:
    pygame.draw.rect(display, active_color, (x,y,w,h))

    if click[0] == 1 and action != None:
      if action == "quit":
        pygame.quit()
        quit()

      if action == "controls":
        pass

      if action == "play":
        gameLoop()

      if action == "menu":
        game_intro()

  else:
    pygame.draw.rect(display, inactive_color, (x,y,w,h))

  text_to_button(text,BLACK,x,y,w,h)

def game_intro():

  intro = True

  while intro:

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()
      

    display.blit(background,(0,0))
    message_to_screen("Lazar's Shooter!", BLACK, -136, 'large')
    message_to_screen("Lazar's Shooter!", RED, -140, 'large')
    message_to_screen('The objective is to shoot and destroy the', BLACK, -70)
    message_to_screen('enemies before they destroy you', BLACK, -40)
    #message_to_screen('Press C to play, P to pause or Q to quit', black, 100)

    button('Play', 380,450,120,60, GREEN, LIGHT_GREEN, action='play')
    button('Controls', 580,450,120,60, YELLOW, LIGHT_YELLOW,action = 'controls')
    button('Quit', 780,450,120,60, RED, LIGHT_RED, action = 'quit')


    pygame.display.update()
    clock.tick(15)

#The x and y for displacing screen and sprites
display_scroll = [0,0]

# Create a list of enemies
enemy_group = pygame.sprite.Group()

# Create a list of all sprites 
all_sprites_group = pygame.sprite.Group() 

# List of bullets
bullet_group = pygame.sprite.Group()

#Creating the instance of the player
player = Player(640,360,64,64,100)
all_sprites_group.add(player)

for i in range(5):
  enemy = [Enemy(random.randint(100,700),random.randint(100,700),64,64)]
  all_sprites_group.add(enemy)
  enemy_group.add(enemy)



#The main game loop
def gameLoop():
  gameExit = False
  gameOver = False

  while not gameExit:
    display.fill(GROUNDGREEN)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
      #endif

      if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
          bullet = (PlayerBullet(player.x+35, player.y+30, mouse_x, mouse_y,5))
          bullet_group.add(bullet)
          all_sprites_group.add(bullet)
        #endif
      #endif


    pygame.draw.rect(display, WHITE, (100-display_scroll[0],100-display_scroll[1],16,16))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
      display_scroll[0] -= offspeed
      for bullet in bullet_group:
        bullet.rect.x +=offspeed
      for enemy in enemy_group:
        enemy.rect.x +=offspeed
      player.moving = True
    #endif

    if keys[pygame.K_d]:
      display_scroll[0] += offspeed
      for bullet in bullet_group:
        bullet.rect.x -=offspeed
      for enemy in enemy_group:
        enemy.rect.x -=offspeed
      player.moving = True
    #endif

    if keys[pygame.K_w]:
      display_scroll[1] -= offspeed
      for bullet in bullet_group:
        bullet.rect.y += offspeed
      for enemy in enemy_group:
        enemy.rect.x +=offspeed
      player.moving = True
    #endif

    if keys[pygame.K_s]:
      display_scroll[1] += offspeed
      for bullet in bullet_group:
        bullet.rect.y -= offspeed
      for enemy in enemy_group:
        enemy.rect.x -=offspeed
      player.moving = True
    #endif

 
    enemy_hit_list = pygame.sprite.groupcollide(enemy_group, bullet_group, True, True)

    #Updates all of the sprites on screen
    all_sprites_group.update(display)

    #Tick the clock and update the display
    clock.tick(60)
    pygame.display.update()
  #endfunction

#Calling the game loop as well as start screen, 
# added __main__ beacuse i want to use libraries with this
if __name__ == '__main__':
  game_intro()
  gameLoop()
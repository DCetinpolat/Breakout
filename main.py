from numpy import disp, full
import pygame
import sys
import os 
from os import walk
import time
from random import choice,randint



class settings():
    window_width = 1280
    window_height = 720
    highscore=0
    path_file = os.path.dirname(os.path.abspath(__file__))
    path_image= os.path.join(path_file,"images")
    path_blocks=os.path.join(path_image,"blocks")
    path_upgrades=os.path.join(path_image,"upgrades")
    path_sound = os.path.join(path_file,"sounds")
   
    map= [
       '444444444444', 
       '333333333333',
       '222222222222',
       '222222222222',
       '111111111111',
       '            ',
       '            ',
       '            ',
       '            ']

    color= {
        '1': 'green',
        '2': 'blue',
        '3': 'yellow',
        '4': 'red',

}

    gadgets= ['speed','heart','size']

    #distanz zwischen obstacle
    dist_size= 2
    block_height= window_height/len(map)-dist_size
    block_width= window_width/len(map[0])-dist_size
    top_distance=window_height//30
    
class graphics:
    def __init__(self):
        for index,info in enumerate(walk(settings.path_blocks)):
            if index == 0:
                self.assets={color:{} for color in info[1]}
            else:
                for image_name in info[2]:
                    color_type = list(self.assets.keys())[index-1]
                    full_path=settings.path_blocks + f'/{color_type}/'+image_name
                    surf=pygame.image.load(full_path).convert_alpha()
                    self.assets[color_type][image_name.split('.')[0]]=surf
        


    def get_surface(self,block_type,size):
        image =pygame.Surface(size)
        image.set_colorkey((0,0,0))
        sides= self.assets[block_type]

        image.blit(sides['topleft'],(0,0))
        image.blit(sides['topright'],(size[0]-sides['topright'].get_width(),0))
        image.blit(sides['bottomleft'],(0,size[1]-sides['bottomleft'].get_height()))
        image.blit(sides['bottomright'],(size[0]-sides['bottomright'].get_width(),size[1]-sides['bottomleft'].get_width()))

        top_width=size[0] - ( sides['topleft'].get_width() + sides['topright'].get_width())
        convert_int=int(top_width)
        convert_int2=int((sides['top'].get_height()))
        scaled_top_surf=pygame.transform.scale(sides['top'],(convert_int,convert_int2))
        image.blit(scaled_top_surf,(sides['topleft'].get_width(),0))


        left_height=size[1] - ( sides['topleft'].get_height() + sides['bottomleft'].get_height())
        convert_int=int(left_height)
        convert_int2=int((sides['left'].get_width()))
        scaled_left_surf=pygame.transform.scale(sides['left'],(convert_int2,convert_int))
        image.blit(scaled_left_surf,(0,sides['topleft'].get_height()))


        right_height=size[1] - ( sides['topright'].get_height() + sides['bottomright'].get_height())
        convert_int=int(right_height)
        convert_int2=int((sides['left'].get_width()))
        scaled_right_surf=pygame.transform.scale(sides['right'],(convert_int2,convert_int))
        image.blit(scaled_right_surf,(size[0] - sides['right'].get_width(),sides['topright'].get_height()))

        bottom_height=size[0] - ( sides['bottomleft'].get_height() + sides['bottomright'].get_height())
        convert_int=int(bottom_height)
        convert_int2=int((sides['bottom'].get_height()))
        scaled_bottom_surf=pygame.transform.scale(sides['bottom'],(convert_int,convert_int2))
        image.blit(scaled_bottom_surf,(sides['topleft'].get_width(),size[1]-sides['bottom'].get_height()))

        center_height=size[1]- (sides['top'].get_height()+sides['bottom'].get_height())
        convert_height=int(center_height)
        center_width= size[0]-(sides['right'].get_width()+sides['left'].get_width())
        convert_width=int(center_width)
        scaled_center= pygame.transform.scale(sides['center'],(convert_width,convert_height))
        image.blit(scaled_center,sides['topleft'].get_size())
        return image



class background:
    def __init__(self,filename="background.png"):
        super().__init__()
        self.image = pygame.image.load(os.path.join(settings.path_image,filename)).convert()
        self.image = pygame.transform.scale(self.image,(settings.window_width,settings.window_height))
    



class Player(pygame.sprite.Sprite):
    def __init__(self,groups,graphics):
        super().__init__(groups)

        

        self.image = pygame.Surface((settings.window_width//10, settings.window_height//20))
        self.rect = self.image.get_rect(midbottom=(settings.window_width//2, settings.window_height-14))
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2()
        self.pos=pygame.math.Vector2(self.rect.topleft)
        self.speed= 300
        self.hearts= 3
        self.graphics=graphics
        self.player_check= 0
        
        

        self.image=graphics.get_surface('player',(settings.window_width//10 ,settings.window_height//20))


    def screen_constraint(self):
       if self.rect.right > settings.window_width:
            self.rect.right = settings.window_width
            self.pos.x=self.rect.x
       if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x=self.rect.x


    def watch_for_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x=1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x=-1
        else:
            self.direction.x=0

    def gadget(self,gadget_type):
        if gadget_type == 'spped':
            self.speed += 50 
        if gadget_type == 'heart':
            self.hearts +=1
        if gadget_type == 'size':
            size_gadget_width= self.rect.width * 1.1
            self.image=self.graphics.get_surface('player',(size_gadget_width , self.rect.height))
            self.rect= self.image.get_rect(center=self.rect.center)
            self.pos.x = self.rect.x

    def highscore_events(self):
        if settings.highscore == 10 and self.player_check==0:
            new_width=self.rect.width *0.9
            self.image=self.graphics.get_surface('player',(new_width , self.rect.height))
            self.rect= self.image.get_rect(center=self.rect.center)
            self.pos.x = self.rect.x
            self.player_check+=1

        if settings.highscore == 20 and self.player_check==1:
            new_width=self.rect.width *0.9
            self.image=self.graphics.get_surface('player',(new_width , self.rect.height))
            self.rect= self.image.get_rect(center=self.rect.center)
            self.pos.x = self.rect.x
            self.player_check+=1
        
        if settings.highscore == 30 and self.player_check==2:
            new_width=self.rect.width *0.9
            self.image=self.graphics.get_surface('player',(new_width , self.rect.height))
            self.rect= self.image.get_rect(center=self.rect.center)
            self.pos.x = self.rect.x
            self.player_check+=1
        
        if settings.highscore == 40 and self.player_check==3:
            new_width=self.rect.width *0.9
            self.image=self.graphics.get_surface('player',(new_width , self.rect.height))
            self.rect= self.image.get_rect(center=self.rect.center)
            self.pos.x = self.rect.x
            self.player_check+=1

        if settings.highscore == 50 and self.player_check==4:
            new_width=self.rect.width *0.9
            self.image=self.graphics.get_surface('player',(new_width , self.rect.height))
            self.rect= self.image.get_rect(center=self.rect.center)
            self.pos.x = self.rect.x
            self.player_check+=1

            

            
            
    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.watch_for_events()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)  
        self.screen_constraint() 
        if self.hearts <= 0:
            self.game_over=True         

class Ball(pygame.sprite.Sprite):
    def __init__(self,groups,player,blocks,filename="ball.png"):
        super().__init__(groups)

        self.player = player
        self.blocks = blocks

        self.image=pygame.image.load(os.path.join(settings.path_image,filename)).convert_alpha()

        self.rect = self.image.get_rect(midbottom=player.rect.midtop)
        self.old_rect = self.rect.copy()
        self.pos=pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2((choice((1,-1)),-1))
        self.speed= 400      
        self.ball_check=0
        self.active = False

        self.collision_sound=pygame.mixer.Sound('sounds/collision.wav')
        self.collision_sound.set_volume(0.1)

        self.miss_sound=pygame.mixer.Sound('sounds/game_over.wav')
        self.miss_sound.set_volume(0.1)

    def collision(self,direction):
        overlap_sprites=pygame.sprite.spritecollide(self,self.blocks,False)
        if self.rect.colliderect(self.player.rect):
            overlap_sprites.append(self.player)

        if overlap_sprites:

            if direction == 'horizontal':
                for sprite in overlap_sprites: 
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left-1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.collision_sound.play()
                        settings.highscore += 1
                    
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right+1
                        self.pos.x = self.rect.x
                        self.direction.x *= -1
                        self.collision_sound.play()
                        settings.highscore += 1
                    
                    if getattr(sprite,'health',None):
                       sprite.get_damage(1)

            if direction == 'vertical':
                for sprite in overlap_sprites: 
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top-1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                        self.collision_sound.play()
                        
                    
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom+1
                        self.pos.y = self.rect.y
                        self.direction.y *= -1
                        self.collision_sound.play()
                        settings.highscore += 1

                    if getattr(sprite,'health',None):
                       sprite.get_damage(1)


                    

    def windows_collision(self,direction):
        if direction == 'horizontal':
            if self.rect.left < 0 :
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x *= -1

            if self.rect.right > settings.window_width :
                self.rect.right = settings.window_width
                self.pos.x = self.rect.x
                self.direction.x *= -1

        if direction == 'vertical':
            if self.rect.top < 0 :
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y *= -1

            if self.rect.bottom > settings.window_height :
                self.active=False
                self.direction.y = -1
                self.player.hearts -= 1
                self.miss_sound.play()

    def update(self,dt):
        if self.active:

            if self.direction. magnitude() != 0:
               self.direction = self.direction.normalize()

            self.old_rect = self.rect.copy()
 
            self.pos.x += self.direction.x * self.speed *dt
            self.rect.x=round(self.pos.x)
            self.collision('horizontal')
            self.windows_collision('horizontal')

            self.pos.y += self.direction.y * self.speed *dt
            self.rect.y=round(self.pos.y)
            self.collision('vertical')
            self.windows_collision('vertical')

        else:
            self.rect.midbottom = self.player.rect.midtop
            self.pos = pygame.math.Vector2(self.rect.topleft)
    
    def highscore_events_ball(self):
        if settings.highscore == 10 and self.ball_check==0:
            self.speed += 50
            self.ball_check+=1
        if settings.highscore == 20 and self.ball_check==1:
            self.speed += 40
            self.ball_check+=1
        if settings.highscore == 30 and self.ball_check==2:
            self.speed += 30
            self.ball_check+=1
        if settings.highscore == 40 and self.ball_check==3:
            self.speed += 10
            self.ball_check+=1
        if settings.highscore == 50 and self.ball_check==4:
            self.speed += 20
            self.ball_check+=1
        
        

class Block(pygame.sprite.Sprite):
    def __init__(self,block_type,pos,groups,graphics,create_gadget):
        super().__init__(groups)
        self.graphics=graphics
        self.image = self.graphics.get_surface(settings.color[block_type],(settings.block_width,settings.block_height))
        self.rect=self.image.get_rect(topleft = pos)
        self.old_rect=self.rect.copy()
        self.destroyed_sound=pygame.mixer.Sound('sounds/block_destroyed.wav')
        self.destroyed_sound.set_volume(0.1)
        self.create_gadget=create_gadget

        self.health= int(block_type)

    def get_damage(self,amount):
        self.health -= amount

        if self.health > 0:
            self.image= self.graphics.get_surface(settings.color[str(self.health)],(settings.block_width,settings.block_height))
        else:
            if randint(0,10) < 3:
                self.create_gadget(self.rect.center)
            self.destroyed_sound.play()
            self.kill()

        if self.health <= 0:
            self.kill()

class Heart():
    def __init__(self,filename='heart.png'):
        super().__init__()
        self.image = pygame.image.load(os.path.join(settings.path_image,filename)).convert_alpha()


class Gadget(pygame.sprite.Sprite):
    def __init__(self,pos,gadget_type,groups):
        super().__init__(groups)
        self.gadget_type= gadget_type
        self.image =pygame.image.load(os.path.join(f'images/upgrades/{gadget_type}.png')).convert_alpha()
        self.rect= self.image.get_rect(midtop=pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed= 230

    def update(self,delta_time):
        self.pos.y +=self.speed * delta_time
        self.rect.y= round(self.pos.y)

        if self.rect.top > settings.window_width+100:
            self.kill()

class Game():
    def __init__(self):
        super().__init__()
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.window_width,settings.window_height))
        pygame.display.set_caption("Breakout")

        self.background = background()
        self.all_sprites=pygame.sprite.Group()
        self.obstacles=pygame.sprite.Group()
        self.gadget_sprites=pygame.sprite.Group()
        self.graphics=graphics()
        self.player=Player(self.all_sprites,self.graphics)
        self.level_setup()
        self.ball=Ball(self.all_sprites,self.player,self.obstacles)
        self.heart=Heart()
        
        



        self.game_over=False



        

    def draw_heart(self):
          for i in range(self.player.hearts):
            x = 2 + i* (self.heart.image.get_width()+5)
            self.display_surface.blit(self.heart.image,(x,4))

    def draw_highscore(self):
        font=pygame.font.SysFont(pygame.font.get_default_font(),30)
        text=font.render(f"Highscore:{settings.highscore}",1,pygame.Color("white"))
        self.display_surface.blit(text,(1140,0))

        

        
    def level_setup(self):
        for row_index,row in enumerate(settings.map):
            for col_index,col in enumerate(row):
                if col != ' ':
                    y = settings.top_distance + row_index * (settings.block_height+settings.dist_size)+settings.dist_size//2
                    x= col_index * (settings.block_width+settings.dist_size)+settings.dist_size//2
                    Block(col,(x,y),[self.all_sprites,self.obstacles],self.graphics,self.create_gadget)
        
    def getHeighestScore(self):
        with open('highscore.txt','r') as f:
            return f.read()



    def end_game(self):
        font=pygame.font.SysFont(pygame.font.get_default_font(),50)
        if self.game_over:
            text=font.render("Game Over!",1,pygame.Color("white"))
            text2=font.render("Press F to restart the game!",1,pygame.Color("white"))
            text3=font.render(f"Highscore:{settings.highscore}",1,pygame.Color("white"))
            
            pygame.mixer.stop()
         
            self.display_surface.fill("black")
            self.display_surface.blit(text,(settings.window_width/2-75,settings.window_height/2))
            self.display_surface.blit(text2,(settings.window_width/2.5-75,settings.window_height/1.8))
            self.display_surface.blit(text3,(settings.window_width/2-75,settings.window_height/2.3))
        else:
            self.all_sprites.draw(self.display_surface)
        
 
    def win_game(self):
        font=pygame.font.SysFont(pygame.font.get_default_font(),50)
        count_blocks= len(self.obstacles)
        if count_blocks <= 0:
            text=font.render("You Win!",1,pygame.Color("white"))
            text2=font.render("Press F to restart the game!",1,pygame.Color("white"))
            text3=font.render(f"Highscore:{settings.highscore}",1,pygame.Color("white"))
            pygame.mixer.stop()
            self.display_surface.fill("black")
            self.display_surface.blit(text,(settings.window_width/2-75,settings.window_height/2))
            self.display_surface.blit(text2,(settings.window_width/2.5-75,settings.window_height/1.8))
            self.display_surface.blit(text3,(settings.window_width/2-75,settings.window_height/2.3))
            
            

        

     
            
    def create_gadget(self,pos):
        gadget_type = choice(settings.gadgets)
        Gadget(pos,gadget_type,[self.all_sprites,self.gadget_sprites])

    def level_reset(self):
        self.game_over=False
        self.player=Player(self.all_sprites,self.graphics)
        self.ball=Ball(self.all_sprites,self.player,self.obstacles)
        self.all_sprites.empty()
        self.all_sprites.add(self.ball,self.player)
        settings.highscore= 0
        self.player.player_check= 0
        self.ball.ball_check =0
        for row_index,row in enumerate(settings.map):
            for col_index,col in enumerate(row):
                if col != ' ':
                    y = settings.top_distance + row_index * (settings.block_height+settings.dist_size)+settings.dist_size//2
                    x= col_index * (settings.block_width+settings.dist_size)+settings.dist_size//2
                    Block(col,(x,y),[self.all_sprites,self.obstacles],self.graphics,self.create_gadget)

    def gadgets_collision(self):
        overlap_sprites= pygame.sprite.spritecollide(self.player,self.gadget_sprites,True)
        for sprite in overlap_sprites:
            self.player.gadget(sprite.gadget_type)

    def run(self):
        last_time=time.time()
        while True:
            delta_time=time.time()-last_time
            last_time=time.time()

                    

            for event in pygame.event.get():
                keys=pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.player.hearts <= 0:
                    self.game_over=True
                if self.end_game and keys[pygame.K_f]:
                    self.level_reset()
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_SPACE:
                        self.ball.active=True
  
            self.all_sprites.update(delta_time)
            self.gadgets_collision()
            self.ball.highscore_events_ball()
            self.player.highscore_events()
            self.display_surface.blit(self.background.image,(0,0))
            self.all_sprites.draw(self.display_surface)
            self.draw_heart()
            self.draw_highscore()
            self.end_game()
            self.win_game()

        
            

            pygame.display.flip()
            pygame.display.update()
        
        

if __name__ == "__main__":
    game = Game()
    game.run()


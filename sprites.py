from settings import *

#spritesheet
class Spritesheet:
    def __init__(self,filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        #grab part of sprote spritesheet
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        image = pg.transform.scale(image, (width // 2,height // 2))
        return image


#sprite object(s)
class Player(pg.sprite.Sprite):
    #sprite for Player
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet2.get_image(67, 190, 66, 92)
        self.image.set_colorkey(BLACK)
        #self.image = pg.Surface((30,40))
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(50, HEIGHT-100)
        self.vel = vec(0,0)
        self.accl = vec(0,0)
        self.view = True
        self.b4 = False
        self.jump_stat=False
        self.jump_b4 = False

    def jump(self):
        #only in standing on platforms
        self.rect.x +=1
        hits=pg.sprite.spritecollide(self,self.game.platforms,False)
        self.rect.x -=1
        if hits:
            self.vel.y = -PLAYER_JUMP
            self.game.jump_sound_1.play()
            self.jump_stat=True
            self.jump_b4 = True
    def jump_cut(self):
        if self.jump_stat:
            if self.vel.y < -8:
                self.vel.y = -8

    def update_sprite(self):
        #jump or no
        if self.jump_stat:
            self.image = self.game.spritesheet2.get_image(423, 95, 66, 94)
            self.image.set_colorkey(BLACK)
            #self.rect = self.image.get_rect()
            #self.rect.center = (WIDTH / 2, HEIGHT / 2)
            if not self.view:
                self.image = pg.transform.flip(self.image,True,False)
            elif self.view is not self.b4:
                self.image = pg.transform.flip(self.image,True,False)
        else:
            self.image = self.game.spritesheet2.get_image(67, 190, 66, 92)
            self.image.set_colorkey(BLACK)
            #self.rect = self.image.get_rect()
            #self.rect.center = (WIDTH / 2, HEIGHT / 2)
            if not self.view:
                self.image = pg.transform.flip(self.image,True,False)#1st arg is for x 2nd is for y
            elif self.view is not self.b4:
                self.image = pg.transform.flip(self.image,True,False)

    def update(self):
        self.accl = vec(0,PLAYER_GRAV)#gravity = y acceleration
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.accl.x = -PLAYER_ACCL
            self.b4 = self.view
            self.view = False
            self.update_sprite()
        if keys[pg.K_RIGHT]:
            self.accl.x = PLAYER_ACCL
            self.b4 = self.view
            self.view = True
            self.update_sprite()

        #applay friction
        self.accl.x += self.vel.x * PLAYER_FRICTION
        #equation of motion
        self.vel += self.accl
        self.pos += self.vel + 0.5 * self.accl

        #boundary
        if self.pos.x > WIDTH:
            self.pos.x=0
        if self.pos.x < 0:
            self.pos.x=WIDTH

        #the real mover
        self.rect.midbottom = self.pos
        if self.jump_stat is not self.jump_b4:
            self.update_sprite()
            self.jump_b4 = self.jump_stat


        #view rignt or no


class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet1.get_image(0, 384, 380, 94),
                  self.game.spritesheet1.get_image(382, 204, 200, 100)]
        self.image = random.choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100) < BOOSS_SPAWN_PCT:
            Pup(self.game, self)

class Pup(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['boost'])
        self.image = self.game.spritesheet1.get_image(820, 1805, 71, 70)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top -5
    def update(self):
        self.rect.bottom = self.plat.rect.top -5
        if not self.game.platforms.has(self.plat):
            self.kill()

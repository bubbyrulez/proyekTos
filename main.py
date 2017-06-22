#lompat platform game
from sprites import *
from settings import *

class Game:
    def __init__(self):
        #init game
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption(game_title)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()
        self.sl = []



    def load_data(self):
        #load high score
        #self.dir = path.dirname(__file__)

        #load spritesheet image
        self.spritesheet1 = Spritesheet(SPRITESHEET_FILE_1)
        self.spritesheet2 = Spritesheet(SPRITESHEET_FILE_2)
        self.jump_sound_1 = pg.mixer.Sound(JUMP_SOUND_1)
        self.pup_sound_1 = pg.mixer.Sound(PUP_SOUND_1)
    def load_hs(self):
        with open(SCORE_FILE, 'a+') as f:
            try:
                searchlines = f.readlines()
                #print searchlines
                found = False
                for i,line in enumerate(searchlines):
                    if TOKEN[0] in line:
                        data = searchlines[i].split(',')
                        TOKEN.append(str(data[1]))
                        TOKEN.append(str(i+1))
                        found = True
                if not found:
                    TOKEN.append(str(0))
                    TOKEN.append(str(len(searchlines)+1))

                    #found = False

                self.highscore = int(TOKEN[1])

            except:
                self.highscore = 0

    def new(self):
        #restart the game
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.player = Player(self)
        #self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)

        pg.mixer.music.load(BGM_1)
        self.run()

    def run(self):
        pg.mixer.music.play(loops=-1)
        #game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    #loop game
    def update(self):
        #game loop - update
        self.all_sprites.update()
        #chek if player is fallin
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player,self.platforms,False)#false mean not delete arg 2(platforms)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left -10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top+1
                        self.player.vel.y = 0
                        self.player.jump_stat = False
                        #self.player.update_sprite()

        #if player reaches 1/4 of screen
        if self.player.rect.top <= HEIGHT / 4:
            self.player.pos.y += max(abs(self.player.vel.y),3)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y),3)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score +=10
        #if player step on pup
        pup_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pup_hits:
            if pow.type == 'boost':
                self.pup_sound_1.play()
                self.player.vel.y = -BOOST_POWER
                self.player.jump_stat =False
        # die
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        #spawn more platforms
        while len(self.platforms) < 5:
            r_width = random.randrange(50,100)
            r_height = random.randrange(-70,-44)
            if len(self.platforms) != 0:
                while r_height > self.platforms.sprites()[len(self.platforms)-1].rect.y + 50:
                    r_height = random.randrange(-70,-44)
                    r_height = random.randrange(-70,-44)
            Platform(self,random.randrange(0,WIDTH-r_width),
                     r_height)

    def events(self):
        #game loop - event
        for event in pg.event.get():
            #check for x button
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                    self.player.update_sprite()

            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
                    self.player.update_sprite()

    def draw(self):
        #game loop - draw
        #draw or render
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.screen.blit(self.player.image, self.player.rect)
        #draw score
        self.draw_text(str(self.score), 20, WHITE, WIDTH*4/5,15)
        #displaythe rendered
        pg.display.flip()

    #other
    def show_input_scren(self):
        pg.mixer.music.load(BGM_2)
        self.screen.fill(BGCOLOR)
        self.draw_text(game_title, 50, WHITE, WIDTH/2,HEIGHT/4)
        pg.mixer.music.play(loops=-1)
        player_name = str(inputbox.ask(self.screen, 'Name'))
        TOKEN.append(str(player_name))
        self.load_hs()
    def show_start_scren(self):
        #game start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(game_title, 50, WHITE, WIDTH/2,HEIGHT/4)
        self.draw_text("right left arrow and space", 20, WHITE, WIDTH/2, HEIGHT/4+70)
        self.draw_text("heyoo, " + TOKEN[0], 20, WHITE, WIDTH/2, HEIGHT/4+100)
        self.draw_text("High score: " + str(self.highscore), 20, WHITE, WIDTH/2, HEIGHT/4+130)
        self.draw_text("Pres any key to play", 20, WHITE, WIDTH/2, HEIGHT-100)
        pg.display.flip()

        self.wait_for_key()
        self.wait_for_key()
        pg.mixer.fadeout(500)

    def show_go_screen(self):
        #game over screen
        if not self.running:
            return
        pg.mixer.music.load(BGM_3)
        self.screen.fill(BGCOLOR)
        self.draw_text("Game Oper wee", 50, WHITE, WIDTH/2,HEIGHT/5)

        #cek if player got new high score
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("Widi high score " + str(TOKEN[0]) + " : " + str(self.score), 20, WHITE, WIDTH/2, HEIGHT/4+60)
            with open(SCORE_FILE,'r+') as f:
                #f.write(str(self.score))
                self.sl = f.readlines()
                TOKEN[1] = str(self.score)
                data = ','.join(TOKEN) + "\n"
                if len(self.sl) < int(TOKEN[2]):
                    self.sl.append(data)
                else:
                    self.sl[int(TOKEN[2])-1] = data
                #print self.sl[int(TOKEN[2])]
            with open(SCORE_FILE,'w') as f:
                for i in self.sl:
                    f.write(i)
                    #f.write("\n")
        else:
            self.draw_text("Sekor: " + str(self.score), 20, WHITE, WIDTH/2, HEIGHT/4+60)

        self.draw_text("Pres any key to play again broo", 20, WHITE, WIDTH/2, HEIGHT-100)
        pg.display.flip()
        pg.mixer.music.play(loops=-1)
        self.wait_for_key()
        pg.mixer.fadeout(500)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)#ture is for anti aliassing
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface,text_rect)

#main


g = Game()
g.show_input_scren()
g.show_start_scren()
while g.running:
    g.new()
    g.show_go_screen()
    #g.show_start_scren()

pg.quit()

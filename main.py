import pygame
from sys import exit
from random import randint, randrange


# SPRITE CLASSES
class Logo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.index = 0
        self.image = pygame.image.load('gallery/sprites/logo.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.08)
        self.rect = self.image.get_rect(topleft=(45, 40))

    def animate(self):
        self.index += 0.04
        if int(self.index) == 1:
            self.rect = self.image.get_rect(topleft=(45, 42))
        else:
            self.rect = self.image.get_rect(topleft=(45, 40))

        if int(self.index) >= 2:
            self.index = 0

    def update(self):
        self.animate()


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bird_surf = pygame.image.load('gallery/sprites/bird.png').convert_alpha()
        bird_fly_surf = pygame.image.load('gallery/sprites/bird_fly.png').convert_alpha()
        self.bird = [bird_surf, bird_fly_surf]
        self.bird_index = 0

        self.image = self.bird[self.bird_index]
        self.rect = self.image.get_rect(topleft=(80, 210))
        
        self.gravity = -5
    
    def animate(self):
        self.bird_index += 0.1
        if self.bird_index >= len(self.bird):
            self.bird_index = 0
        self.image = self.bird[int(self.bird_index)]
    
    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.top += self.gravity
        if self.rect.top <= 0:
            self.rect.top = 0
    
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.gravity = -5

    def update(self):
        self.animate()
        self.apply_gravity()
        self.player_input()


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, dir):
        super().__init__()
        self.image = pygame.image.load(f'gallery/sprites/pipe_{dir}.png').convert_alpha()
        self.rect = self.image.get_rect(midtop=(x_pos, y_pos))
    
    def move(self):
        self.rect.left -= 2
    
    def destroy(self):
        if self.rect.left <= -50:
            self.kill()
    
    def update(self):
        self.move()
        self.destroy()


class Bottom(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('gallery/sprites/base.png').convert()
        self.rect = self.image.get_rect(topleft=(0, 430))


class Score(pygame.sprite.Sprite):
    def __init__(self, image_no, score_x_pos):
        super().__init__()
        self.image_no = image_no
        self.score_x_pos = score_x_pos
        self.image = pygame.image.load(f'gallery/sprites/{self.image_no}.png').convert_alpha()
        self.rect = self.image.get_rect(center=(score_x_pos, 38))


def collisions():
    global game_active, i
    if pygame.sprite.spritecollide(bird.sprite, pipe, False):
        channel_3.play(hit_sound)
        i = 0
        go_animation()
        channel_4.play(die_sound)
        game_active = False


def go_animation():
    global go_y_cord, score_y_cord, button_y_cord, sc_text_y_cord, new_y_cord
    go_y_cord = 440
    score_y_cord = 540
    sc_text_y_cord = 600
    button_y_cord = 680
    new_y_cord = 571


def score_counter():
    global score_count
    for sprite in pipe:
            if list(pipe).index(sprite) % 2 != 0:
                if sprite.rect.left == 26:
                    score_count += 1
                    score.empty()

                    if score_count >= 10:
                        count_digits = len(str(score_count))
                        score_x_pos = 140 - (12.5 * (count_digits - 1))
                        score_list = [int(a) for a in str(score_count)]
                        for n in score_list:
                            score.add(Score(n, score_x_pos))
                            score_x_pos += 25
                    else:
                        score.add(Score(score_count, 140))
                    channel_5.play(point_sound)


# DISPLAY CONFIG
bird_icon = pygame.image.load('gallery/sprites/bird_icon.png')
pygame.display.set_icon(bird_icon)
screen = pygame.display.set_mode((280, 500))
pygame.display.set_caption('Flappy Bird')

# initializes all modules
pygame.init()

clock = pygame.time.Clock()

# font settings
text_font = pygame.font.Font('font/Pixeltype.ttf', 32)
text_font.bold = True
score_font = pygame.font.Font('font/Pixeltype.ttf', 24)

# inital flags
game_active = False
i = 1
score_count = 0


# DISPLAY
bird_surf = pygame.image.load('gallery/sprites/bird.png').convert_alpha()
background_surf = pygame.image.load('gallery/sprites/background.png').convert()

bottom_surf = pygame.image.load('gallery/sprites/base.png').convert()
bottom_rect = bottom_surf.get_rect(topleft=(0, 430))

logo_surface = pygame.image.load('gallery/sprites/logo.png').convert_alpha()
logo_surface = pygame.transform.rotozoom(logo_surface, 0, 0.08)

text_surf = text_font.render('Press Space To start', True, (222, 95, 27))

ready_surface = pygame.image.load('gallery/sprites/get_ready.png').convert_alpha()
tap_surface = pygame.image.load('gallery/sprites/tap.png').convert_alpha()
arrow_surface = pygame.image.load('gallery/sprites/arrow.png').convert_alpha()

gameover_surf = pygame.image.load('gallery/sprites/gameover.png').convert_alpha()
gameover_surf = pygame.transform.scale(gameover_surf, (250, 70))
scoreboard_surf = pygame.image.load('gallery/sprites/scoreboard.png').convert_alpha()

new_surf = pygame.image.load('gallery/sprites/new.png').convert_alpha()

ok_surf = pygame.image.load('gallery/sprites/ok.png').convert_alpha()
ok_surf = pygame.transform.rotozoom(ok_surf, 0, 1.5)
ok_rect = ok_surf.get_rect(topleft=(30, 300))
ok_dark_surf = pygame.image.load('gallery/sprites/ok_dark.png').convert_alpha()
ok_dark_surf = pygame.transform.rotozoom(ok_dark_surf, 0, 1.5)
ok_dark_rect = ok_surf.get_rect(topleft=(30, 300))

exit_surf = pygame.image.load('gallery/sprites/exit.png').convert_alpha()
exit_surf = pygame.transform.rotozoom(exit_surf, 0, 1.5)
exit_rect = exit_surf.get_rect(topleft=(156, 300))
exit_dark_surf = pygame.image.load('gallery/sprites/exit_dark.png').convert_alpha()
exit_dark_surf = pygame.transform.rotozoom(exit_dark_surf, 0, 1.5)
exit_dark_rect = exit_surf.get_rect(topleft=(156, 300))

go_animation()


# SPRITE OBJECTS
logo = pygame.sprite.GroupSingle()
logo.add(Logo())

bird = pygame.sprite.GroupSingle()
bird.add(Bird())

bottom = pygame.sprite.GroupSingle()
bottom.add(Bottom())

pipe = pygame.sprite.Group()

score = pygame.sprite.Group()
score_x_pos = 140
score.add(Score(score_count, score_x_pos))


# TIMER
pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, 2000)


# SOUND
fly_sound = pygame.mixer.Sound('gallery/audio/wing.wav')
channel_1 = pygame.mixer.Channel(1)
channel_1.set_volume(0.2)

start_sound = pygame.mixer.Sound('gallery/audio/swoosh.wav')
channel_2 = pygame.mixer.Channel(2)
channel_2.set_volume(0.5)

hit_sound = pygame.mixer.Sound('gallery/audio/hit.wav')
channel_3 = pygame.mixer.Channel(3)
channel_3.set_volume(0.5)

die_sound = pygame.mixer.Sound('gallery/audio/die.wav')
channel_4 = pygame.mixer.Channel(4)
channel_4.set_volume(0.5)

point_sound = pygame.mixer.Sound('gallery/audio/point.wav')
channel_5 = pygame.mixer.Channel(4)
channel_5.set_volume(0.7)


while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pipe_timer and game_active:
            x = randrange(400, 480, 2)
            y_1 = randint(-220, -80)
            y_2 = y_1 + 440

            pipe.add(Pipe(x, y_1, 'down'))
            pipe.add(Pipe(x, y_2, 'up'))

        if event.type == pygame.MOUSEBUTTONDOWN:
            if ok_rect.collidepoint(pygame.mouse.get_pos()):
                pipe.empty()
                score.empty()
                score_count = 0
                score_x_pos = 140
                score.add(Score(score_count, score_x_pos))
                bird.add(Bird())
                i = 2
            elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.quit()
                exit()
        
        if event.type == pygame.KEYDOWN and game_active == True:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                channel_1.play(fly_sound)


    screen.blit(background_surf, (0, 0))

    if game_active:
        screen.blit(background_surf, (0, 0))
        score.draw(screen)

        pipe.draw(screen)
        pipe.update()

        score.draw(screen)

        bird.draw(screen)
        bird.update()
        bottom.draw(screen)

        screen.blit(bottom_surf, (0, 430))

        score_counter()

        # reads score from file
        with open('high_score.txt') as file:
                old_score = file.read()
                        

        if bird.sprite.rect.bottom >= 430:
            bird.sprite.rect.bottom = 430
            channel_4.play(die_sound)
            i = 0
            go_animation()
            channel_3.play(hit_sound)
            game_active = False
        
        collisions()

    else:
        if i == 1:
            logo.draw(screen)
            logo.update()
            screen.blit(bird_surf, (120, 210))
            screen.blit(text_surf, (10, 340))
            bottom.draw(screen)

            if keys[pygame.K_SPACE]:
                i = 2

        elif i == 2:
            screen.blit(ready_surface, (52, 80))
            screen.blit(arrow_surface, (126, 220))
            screen.blit(tap_surface, (52, 260))
            score.draw(screen)
            bird.draw(screen)
            bird.sprite.animate()
            bottom.draw(screen)

            if keys[pygame.K_UP]:
                channel_2.play(start_sound)
                game_active = True
                i == 0

        else:
            if go_y_cord != 60 and score_y_cord != 160 and button_y_cord != 300 and sc_text_y_cord != 220 and new_y_cord != 191:
                go_y_cord -= 20
                score_y_cord -= 20
                sc_text_y_cord -= 20
                button_y_cord -= 20
                new_y_cord -= 20

            pipe.draw(screen)
            bird.draw(screen)
            bottom.draw(screen)

            bird.sprite.rect.bottom += 10
            if bird.sprite.rect.bottom >= 430:
                bird.sprite.rect.bottom = 430

            screen.blit(gameover_surf, (20, go_y_cord))
            screen.blit(scoreboard_surf, (40, score_y_cord))
            screen.blit(ok_surf, (30, button_y_cord))
            screen.blit(exit_surf, (156, button_y_cord))
            score_surf = score_font.render(f'{score_count}', True, (10, 10, 10))
            screen.blit(score_surf, (63, sc_text_y_cord))

            if ok_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(ok_dark_surf, (30, 300))
            elif exit_rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(exit_dark_surf, (156, 300))

            # with open('high_score.txt') as file:
            #     old_score = file.read()
            
            if int(old_score) < score_count:
                with open('high_score.txt', mode='w') as file:
                    file.write(f'{score_count}')
                    high_score_surf = score_font.render(f'{score_count}', True, (10, 10, 10))
            else:
                high_score_surf = score_font.render(f'{old_score}', True, (10, 10, 10))
            
            if int(old_score) < score_count:
                screen.blit(new_surf, (145, new_y_cord))
            screen.blit(high_score_surf, (175, sc_text_y_cord))

    
    pygame.display.update()
    clock.tick(60)

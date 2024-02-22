import pygame
from math import atan2, sin, cos
from typing import Optional
from random import randint, choice
# noinspection PyUnresolvedReferences,PyProtectedMember
from pygame._sdl2 import Window

pygame.init()

WIDTH, HEIGHT = 1280, 720
FRAMERATE = 75

screen = pygame.display.set_mode([WIDTH, HEIGHT])
clock = pygame.time.Clock()
pygame.display.set_caption("YOU CANT LEAVE")
font = pygame.font.SysFont("Arial", 30)

message_index = -1
message_surf: Optional[pygame.Surface] = None
text_direction = [1, 1]
text_speed = 4
wobble = 0
do_shake = False

MESSAGES = {
    "Do you know what is overused in games?": 0,
    "The quit button.": 0,
    "Yeah that's correct": 0,
    "You can not leave": 0,
    "Stop trying to leave": 0,
    "You won't succeed": 0,
    "This is annoying me": 0,
    "Stop clicking the quit button": 0,
    "Stop.": 0,
    "Stop now.": 0,
    "It won't help you": 0,
    "Clicking is futile": 0,
    "Your efforts will die in vain": 0,
    "Stop trying!": 0,
    "Stop!": 0,
    "Seriously.": 0,
    "There's nothing else": 0,
    "I swear...": 0,
    "Please stop!": 0,
    "Here's something that will distract you from clicking it": 1,
    "Distracted you, did it?": 0,
    "Surely you won't click it anymore": 0,
    "Please don't leave!": 0,
    "Stop trying.": 0,
    "...": 0,
    "You are very determined": 0,
    "What if..": 0,
    "What if I did this?": 2,
    "Surely you'll be trapped!": 0,
    "You are too good at this...": 3,
    "Fine, you shall pass": 0,
    "The end": 0,
    "Goodbye": 0,
    "Game made by quasar098": 0
}

def next_message():
    global message_surf
    global message_index
    global running
    global do_letter_spam
    global do_shake
    message_index += 1
    try:
        modifier = list(MESSAGES.values())[message_index]
        if modifier == 1:
            do_letter_spam = True
        if modifier == 2:
            do_shake = True
        if modifier == 3:
            do_shake = False
        message_surf = font.render(list(MESSAGES.keys())[message_index], True, (255, 255, 255))
    except IndexError:
        running = False


def text_wobble(direction=1):
    # direction 1 = squish flat, direction 0 = squish wall
    global wobble
    wobble = 20*(direction*2-1)


text_center = [WIDTH / 2, HEIGHT / 2]
letter_surfs = {}

qwertyuiop = "h3hehd38h2iush8u2sdn92u29hndbt7qrf56afsgb1y6t16twgysxnmcj8vu98029w02;cs.dwsw/swd;.wsi2u28u1whsnw6teb2635re5rdf65f36f72fg11h79g871gf25rfw"
for letter in qwertyuiop:
    letter_surfs[letter] = font.render(letter, True, choice([
        (104, 216, 214), (156, 234, 239), (61, 204, 199), (7, 190, 184), (196, 255, 249)
    ]))

letter_spam = []
do_letter_spam = False
letter_index = 0
screen_offset = [None, None]

next_message()
running = True
while running:
    mx, my = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            next_message()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                angle = atan2(text_center[1] - my, text_center[0] - mx)
                text_direction = [-cos(angle), -sin(angle)]
                text_speed = randint(3, 8)
                text_wobble()

    if do_shake:
        pgwindow = Window.from_display_module()
        ticky = pygame.time.get_ticks()/100
        if screen_offset[0] is None:
            screen_offset = [pgwindow.position[0], pgwindow.position[1]]
        screen_offset[0] += cos(ticky)*7
        screen_offset[1] += sin(ticky)*7
        pgwindow.position = screen_offset[0], screen_offset[1]

    # letter spam
    if pygame.time.get_ticks() % int(FRAMERATE/7) == 0 and do_letter_spam:
        randangle = randint(0, 300)
        letter_spam.append([qwertyuiop[letter_index], [WIDTH/2, HEIGHT/2], [sin(randangle), cos(randangle)]])
        letter_index += 1
        if letter_index >= len(qwertyuiop):
            letter_index = 0

    for letter_info in letter_spam:
        screen.blit(letter_surfs[letter_info[0]], letter_info[1])
        letter_info[1][0] += 3*letter_info[2][0]
        letter_info[1][1] += 3*letter_info[2][1]
        lpos = letter_info[1]
        if lpos[0] > WIDTH:
            letter_info[2][0] = -1*abs(letter_info[2][0])
        if lpos[1] > HEIGHT:
            letter_info[2][1] = -1*abs(letter_info[2][1])
        if lpos[0] < 0:
            letter_info[2][0] = 1*abs(letter_info[2][0])
        if lpos[1] < 0:
            letter_info[2][1] = 1*abs(letter_info[2][1])

    if len(letter_spam) > 150:
        letter_spam.pop(0)

    # message text
    surf_rect = message_surf.get_rect(center=text_center)
    if surf_rect.bottom > HEIGHT:
        text_direction[1] = -1 * abs(text_direction[1])
        text_wobble()
    if surf_rect.right > WIDTH:
        text_direction[0] = -1 * abs(text_direction[0])
        text_wobble(0)
    if surf_rect.left < 0:
        text_direction[0] = 1 * abs(text_direction[0])
        text_wobble(0)
    if surf_rect.top < 0:
        text_direction[1] = 1 * abs(text_direction[1])
        text_wobble()
    text_center[0] += text_speed * text_direction[0]
    text_center[1] += text_speed * text_direction[1]

    new_surf = message_surf
    if wobble != 0:
        wobble -= wobble/abs(wobble)/2
        new_surf = pygame.transform.scale(
            new_surf,
            [
                int(new_surf.get_width()+wobble),
                int(new_surf.get_height()-wobble)
            ]
        )
        new_surf = pygame.transform.rotate(new_surf, sin(pygame.time.get_ticks()/60)*wobble/7)
    screen.blit(new_surf, new_surf.get_rect(center=text_center))

    pygame.display.flip()
    clock.tick(FRAMERATE)
pygame.quit()

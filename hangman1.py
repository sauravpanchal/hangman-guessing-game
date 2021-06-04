#Python December 2021, Saurav Panchal
import pygame #helpful for 2-D games. Not inbuilt python module
import math
import random
from random import shuffle

#setup display

#initializing pygame module. Saying that we are ready to go
pygame.init()
#find dimensions of our screen (in pixels). 
WIDTH, HEIGHT = 800, 500 #constant hence capital
#actually telling python to set the dimensions as required 
win = pygame.display.set_mode((WIDTH, HEIGHT)) #as a tuple remember
#naming your game
pygame.display.set_caption("Hangman Game!")

#load images (images turns into pixels that can be surfaced or drawed on the screen)
images = list()
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)
#print(images)

#button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS*2 + GAP) * 13) / 2)
starty = 400
A = 65

for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2)) #integer division
    letters.append([x, y, chr(A + i), True]) #characte representation of A + i

#fonts
MENU_FONT = pygame.font.SysFont('comicsans', 25)
LETTER_FONT = pygame.font.SysFont('comicsans', 40) #font & size stored in LETTER_FONT variable
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

#game variable
hangman_status = 0 #which image you want to draw during the game (i.e 0 = hangman0.png, 2 = hangman2.png)
words = ["ZAYN", "SABRINA", "RAGNAR", "VALHALLA", "SKOL", "PYGAME", "SPOTIFY",]
word = random.choice(words)
#print(word)
#word = "DEVELOPER" #-> D _ _ _ _ _ _...
guessed = []

#colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw():
    win.fill(WHITE) # background colour (R,G,B) value

    #draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN !", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))


    #draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))
    #draw buttons
    for letter in letters:
        x, y, ltr, visible = letter #-> assigns value e.g x,y = [6,10] then, x = 6 & y = 10 (unpacking or splitting of variables)
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3) #(where, colour, position, radius, border in px) here position will be from center not top-left
            #render text
            text = LETTER_FONT.render(ltr, 1, BLACK) #variable, 1 stands for antialiasing, colour you want to render with
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
            #win.blit(text, (x , y))

    #drawa surfaces. It overwrites, so we cannot see that multiple images is being drawn
    win.blit(images[hangman_status], (150, 100))

    #we need to update screen manually. If you omit next line you will not get background colour
    pygame.display.update()

#speed at which game goes on (FPS). Not actually FPS similar though
FPS = 30

#GAME LOOP (this loop checks any kind response we get from user)
#this response may be in form of click, timeout etc.

#clock object makes sure that loop runs at FPS speed
clock = pygame.time.Clock() 
run = True #while loop controller

def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    global FPS, run, hangman_status    
    while run:
        clock.tick(FPS) #necessary that loop runs at speed we set up

        #look for event during game

        #any event (click, keystroke,etc) happened during game will be stored in pygame.event.get()
        for event in pygame.event.get():
            #looping through event & its going to thrown in event variable
            if event.type == pygame.QUIT: #close button of your game (red cross)
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                #print(m_x, m_y)
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)#distance formula
                        if dis < RADIUS:
                            #print(ltr)
                            letter[3] = False #letter[3] is boolean value stored in sub-list            
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        
        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            display_message('You WON !')
            #print("You Won !")
            hangman_status = 0
            won = True
            guessed.clear()
            for letter in letters:
                a, b, c, d = letter
                letter[3] = True
            break

        if hangman_status == 6:
            display_message('You LOST !')
            #print("You Lost !")
            hangman_status = 0
            won = True
            guessed.clear()
            for letter in letters:
                a, b, c, d = letter
                letter[3] = True
            break

def mainmenu(message, r):
    win.fill(WHITE)
    pygame.draw.circle(win, BLACK, (400, 150), r,3)
    text = MENU_FONT.render(message, 1, BLACK)
    win.blit(text, (400 - text.get_width()/2, 150 - text.get_height()/2))
    pygame.display.update()
    #pygame.time.delay(1000)

def line_start():
    mainmenu("PLAY", 29)
    pygame.time.delay(2000)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            #print(m_x, m_y)
            dis = math.sqrt((400 - m_x) ** 2 + (150 - m_y) ** 2)
            #print(dis)
            if dis < 29:
                #print('clicked')
                main()
    #pygame.time.delay(1000)

def line_restart():
    mainmenu("RESTART", 44)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            #print(m_x, m_y)
            dis = math.sqrt((400 - m_x) ** 2 + (150 - m_y) ** 2)
            #print(dis)
            if dis < 44:
                main()
    #pygame.time.delay(3000)


def startgame():
    word = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                line_start()
                pygame.display.update()
                pygame.time.delay(3000)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.display.update()
                    pygame.time.delay(1500)
                    line_restart()
                    pygame.display.update()                    
pygame.init()
startgame()
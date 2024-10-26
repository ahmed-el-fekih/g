import pygame
import sys
import os
import time
from world import World
from store import Store

# initialize pygame
pygame.init()
BLACK = (0,0,0)
WHITE = (255,255,255)

path = os.getcwd()

class Platformer:
    def __init__(self, width, height, tile_size):
        # variables for height and width
        self.width = width
        self.height = height
        self.tile_size = tile_size

        # fonts
        self.small_font = pygame.font.Font(None, 36)
        self.font = pygame.font.Font(None, 74)

        # screen and clock
        self.screen = pygame.display.set_mode((self.width,self.height))
        self.clock = pygame.time.Clock()

        # bg images
        bg_path = r'{}'.format(path + "\pictures\mountains.jpg")
        self.bg_img = pygame.image.load(bg_path)
        self.bg_img = pygame.transform.scale(self.bg_img, (self.width,self.height))

        # variable for in menu state or not
        # 0 means menu, 1 means game, 2 means store
        self.state = 0

        # store skins
        self.store = Store(path, self.screen, self.font, self.width, self.height)
        self.coins = 0
    
    ################## functions for drawing #####################

    def draw_button(self, text, x, y, width, height, color, hover_color, start, skin):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # if mouse within bounds of box
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height))
            # if box was clicked
            if click[0] == 1:
                # starting the game
                if start == 1:
                    self.state = 1
                    
                # going from menu to store
                elif start == 2:
                    self.state = 2
                
                # going back from store to menu
                elif start == 0:
                    self.state = 0
                
                # buying the skin
                else:
                    if skin in self.store.owned_skins:
                        self.set_skin(skin)
                    else:
                        self.buy_skin(skin)
        # mouse not hovering
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))

        # rendering the text on the button
        text_surface = self.small_font.render(text, True, WHITE)
        self.screen.blit(text_surface, (x + (width // 2 - text_surface.get_width() // 2), 
                                y + (height // 2 - text_surface.get_height() // 2)))
        return
    
    def draw_menu(self):
        # title
        title = self.font.render("Game Menu",True,BLACK)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 150))

        # draw buttons
        self.draw_button("Start Game", self.width // 2 - 100, 300, 200, 50, (0, 128, 0), (0, 255, 0), 1, None)
        self.draw_button("Store", self.width // 2 - 100, 400, 200, 50, (128, 0, 0), (255, 0, 0), 2, None)

        # flip to show all the changes
        pygame.display.flip()

    # draws the amount of coins on the top left of the screen
    def show_coins(self):
        money_size = 30
        img_path = r'{}'.format(path + "\pictures\coin.png")
        coin = pygame.image.load(img_path).convert_alpha()
        coin = pygame.transform.scale(coin, (money_size, money_size))
        amount = self.small_font.render(str(self.coins)+" x ", True, BLACK)
        self.screen.blit(amount, (0,3))
        self.screen.blit(coin, (40, 0))
    
    ################## functions for drawing #####################

    # called when user wants to buy skin from store
    def buy_skin(self, skin):
        if skin not in self.store.owned_skins and self.coins >= self.store.skins[skin]["cost"]:
            self.coins -= self.store.skins[skin]["cost"]
            self.store.owned_skins.append(skin)
    
    # called when user wants to set the current skin
    def set_skin(self, skin):
        if skin in self.store.owned_skins:
            self.store.current_skin = skin
    


    # main function that has the whole code of the game, menu, and store
    def main(self):
        running = True
        world = None
        while running:
            # check for quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            # add background to screen
            self.screen.blit(self.bg_img, (0,0))

            # go to menu if state is 0
            if self.state == 0:
                self.show_coins()
                self.draw_menu()
                continue

            # go to store if state is 2
            elif self.state == 2:
                self.show_coins()
                self.store.draw_store(self.draw_button, BLACK, WHITE)
                continue
            
            # create world if not created
            # this takes some time
            if world is None:
                skin = self.store.get_current_skin_img()
                world = World(self.screen, self.width, self.tile_size, self.height, skin, path)


            # we are not in the menu
            # update the world
            keys = pygame.key.get_pressed()
            world.update(keys)

            # show the changes on the screen
            pygame.display.flip()

            # check if game is done
            state = world.game_state()
            if state[0]:
                if state[1] == "win":
                    self.coins += state[2]
                else:
                    self.coins = 0

                pygame.display.flip()
                self.state = 0
                world = None

            # frame rate
            self.clock.tick(70)


# start the game
width = 1000
height = 500
tile_size = 50
game = Platformer(width,height,tile_size)
game.main()

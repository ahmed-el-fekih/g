import pygame
import sys
from world import World

# initialize pygame
pygame.init()
BLACK = (0,0,0)
WHITE = (255,255,255)

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

        # denotes what the player did if they did anything
        self.player_event = False

        # bg images
        self.bg_img = pygame.image.load(r"C:\Users\azgui\OneDrive\Desktop\tutoring\hamad ib\cs\ia\game\pictures\mountains.jpg")
        self.bg_img = pygame.transform.scale(self.bg_img, (self.width,self.height))
        

        # variable for in menu state or not
        self.menu = True

    def draw_button(self, text, x, y, width, height, color, hover_color, start):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # if mouse within bounds of box
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, hover_color, (x, y, width, height))
            # if box was clicked
            if click[0] == 1:
                if start:
                    self.menu = False
                    return

                else:
                    pygame.quit()
                    exit()
            
        # mouse not hovering
        else:
            pygame.draw.rect(self.screen, color, (x, y, width, height))

        # rendering the text on the button
        text_surface = self.small_font.render(text, True, WHITE)
        self.screen.blit(text_surface, (x + (width // 2 - text_surface.get_width() // 2), 
                                y + (height // 2 - text_surface.get_height() // 2)))
        return

    
    def draw_menu(self):
        self.screen.fill(BLACK)

        # title
        title = self.font.render("Game Menu",True,WHITE)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 150))

        # draw buttons
        self.draw_button("Start Game", self.width // 2 - 100, 300, 200, 50, (0, 128, 0), (0, 255, 0), True)
        self.draw_button("Quit", self.width // 2 - 100, 400, 200, 50, (128, 0, 0), (255, 0, 0), False)

        # flip to show all the changes
        pygame.display.flip()
    
    def main(self):
        running = True
        world = World(self.screen, self.width, self.tile_size)
        while running:
            # check for quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            
            keys = pygame.key.get_pressed()

            # check if we are in the menu state or not
            if self.menu:
                self.draw_menu()
                continue

            # we are not in the menu
            self.screen.blit(self.bg_img, (0,0))

            # update the world
            world.update(keys)

            # show the changes on the screen
            pygame.display.flip()

            # frame rate
            self.clock.tick(70)

width = 1000
height = 500
tile_size = 50
game = Platformer(width,height,tile_size)
game.main()
                
                
                    



        


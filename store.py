import pygame
import time

# class that represents the store of the game
class Store:
    def __init__(self, path, screen, font, width, height):
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height

        # all skins and their information
        self.skins = {
            "default": {"cost": 0, "img": r'{}'.format(path+"\pictures\player2.png")},
            "upgrade": {"cost": 4, "img": r'{}'.format(path+"\pictures\player3.png")},
            "upgrade2": {"cost": 6, "img": r'{}'.format(path+"\pictures\player4.png")}
        }

        # we start with the default skin
        self.owned_skins = ["default"]
        self.current_skin = "default"
        
    
    def get_current_skin_img(self):
        return self.skins[self.current_skin]["img"]

    def draw_store(self, draw_button, black, white):
        title = self.font.render("Store", True, black)
        self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))

        y_offset = 150

        # show all skins on the screen
        for skin in self.skins:
            # green color if skin is bought, else grey color
            color = (0, 120, 0) if skin in self.owned_skins else (128, 128, 128)

            if skin == self.current_skin:
                # current equipped skin is in gold
                border_color = (255, 215, 0) 
            else:
                border_color = color

            pygame.draw.rect(self.screen, border_color, (self.width // 2 - 105, y_offset - 5, 210, 60), 2)

            # buy button
            draw_button(
                f"{skin} - {self.skins[skin]['cost']} coins",
                self.width // 2 - 100, y_offset, 200, 50, color, (0, 255, 255),
                3,
                skin
            )
            y_offset += 70

        # Back to Menu Button
        draw_button("Back", self.width // 2 - 50, y_offset , 100, 40, (128, 0, 0), (255, 0, 0), 0, None)
        pygame.display.flip()


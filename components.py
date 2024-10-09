import pygame

class Tile(pygame.sprite.Sprite):
    # pos is position of the tile, size is the size of the tile
    def __init__(self, pos, size) -> None:
        # initialize sprite
        super().__init__()
        img_path  = r"C:\Users\azgui\OneDrive\Desktop\tutoring\hamad ib\cs\ia\game\pictures\tile2.png"

        # load and scale image
        self.image = pygame.image.load(img_path)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
    
    # method to be used when the world is scrolled
    def update(self, x_shift):
        self.rect.x += x_shift


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        img_path = r"C:\Users\azgui\OneDrive\Desktop\tutoring\hamad ib\cs\ia\game\pictures\player.png"
        # convert alpha is for improving game performance
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image,(size,size))
        self.rect = self.image.get_rect(topleft = pos)

        # mask is for perfect collision
        self.mask = pygame.mask.from_surface(self.image)

        # player movement
        self.direction = pygame.math.Vector2(0,0) # this is an x, y list that represents the player movment
        self.speed = 5
        self.jump_move = -10 # how much the character jumps

        # player status
        self.life = 5
        self.game_over = False
        self.win = False
        self.status = "idle"
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    
    def update_helper(self, keys):
        
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE]:
            self.direction.y = self.jump_move
    
    def update(self, keys):
        if self.life > 0 and not self.game_over:
            self.update_helper(keys)
        
        elif self.game_over and self.win:
            self.direction.x = 0
        
        else:
            self.direction.x = 0


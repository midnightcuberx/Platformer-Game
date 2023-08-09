"""
Python game
"""

# Potentially to fix my problem with the screen I could reset the game with a level parameter required for each time the game view is called
#To stop the camera and character shaking I could maybe use level pass as a variable to stop on_update

#If you pass a checkpoint the number of checkpints passsed will equal 0
# Imports the modules needed
from gc import collect
import arcade
import random
import time
import math
#import json

# Main file path
#MAIN_FILE_PATH = "C:/python projects/Python Assessment/"
#MAIN_FILE_PATH = "C:/school/python/Python Assessment/"
#MAIN_FILE_PATH = "S:/Computing/Assessment/2022/Year 13/Subject 13DTP Class 2-1/dh19502/Python Assessment/"
MAIN_FILE_PATH = "F:/Python Assessment/"

# Constants that will be used later in the code for setting up the window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Python Assessment Game"

# These are the scaling constants
TILE_SIZE = 0.5
CHARACTER_SIZE = TILE_SIZE * 0.45
COIN_SIZE = TILE_SIZE
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SIZE
HEART_SIZE = 0.75
BG_SIZE = 1.25
HEART_HEAL_SIZE = TILE_SIZE

# Constant used for determining the player speed
CHARACTER_MOVEMENT_SPEED = 7
GRAVITY_CONSTANT = 1
CHARACTER_JUMP_SPEED = 20

# Knife constants
KNIFE_SIZE = 0.3
KNIFE_SPEED = 15
KNIFE_ROTATION_ANGLE = 30
KNIFE_THROW_RATE = 10
KNIFE_GRAVITY = 1.25
KNIFE_RANGE = 400
#KNIFE_DAMAGE = random.randint(10,30)

# Health constants
ENEMY_HEALTH_WIDTH = 40
MAX_HEALTH = 100
PLAYER_HEALTH_WIDTH = ENEMY_HEALTH_WIDTH

# Other
NUM_OF_LEVELS = 3
POWERUP_RATE = 10
SPEED_BOOST_RATE = 1.5
SPEED_BOOST_FRAMES = 300
SWORD_OFFSET_X = 15
CRATE_MOVE_RATE = 2
BOTTOM_MAP_LIMIT = -100

# Constants used for sprite centering
CHARACTER_CENTRE_X = SPRITE_PIXEL_SIZE * TILE_SIZE * 2
CHARACTER_CENTRE_Y = SPRITE_PIXEL_SIZE * TILE_SIZE * 3.75
#CHECKPOINTS = [[[CHARACTER_CENTRE_X,CHARACTER_CENTRE_Y],[1625, 300],[2500,430],[4320, 560]],"[[x,y],[x,y]],etc etc for checkpoint co-ordinates of levels"]
HEART_CENTRE_X = 80
HEART_CENTRE_Y = 615
BG_CENTRE_X = 500
BG_CENTRE_Y = 325

# Tracks which direction the player is facing
RIGHT_FACING = 0
LEFT_FACING = 1

#Keeps track of which character is which
NINJA_GIRL = 0
NINJA_BOY = 1

# Layer names for tilesets
PLATFORM_LAYER = "Platforms"
COIN_LAYER = "Coins"
FOREGROUND_LAYER = "Foreground"
BACKGROUND_LAYER = "Background"
DEADLY_LAYER = "Deadly Stuff"
MOVING_PLATFORMS_LAYER = "Moving Platforms"
LADDER_LAYER = "Ladders"
PLAYER_LAYER = "Player"
LEVEL_PASS_LAYER = "Level Pass"
ENEMY_LAYER = "Enemies"
KNIFE_LAYER = "Knives"
CHECKPOINT_LAYER = "Checkpoints"
POWERUP_LAYER = "Powerups"
DASH_LAYER = "Dash"
CRATE_LAYER = "Crates"
#COLLECTABLE_OBJECTS_LAYER = "Collectables"
GEM_LAYER="Gems"

def load_textures(filename):
    """
    Load a texture pair with the second being the mirror image of the first
    """
    return arcade.load_texture_pair(filename, hit_box_algorithm= "Detailed")

def damage_dealt():
    """Returns the amount of damage done"""
    return random.randint(1,10)

class BasicView(arcade.View):
    """The Basic View for all View screens I'll use"""

    def __init__(self):
        """Initialises everything"""
        
        # Inherits the parent class of arcade.view and all its variables
        # and functions etc
        super().__init__()

    def on_show(self):

        """This code runs when this view is shown"""
        # This sets the background colour of the view to blue
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # This resets the viewpoint back to the start of the level (the window will be viewed
        # from the starting position of the game)
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

class PauseView(BasicView):
    """The basic View for any view that is shown during gameplay"""

    def __init__(self, game_view, score:int, time:float, fill_colour: arcade.color = arcade.color.WHITE):
        """This is run as soon as this view is switched to and intialises all variables"""
        fill_colour = arcade.color.RED_DEVIL
        # Inherits the parent class of LevelPass and takes on 
        # all of its variables and functions
        super().__init__()
        self.game_view = game_view
        self.score = score
        self.time = time
        self.fill_color = arcade.make_transparent_color(
            fill_colour, transparency=150
        )


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """This starts the game if the user clicked their mouse"""

        # Sets up the main game which runs after the user clicks the mouse 
        # to go onto the next level
        main_game = Game(self.game_view.level,self.game_view.music_playing,self.game_view.character.type)
        main_game.setup()
        self.window.show_view(main_game)

class InstructionView(BasicView):
    """The instructions which the player will see to start off with"""

    def __init__(self):
        """Intialises all variables and runs when this view is shown"""

        # This inherits the parent class of BasicView and
        # takes on all of its variables and functions
        super().__init__()

    def on_draw(self):

        """This draws the view"""
        # This clears the window before drawing
        self.clear()

        # This draws the instructions by placing text across the background
        arcade.draw_text("Instructions Screen", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """This starts the game if the user pressed the screen"""

        # This sets up the main game and shows it on the screen
        main_game = Game(1,False)
        main_game.setup()
        self.window.show_view(main_game)

class LevelPassed(PauseView):
    """Runs when the level is passed"""

    def __init__(self, game_view, score:int, time:float, fill_colour = arcade.color.WHITE):

        # Inherits the parent class of BasicView and takes on 
        # all of its variables and functions
        super().__init__(game_view,score,time)
        
        """with open("scores.json","r") as read_scores:
            self.score_file_read = json.load(read_scores)"""
        # Initializing all the variables needed for the level
        # passing screen
        self.game_view = game_view
        self.score = score
        self.time = time
        #self.new_fastest_time = False
        #self.new_high_score = False
        #self.msg_list = ["You achieved a new"]
        #self.high_score = self.score_file_read[str(self.game_view.level-1)]["score"]
        #self.fastest_time = self.score_file_read[str(self.game_view.level-1)]["time"]
        #self.level = level
        self.fill_color = arcade.make_transparent_color(
            fill_colour, transparency=150
        )

        #if self.fastest_time == "None" or self.fastest_time < self.time:
            #self.new_fastest_time = True
            #self.score_file_read[str(self.game_view.level-1)]["time"] =  self.time
        """else:
            if self.fastest_time < self.time:
                self.new_fastest_time = True"""
        
        #if self.score > self.high_score:
            #self.new_high_score = True
            #self.score_file_read[str(self.game_view.level-1)]["score"] =  self.score

    def on_draw(self):
        """Draws on the window"""

        # Draws the paused game view in the background 
        # from the original game view
        self.game_view.on_draw()

        # Draws a white transparent layer over the frozen game screen
        arcade.draw_lrtb_rectangle_filled(
            left = 0,
            right = SCREEN_WIDTH,
            top = SCREEN_HEIGHT,
            bottom=0,
            color=self.fill_color,
        )
        # Draws the text on the screen telling the user their score
        arcade.draw_text(f"Congrats for passing level {self.game_view.level-1}!",\
            self.window.width / 2, self.window.height / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text(f"You passed the level with a score of {self.score} and a time of {self.time}",\
             self.window.width / 2, self.window.height / 2-75,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        """if self.new_high_score or self.new_fastest_time:
            if self.new_high_score:
                self.msg_list.append(f"high score of {self.score}")

            if self.new_fastest_time and self.new_high_score:
                self.msg_list.append(f"and a new")
            if self.new_fastest_time:
                self.msg_list.append(f"fastest time of {self.time}")

            with open("scores.json","w") as write_file:
                json.dump(self.score_file_read,write_file)
            msg = " ".join(self.msg_list)
            arcade.draw_text(msg, self.window.width / 2, self.window.height / 2-100,
                         arcade.color.BLACK, font_size=10, anchor_x="center")
            #write in json files here and also prinyt draw text"""

class GameOver(PauseView):
    """Runs when the game is over"""

    def __init__(self, game_view, score:int, time:float):
        """Initialises all variables and runs when this View is shown"""
        
        # Creates the colour which will be our background colour when the game is over
        fill_colour = arcade.color.RED_DEVIL

        # Inherits the parent class of LevelPass and takes on 
        # all of its variables and functions
        super().__init__(game_view, score, time,fill_colour)


    def on_draw(self):
        """Draws on the window"""

        # Draws the paused game view in the background 
        # from the original game view
        self.game_view.on_draw()

        # Draws a white transparent layer over the frozen game screen
        arcade.draw_lrtb_rectangle_filled(
            left = 0,
            right = SCREEN_WIDTH,
            top = SCREEN_HEIGHT,
            bottom=0,
            color=self.fill_color,
        )
        # Draws the text on the screen telling the user their score
        arcade.draw_text(f"You died", self.window.width / 2, self.window.height / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text(f"Your final score was {self.score}", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

class Enemy(arcade.Sprite):
    """Sprite class for entities which will be inherited"""

    def __init__(self,folder_name, file_name, scale : int, no_of_frames: int, idle_img, walking_img):
        """This runs when the class is called, and it intialises all variables"""

        # Inherits the parent class of arcade.Sprite
        # and takes on all the variables of it
        super().__init__()

        self.alive = True
        self.health = MAX_HEALTH
        self.should_update_walk = 0
        self.no_of_frames = no_of_frames

        # This sets the intial direction of the character to right
        self.character_direction = RIGHT_FACING

        # This is used in order to flip through the images in texture pairs
        self.current_texture = 0
        self.scale = scale
        # --- Loading textures ---

        file_path = f"{MAIN_FILE_PATH}Assets/{folder_name}/{file_name}"
        # Loading texture pairs for when the character is idle, jumping, or falling
        self.idle_textures = load_textures(f"{file_path}{idle_img}.png")
        self.walking_textures = []

        # Loading the walking textures into a list of textures
        for i in range(no_of_frames):
            texture = load_textures(f"{file_path}{walking_img}{i}.png")
            self.walking_textures.append(texture)

        # This sets the first (intial) texture to facing to the right
        # This is because the chzracter starts on the left side of the map 
        # and therefore should be running right
        self.texture = self.idle_textures[0]

        # Sets the hit box (edge co-ordinates of image) to the
        # hit box points of the textured image
        #self.hit_box = self.texture.hit_box_points


    def update_animation(self, delta_time: float = 1 / 60):

        """Updates animations for the enemy"""
        
        # This changes the direction that the sprite is facing depending
        # on which way it is moving
        if self.change_x < 0 and self.character_direction == RIGHT_FACING:
            self.character_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_direction == LEFT_FACING:
            self.character_direction = RIGHT_FACING

        # This runs if the enemy is not moving
        # and sets the animation to the idle enemy
        if self.change_x == 0:
            self.texture = self.idle_textures[self.character_direction]
            return

        # This animates the sprite when it walks
        if self.should_update_walk == 3:
            self.current_texture += 1
            if self.current_texture > self.no_of_frames - 1:
                self.current_texture = 0
            self.texture = self.walking_textures[self.current_texture][self.character_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1

class Weapon(arcade.Sprite):
    """Weapon sprite for attacking sword hitbox"""
    
    def __init__(self,character):
        """Initialises variables and runs when this class is called"""

        # Inherits the arcade.sprite parent class and inherits
        # all the variables and methods from that class
        super().__init__()
        
        # Initialises the variables
        self.character = character
        self.scale = CHARACTER_SIZE

        # This sets up the textures for the weapon
        self.weapon_textures = []
        for i in range(10):
            texture = load_textures(f"{MAIN_FILE_PATH}/Assets/Ninja/png/Attacking/Attack__00{i}.png")
            self.weapon_textures.append(texture)
        
        # Sets the orginal texture to the first texture
        self.texture = self.weapon_textures[0][self.character.character_direction]

    def check_for_attack_collision(self, enemy_sprites: arcade.Sprite):
        """Checks for collisions with enemy sprites"""

        #Sees if the weapon hits any enemies and deduct health from the enemies if it is
        hit_enemies = arcade.check_for_collision(self, enemy_sprites)
        if hit_enemies and self.character.is_attacking:
            enemy_sprites.health -= random.randint(1,5)

    def update_animation(self, delta_time: float = 1 / 60):
        """Updates the weapon hitbox (because the weapon sprite is an invisiible hitbox)"""

        # If the character is attacking then the texture will change to fit
        # the according texture of the player animation
        if self.character.is_attacking:
            self.texture = self.weapon_textures[self.character.current_texture]\
                [self.character.character_direction]
            self.hit_box = self.texture.hit_box_points
            # This changes the center_x of the weapon based on the direction the player is facing
            # and then sets up the player sprite co-ordinates
            if self.character.character_direction == RIGHT_FACING:
                self.left = self.character.right + SWORD_OFFSET_X
            else:
                self.right = self.character.left - SWORD_OFFSET_X
            
            self.center_y = self.character.center_y

        
class Character(arcade.Sprite):
    """Player sprite class"""

    def __init__(self,moving_platforms, character_type = NINJA_GIRL):
        """Runs when the character class is called and initialises variables"""

        # Inherits the parent class of arcade.Sprite
        # and takes on all the variables of it
        super().__init__()

        # Sets the hit box (edge co-ordinates of image) to the
        # hit box points of the textured image
        #self.hit_box = self.texture.hit_box_points
        # These variables track the characters actions and what they are doing
        self.jumping = False
        self.climbing = False
        self.on_ladder = False
        self.is_throwing = False
        self.is_attacking = False


        # This sets the intial direction of the character to right
        self.character_direction = RIGHT_FACING

        # This is used in order to flip through the images in texture pairs
        self.current_texture = 0
        self.scale = CHARACTER_SIZE

        # Moving platforms
        self.moving_platforms = moving_platforms
        
        # Character health
        self.alive = True
        self.health = MAX_HEALTH
        self.type = character_type

        # Character textures
        self.idle_textures = []
        self.jumping_textures = []
        self.falling_textures = []
        self.walking_textures = []
        self.climbing_textures = []
        self.throwing_textures = []
        self.jump_throw_textures = []
        self.attacking_textures = []

        # This is crating the weapon and setting up the attacking textures
        self.weapon = Weapon(self)
        # --- Loading textures ---
        folder_names = ["Ninja/png","ninjaadventurenew/png"]
        for i in range(2):
            file_path = f"{MAIN_FILE_PATH}Assets/{folder_names[i]}/"
            # Loading texture pairs for when the character is idle, jumping, or falling
            self.idle_textures.append(load_textures(f"{file_path}Idle__000.png"))
            self.jumping_textures.append(load_textures(f"{file_path}Jump__001.png"))
            self.falling_textures.append(load_textures(f"{file_path}Jump__009.png"))

            # Loading the walking textures into a list of textures
            walking_textures = []
            for i in range(10):
                texture = load_textures(f"{file_path}Run__00{i}.png")
                walking_textures.append(texture)

            # This loads the textures for climbing
            climbing_textures = []
            for i in range(10):
                texture = arcade.load_texture(f"{file_path}Climb_00{i}.png", hit_box_algorithm= "Detailed")
                climbing_textures.append(texture)

            # Loads the throwing textures
            throwing_textures = [] 
            for i in range(10):
                texture = load_textures(f"{file_path}Throw__00{i}.png")
                throwing_textures.append(texture)
            
            # Loads jump throw textures
            jump_throw_textures = [] 
            for i in range(10):
                texture = load_textures(f"{file_path}Jump_Throw__00{i}.png")
                jump_throw_textures.append(texture)

            # Loads attacking textures
            attacking_textures = []
            for i in range(10):
                texture = load_textures(f"{file_path}Attack__00{i}.png")
                attacking_textures.append(texture)

            self.walking_textures.append(walking_textures)
            self.climbing_textures.append(climbing_textures)
            self.throwing_textures.append(throwing_textures)
            self.jump_throw_textures.append(jump_throw_textures)
            self.attacking_textures.append(attacking_textures)

            
        

        # This sets the first (intial) texture to facing to the right
        # This is because the chzracter starts on the left side of the map 
        # and therefore should be running right
        self.texture = self.idle_textures[self.type][0]
    
    def on_moving_platform(self,moving_platforms):
        """Checks if the player is on a moving platform or not"""

        # Returns true if the player is on a moving platform
        if len(arcade.check_for_collision_with_list(self,moving_platforms)) > 0:
            return True

    def texture_count(self,lower_limit:int = 0,upper_limit:int = 9):
        "Updates the texture count"

        # Resets the texture to the lowest limit if it exceeds the upper
        # limit or if it is under the lowe limit. Also increments the texture by 1.
        self.current_texture += 1
        if self.current_texture < lower_limit:
            self.current_texture = lower_limit
        
        elif self.current_texture > upper_limit:
            self.current_texture = lower_limit

    #Test moving platforms on l2
    def throwing_animation(self,texture_list, lower_limit:int = 0,upper_limit:int = 9):
        """Updates the texture if the character is throwing a knife"""

        self.texture_count(lower_limit, upper_limit)
        self.texture = texture_list[self.current_texture][self.character_direction]

    def update_animation(self, delta_time: float = 1 / 60):
        """Updates the animation for the character sprite"""

        # If the character is attacking, set the hitbox to the first attacking animation
        # Then update the weapon texture and hitbox
        if self.is_attacking:
            self.texture_count()
            self.texture = self.attacking_textures[self.type][self.current_texture][self.character_direction]
            self.hit_box = self.attacking_textures[self.type][0][self.character_direction].hit_box_points
            self.weapon.update_animation()
            
        else:

            # This figures out if we need to flip face left or right
            # This if statement turns the direction of animation to left if the character's change
            # in direction is less than 0 (ie it is moving to the left) and the character was
            # facing right to start with
            # Meanwhile the elif statement turns the  direction of animation to the right if 
            # the character's change in direction is positive( it moves to the right) and also 
            # only if the character is moving left to start with
            if self.change_x < 0 and self.character_direction == RIGHT_FACING:
                self.character_direction = LEFT_FACING
            elif self.change_x > 0 and self.character_direction == LEFT_FACING:
                self.character_direction = RIGHT_FACING


            # This is the climbing animation
            # It changes the climbing variable depending if the character is on a ladder or not
            # It also animates the sprite when its moving up and down the ladder
            if self.on_ladder:
                self.climbing = True
                print("True")
            if not self.on_ladder and self.climbing:
                self.climbing = False
                print("False")
            if self.climbing and abs(self.change_y) > 1:
                self.current_texture += 1
                if self.current_texture > 9:
                    self.current_texture = 0
            if self.climbing:
                self.texture = self.climbing_textures[self.type][self.current_texture]
                return

            # This changes textures depending on if the character is jumping or falling
            if self.change_y > 0 and not self.on_ladder and not self.on_moving_platform(self.moving_platforms):
                if not self.is_throwing:
                    self.texture = self.jumping_textures[self.type][self.character_direction]
                else:
                    self.throwing_animation(self.jump_throw_textures[self.type], upper_limit=4)
                return

            elif self.change_y < 0 and not self.on_ladder and not self.on_moving_platform(self.moving_platforms):
                if not self.is_throwing:
                    self.texture = self.falling_textures[self.type][self.character_direction]
                else:
                    self.throwing_animation(self.jump_throw_textures[self.type], 5)
                return

            
            # This sets the animation to the idle animation if the character is not moving
            if self.change_x == 0:
                if not self.is_throwing:
                    self.texture = self.idle_textures[self.type][self.character_direction]
                else:
                    self.throwing_animation(self.throwing_textures[self.type])
                return

            # This sets the animation to the walking animation, looping through the 
            # number of different walking textures there are
            if not self.is_throwing:
                self.throwing_animation(self.walking_textures[self.type])
            else:
                self.throwing_animation(self.throwing_textures[self.type])

""""class Enemy(Entity):
    Enemy class

    def __init__(self,folder_name, file_name, scale:int, no_of_frames: int, idle_img, walking_img = None,jumping_img = None, falling_img = None, climbing_img = None):
        Runs when the Enemy class is called and initialises variables

        # Inherits the parent class of Entity
        # and takes on all the variables of it
        super().__init__(folder_name, file_name, scale, no_of_frames, idle_img, walking_img)

        self.should_update_walk = 0
        self.no_of_frames = no_of_frames

    def update_animation(self, delta_time: float = 1 / 60):

        Updates animations for the enemy
        
        # This changes the direction that the sprite is facing depending
        # on which way it is moving
        if self.change_x < 0 and self.character_direction == RIGHT_FACING:
            self.character_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_direction == LEFT_FACING:
            self.character_direction = RIGHT_FACING

        # This runs if the enemy is not moving
        # and sets the animation to the idle enemy
        if self.change_x == 0:
            self.texture = self.idle_textures[self.character_direction]
            return

        # This animates the sprite when it walks
        if self.should_update_walk == 3:
            self.current_texture += 1
            if self.current_texture > self.no_of_frames - 1:
                self.current_texture = 0
            self.texture = self.walking_textures[self.current_texture][self.character_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1"""

class RobotEnemy(Enemy):

    def __init__(self):

        # Inherits the parent class of Enemy
        # and takes on all the variables of it
        super().__init__("resources/images/animated_characters/robot", "robot", 7)


class ZombieEnemy(Enemy):

    def __init__(self):

        # Inherits the parent class of Enemy
        # and takes on all the variables of it
        super().__init__("Golem Enemy", "0_Golem_", 0.2, 12,"Idle_000","Running_00")

class KnivesAttack(arcade.Sprite):
    """Class for throwing knives"""

    def __init__(self, filename: str , scale: float, hit_box_algorithm: str, left_boundary:int, right_boundary:int):
        """Runs when the KnivesAttack class is called and initialises variables"""

        # Inherits the parent class of arcade.Sprite and takes
        # on all its variables and functions
        super().__init__(filename,scale, hit_box_algorithm=hit_box_algorithm)

        self.original_direction = RIGHT_FACING

        self.left_boundary = left_boundary
        self.right_boundary = right_boundary



    def damage(self):
        return random.randint(10,30)

class SpeedDash(arcade.Sprite):
    """Dash animation for speed powerup"""

    def __init__(self, filename: str, character, hit_box_algorithm: str = "Detailed"):
        """Runs when the SpeedDash class is called and initialises variables"""

        # Inherits the parent class of arcade.Sprite and takes
        # on all its variables and functions
        super().__init__(filename, hit_box_algorithm=hit_box_algorithm)
        self.character = character
        self.direction = character.character_direction
        self.dash_texture_pair = load_textures(filename)
        if self.character.character_direction == RIGHT_FACING:
            offset_x = -25 #Use constant for this
        else:
            offset_x = 25
        self.center_x = self.character.center_x + offset_x
        self.center_y = self.character.center_y

    def update_animation(self, delta_time: float = 1 / 60):
        """Updates the animation for speed powerup effects"""
        # This figures out if we need to flip face left or right
        # This if statement turns the direction of animation to left if the character's change
        # in direction is less than 0 (ie it is moving to the left) and the character was
        # facing right to start with
        # Meanwhile the elif statement turns the  direction of animation to the right if 
        # the character's change in direction is positive( it moves to the right) and also 
        # only if the character is moving left to start with
        if self.change_x < 0 and self.direction == RIGHT_FACING:
            self.direction = LEFT_FACING
        elif self.change_x > 0 and self.direction == LEFT_FACING:
            self.direction = RIGHT_FACING
        
        # Sets the texture to facing the right direction
        self.texture = self.dash_texture_pair[self.direction]


        
class HealthBar(arcade.Sprite):
    """Healthbar sprite"""

    def __init__(self, sprite,health_width):
        """Runs when the HealthBar class is called and initialises variables"""

        # Takes on the variables and functions of arcade.sprite,
        # the parent class
        super().__init__()

        # Initialises variables
        self.sprite = sprite
        self.health_width = health_width
  
    def draw_health(self):
        """Draws the health bar"""
        # Draws 2 rectangles above the sprite, one red one green in order to represent health
        arcade.draw_rectangle_filled(self.sprite.center_x, self.sprite.top + 10, self.health_width, 4 ,color= arcade.color.RED)
        health_width = self.health_width * self.sprite.health / MAX_HEALTH
        arcade.draw_rectangle_filled(self.sprite.center_x - 0.5 * self.health_width + 0.5 * health_width, self.sprite.top + 10, health_width, 4 ,color= arcade.color.GREEN)

class CharacterHealth(HealthBar):
    """Character health bar"""

    def __init__(self, character):
        """Runs when the CharacterHealth class is called and initialises variables"""

        # Takes on the variables and functions of HealthBar,
        # the parent class
        super().__init__(character,PLAYER_HEALTH_WIDTH)

class EnemyHealth(HealthBar):
    """Enemy health bar"""

    def __init__(self, enemy):
        """Runs when the EnemyHealth class is called and initialises variables"""

        # Takes on the variables and functions of HealthBar,
        # the parent class
        super().__init__(enemy,ENEMY_HEALTH_WIDTH)

class AnimatedObject(arcade.Sprite):
    """A class that animates objects such as coins and hearts/potions"""

    def __init__(self, file_path:str, scaling:int, num_of_frames:int, frame_rate:int = 1):
        """Runs when the Animated class is called and initialises variables"""

        # Inherits the parent class, that is
        # The hearts class becomes a sprite in arcade
        # and takes on all its variables
        super().__init__()

        # Intializing of variables needed later
        self.scale = scaling
        self.current_texture = 0
        self.frames = num_of_frames
        self.frame_rate = frame_rate
        self.frames_since_reset = 0
        self.texture_list = []

        # Loads textures for the animated object
        for i in range(num_of_frames):
            texture = arcade.load_texture(f"{file_path}{i}.png")
            self.texture_list.append(texture)

        # Sets the initial texture to the first texture
        self.texture = self.texture_list[0]

    def update_animation(self, delta_time: float = 1 / 60):
        """Updates animation for animated objects"""
        
        self.frames_since_reset += 1

        if self.frames_since_reset == self.frame_rate:

            # Changes the image number so the object is animated
            # It basically switched through frames
            self.current_texture += 1
            if self.current_texture == self.frames:
                self.current_texture = 0
            self.texture = self.texture_list[self.current_texture]
            self.frames_since_reset = 0

class HealthPotion(AnimatedObject):
    """Class for the health powerups"""

    def __init__(self):
        """Runs when the HealthPotion class is called and initialises variables"""

        # Inherits the parent class, that is
        # The hearts class becomes an animated object
        # and takes on all its variables
        super().__init__(f"{MAIN_FILE_PATH}Assets/Collectables/heart", HEART_HEAL_SIZE, 6, POWERUP_RATE)
        # Use like enemies crate layer with the placeholders (spawn ppoints)
        # Have a list of the layers that need object placing at placeholders and have a foor loop eg
        # for layer in list
        #     for item in layer

class SpeedPowerup(AnimatedObject):
    """A class for The speed powerups"""

    def __init__(self):
        """Runs when the SpeedPowerup class is called and initialises variables"""

        # Inherits the parent class, that is
        # The hearts class becomes an animated object
        # and takes on all its variables
        super().__init__(f"{MAIN_FILE_PATH}Assets/Collectables/speed", HEART_HEAL_SIZE, 12,POWERUP_RATE) #Make heart heal size powerup size


#class Coins(AnimatedObject):
    #"""A class for The speed powerups"""

    #def __init__(self):
        #"""Runs when the SpeedPowerup class is called and initialises variables"""

        # Inherits the parent class, that is
        # The hearts class becomes an animated object
        # and takes on all its variables
        #super().__init__(f"{MAIN_FILE_PATH}Assets/Collectables/coin", HEART_HEAL_SIZE, 6,POWERUP_RATE)

#class Gem(AnimatedObject):
    #"""A class for The speed powerups"""

    #def __init__(self):
        #"""Runs when the SpeedPowerup class is called and initialises variables"""

        # Inherits the parent class, that is
        # The hearts class becomes an animated object
        # and takes on all its variables
        #super().__init__(f"{MAIN_FILE_PATH}Assets/Collectables/gem", HEART_HEAL_SIZE, 6,POWERUP_RATE)
        
class KnifeIcon(arcade.Sprite):
    # Needs character to have a self.knives thing
    # also character needs self.has_wings 
    
    def __init__(self):
        pass

class Shield(AnimatedObject):
    pass

# if self.up_pressed is True then move the characters center_x even more
# Need several variables within character sprite to see if stuff is equipped and also several counters for attack boost or whatever


class Hearts(AnimatedObject):
    """Hearts Class"""

    def __init__(self):
        """Runs when the Hearts class is called and initialises variables"""
        
        # Inherits the parent class, that is
        # The hearts class becomes a sprite in arcade
        # and takes on all its variables
        super().__init__(f"{MAIN_FILE_PATH}Assets/Kenney Platform Art/Base pack/HUD/hud_heart", HEART_SIZE, 4)

        # Number of lives initially
        self.lives = 3

        # Initial texture
        self.texture = self.texture_list[3]

    
    def update_animation(self, delta_time: float = 1 / 60):
        """Updates the hearts animation"""
        
        # Updates the texture to how many hearts the user has remaining
        self.texture = self.texture_list[self.lives]

#class Crates(arcade.Sprite):
    #"""Crates class"""

    #def __init__(self):

        #super().__init__(f"{MAIN_FILE_PATH}Assets/Kenney Platform Art/Base pack/Tiles/stoneWall.png")
        #self.scale = TILE_SIZE * 2
    
    #def move_crate(self,move_rate):
        #"""This moves the crate"""
        #self.center_x += move_rate
    
class Game(arcade.View):
    """
    Main class that runs the game
    """

    def __init__(self, level:int, music:bool, character_num = 0):

        # This inherits the parent class and sets up the platform
        super().__init__()
        
        # Intializes window width and height
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        # Initializes the map
        self.map = None

        #Intializes layers needed later
        self.enemies_layer = None
        self.powerups_layer = None


        # Intializes the character sprite
        self.character = None
        self.character_health = None
        self.character_num = character_num


        # Intialize the heart sprite list
        self.heart_sprite_list = None
        self.hearts = None

        # Intilaises bg spritelist
        self.bg_sprite_list = None
        self.bg = None


        #Initializes the physics engine
        self.physics_engine = None

        #Checkpoint stuff
        self.last_checkpoint = None
        self.passed_checkpoints = []

        # Sets up camera that will follow the player around
        self.cam = None

        # A Camera that can be used to draw GUI elements
        self.gui_cam = None

        # The background camera which will move the background around
        self.bg_cam = None

        # Sets the end of map to 0 (Will be changed later, this is only intializing)
        self.map_end = 0



        # The level
        self.level = level

        self.collectable_layers = [COIN_LAYER,GEM_LAYER]


        # This code loads the sounds that we need later
        self.coin_collection_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jumping_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        #self.game_bg_track = arcade.load_sound(f"{MAIN_FILE_PATH}Assets/Adorable_Little_Chiptune_Loop.mp3", streaming=True)
        self.game_bg_track = arcade.load_sound(f"{MAIN_FILE_PATH}Assets/Funky_funk.mp3", streaming=True)


        # Sets the original score to 0
        self.player_score = 0

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.is_throwing = False

        #  Track knife stuff
        self.can_throw = True
        self.frames_between_shots = 0
        self.angle = 0
        #used for counting how many knives the user has (can also use a class for that similar to hearts)

        # Timer for speed powerup
        self.speed_boost_equipped = False
        self.num_of_speed_boosts = 0
        self.boost_frames_since_reset = 0
        
        # Initialises the tile map
        self.tiled_map = None

        # Keeps track of whether the music is playing or not
        self.music_playing = music

        # Variables that keep track of time
        self.timer_running = False
        self.start_time = None
        self.total_time = 0.000

        # This sets the background colour
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """
        Setup the game and call this to start the game.
        This is to make it easier to restart the game when the character dies etc
        """

        #Makes it so the time resets every time a new level starts/
        # a level is reset
        #self.timer_running = False
        #self.start_time = None
        #self.total_time = 0.000

        # Plays the music if it is not already playing
        if self.music_playing is False:
            arcade.play_sound(self.game_bg_track, looping=True)
            self.music_playing = True

        # Sets up the Camera
        self.cam = arcade.Camera(self.width, self.height)

        # Setup the GUI Camera
        self.gui_cam = arcade.Camera(self.width, self.height)

        # Sets up the background camera
        self.bg_cam = arcade.Camera(self.width, self.height)

        # This keeps track of the score
        self.player_score = 0

        # Name of map file to load
        map_path = MAIN_FILE_PATH

        map_name = f"{map_path}level{self.level}.tmx"

        # This is a dictionary full of possible layers
        layer_options = {
            PLATFORM_LAYER : {
                "use_spatial_hash": True,
            },
            COIN_LAYER : {
                "use_spatial_hash": True,
            },
            DEADLY_LAYER : {
                "use_spatial_hash": True,
            },
            MOVING_PLATFORMS_LAYER : {
                "use_spatial_hash": False,
            },
            LEVEL_PASS_LAYER : {
                "use_spatial_hash" : True,
            },
            ENEMY_LAYER : {
                "use_spatial_hash" : False,
                #"scaling" : 4,
            },
            CHECKPOINT_LAYER : {
                "use_spatial_hash" : True,
            },
            POWERUP_LAYER : {
                "use_spatial_hash" : True,
            },
            GEM_LAYER : {
                "use_spatial_hash" : True,
            },
        }

        # Load the scene from Tiled
        self.tile_map = arcade.load_tilemap(map_name, TILE_SIZE, layer_options)

        # This creates the scene with the tilemap, and this will add all layers of the tilemap as sprtitelists
        # The 2nd line will add the player sprite as a layer before the foreground
        self.map = arcade.Scene.from_tilemap(self.tile_map)
        self.map.add_sprite_list_before(PLAYER_LAYER,FOREGROUND_LAYER)
        # This adds the bullet layer to the map
        self.map.add_sprite_list_before(KNIFE_LAYER,FOREGROUND_LAYER)
        # This adds a dash layer to the map
        self.map.add_sprite_list_before(DASH_LAYER,PLAYER_LAYER)

        # This creates the spritelists for hearts and background and dash
        self.heart_sprite_list = arcade.SpriteList()
        self.bg_sprite_list = arcade.SpriteList()


        # Adds health bar to game, adding it to the health sprite list
        # and setting its centre to preset co-ordinates
        self.hearts= Hearts()
        self.hearts.center_x = HEART_CENTRE_X
        self.hearts.center_y = HEART_CENTRE_Y
        self.heart_sprite_list.append(self.hearts)


        # This adds the background to the background sprite list
        # and sets its co-ordinates to the predetermined ones
        img_src = f"{MAIN_FILE_PATH}Assets/Backgrounds/Background.png"
        self.bg = arcade.Sprite(img_src, BG_SIZE)
        self.bg.center_x = BG_CENTRE_X
        self.bg.center_y = BG_CENTRE_Y
        self.bg_sprite_list.append(self.bg)

        # This sets up the player sprite and the co-ordinates where it will initially start from
        self.character = Character(self.map[MOVING_PLATFORMS_LAYER])
        self.character.center_x = CHARACTER_CENTRE_X
        self.character.center_y = CHARACTER_CENTRE_Y
        self.character.type = self.character_num
        self.map.add_sprite(PLAYER_LAYER, self.character)
        self.character_health = CharacterHealth(self.character)

        # This sets the enemy layer to a list of the placeholders in the enemy layer
        # and the powerup layer to a list of the placeholders in its respective layers
        self.enemies_layer = self.tile_map.object_lists[ENEMY_LAYER]
        self.powerups_layer = self.tile_map.object_lists[POWERUP_LAYER]
        #self.crates_layer = self.tile_map.object_lists[CRATE_LAYER]
        #self.layers_to_setup = [POWERUP_LAYER,COLLECTABLE_OBJECTS_LAYER]

        # This sets up the checkpoint list
        self.last_checkpoint = self.map[CHECKPOINT_LAYER][0]
        self.passed_checkpoints = []

        # This creates a sprite with properties of change_x and the boundaries
        # required for it to move. It then adds each enemy to the enemy layer in the map
        for my_enemy in self.enemies_layer:
            enemy_coordinates = self.tile_map.get_cartesian(
                my_enemy.shape[0], my_enemy.shape[1]
            )
            print(enemy_coordinates)
            enemy_type = my_enemy.properties["type"]
            if enemy_type == "robot":
                enemy = RobotEnemy()
            elif enemy_type == "zombie":
                enemy = ZombieEnemy()
            enemy.center_x = math.floor(
                enemy_coordinates[0] * TILE_SIZE * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (enemy_coordinates[1] + 1) * (self.tile_map.tile_height * TILE_SIZE)
            )
            if "boundary_left" in my_enemy.properties:
                enemy.boundary_left = my_enemy.properties["boundary_left"]
            if "boundary_right" in my_enemy.properties:
                enemy.boundary_right = my_enemy.properties["boundary_right"]
            if "boundary_top" in my_enemy.properties:
                enemy.boundary_top = my_enemy.properties["boundary_top"]
            if "boundary_bottom" in my_enemy.properties:
                enemy.boundary_bottom = my_enemy.properties["boundary_bottom"]
            if "change_x" in my_enemy.properties:
                enemy.change_x = my_enemy.properties["change_x"]
            if "change_y" in my_enemy.properties:
                enemy.change_y = my_enemy.properties["change_y"]
            self.map.add_sprite(ENEMY_LAYER, enemy)

        # This creates a sprite with properties of change_x and the boundaries
        # required for it to move. It then adds each enemy to the enemy layer in the map
        for my_powerups in self.powerups_layer:
            powerup_coordinates = self.tile_map.get_cartesian(
                my_powerups.shape[0], my_powerups.shape[1]
            )
            powerup_type = my_powerups.properties["type"]

            if powerup_type == "health":
                powerup = HealthPotion()
            elif powerup_type == "speed":
                powerup = SpeedPowerup()

            powerup.center_x = math.floor(
                powerup_coordinates[0] * TILE_SIZE * self.tile_map.tile_width
            )
            powerup.center_y = math.floor(
                (powerup_coordinates[1] + 1) * (self.tile_map.tile_height * TILE_SIZE)
            )
            powerup.type = my_powerups.properties["type"]
            self.map.add_sprite(POWERUP_LAYER, powerup)

        """# This creates a sprite with a property of type and adds
        # it to the map
        for layer in self.layers_to_setup:
            for my_object in self.tile_map.object_lists[layer]:
                object_coordinates = self.tile_map.get_cartesian(
                    my_object.shape[0], my_object.shape[1]
                )
                object_type = my_object.properties["type"]

                if object_type == "health":
                    map_object = HealthPotion()
                elif object_type == "speed":
                    map_object = SpeedPowerup()
                elif object_type == "coin":
                    map_object = Coins()
                elif object_type == "gem":
                    map_object = Gem()

                map_object.center_x = math.floor(
                    object_coordinates[0] * TILE_SIZE * self.tile_map.tile_width
                )
                map_object.center_y = math.floor(
                    (object_coordinates[1] + 1) * (self.tile_map.tile_height * TILE_SIZE)
                )
                map_object.type = my_object.properties["type"]
                self.map.add_sprite(layer, map_object)"""

        # This creates a sprite with properties of change_x and the boundaries
        # required for it to move. It then adds each enemy to the enemy layer in the map
        """for my_crate in self.crates_layer:
            crate_coordinates = self.tile_map.get_cartesian(
                my_crate.shape[0], my_crate.shape[1]
            )

            crate = Crates()

            crate.center_x = math.floor(
                crate_coordinates[0] * TILE_SIZE * self.tile_map.tile_width
            )
            crate.center_y = math.floor(
                (crate_coordinates[1] + 1) * (self.tile_map.tile_height * TILE_SIZE)
            )

            self.map.add_sprite(CRATE_LAYER, crate)

        # Determines the end of the map
        self.map_end = self.tile_map.width * GRID_PIXEL_SIZE"""

        # Sets the background colour to the background of the map if there is one
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
    
        # Sets up the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.character, gravity_constant=GRAVITY_CONSTANT, platforms = [self.map[MOVING_PLATFORMS_LAYER], self.map[ENEMY_LAYER]],
                ladders = self.map[LADDER_LAYER], walls = self.map[PLATFORM_LAYER]
                )

    def on_draw(self):
        """Draws the sprites, enemies, map, etc on the screen"""

        # This clears the screen before drawing
        self.clear()

        # This uses the background camera (whatever comes next will be drawn onto this camera)
        self.bg_cam.use()
        
        # Draws the background
        self.bg_sprite_list.draw()
        # Draw bg as a seperate sprite list (crop bg and adjus to 650 x 1000)
        # Then set the co-ordinates

        # This uses the camera (which will follow the sprite) anything that comes next
        # will be drawn on this camera
        self.cam.use()

        # This draws out the map
        self.map.draw()

        for enemy in self.map[ENEMY_LAYER]:
            health_bar = EnemyHealth(enemy)
            health_bar.draw_health()
        
        self.character_health.draw_health()

        # Activate the GUI camera before drawing GUI elements
        # Whatever comes next will be drawn on this camera
        self.gui_cam.use()

        # Draws the hearts
        self.heart_sprite_list.draw()

        # This draws the score on a specific co-ordinate on the screen at which
        # it will stay for the rest of the game
        score_text = f"Score: {self.player_score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )
        # This draws the time taken since the level was started
        time_text = f"Time: {self.total_time}"
        arcade.draw_text(
            time_text,
            600,
            600,
            arcade.csscolor.WHITE,
            18,
        )

        

    def process_keychange(self):
        """
        Called when there is a change in the keys being pressed
        """

        # This checks if the keychange is between up and down
        # and changes the character y ordinates accordingly
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.character.change_y = CHARACTER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.character.change_y = CHARACTER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jumping_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.character.change_y = -CHARACTER_MOVEMENT_SPEED

        # This processes a change through up and down keys
        # when character is on a ladder and there is no movement
        # It sets the change in y ordinates for the character to 0
        if self.physics_engine.is_on_ladder():

            if not self.up_pressed and not self.down_pressed:
                self.character.change_y = 0

            elif self.up_pressed and self.down_pressed:
                self.character.change_y = 0
        
        else:
            self.character.on_ladder = False

        # Changes the speed of the character depending on whether they have the speed boost or not
        if self.speed_boost_equipped:
            speed = CHARACTER_MOVEMENT_SPEED * SPEED_BOOST_RATE
        else:
            speed = CHARACTER_MOVEMENT_SPEED
        # This processes if the key changes between left and right
        # and changes the x ordinates of the character accordingly
        if self.right_pressed and not self.left_pressed:
            self.character.change_x = speed

        elif self.left_pressed and not self.right_pressed:
            self.character.change_x = -speed
            
        else:
            self.character.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        timer_start_keys = [arcade.key.W, arcade.key.A,\
            arcade.key.S, arcade.key.D, arcade.key.UP, arcade.key.DOWN,\
                arcade.key.LEFT, arcade.key.RIGHT, arcade.key.R, arcade.key.E]
        # Starts the timer when the player starts moving
        if self.timer_running is False and key in timer_start_keys:
            self.start_time = time.time()
            self.timer_running = True

        # This sets the keys pressed to true so when the keychange is processed the sprite will move
        # It also keeps track of whether the character is throwing a knife or not
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.E and self.character.type == NINJA_GIRL:
            self.character.is_throwing = True
        elif key == arcade.key.R and self.character.type == NINJA_BOY:
            self.character.is_attacking = True
        elif key == arcade.key.KEY_1 and self.character.type != NINJA_GIRL:
            # And also check if their change y (and maybe change x too) is 0 if it is you can change
            self.character.type = NINJA_GIRL
        elif key == arcade.key.KEY_2 and self.character.type!= NINJA_BOY:
            self.character.type = NINJA_BOY
            #self.character.scale = 1
        elif key == arcade.key.SPACE and self.num_of_speed_boosts > 0 \
            and self.speed_boost_equipped is False:
            self.speed_boost_equipped = True
            self.num_of_speed_boosts -= 1
            #self.boost_start_time = time.time()
        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        # This makes sure that the sprite stops moving in a specific direction every time a key is released
        # It also keeps track of whether the character is throwing a knife or not
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.E:
            self.character.is_throwing = False
        elif key == arcade.key.R:
            self.character.is_attacking = False
        elif key == arcade.key.SPACE:
            #self.speed_boost_equipped = False
            pass

        self.process_keychange()

    def center_camera_to_player(self):
        """Centres camera to sprite"""

        # Sets the co-ordinates for the camera 
        screen_center_x = self.character.center_x - (self.cam.viewport_width / 2)
        screen_center_y = self.character.center_y - (
            self.cam.viewport_height / 2
        )
        #print(screen_center_x,self.character.center_x)
        # This makes sure the camera cannot go past the left edge of the map
        if screen_center_x < 0:
            screen_center_x = 0
        """if screen_center_x > PLAYER_BOUNDARY_RIGHT:
            screen_center_x = PLAYER_BOUNDARY_RIGHT"""
        # This makes sure that the camera cannot beneath the map
        if screen_center_y < 0:
            screen_center_y = 0
        """if screen_center_y > PLAYER_BOUNDARY_TOP:
            screen_center_y = PLAYER_BOUNDARY_TOP"""
        
        # Sets co-ordinates of the camera
        player_centered = screen_center_x, screen_center_y

        # Sets camera center
        #self.cam.centre_x = screen_center_x
        #self.cam.centre_y = screen_center_y
        # Moves the camera to the set co-ordinates
        self.cam.move_to(player_centered,0.2)

    def on_update(self, delta_time):
    
        """This function updates info from the game regularly"""
        #print(self.character.center_x,self.character.center_y)
        # This moves the player sprite and updates the positioning of the platforms
        self.physics_engine.update()
    
        # Update character and heart animation
        self.character.update_animation()
        self.hearts.update_animation()


        # This updates the info on whether a sprite can jump or not
        # and also whether they are on a ladder or not
        if self.physics_engine.can_jump():
            self.character.can_jump = False
        else:
            self.character.can_jump = True

        # This checks whether the character is on a ladder and can't jump or 
        # if they are in the air and adjusts the on_ladder variables as they should be
        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.character.on_ladder = True
            self.process_keychange()
        else:
            self.character.is_on_ladder = False
            self.process_keychange()

        # If the speed boost is equipped then this will create a sprite that will 
        # act as a sort of visual thing as to when the character moves faster
        if self.speed_boost_equipped is True:
            
            img_src = f"{MAIN_FILE_PATH}Assets/Dash.png"
            dash_sprite = SpeedDash(img_src,self.character)
            dash_sprite.start_frame = self.boost_frames_since_reset
            self.map.add_sprite(DASH_LAYER, dash_sprite)

            # For every sprite in the dash layer it will remove them if they have 
            # existed for 3 frames so it looks animated
            for sprite in self.map[DASH_LAYER]:
                if self.boost_frames_since_reset == sprite.start_frame + 3:
                    sprite.remove_from_sprite_lists()

            # If the powerup expires then the whole dash layer will be cleared
            # and the boost frames since reset will be set back to 0 (-1+1=0)
            if self.boost_frames_since_reset == SPEED_BOOST_FRAMES:
                self.map[DASH_LAYER].clear()
                self.speed_boost_equipped = False
                self.boost_frames_since_reset = -1



            self.boost_frames_since_reset += 1

        # Updates the timer
        if self.timer_running:
            self.total_time = round(time.time() - self.start_time,3)

        # Runs if the player is able to throw a knife
        if self.can_throw:
            
            # If the player is throwing a knife (aka they pressed space)
            # then a new knife sprite will be created and added to the layer "Knives"
            # The original direction variable is to track which way the knife was first going in
            if self.character.is_throwing:

                img_src = f"{MAIN_FILE_PATH}Assets/Ninja/png/Kunai.png"
                knife = KnivesAttack(img_src, KNIFE_SIZE, "Detailed",self.character.center_x - KNIFE_RANGE,self.character.center_x + KNIFE_RANGE)
                knife.change_angle = KNIFE_ROTATION_ANGLE
                if self.character.character_direction == RIGHT_FACING:
                    knife.left = self.character.right
                else:
                    knife.right = self.character.left
                knife.original_direction = self.character.character_direction
                knife.center_y = self.character.center_y
                self.map.add_sprite(KNIFE_LAYER, knife)

                self.can_throw = False

            else:
                pass
        
        # IF the player is unable to throw knives because they threw a knife less than
        #  x frames ago, then it will increase the number of frames between shots
        # If the number of frames is enough then the character will once again be able
        # to throw knives
        else:
            
            self.frames_between_shots += 1
            if self.frames_between_shots == KNIFE_THROW_RATE:
                self.can_throw = True
                self.frames_between_shots = 0

        # If the knife layer exists (there is a knife in it) then this will run
        # It will remove an knives that have collided with the platform or enemy layer
        # and also update the knife speed and rotation (basically animation)
        if self.map[KNIFE_LAYER]:
            for knife in self.map[KNIFE_LAYER]:

                if knife.center_x > knife.right_boundary or knife.center_x < knife.left_boundary:
                    knife.remove_from_sprite_lists()

                for enemy in self.map.get_sprite_list(ENEMY_LAYER): 
                    
                    if arcade.check_for_collision(knife, enemy):
                        knife.remove_from_sprite_lists()
                        enemy.health -= knife.damage()
                
                if arcade.check_for_collision_with_list(knife,self.map[PLATFORM_LAYER]):
                    knife.remove_from_sprite_lists()

                if knife.original_direction == RIGHT_FACING:

                    speed = KNIFE_SPEED
                    #angle = math.tan(self.angle) * speed

                else:

                    speed = -KNIFE_SPEED
                    #angle = math.tan(180-self.angle) * speed
                knife.center_x += speed
                #knife.center_y -= KNIFE_GRAVITY
                #knife.center_y += angle
                
                knife.angle += KNIFE_ROTATION_ANGLE

        # If any coins are hit those coins are removed from the sprite list
        # and the score is increased
        for layer in self.collectable_layers:
            for collectable in self.map.get_sprite_list(layer):
                # Removes coins if the player hits them
                #for coin in coin_hit_list:
                if arcade.check_for_collision(self.character,collectable):
                    if layer == COIN_LAYER and self.character.type == NINJA_GIRL or layer == GEM_LAYER and self.character.type == NINJA_BOY:
                    # Remove the coin from the coin sprite list
                        collectable.remove_from_sprite_lists()
                        # Plays the sound when the coins are collected
                        arcade.play_sound(self.coin_collection_sound)
                        # Increments score
                        self.player_score += 1    

        # Updates the checkpoints the player has gone through
        for checkpoint in self.map[CHECKPOINT_LAYER]:

            if arcade.check_for_collision(self.character, checkpoint) and checkpoint not in self.passed_checkpoints:
                self.passed_checkpoints.append(checkpoint)
                self.last_checkpoint = checkpoint

        """"""""""""""""""""""""""""""""""""""""""""""""""
        for powerup in self.map.get_sprite_list(POWERUP_LAYER):
            powerup.update_animation()
            if arcade.check_for_collision(self.character,powerup):
                if powerup.type == "health":
                    if self.hearts.lives <3:
                        self.hearts.lives +=1
                        powerup.remove_from_sprite_lists()
                    else:
                        pass
                elif powerup.type == "speed":
                    self.num_of_speed_boosts += 1
                    powerup.remove_from_sprite_lists()

        # Updates the enemies animation and also removes them from the enemy list 
        # if enemies died
        for enemy in self.map.get_sprite_list(ENEMY_LAYER):
            if not arcade.check_for_collision_with_list(enemy,self.map[PLATFORM_LAYER]):
                enemy.center_y -= GRAVITY_CONSTANT
            self.character.weapon.check_for_attack_collision(enemy)
            if enemy.health <= 0:
                enemy.remove_from_sprite_lists()
            enemy.update_animation()

        """# Updates the animation for coins and gems
        for object in self.map.get_sprite_list(COLLECTABLE_OBJECTS_LAYER):
            object.update_animation()
            if arcade.check_for_collision(self.character,object):
                if object.type == "coin" and self.character.type == NINJA_GIRL:
                    object.remove_from_sprite_lists()
                    arcade.play_sound(self.coin_collection_sound)
                    
                    # Can use ninja variable as constant to check if its first ninja or whatever
            #if arcade.check_for_collision_with_list(self.map[COLLECTABLE_OBJECTS_LAYER]):"""

        # If the player touches a deadly object (spikes or lava)
        # then this will run and deduct health from the player.
        # If they end up with no health then the game will reset
        # If they do have health they will go to the last checkpoint they passed but
        # their score will remain intact
        # This also updates the hearts animation after a character loses a heart
        if arcade.check_for_collision_with_lists(
            self.character, [self.map[DEADLY_LAYER], self.map[ENEMY_LAYER]]
        ) or self.character.center_y < BOTTOM_MAP_LIMIT:
            if arcade.check_for_collision_with_list(self.character,self.map[ENEMY_LAYER]):
                amt_damage_dealt = damage_dealt()
            else:
                amt_damage_dealt = MAX_HEALTH
            self.character.health -= amt_damage_dealt
            if self.character.health <= 0:
                self.hearts.lives -= 1
                self.hearts.update_animation()

                if self.hearts.lives == 0:
                    arcade.play_sound(self.game_over_sound)
                    game_over_view = GameOver(self,self.player_score, self.total_time)
                    self.window.show_view(game_over_view)

                else:
                    self.character.health = MAX_HEALTH
                    last_checkpoint = self.last_checkpoint
                    self.character.center_x = last_checkpoint.center_x
                    self.character.center_y = last_checkpoint.center_y
                    self.character.character_direction = RIGHT_FACING
                    return
        
        """if arcade.check_for_collision_with_list(self.character,self.map[CRATE_LAYER]):
            print("1yes")
            for crate in self.map[CRATE_LAYER]:

                if arcade.check_for_collision(self.character,crate):
                    print("yes")
                    crate.move_crate(CRATE_MOVE_RATE)"""
        
        # Moves the user onto the next level if they have touched the level pass object
        if arcade.check_for_collision_with_list(
            self.character, self.map[LEVEL_PASS_LAYER]
            ) and len(self.map[GEM_LAYER]) == 0 and \
                len(self.map[COIN_LAYER])== 0 and \
                    len(self.map[ENEMY_LAYER]) ==0:


            # Moves onto next level if its not the highest level already
            if self.level != NUM_OF_LEVELS:
                self.level += 1

            # Runs the game over screen if the user has completed the game
            else:
                pass
            
            # Sets window so we can use it later
            window = self.window

            # Creates total time variable so we can use it in the level pass view
            current_total_time = self.total_time

            # Calls level passed view which carries onto next level passing the game view as self
            pass_view = LevelPassed(self, self.player_score, current_total_time)
            window.show_view(pass_view)

        # Centres the camera on the sprite
        self.center_camera_to_player()

def main():
    """Main function"""

    # This sets up and runs the game
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = InstructionView()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()
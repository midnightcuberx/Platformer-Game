"""
Python game
"""

# Imports the modules needed
import arcade
import random
import time
import math

# Main file path
# MAIN_FILE_PATH = "C:/python projects/Python Assessment/"
# MAIN_FILE_PATH = "C:/school/python/Python Assessment/"
# MAIN_FILE_PATH = "S:/Computing/Assessment/2022/Year 13\
# /Subject 13DTP Class 2-1/dh19502/Python Assessment/"
MAIN_FILE_PATH = "F:/Python Assessment/"

# Constants that will be used later in the code
# for setting up the window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Python Assessment Game"

# These are the scaling constants
TILE_SIZE = 0.5
CHARACTER_SIZE = TILE_SIZE * 0.45
COIN_SIZE = TILE_SIZE
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SIZE)
HEART_SIZE = 0.75
BG_SIZE = 1.25
POWERUP_SIZE = TILE_SIZE
ENEMY_SIZE = 0.2

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
GEM_LAYER = "Gems"
TELEPORT_LAYER = "Teleport"
HIDDEN_LAYER = "Hidden"

# Constant used for determining the player speed
CHARACTER_MOVEMENT_SPEED = 7
GRAVITY_CONSTANT = 1
ENEMY_GRAVITY_CONSTANT = 5
CHARACTER_JUMP_SPEED = 20

# Knife constants
KNIFE_SIZE = 0.3
KNIFE_SPEED = 15
KNIFE_ROTATION_ANGLE = 30
KNIFE_THROW_RATE = 10
KNIFE_RANGE = 400
STARTING_KNIVES_NUM = 10
KNIFE_INCREASE_AMT = 3
KNIFE_MIN_DMG = 10
KNIFE_MAX_DMG = 30
JUMP_THROW_ANIMATION_MAX_FRAME = 4
FALL_THROW_ANIMATION_MIN_FRAME = 5

# Health constants
HEALTH_WIDTH = 40
ENEMY_FRAMES = 12
CHARACTER_FRAMES = 10
MAX_HEALTH = 100
MAX_HEARTS = 3
HEALTHBAR_OFFSET = 10
HEALTHBAR_HEIGHT = 4
HEALTH_INC = 0.125

# Level Stuff
NUM_OF_LEVELS = 3
STARTING_LEVEL = 1

# Damage
ENEMY_DMG = 5
SWORD_DMG = 5

# Rates
POWERUP_RATE = 10
SPEED_BOOST_RATE = 1.5

# Offsets
TELEPORT_OFFSET_X = 100
DASH_OFFSET = 25
SWORD_OFFSET_X = 15
TEXT_OFFSET = 75

# Update frame constants
ENEMY_WALKING_UPDATE_FRAMES = 3
DASH_UPDATE_FRAMES = 3

# Frames
HEART_FRAMES = 4
HEALTH_POWERUP_FRAMES = 6
SPEED_POWERUP_FRAMES = 12
CHARACTER_FRAMES = 10
SPEED_BOOST_FRAMES = 300

# Constants used for sprite centering
CHARACTER_CENTRE_X = SPRITE_PIXEL_SIZE * TILE_SIZE * 2
CHARACTER_CENTRE_Y = SPRITE_PIXEL_SIZE * TILE_SIZE * 5
HEART_CENTRE_X = 80
HEART_CENTRE_Y = 615
BG_CENTRE_X = 500
BG_CENTRE_Y = 325

# Tracks which direction the player is facing
RIGHT_FACING = 0
LEFT_FACING = 1

# Keeps track of which character is which
NINJA_GIRL = 0
NINJA_BOY = 1

# Font size
BIG_FONT_SIZE = 50
SMALL_FONT_SIZE = 20

# Other
HITBOX_ALGORITHM = "Detailed"
TIMER_DP = 3
CAMERA_SPEED = 0.2
BOTTOM_MAP_LIMIT = -100
PAUSE_SCREEN_TRANSPARENCY = 150


def load_textures(filename):
    """
    Load a texture pair with the second being the mirror image of the first
    """
    return arcade.load_texture_pair(filename, hit_box_algorithm="Detailed")


class ImgView(arcade.View):
    """This is a view that consists of an img"""

    def __init__(self, img, music_playing: bool = False):
        """Initialises variables and runs when this view is shown"""

        # Inherits the parent class of arcade.View
        # and its variables and methods
        super().__init__()

        # Loads and sets the texture for this class
        self.texture = arcade.load_texture(img)

        # Music playing
        self.music_playing = music_playing

    def on_draw(self):
        """Draws the view"""

        # Clears the view to just the background
        self.clear()

        # Resize the texure so that it fits the view and draws it
        self.texture.draw_sized(SCREEN_WIDTH / 2,
                                SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT
                                )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """This starts the game if the user pressed the screen"""

        # This sets up the main game and shows it on the screen
        main_game = Game(STARTING_LEVEL, self.music_playing)
        main_game.setup()
        self.window.show_view(main_game)


class Instructions(ImgView):
    """The instructions for the player when they run the game"""

    def __init__(self):
        """Initialises variables and runs when this view is shown"""

        # Inherits the parent class of ImgView with
        # its variables and methods
        super().__init__("Intro.jpg")


class GameCompleted(ImgView):
    """The instructions for the player when they run the game"""

    def __init__(self):
        """Initialises variables and runs when this view is shown"""

        # Inherits the parent class of ImgView with
        # its variables and methods
        super().__init__("GameCompleted.jpg", True)


class PauseView(arcade.View):
    """The basic View for any view that is shown during gameplay"""

    def __init__(self, game_view, score: int, time: float,
                 fill_colour: arcade.color = arcade.color.WHITE,
                 level_increment: bool = False):
        """
        This is run as soon as this view is switched to
        and intialises all variables
        """

        # Inherits the parent class of LevelPass and takes on
        # all of its variables and methods
        super().__init__()

        # Initializes attributes
        self.game_view = game_view
        self.score = score
        self.time = time
        self.level_incremement = level_increment
        self.fill_color = arcade.make_transparent_color(
            fill_colour, transparency=PAUSE_SCREEN_TRANSPARENCY)

    def on_mouse_press(self, _x, _y, _button, _modifiers):

        """This starts the game if the user clicked their mouse"""

        # Will increment the level if necessary
        if self.level_incremement:
            self.game_view.level += 1

        # Sets up the next view depending on if the game has finished
        if self.game_view.level <= NUM_OF_LEVELS:
            view = Game(self.game_view.level, self.game_view.music_playing,
                        self.game_view.character.type)
            view.setup()
        else:
            view = GameCompleted()

        # Shows the view
        self.window.show_view(view)


class LevelPassed(PauseView):
    """Runs when the level is passed"""

    def __init__(self, game_view, score: int, time: float,
                 level_increment: bool = True):

        # Fill colour
        fill_colour = arcade.color.WHITE

        # Inherits the parent class of PauseView and takes on
        # all of its variables and methods
        super().__init__(game_view, score, time, fill_colour, level_increment)

    def on_draw(self):
        """Draws on the window"""

        # Clears the view
        self.clear()

        # Draws the paused game view in the background
        # from the original game view
        self.game_view.on_draw()

        # Draws a white transparent layer over the frozen game screen
        arcade.draw_lrtb_rectangle_filled(
            left=0,
            right=SCREEN_WIDTH,
            top=SCREEN_HEIGHT,
            bottom=0,
            color=self.fill_color,
        )

        # Draws the text on the screen telling the user their score
        arcade.draw_text(
            f"Congrats for passing level {self.game_view.level}!",
            self.window.width / 2, self.window.height / 2,
            arcade.color.BLACK, font_size=BIG_FONT_SIZE, anchor_x="center")
        arcade.draw_text(
            "You passed the level with a score of " +
            f"{self.score} and a time of {self.time}",
            self.window.width / 2, self.window.height / 2 - TEXT_OFFSET,
            arcade.color.BLACK, font_size=SMALL_FONT_SIZE, anchor_x="center")


class GameOver(PauseView):
    """Runs when the game is over"""

    def __init__(self, game_view, score: int, time: float):
        """Initialises all variables and runs when this View is shown"""

        # Background colour of view
        fill_colour = arcade.color.RED_DEVIL

        # Inherits the parent class of PauseView and takes on
        # all of its variables and methods
        super().__init__(game_view, score, time, fill_colour)

    def on_draw(self):
        """Draws on the window"""

        # Draws the paused game view in the background
        # from the original game view
        self.game_view.on_draw()

        # Draws a white transparent layer over the frozen game screen
        arcade.draw_lrtb_rectangle_filled(
            left=0,
            right=SCREEN_WIDTH,
            top=SCREEN_HEIGHT,
            bottom=0,
            color=self.fill_color,
        )

        # Draws the text on the screen telling the user their score
        arcade.draw_text(f"You died", self.window.width / 2,
                         self.window.height / 2, arcade.color.BLACK,
                         font_size=BIG_FONT_SIZE, anchor_x="center")
        arcade.draw_text(f"Your final score was {self.score}",
                         self.window.width / 2, self.window.height / 2 -
                         TEXT_OFFSET, arcade.color.BLACK,
                         font_size=SMALL_FONT_SIZE, anchor_x="center")


class Weapon(arcade.Sprite):
    """Weapon sprite for attacking sword hitbox"""

    def __init__(self, character):
        """Initialises variables and runs when this class is called"""

        # Inherits the arcade.sprite parent class and inherits
        # all the variables and methods from that class
        super().__init__()

        # Initialises the attributes
        self.character = character
        self.scale = CHARACTER_SIZE

        # This sets up the textures for the weapon
        self.weapon_textures = []
        for i in range(CHARACTER_FRAMES):
            texture = load_textures(MAIN_FILE_PATH +
                                    "/Assets/Ninja/png/Attacking/Attack__00" +
                                    str(i) + ".png")
            self.weapon_textures.append(texture)

        # Sets the orginal texture to the first texture
        self.texture = self.weapon_textures[0][
            self.character.direction]

    def check_for_attack_collision(self, enemy_sprites: arcade.Sprite):
        """Checks for collisions with enemy sprites"""

        # Sees if the weapon hits any enemies and deduct health
        # from the enemies if it is
        hit_enemies = arcade.check_for_collision(self, enemy_sprites)
        if hit_enemies and self.character.is_attacking:
            enemy_sprites.health -= SWORD_DMG

    def update_animation(self, delta_time: float = 1 / 60):
        """Updates the weapon hitbox """

        # If the character is attacking then the texture will
        # change to fit the according texture of the player animation
        if self.character.is_attacking:
            self.texture = self.weapon_textures[
                self.character.current_texture][
                    self.character.direction]
            self.hit_box = self.texture.hit_box_points

            # Changes the centre and direction of the weapon
            if self.character.direction == RIGHT_FACING:
                self.left = self.character.right + SWORD_OFFSET_X
            else:
                self.right = self.character.left - SWORD_OFFSET_X
            self.center_y = self.character.center_y


class Character(arcade.Sprite):
    """Player sprite class"""

    def __init__(self, moving_platforms, character_type=NINJA_GIRL):
        """
        Runs when the character class is called and initialises variables
        """

        # Inherits the parent class of arcade.Sprite
        # and takes on all the variables of it
        super().__init__()

        # These variables track the characters actions
        self.jumping = False
        self.climbing = False
        self.on_ladder = False
        self.is_throwing = False
        self.is_attacking = False

        # Other character attributes
        self.direction = RIGHT_FACING
        self.scale = CHARACTER_SIZE
        self.health = MAX_HEALTH
        self.type = character_type
        self.knives_num = STARTING_KNIVES_NUM

        # Character textures
        self.idle_textures = []
        self.jumping_textures = []
        self.falling_textures = []
        self.walking_textures = []
        self.climbing_textures = []
        self.throwing_textures = []
        self.jump_throw_textures = []
        self.attacking_textures = []

        # Moving platforms
        self.moving_platforms = moving_platforms

        # This is crating the weapon and
        # setting up the attacking textures
        self.weapon = Weapon(self)

        # Current character texture
        self.current_texture = 0

        # Loads character textures
        folder_names = ["Ninja/png", "ninjaadventurenew/png"]

        for folder in folder_names:
            file_path = f"{MAIN_FILE_PATH}Assets/{folder}/"

            # Loading texture pairs for when the
            # character is idle, jumping, or falling
            self.idle_textures.append(
                load_textures(f"{file_path}Idle__000.png"))
            self.jumping_textures.append(
                load_textures(f"{file_path}Jump__001.png"))
            self.falling_textures.append(
                load_textures(f"{file_path}Jump__009.png"))

            # Loading the walking textures into a list of textures
            walking_textures = []
            for i in range(CHARACTER_FRAMES):
                texture = load_textures(f"{file_path}Run__00{i}.png")
                walking_textures.append(texture)

            # Loads climbing textures
            climbing_textures = []
            for i in range(CHARACTER_FRAMES):
                texture = arcade.load_texture(f"{file_path}Climb_00{i}.png",
                                              hit_box_algorithm="Detailed")
                climbing_textures.append(texture)

            # Loads the throwing textures
            throwing_textures = []
            for i in range(CHARACTER_FRAMES):
                texture = load_textures(f"{file_path}Throw__00{i}.png")
                throwing_textures.append(texture)

            # Loads jump throw textures
            jump_throw_textures = []
            for i in range(CHARACTER_FRAMES):
                texture = load_textures(f"{file_path}Jump_Throw__00{i}.png")
                jump_throw_textures.append(texture)

            # Loads attacking textures
            attacking_textures = []
            for i in range(CHARACTER_FRAMES):
                texture = load_textures(f"{file_path}Attack__00{i}.png")
                attacking_textures.append(texture)

            # Adds the texture lists to their respective lists
            self.walking_textures.append(walking_textures)
            self.climbing_textures.append(climbing_textures)
            self.throwing_textures.append(throwing_textures)
            self.jump_throw_textures.append(jump_throw_textures)
            self.attacking_textures.append(attacking_textures)

        # Sets initial texture to right facing
        self.texture = self.idle_textures[self.type][RIGHT_FACING]

    def on_moving_platform(self, moving_platforms):
        """Checks if the player is on a moving platform or not"""

        # Checks if the player is on a moving platform
        if len(
                arcade.check_for_collision_with_list(self, moving_platforms)
                ) > 0:
            return True

    def texture_count(self, lower_limit: int = 0, upper_limit: int = 9):
        "Updates the texture count"

        # Changes the character texture
        self.current_texture += 1

        # Resets the texture to the lowest limit if it exceeds
        # the upper limit or if it is under the lower limit.
        if self.current_texture < lower_limit:
            self.current_texture = lower_limit
        elif self.current_texture > upper_limit:
            self.current_texture = lower_limit

    def throwing_animation(self, texture_list,
                           lower_limit: int = 0,
                           upper_limit: int = CHARACTER_FRAMES - 1):
        """Updates the texture if the character is throwing a knife"""

        self.texture_count(lower_limit, upper_limit)
        self.texture = texture_list[self.current_texture][
            self.direction]

    def update_animation(self, delta_time: float = 1 / 60):
        """Updates the animation for the character sprite"""

        # Updates weapon texture and character and weapon
        # hitbox if character is attacking
        if self.is_attacking:
            self.texture_count()
            self.texture = self.attacking_textures[self.type][
                self.current_texture][self.direction]
            self.hit_box = self.attacking_textures[self.type][0][
                self.direction].hit_box_points
            self.weapon.update_animation()
        else:
            # Updates character direction
            if (self.change_x < 0 and
                    self.direction == RIGHT_FACING):
                self.direction = LEFT_FACING
            elif (self.change_x > 0 and
                    self.direction == LEFT_FACING):
                self.direction = RIGHT_FACING

            # Updates self.climbing based if the
            # character is actually climbing or not
            if self.on_ladder:
                self.climbing = True
            if not self.on_ladder and self.climbing:
                self.climbing = False

            # Changes textures if charactr is climbing
            if self.climbing:
                if abs(self.change_y) > 1:
                    self.texture_count()
                self.texture = self.climbing_textures[self.type][
                    self.current_texture]
                return

            # This changes textures depending on if the character
            # is jumping or falling or even knife throwing
            if self.change_y > 0 and not self.on_ladder and not\
                    self.on_moving_platform(self.moving_platforms):
                if not self.is_throwing:
                    # Jumping texture if character is jumping
                    self.texture = self.jumping_textures[self.type][
                        self.direction]
                else:
                    # Throwing animation if character throws knives
                    self.throwing_animation(
                        self.jump_throw_textures[self.type],
                        upper_limit=JUMP_THROW_ANIMATION_MAX_FRAME)
                return
            elif self.change_y < 0 and not self.on_ladder and not\
                    self.on_moving_platform(self.moving_platforms):
                if not self.is_throwing:
                    # Falling texture if character is falling
                    self.texture = self.falling_textures[self.type][
                        self.direction]
                else:
                    # Throwing animation if the character throws knives
                    self.throwing_animation(
                        self.jump_throw_textures[self.type],
                        FALL_THROW_ANIMATION_MIN_FRAME)
                return

            # Idle animation and knife throwing
            if self.change_x == 0:
                if not self.is_throwing:
                    # Idle animation
                    self.texture = self.idle_textures[self.type][
                        self.direction]
                else:
                    # Throwing knives animation
                    self.throwing_animation(self.throwing_textures[self.type])
                return

            # Loops through walking or knife throwing animation
            if not self.is_throwing:
                # Throwing animation
                self.throwing_animation(self.walking_textures[self.type])
            else:
                # Walking animation
                self.throwing_animation(self.throwing_textures[self.type])


class Golem(arcade.Sprite):
    """Sprite class for entities which will be inherited"""

    def __init__(self):
        """
        This runs when the class is called, and it intialises all variables
        """

        # Inherits the parent class of arcade.Sprite
        # and takes on all the variables of it
        super().__init__()

        # Adds extra attributes
        self.health = MAX_HEALTH
        self.no_of_frames = ENEMY_FRAMES
        self.direction = RIGHT_FACING
        self.scale = ENEMY_SIZE
        self.should_update_walk = 0
        self.current_texture = 0

        # --- Loading textures ---
        img_path = f"{MAIN_FILE_PATH}Assets/Golem Enemy/0_Golem_Running_00"
        self.walking_textures = []

        # Loading the walking textures into a list of textures
        for i in range(self.no_of_frames):
            texture = load_textures(f"{img_path}{i}.png")
            self.walking_textures.append(texture)

        # This sets the initial texture to right facing
        self.texture = self.walking_textures[
            self.current_texture][RIGHT_FACING]

    def update_animation(self, delta_time: float = 1 / 60):

        """Updates animations for the enemy"""

        # Sprite direction adjustments
        if self.change_x < 0 and self.direction == RIGHT_FACING:
            self.direction = LEFT_FACING
        elif self.change_x > 0 and self.direction == LEFT_FACING:
            self.direction = RIGHT_FACING

        # This animates the sprite when it walks
        if self.should_update_walk == ENEMY_WALKING_UPDATE_FRAMES:
            self.current_texture += 1
            if self.current_texture > self.no_of_frames - 1:
                self.current_texture = 0
            self.texture = self.walking_textures[
                self.current_texture][self.direction]
            self.should_update_walk = 0
            return

        # Updates the number of frames since
        # the sprite last updated its texture
        self.should_update_walk += 1


class KnivesAttack(arcade.Sprite):
    """Class for throwing knives"""

    def __init__(self, filename: str, scale: float, hit_box_algorithm: str,
                 left_boundary: int, right_boundary: int):
        """
        Runs when the KnivesAttack class is called and initialises variables
        """

        # Inherits the parent class of arcade.Sprite and takes
        # on all its variables and functions
        super().__init__(filename, scale, hit_box_algorithm=hit_box_algorithm)

        # Sprite attributes
        self.original_direction = RIGHT_FACING
        self.left_boundary = left_boundary
        self.right_boundary = right_boundary

    def damage(self):
        """Determins how much damage the knife does"""
        return random.randint(KNIFE_MIN_DMG, KNIFE_MAX_DMG)


class SpeedDash(arcade.Sprite):
    """Dash animation for speed powerup"""

    def __init__(self, filename: str, character):
        """
        Runs when the SpeedDash class is called and initialises variables
        """

        # Inherits the parent class of arcade.Sprite and takes
        # on all its variables and functions
        super().__init__(filename, hit_box_algorithm=HITBOX_ALGORITHM)

        # Sprite attributes
        self.character = character
        self.direction = character.direction
        self.dash_texture_pair = load_textures(filename)

        # Offset based on character direction
        if self.character.direction == RIGHT_FACING:
            offset_x = - DASH_OFFSET
        else:
            offset_x = DASH_OFFSET

        # Sprite centering
        self.center_x = self.character.center_x + offset_x
        self.center_y = self.character.center_y

    def update_animation(self, delta_time: float = 1 / 60):
        """Updates the animation for speed powerup effects"""

        # Direction for dash sprite based on character direction
        if self.character.change_x < 0 and self.direction == RIGHT_FACING:
            self.direction = LEFT_FACING
        elif self.character.change_x > 0 and self.direction == LEFT_FACING:
            self.direction = RIGHT_FACING

        # Sets the texture to facing the right direction
        self.texture = self.dash_texture_pair[self.direction]


class HealthBar(arcade.Sprite):
    """Healthbar sprite"""

    def __init__(self, sprite):
        """
        Runs when the HealthBar class is called and initialises variables
        """

        # Takes on the variables and functions of arcade.sprite,
        # the parent class
        super().__init__()

        # Initialises variables
        self.sprite = sprite
        self.health_width = HEALTH_WIDTH

    def draw_health(self):
        """Draws the health bar"""

        # Draws 2 rectangles above the sprite
        # one red one green in order to represent health
        arcade.draw_rectangle_filled(
            self.sprite.center_x, self.sprite.top + HEALTHBAR_OFFSET,
            self.health_width, HEALTHBAR_HEIGHT, color=arcade.color.RED)
        health_width = self.health_width * self.sprite.health / MAX_HEALTH
        arcade.draw_rectangle_filled(
            self.sprite.center_x - self.health_width / 2 +
            health_width / 2, self.sprite.top + HEALTHBAR_OFFSET,
            health_width, HEALTHBAR_HEIGHT, color=arcade.color.GREEN)


class AnimatedObject(arcade.Sprite):
    """A class that animates objects such as coins and hearts/potions"""

    def __init__(self, file_path: str, scaling: int,
                 num_of_frames: int, frame_rate: int = 1):
        """Runs when the Animated class is called and initialises variables"""

        # Inherits the parent class of arcade.Sprite
        # with its variables and methods
        super().__init__()

        # Intializing of attributes and variables needed later
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

        # Counts frames since the last animation happened
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
        """
        Runs when the HealthPotion class is called and initialises variables
        """

        # Inherits the parent class, that is
        # The hearts class becomes an animated object
        # and takes on all its variables
        super().__init__(f"{MAIN_FILE_PATH}Assets/Collectables/heart",
                         POWERUP_SIZE, HEALTH_POWERUP_FRAMES, POWERUP_RATE)


class SpeedPowerup(AnimatedObject):
    """A class for The speed powerups"""

    def __init__(self):
        """
        Runs when the SpeedPowerup class is called and initialises variables
        """

        # Inherits the parent class, that is
        # The hearts class becomes an animated object
        # and takes on all its variables
        super().__init__(f"{MAIN_FILE_PATH}Assets/Collectables/speed",
                         POWERUP_SIZE, SPEED_POWERUP_FRAMES, POWERUP_RATE)


class PlayerHearts(AnimatedObject):
    """Hearts Class"""

    def __init__(self):
        """Runs when the Hearts class is called and initialises variables"""

        # Inherits the parent class, that is
        # The hearts class becomes a sprite in arcade
        # and takes on all its variables
        super().__init__(
            MAIN_FILE_PATH +
            f"Assets/Kenney Platform Art/Base pack/HUD/hud_heart",
            HEART_SIZE, HEART_FRAMES)

        # Number of lives initially
        self.lives = MAX_HEARTS

        # Initial texture
        self.texture = self.texture_list[MAX_HEARTS]

    def update_animation(self, delta_time: float = 1 / 60):
        """Updates the hearts animation"""

        # Updates the texture to how many hearts the user has remaining
        self.texture = self.texture_list[self.lives]


class Game(arcade.View):
    """
    Main class that runs the game
    """

    def __init__(self, level: int, music: bool = False,
                 character_num: int = NINJA_GIRL):

        # This inherits the parent class and sets up the platform
        super().__init__()

        # Intializes window width and height
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        # Map stuff
        self.tiled_map = None
        self.map_end = 0
        self.map = None

        # Intializes layers needed later
        self.enemies_layer = None
        self.powerups_layer = None
        self.collectable_layers = [COIN_LAYER, GEM_LAYER]

        # Intializes the character sprite
        self.character = None
        self.character_health = None
        self.character_num = character_num

        # Intialize the heart sprite list
        self.hearts = None
        self.bg = None

        # Checkpoint stuff
        self.last_checkpoint = None
        self.passed_checkpoints = []

        # Sets up the cameras
        self.cam = None
        self.gui_cam = None
        self.bg_cam = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.is_throwing = False
        self.speed_boost_equipped = False
        self.can_throw = True

        # Frame tracking variables
        self.frames_between_shots = 0
        self.num_of_speed_boosts = 0
        self.boost_frames_since_reset = 0

        # Variables that keep track of time
        self.timer_running = False
        self.start_time = None
        self.total_time = 0.000

        # The level
        self.level = level
        self.player_score = 0

        # Initializes the physics engine
        self.physics_engine = None

        # Keeps track of whether the music is playing or not
        self.music_playing = music

        # This code loads the sounds that we need later
        self.coin_collection_sound = arcade.load_sound(
            ":resources:sounds/coin1.wav")
        self.jumping_sound = arcade.load_sound(
            ":resources:sounds/jump1.wav")
        self.game_over_sound = arcade.load_sound(
            ":resources:sounds/gameover1.wav")
        self.game_bg_track = arcade.load_sound(
            f"{MAIN_FILE_PATH}Assets/Funky_funk.mp3", streaming=True)

        # This sets the background colour
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """
        Setup the game and call this to start the game.
        This is to make it easier to restart the game
        when the character dies etc
        """

        # Plays the music if it is not already playing
        if self.music_playing is False:
            arcade.play_sound(self.game_bg_track, looping=True)
            self.music_playing = True

        # Sets up the cameras
        self.cam = arcade.Camera(self.width, self.height)
        self.gui_cam = arcade.Camera(self.width, self.height)
        self.bg_cam = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_path = MAIN_FILE_PATH
        map_name = f"{map_path}level{self.level}.tmx"

        # This is a dictionary full of possible layers
        layer_options = {
            PLATFORM_LAYER: {
                "use_spatial_hash": True,
            },
            COIN_LAYER: {
                "use_spatial_hash": True,
            },
            DEADLY_LAYER: {
                "use_spatial_hash": True,
            },
            MOVING_PLATFORMS_LAYER: {
                "use_spatial_hash": False,
            },
            LEVEL_PASS_LAYER: {
                "use_spatial_hash": True,
            },
            ENEMY_LAYER: {
                "use_spatial_hash": False,
            },
            CHECKPOINT_LAYER: {
                "use_spatial_hash": True,
            },
            POWERUP_LAYER: {
                "use_spatial_hash": True,
            },
            GEM_LAYER: {
                "use_spatial_hash": True,
            },
            TELEPORT_LAYER: {
                "use_spatial_hash": True,
            },
            HIDDEN_LAYER: {
                "use_spatial_hash": True,
            },
            FOREGROUND_LAYER: {
                "use_spatial_hash": True,
            },
        }

        # Load the scene from Tiled
        self.tile_map = arcade.load_tilemap(
            map_name, TILE_SIZE, layer_options)

        # List of object layers with placeholders
        self.enemies_layer = self.tile_map.object_lists[ENEMY_LAYER]
        self.powerups_layer = self.tile_map.object_lists[POWERUP_LAYER]

        # Creates a scene from the tilemap and adds necessary layers
        self.map = arcade.Scene.from_tilemap(self.tile_map)
        self.map.add_sprite_list_before(PLAYER_LAYER, FOREGROUND_LAYER)
        self.map.add_sprite_list_before(DASH_LAYER, PLAYER_LAYER)
        self.map.add_sprite_list_before(KNIFE_LAYER, FOREGROUND_LAYER)

        # Sets up the health bar
        self.hearts = PlayerHearts()
        self.hearts.center_x = HEART_CENTRE_X
        self.hearts.center_y = HEART_CENTRE_Y

        # Sets up the background sprite
        img_src = f"{MAIN_FILE_PATH}Assets/Backgrounds/Background.png"
        self.bg = arcade.Sprite(img_src, BG_SIZE)
        self.bg.center_x = BG_CENTRE_X
        self.bg.center_y = BG_CENTRE_Y

        # This sets up the checkpoint list
        self.passed_checkpoints = []
        self.last_checkpoint = self.map[CHECKPOINT_LAYER][0]

        # Sets up enemies and adds them to the map
        for my_enemy in self.enemies_layer:
            # Gets enemy co-ordinates
            enemy_coordinates = self.tile_map.get_cartesian(
                my_enemy.shape[0], my_enemy.shape[1]
            )

            # Creates an enemy and sets up their co-ordinates
            enemy = Golem()
            enemy.center_x = math.floor(
                enemy_coordinates[0] * TILE_SIZE * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (enemy_coordinates[1] + 1) *
                (self.tile_map.tile_height * TILE_SIZE)
            )

            # Adds attributes to the enemy
            enemy.boundary_left = my_enemy.properties["boundary_left"]
            enemy.boundary_right = my_enemy.properties["boundary_right"]
            enemy.change_x = my_enemy.properties["change_x"]

            # Adds the enemy to the map as a sprite
            self.map.add_sprite(ENEMY_LAYER, enemy)

        # Sets up the powerups and adds them to the map
        for my_powerups in self.powerups_layer:
            # Gets the co-ordinates for the powerups
            powerup_coordinates = self.tile_map.get_cartesian(
                my_powerups.shape[0], my_powerups.shape[1]
            )
            powerup_type = my_powerups.properties["type"]

            # Creates the powerup depending on what type they are
            if powerup_type == "health":
                powerup = HealthPotion()
            elif powerup_type == "speed":
                powerup = SpeedPowerup()

            # Sets up enemy co-ordinates
            powerup.center_x = math.floor(
                powerup_coordinates[0] * TILE_SIZE * self.tile_map.tile_width
            )
            powerup.center_y = math.floor(
                (powerup_coordinates[1] + 1) *
                (self.tile_map.tile_height * TILE_SIZE)
            )

            # Powerup type
            powerup.type = my_powerups.properties["type"]

            # Adds powerup to map
            self.map.add_sprite(POWERUP_LAYER, powerup)

        # Sets up player sprite
        self.character = Character(self.map[MOVING_PLATFORMS_LAYER])
        self.character.center_x = self.last_checkpoint.center_x
        self.character.center_y = self.last_checkpoint.center_y
        self.character.type = self.character_num
        self.map.add_sprite(PLAYER_LAYER, self.character)
        self.character_health = HealthBar(self.character)

        # Sets the background colour to the background
        # of the map if there is one
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Sets up the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.character, gravity_constant=GRAVITY_CONSTANT,
                platforms=[self.map[MOVING_PLATFORMS_LAYER],
                self.map[ENEMY_LAYER]],
                ladders=self.map[LADDER_LAYER],
                walls=[self.map[PLATFORM_LAYER], self.map[HIDDEN_LAYER]]
                )

    def on_draw(self):
        """Draws the sprites, enemies, map, etc on the screen"""

        # This clears the screen before drawing
        self.clear()

        # Activates the background camera
        self.bg_cam.use()

        # Draws the background
        self.bg.draw()

        # Activates the main camera
        self.cam.use()

        # This draws out the map
        self.map.draw()

        # Draws enemy health bars
        for enemy in self.map[ENEMY_LAYER]:
            health_bar = HealthBar(enemy)
            health_bar.draw_health()

        # Draws the character health bar
        self.character_health.draw_health()

        # Activate the GUI camera before drawing GUI elements
        self.gui_cam.use()

        # Draws the hearts
        self.hearts.draw()

        # Draws the score
        score_text = f"Score: {self.player_score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )
        # Draws text which holds the number of knives left
        score_text = f"Knives: {self.character.knives_num}"
        arcade.draw_text(
            score_text,
            10,
            30,
            arcade.csscolor.WHITE,
            18,
        )
        # Draws the timer
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
            elif (self.physics_engine.can_jump() and
                    not self.jump_needs_reset):
                self.character.change_y = CHARACTER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jumping_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.character.change_y = -CHARACTER_MOVEMENT_SPEED

        # Processes character vertical speed
        # based on up/down key presses
        if self.physics_engine.is_on_ladder():

            if not self.up_pressed and not self.down_pressed:
                self.character.change_y = 0

            elif self.up_pressed and self.down_pressed:
                self.character.change_y = 0
        else:
            self.character.on_ladder = False

        # Adjusts character speed based on whether or not they have
        # a speed boost
        if self.speed_boost_equipped:
            speed = CHARACTER_MOVEMENT_SPEED * SPEED_BOOST_RATE
        else:
            speed = CHARACTER_MOVEMENT_SPEED

        # Left and right key processes
        if self.right_pressed and not self.left_pressed:
            self.character.change_x = speed
        elif self.left_pressed and not self.right_pressed:
            self.character.change_x = -speed
        else:
            self.character.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        # List of valid keys
        timer_start_keys = [arcade.key.W, arcade.key.A,
                            arcade.key.S, arcade.key.D,
                            arcade.key.UP, arcade.key.DOWN,
                            arcade.key.LEFT, arcade.key.RIGHT,
                            arcade.key.R, arcade.key.E]

        # Starts the timer when the player starts moving
        if self.timer_running is False and key in timer_start_keys:
            self.start_time = time.time()
            self.timer_running = True

        # Adjusts variables as needed when keys are pressed
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.E and self.character.type == NINJA_BOY:
            self.character.is_throwing = True
        elif key == arcade.key.R and self.character.type == NINJA_GIRL:
            self.character.is_attacking = True
        elif key == arcade.key.KEY_1 and self.character.type != NINJA_GIRL:
            self.character.type = NINJA_GIRL
        elif key == arcade.key.KEY_2 and self.character.type != NINJA_BOY:
            self.character.type = NINJA_BOY
        elif key == arcade.key.SPACE and self.num_of_speed_boosts > 0 \
                and self.speed_boost_equipped is False:
            self.speed_boost_equipped = True
            self.num_of_speed_boosts -= 1

        # Processes the keychange
        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        # Adjusts variables as needed when keys are released
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

        # Processes the keychange
        self.process_keychange()

    def center_camera_to_player(self):
        """Centres camera to sprite"""

        # Sets the co-ordinates for the camera
        screen_center_x = self.character.center_x - (
            self.cam.viewport_width / 2)
        screen_center_y = self.character.center_y - (
            self.cam.viewport_height / 2
        )

        # Makes sure the camera cannot go past the left edge of the map
        if screen_center_x < 0:
            screen_center_x = 0
        # Makes sure that the camera cannot go beneath the map
        if screen_center_y < 0:
            screen_center_y = 0

        # Sets co-ordinates of the camera
        player_centered = screen_center_x, screen_center_y
        self.cam.move_to(player_centered, CAMERA_SPEED)

    def on_update(self, delta_time):
        """This function updates info from the game regularly"""

        # Update animation and physics engine
        self.physics_engine.update()
        self.character.update_animation()
        self.hearts.update_animation()
        for powerup in self.map[POWERUP_LAYER]:
            powerup.update_animation()
        for enemy in self.map[ENEMY_LAYER]:
            enemy.update_animation()

        # Updates the timer
        if self.timer_running:
            self.total_time = round(time.time() - self.start_time, TIMER_DP)

        # Increments health if the user doesn't have max health
        if self.character.health < MAX_HEALTH:
            self.character.health += HEALTH_INC

        # This updates the info on whether a sprite can jump or not
        # and also whether they are on a ladder or not
        if self.physics_engine.can_jump():
            self.character.can_jump = False
        else:
            self.character.can_jump = True

        # Checks whether the character is on the top of a ladder or not
        # and updates the on_ladder variable accordingly
        if (self.physics_engine.is_on_ladder() and not
                self.physics_engine.can_jump()):
            self.character.on_ladder = True
            self.process_keychange()
        else:
            self.character.on_ladder = False
            self.process_keychange()

        # Updates the checkpoints the player has gone through
        for checkpoint in self.map[CHECKPOINT_LAYER]:
            if (arcade.check_for_collision(self.character, checkpoint) and
                    checkpoint not in self.passed_checkpoints):
                self.passed_checkpoints.append(checkpoint)
                self.last_checkpoint = checkpoint

        # Teleports character based on which teleport they touched
        for teleport in self.map.get_sprite_list(TELEPORT_LAYER):
            if arcade.check_for_collision(self.character, teleport):
                if teleport == self.map[TELEPORT_LAYER][0]:
                    # Teleports from first teleport to 2nd teleport
                    self.character.center_x = self.map[
                        TELEPORT_LAYER][1].center_x + TELEPORT_OFFSET_X
                    self.character.center_y = self.map[
                        TELEPORT_LAYER][1].center_y
                else:
                    # Teleports from 2nd teleport to first one
                    self.character.center_x = self.map[
                        TELEPORT_LAYER][0].center_x - TELEPORT_OFFSET_X
                    self.character.center_y = self.map[
                        TELEPORT_LAYER][0].center_y

        # Clears the hidden layer if all collectables have been
        # collected and the character touches the invisible layer
        if arcade.check_for_collision_with_list(
            self.character, self.map[FOREGROUND_LAYER]
            ) and len(self.map[GEM_LAYER]) == 0 and \
                len(self.map[COIN_LAYER]) == 0:
            self.map[HIDDEN_LAYER].clear()

        # If the player touches an untouchable
        # layer or falls off the map
        if arcade.check_for_collision_with_lists(
            self.character, [self.map[DEADLY_LAYER], self.map[ENEMY_LAYER]]
        ) or self.character.center_y < BOTTOM_MAP_LIMIT:
            if arcade.check_for_collision_with_list(
                    self.character, self.map[ENEMY_LAYER]):
                # Sets damage dealth to the damage dealth function
                # which outputs the damage dealt
                amt_damage_dealt = ENEMY_DMG
            else:
                # Sets damage dealt to max health so the character dies
                amt_damage_dealt = MAX_HEALTH

            # Deducts health from the character
            self.character.health -= amt_damage_dealt

            # If character dies
            if self.character.health <= 0:
                # Takes away one heart and updates animation
                self.hearts.lives -= 1
                self.hearts.update_animation()

                # If player runs out of lives
                if self.hearts.lives == 0:
                    # Plays game over sound and starts new game
                    arcade.play_sound(self.game_over_sound)
                    game_over_view = GameOver(
                        self, self.player_score, self.total_time)
                    self.window.show_view(game_over_view)
                else:
                    # Gives the character full health and spawns them
                    # at the last checkpoint they passed
                    self.character.health = MAX_HEALTH
                    last_checkpoint = self.last_checkpoint
                    self.character.center_x = last_checkpoint.center_x
                    self.character.center_y = last_checkpoint.center_y
                    self.character.direction = RIGHT_FACING

        # Removes gems and coins if they have been collected
        for layer in self.collectable_layers:
            for collectable in self.map.get_sprite_list(layer):
                # Removes collectables if the player hits them
                if arcade.check_for_collision(self.character, collectable):
                    if (layer == COIN_LAYER and
                            self.character.type == NINJA_GIRL or
                            layer == GEM_LAYER and
                            self.character.type == NINJA_BOY):
                        # Removes the collectable from
                        # the coin sprite list
                        collectable.remove_from_sprite_lists()
                        # Plays the sound when the coins are collected
                        arcade.play_sound(self.coin_collection_sound)
                        # Increments score
                        self.player_score += 1

        # Updates powerups
        for powerup in self.map.get_sprite_list(POWERUP_LAYER):

            # Checks for character picking up a powerup
            # Also increments the number of powerups
            # and removes the powerup they just collected
            if arcade.check_for_collision(self.character, powerup):
                if (powerup.type == "health" and
                        self.hearts.lives < MAX_HEARTS):
                    self.hearts.lives += 1
                    powerup.remove_from_sprite_lists()
                elif powerup.type == "speed":
                    self.num_of_speed_boosts += 1
                    powerup.remove_from_sprite_lists()
                elif powerup.type == "knife":
                    self.character.knives_num += KNIFE_INCREASE_AMT
                    powerup.remove_from_sprite_lists()

        # Creates a speed boost effect
        if self.speed_boost_equipped:

            # Creates a speed boost effect sprit
            # and adds it to the map
            img_src = f"{MAIN_FILE_PATH}Assets/Dash.png"
            dash_sprite = SpeedDash(img_src, self.character)
            dash_sprite.start_frame = self.boost_frames_since_reset
            self.map.add_sprite(DASH_LAYER, dash_sprite)

            # Removes dash layer sprites after 3 frames
            for sprite in self.map[DASH_LAYER]:
                if (self.boost_frames_since_reset ==
                        sprite.start_frame + DASH_UPDATE_FRAMES):
                    sprite.remove_from_sprite_lists()

            # Resets the number of frames and clears the layer
            if self.boost_frames_since_reset == SPEED_BOOST_FRAMES:
                self.map[DASH_LAYER].clear()
                self.speed_boost_equipped = False
                self.boost_frames_since_reset = -1

            # Increments the frames since the the speed boost started
            self.boost_frames_since_reset += 1

        # Runs if the player is able to throw a knife
        if self.can_throw:
            # Runs if the character is throwing a knife
            if self.character.is_throwing:
                # Runs if the character has more than 1 knife
                if self.character.knives_num > 0:
                    # Creates a knife and gives it attributes
                    img_src = f"{MAIN_FILE_PATH}Assets/Ninja/png/Kunai.png"
                    knife = KnivesAttack(img_src, KNIFE_SIZE, "Detailed",
                                         self.character.center_x -
                                         KNIFE_RANGE,
                                         self.character.center_x +
                                         KNIFE_RANGE)

                    # Sets the knife co-ordinates based on
                    # character direction and adds it to the map
                    if self.character.direction == RIGHT_FACING:
                        knife.left = self.character.right
                    else:
                        knife.right = self.character.left
                    knife.original_direction = \
                        self.character.direction
                    knife.center_y = self.character.center_y

                    # Adds knife to the map
                    self.map.add_sprite(KNIFE_LAYER, knife)

                    # Decreases the number of knives and makes
                    # it so the character cannot throw knives
                    self.character.knives_num -= 1
                    self.can_throw = False
                else:
                    self.character.is_throwing = False
        else:
            # Increaments the frames between knife throwing
            self.frames_between_shots += 1

            # If there has been enough of a break between throws
            # the character can throw knives again
            if self.frames_between_shots == KNIFE_THROW_RATE:
                self.can_throw = True
                self.frames_between_shots = 0

        # If there are knives
        if self.map[KNIFE_LAYER]:
            for knife in self.map[KNIFE_LAYER]:
                # Removes knives if they exceed the range
                if (knife.center_x > knife.right_boundary or
                        knife.center_x < knife.left_boundary):
                    knife.remove_from_sprite_lists()

                for enemy in self.map.get_sprite_list(ENEMY_LAYER):
                    # If an enemy is hit by a knife they recieve damage
                    if arcade.check_for_collision(knife, enemy):
                        knife.remove_from_sprite_lists()
                        enemy.health -= knife.damage()

                # Removes knives if they hit a wall
                if arcade.check_for_collision_with_list(
                        knife, self.map[PLATFORM_LAYER]):
                    knife.remove_from_sprite_lists()

                # Updates knife co-ordinates and angle
                if knife.original_direction == RIGHT_FACING:
                    speed = KNIFE_SPEED
                else:
                    speed = -KNIFE_SPEED
                knife.center_x += speed
                knife.angle += KNIFE_ROTATION_ANGLE

        # Updates enemies
        for enemy in self.map.get_sprite_list(ENEMY_LAYER):
            # Enemy gravity
            if not arcade.check_for_collision_with_list(
                    enemy, self.map[PLATFORM_LAYER]):
                enemy.center_y -= ENEMY_GRAVITY_CONSTANT

            # Checks for collision between weapon and enemy
            self.character.weapon.check_for_attack_collision(enemy)

            # Removes the enemy and adds a knife powerup in its place
            # when the enemy dies
            if enemy.health <= 0:
                # Creates a knife powerup and gives it attributes
                knife = arcade.Sprite(
                    f"{MAIN_FILE_PATH}Assets/Collectables/Kunai.png",
                    POWERUP_SIZE/2)
                knife.type = "knife"
                knife.center_x = enemy.center_x
                knife.center_y = enemy.center_y
                self.map.add_sprite(POWERUP_LAYER, knife)

                # Removes enemy from map
                enemy.remove_from_sprite_lists()

        # Moves the user onto the next level if they have
        # done everything to pass the level
        if arcade.check_for_collision_with_list(
            self.character, self.map[LEVEL_PASS_LAYER]
            ) and len(self.map[GEM_LAYER]) == 0 and \
                len(self.map[COIN_LAYER]) == 0 and \
                len(self.map[ENEMY_LAYER]) == 0:

            # Move onto next level
            level_inc = True

            # Sets window so we can use it later
            window = self.window

            # Creates total time variable so we can use it
            # in the level pass view
            current_total_time = self.total_time

            # Calls level passed view which carries onto next
            # level passing the game view as self
            pass_view = LevelPassed(
                self, self.player_score, current_total_time, level_inc)
            window.show_view(pass_view)

        # Centres the camera on the sprite
        self.center_camera_to_player()


def main():
    """Main function"""

    # This sets up and runs the game
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game_view = Instructions()
    window.show_view(game_view)
    arcade.run()


if __name__ == "__main__":
    main()

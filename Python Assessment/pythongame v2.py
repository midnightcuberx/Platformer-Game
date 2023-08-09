"""
Python game
"""

#If you pass a checkpoint the number of checkpints passsed will equal 0

# i SHould reset level if the character dies
# Imports the modules needed
import arcade
import random
import time
import math

# Main file path

MAIN_FILE_PATH = "C:/python projects/Python Assessment/"
#MAIN_FILE_PATH = "S:/Computing/Assessment/2022/Year 13/Subject 13DTP Class 2-1/dh19502/Python Assessment/"
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

# Constant used for determining the player speed
CHARACTER_MOVEMENT_SPEED = 7
GRAVITY_CONSTANT = 1
CHARACTER_JUMP_SPEED = 20

MAX_HEALTH = 3

# Constants used for sprite centering
CHARACTER_CENTRE_X = SPRITE_PIXEL_SIZE * TILE_SIZE * 2
CHARACTER_CENTRE_Y = SPRITE_PIXEL_SIZE * TILE_SIZE * 3.75
CHECKPOINTS = [[[CHARACTER_CENTRE_X,CHARACTER_CENTRE_Y],[1625, 300],[2500,430],[4320, 560]],"[[x,y],[x,y]],etc etc for checkpoint co-ordinates of levels"]
HEART_CENTRE_X = 80
HEART_CENTRE_Y = 615
BG_CENTRE_X = 500
BG_CENTRE_Y = 325

# Tracks which direction the player is facing
RIGHT_FACING = 0
LEFT_FACING = 1

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


def load_textures(filename):
    """
    Load a texture pair with the second being the mirror image of the first
    """
    return arcade.load_texture_pair(filename, hit_box_algorithm= "Detailed")

class Entity(arcade.Sprite):
    """Sprite class for entities which will be inherited"""

    def __init__(self,folder_name, file_name, no_of_frames: int, idle_img, walking_img = None,jumping_img = None, falling_img = None, climbing_img = None):
        # Inherits the parent class 
        super().__init__()

        self.alive = True
        # This sets the intial direction of the character to right
        self.character_direction = RIGHT_FACING

        # This is used in order to flip through the images in texture pairs
        self.current_texture = 0
        self.scale = CHARACTER_SIZE

        # --- Loading textures ---

        file_path = f"{MAIN_FILE_PATH}Assets/{folder_name}/{file_name}"
        # Loading texture pairs for when the character is idle, jumping, or falling
        self.idle_textures = load_textures(f"{file_path}{idle_img}.png")

        if jumping_img:        
            self.jumping_textures = load_textures(f"{file_path}{jumping_img}.png")
        
        if falling_img:
            self.falling_textures = load_textures(f"{file_path}{falling_img}.png")

        if walking_img:
            self.walking_textures = []

            # Loading the walking textures into a list of textures
            for i in range(no_of_frames):
                texture = load_textures(f"{file_path}{walking_img}{i}.png")
                self.walking_textures.append(texture)
        
        if climbing_img:
            # This loads the textures for climbing
            self.climbing_textures = []

            for i in range(no_of_frames):
                texture = arcade.load_texture(f"{file_path}{climbing_img}{i}.png", hit_box_algorithm= "Detailed")
                self.climbing_textures.append(texture)

        # This sets the first (intial) texture to facing to the right
        # This is because the chzracter starts on the left side of the map 
        # and therefore should be running right
        self.texture = self.idle_textures[0]

        # Sets the hit box (edge co-ordinates of image) to the
        # hit box points of the textured image
        #self.hit_box = self.texture.hit_box_points

class Character(Entity):
    """Player sprite class"""

    def __init__(self):
        
        # Inherits the parent class 
        super().__init__("Ninja/png", "", 10,"Idle__000", "Run__00","Jump__001", "Jump__009", "Climb_00")

        # These variables track the characters actions and what they are doing
        self.jumping = False
        self.climbing = False
        self.on_ladder = False

    def update_animation(self, delta_time: float = 1 / 60):

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
        if not self.on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.current_texture += 1
            if self.current_texture > 9:
                self.current_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.current_texture]
            return

        # This changes textures depending on if the character is jumping or falling
        if self.change_y > 0 and not self.on_ladder:
            self.texture = self.jumping_textures[self.character_direction]
            return
        elif self.change_y < 0 and not self.on_ladder:
            self.texture = self.falling_textures[self.character_direction]
            return

        
        # This sets the animation to the idle animation if the character is not moving
        if self.change_x == 0:
            self.texture = self.idle_textures[self.character_direction]
            return

        # This sets the animation to the walking animation, looping through the 
        # number of different walking textures there are
        self.current_texture += 1
        if self.current_texture > 9:
            self.current_texture = 0
        self.texture = self.walking_textures[self.current_texture][
            self.character_direction
        ]

class Enemy(Entity):
    def __init__(self,folder_name, file_name, no_of_frames: int, idle_img, walking_img = None,jumping_img = None, falling_img = None, climbing_img = None):

        # This will inherit the parent class of entity
        super().__init__(folder_name, file_name, no_of_frames, idle_img, walking_img, jumping_img, falling_img, climbing_img)

        self.should_update_walk = 0

    def update_animation(self, delta_time: float = 1 / 60):

        # This changes the direction that the sprite is facing depending
        # on which way it is moving
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # This runs if the enemy is not moving
        if self.change_x == 0:
            self.texture = self.idle_textures[self.facing_direction]
            return

        # Walking animation
        if self.should_update_walk == 3:
            self.current_texture += 1
            if self.current_texture > 7:
                self.current_texture = 0
            self.texture = self.walking_textures[self.current_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1


class RobotEnemy(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("images/animated_characters/robot", "robot", 7)


class ZombieEnemy(Enemy):
    def __init__(self):

        # Set up parent class
        super().__init__("images/animated_characters/zombie", "zombie", 7,"_idle")

class Hearts(arcade.Sprite):
    """Hearts Class"""

    def __init__(self):
        
        # Inherits the parent class, that is
        # The hearts class becomes a sprite in arcade
        super().__init__()

        # Number of lives initially
        self.lives = 3
        #Heart scaling
        self.scale = HEART_SIZE

        file_path = f"{MAIN_FILE_PATH}Assets/Kenney Platform Art/Base pack/HUD/hud_heart"

        self.hearts_list = []
        
        # This loads the possible health textures
        for i in range(4):
            texture = arcade.load_texture(f"{file_path}{i}.png")
            self.hearts_list.append(texture)

        # This sets the initial texture to 3 hearts
        self.texture = self.hearts_list[3]

    
    def update_animation(self, delta_time: float = 1 / 60):
        
        # Updates the texture to how many hearts the user has remaining
        self.texture = self.hearts_list[self.lives]
        return
    
class Game(arcade.Window):
    """
    Main class that runs the game
    """

    def __init__(self):

        # This inherits the parent class and sets up the platform
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        
        # Initializes the map
        self.map = None

        # Intializes the character sprite
        self.character = None

        # Intialize the heart sprite list
        self.heart_sprite_list = None
        self.hearts = None

        # Intilaises bg spritelist
        self.bg_sprite_list = None
        self.bg = None


        #Initializes the physics engine
        self.physics_engine = None

        # Sets up camera that will follow the player around
        self.cam = None

        # A Camera that can be used to draw GUI elements
        self.gui_cam = None

        # The background camera which will move the background around
        self.bg_cam = None

        # Sets the end of map to 0 (Will be changed later, this is only intializing)
        self.map_end = 0

        # The level
        self.level = 1

        # This code loads the sounds that we need later
        self.coin_collection_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jumping_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over_sound = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.game_bg_track = arcade.load_sound(f"{MAIN_FILE_PATH}Assets/Adorable_Little_Chiptune_Loop.mp3", streaming=True)


        # Sets the original score to 0
        self.player_score = 0

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False

        # Initialises the tile map
        self.tiled_map = None

        # Keeps track of whether the music is playing or not
        self.music_playing = False

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
        self.timer_running = False
        self.start_time = None
        self.total_time = 0.000

        # Plays the music if it is not already playing
        if not self.music_playing:
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
        }

        # Load the scene from Tiled
        self.tile_map = arcade.load_tilemap(map_name, TILE_SIZE, layer_options)

        # This creates the scene with the tilemap, and this will add all layers of the tilemap as sprtitelists
        # The 2nd line will add the player sprite as a layer before the foreground
        self.map = arcade.Scene.from_tilemap(self.tile_map)
        self.map.add_sprite_list_before(PLAYER_LAYER,FOREGROUND_LAYER)

        # This creates the spritelists for hearts and background
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
        
        #self.map.add_sprite_list("Walls", use_spatial_hash=True)
        #self.map.add_sprite_list("Coins",use_spatial_hash=True)

        # This sets up the player sprite and the co-ordinates where it will initially start from
        self.character = Character()
        self.character.center_x = CHARACTER_CENTRE_X
        self.character.center_y = CHARACTER_CENTRE_Y
        self.map.add_sprite(PLAYER_LAYER, self.character)
        
        # Determines the end of the map
        self.map_end = self.tile_map.width * GRID_PIXEL_SIZE

        # Enemy stuff imc,ented
        object_layer=self.tile_map._process_object_layer(self.map, self.map[ENEMY_LAYER])
        enemies_layer = self.tile_map.object_lists[ENEMY_LAYER]
        for my_object in enemies_layer:
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            enemy_type = my_object.properties["type"]
            if enemy_type == "robot":
                enemy = RobotEnemy()
            elif enemy_type == "zombie":
                enemy = ZombieEnemy()
            enemy.center_x = math.floor(
                cartesian[0] * TILE_SIZE * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SIZE)
            )
            if "boundary_left" in my_object.properties:
                enemy.boundary_left = my_object.properties["boundary_left"]
            if "boundary_right" in my_object.properties:
                enemy.boundary_right = my_object.properties["boundary_right"]
            if "change_x" in my_object.properties:
                enemy.change_x = my_object.properties["change_x"]
            self.scene.add_sprite(ENEMY_LAYER, enemy)



        # Sets the background colour to the mackground of the map if there is one
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
    
        # Sets up the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.character, gravity_constant=GRAVITY_CONSTANT, platforms = self.map[MOVING_PLATFORMS_LAYER],
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

        # This processes if the key changes between left and right
        # and changes the x ordinates of the character accordingly
        if self.right_pressed and not self.left_pressed:
            self.character.change_x = CHARACTER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.character.change_x = -CHARACTER_MOVEMENT_SPEED
        else:
            self.character.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        # Starts the timer when the player starts moving
        if self.timer_running is False:
            self.start_time = time.time()
            self.timer_running = True

        # This sets the keys pressed to true so when the keychange is processed the sprite will move
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        # This makes sure that the sprite stops moving in a specific direction every time a key is released
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

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

        # Moves the camera to the set co-ordinates
        self.cam.move_to(player_centered,0.2)

    def on_update(self, delta_time):
    
        """This function updates info from the game regularly"""
        #print(self.character.center_x,self.character.center_y)
        # This moves the player sprite and updates the positioning of the platforms
        self.physics_engine.update()

        # This updates the info on whether a sprite can jump or not
        # and also whether they are on a ladder or not
        if self.physics_engine.can_jump():
            self.character.can_jump = False
        else:
            self.character.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.character.is_on_ladder = True
            self.process_keychange()
        else:
            self.character.is_on_ladder = False
            self.process_keychange()

        # Update character and heart animations
        self.character.update_animation(delta_time)
        self.hearts.update_animation(delta_time)

        # Updates the timer
        if self.timer_running:
            self.total_time = round(time.time() - self.start_time,3)

        # This checks if there is a collision between the coin and player sprite
        coin_hit_list = arcade.check_for_collision_with_list(
            self.character, self.map["Coins"]
        )

        # If any coins are hit those coins are removed from the sprite list
        # and the score is increased
        if coin_hit_list:
            # Removes coins if the player hits them
            for coin in coin_hit_list:
                # Remove the coin from the coin sprite list
                coin.remove_from_sprite_lists()
                # Plays the sound when the coins are collected
                arcade.play_sound(self.coin_collection_sound)
                # Increments score
                self.player_score += 1

        # If the player touches a deadly object (spikes or lava)
        # then this will run and deduct health from the player.
        # If they end up with no health then the game will reset
        # If they do have health they will go back to the beginning but
        # their score will remain intact
        if arcade.check_for_collision_with_list(
            self.character, self.map[DEADLY_LAYER]
        ) or self.character.center_y < -100:
            if self.hearts.lives > 0:
                self.hearts.lives -= 1
                if self.hearts.lives == 0:
                    arcade.play_sound(self.game_over_sound)
                    self.setup()
                else:
                    self.character.center_x = CHARACTER_CENTRE_X
                    self.character.center_y = CHARACTER_CENTRE_Y
                    self.character.character_direction = RIGHT_FACING
                return
            else:
                pass
        
        # Moves the user onto the next level if they have touched the level pass object
        if arcade.check_for_collision_with_list(
            self.character, self.map[LEVEL_PASS_LAYER]
            ):

            print(self.total_time)

            # Moves onto next level
            #self.level += 1

            # Load the next level
            self.setup()


        # See if the user got to the end of the level
        if self.character.center_x >= self.map_end:
            # Advance to the next level
            self.level += 1

            # Load the next level
            self.setup()
        self.hearts.update_animation()
        # Centres the camera on the sprite
        self.center_camera_to_player()

def main():
    """Main function"""

    # This sets up and runs the game
    game_window = Game()
    game_window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

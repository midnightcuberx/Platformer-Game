"""
Platformer Game
"""
import arcade

# Constants that will be used later in the code for setting up the window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to set the size of the sprites in comparison to their original sizes
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
GEM_SCALING = 0.5

# Constant used for determining the player speed
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED =20

# COnstants used for sprite centering
PLAYER_CENTRE_X = 64
PLAYER_CENTRE_Y = 192


# Layer names for tilesets
LAYER_NAME_PLATFORMS = "Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_FOREGROUND = "Foreground"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_DONT_TOUCH = "Deadly Stuff"

class MyGame(arcade.Window):
    """
    Main class that runs the game
    """

    def __init__(self):

        # Calls the class of the inherited parent function
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE,False,True)

        self.scene = None

        # This variable holds the player sprite
        self.player_sprite = None

        # This is the physics engine
        self.physics_engine = None

        # This sets up the camera
        self.camera = None

        # Right edge of the map
        self.end_of_map = 0

        # The level
        self.level = 1

        # This code loads the sounds that we need later
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        # A Camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0

        # Initialises the tile set
        self.tile_map = None

        # Sets the background of the window to cornflower blue
        arcade.set_background_color(arcade.csscolor.SKY_BLUE)


    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # This initializes the scene
        self.scene = arcade.Scene()

        # Sets up the Camera
        self.camera = arcade.Camera(self.width, self.height)

        # Setup the GUI Camera
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_name = "level1.tmx"
        # This is a dictionary full of layers
        layer_options = {
            LAYER_NAME_PLATFORMS : {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS : {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DONT_TOUCH : {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.score = 0

        # Create the Sprite lists
        self.scene.add_sprite_list_before("Player",LAYER_NAME_FOREGROUND)
        
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins",use_spatial_hash=True)

        # This sets up the player sprite and the co-ordinates where it will initially start from
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = PLAYER_CENTRE_X
        self.player_sprite.center_y = PLAYER_CENTRE_Y
        self.scene.add_sprite("Player", self.player_sprite)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)
    
        self.physics_engine = arcade.PhysicsEnginePlatformer(
                self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"]
            )

    def on_draw(self):
        """Draws on the window and sets up the game by drawing all the objects"""

        # Clears the screen so that only the window and the original background colour is left
        self.clear()

        # Activates the camera so we can move
        self.camera.use()

        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        # This determines how the co-ordinates of the sprites move depending on which keys are pressed.
        if key == arcade.key.UP or key == arcade.key.W:
            #if self.physics_engine.can_jump():
            #self.physics_engine.enable_multi_jump(3)
            #self.physics_engine.increment_jump_counter()
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
            arcade.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        # This makes sure that the sprite stops moving in a specific direction every time a key is released
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        #print(screen_center_x,self.player_sprite.center_x)
        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Check for out-of-bounds
        if self.player_sprite.left < 0:
            self.player_sprite.left = 0
        #elif self.right > SCREEN_WIDTH - 1:
            #self.right = SCREEN_WIDTH - 1

        if self.player_sprite.bottom < 0:
            self.player_sprite.bottom = 0
        #elif self.top > SCREEN_HEIGHT - 1:
            #self.top = SCREEN_HEIGHT - 1

        # This moves the player sprite
        self.physics_engine.update()

        # This checks if there is a collision between the coin and player sprite
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )


        if coin_hit_list:
            # Removes coins if the player hits them
            for coin in coin_hit_list:
                # Remove the coin
                coin.remove_from_sprite_lists()
                # Play a sound
                arcade.play_sound(self.collect_coin_sound)

                self.score += 1

        # Centres the camera on the sprite
        self.center_camera_to_player()

def main():

    """Main function of the program"""
    #Calls the game function
    window = MyGame()
    #Sets up the game
    window.setup()
    #Runs the program
    arcade.run()

if __name__ == "__main__":
    # Calls the main function and runs the game
    main()
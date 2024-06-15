import arcade
import random
import math
from pyglet.math import Vec2


# --- Constants ---
SCREEN_TITLE = "Game"
WIDTH = 1600
HEIGHT = 900

SPRITE_SCALING = 0.5
SPRITE_SCALING_BULLET = 0.8
TILE_SCALING = 1.5
GRID_PIXEL_SIZE = 128

VIEWPORT_MARGIN = 220
CAMERA_SPEED = 0.1

BULLET_SPEED = 6


class MenuView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Menu Screen", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)

    #asdfasdlfj asdfasdf


class InstructionView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.color.ORANGE_PEEL)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Instructions Screen", WIDTH / 2, HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", WIDTH / 2, HEIGHT / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)

# class Enemy():
#     def __init__(self, health, xCoordinate, yCoordinate):
#         self.health = health
#         self.xCoordinate = xCoordinate
#         self.yCoordinate = yCoordinate

# for (3) 
#     Enemy(3, radomgenerate, randomgenerate)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        # Game Level
        self.level = 1
        
        # Frame count
        self.frame_count = 0
        
        # Sprite lists
        self.player_sprite = None
        self.player_list = None
        self.enemy_list = None
        self.player_bullet_list = None
        self.enemy_bullet_list = None

        # Map layers
        self.wall_list = None
        self.floor_list = None
        self.enemy_list = None
        self.gate_list = None
        self.chest_list = None

        # Player Attributes
        self.player_health = 0
        self.player_speed = 0
        self.player_ammo = 0
        
        # Enemy Attribute 
        self.enemy_health = 0

        # Load our map
        map_name = f"data\map\level{self.level}.tmj"
        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)

        # Create cameras
        self.camera_sprites= None
        self.camera_gui = None

        # Set up physics engine
        self.physics_engine = None

        
    def setup(self):
        """ Initialize variables """
        # Set background color
        arcade.set_background_color(arcade.color.AMAZON)
        
        # Frame count
        self.frame_count = 0
        
        # Load our map
        map_name = f"data\map\level{self.level}.tmj"
        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SCALING)        

        # Sprite lists
        self.player_sprite = arcade.AnimatedTimeBasedSprite()
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_bullet_list = arcade.SpriteList()
        self.enemy_bullet_list = arcade.SpriteList()

        # Map layers
        self.wall_list = self.tile_map.sprite_lists["Wall"]
        self.floor_list = self.tile_map.sprite_lists["Floor"]
        self.enemy_list = self.tile_map.sprite_lists["Enemy"]
        self.gate_list = self.tile_map.sprite_lists["Gate"]
        self.chest_list = self.tile_map.sprite_lists["Chest"]

        # Player Attributes
        self.player_health = 100
        self.player_speed = 2
        self.player_ammo = 30

        texture = arcade.load_texture("data\sprites\sprite.png", x = 0, y = 0, width = 32, height = 32)
        anim = arcade.AnimationKeyframe(1,10,texture)
        self.player_sprite.frames.append(anim)

        self.player_sprite.center_x = 4800
        self.player_sprite.center_y = 4800
        self.player_list.append(self.player_sprite)
        
        # Enemy Attribute
        self.enemy_health = 3
        
        # Don't show the mouse cursor
        self.window.set_mouse_visible(True)

        # Create cameras
        self.camera_sprites= arcade.Camera(WIDTH, HEIGHT)
        self.camera_gui = arcade.Camera(WIDTH, HEIGHT)

        # Set up physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)


    def on_show_view(self):
        """ run the game on show view """
        # set up the game
        self.setup()


    def on_draw(self):
        """ draw the game """ 
        self.clear()
        arcade.start_render()
        
        self.camera_sprites.use()
        
        self.floor_list.draw()
        self.wall_list.draw()
        self.gate_list.draw()
        self.chest_list.draw()
        self.player_list.draw()
        self.enemy_list.draw()
        self.player_bullet_list.draw()
        self.enemy_bullet_list.draw()

        self.camera_gui.use()
        
        text = f"Mobs left: {len(self.enemy_list)}"
        arcade.draw_text(text, 600, HEIGHT- 200, arcade.color.WHITE, 55)

        # coordinate = f"Y cord: {self.player_sprite.center_y}"
        # arcade.draw_text(coordinate, 600, HEIGHT- 400, arcade.color.WHITE, 55)

        #-------------------------- DRAW HEALTH BAR ------------------------------------
        arcade.draw_rectangle_filled(WIDTH // 2,
                                     0,
                                     WIDTH,
                                     200,
                                     arcade.color.WHITE)


        arcade.draw_lrtb_rectangle_outline(15,
                                           315,
                                           80,
                                           20,
                                           arcade.color.BLACK,
                                           5)       

        arcade.draw_lrtb_rectangle_filled(20,
                                          self.player_health*3.1,
                                          75,
                                          25,
                                          arcade.color.RED)      


    def scroll_to_player(self):
        """
        Scroll the window to the player.
        """
        
        position = Vec2(self.player_sprite.center_x - WIDTH / 2,
                        self.player_sprite.center_y - HEIGHT / 2)

        self.camera_sprites.move_to(position, CAMERA_SPEED)        
 

    def on_resize(self, width, height):
        """ Resize window
        Handle the user grabbing edge and resizing the window
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))


    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        # Create a bullet
        bullet = arcade.Sprite("data\sprites\gun_bullet.png", SPRITE_SCALING_BULLET)

        # Position the bullet at the player's current location
        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        # Get from the mouse the destination location for the bullet
        dest_x = x + self.camera_sprites.position[0]
        dest_y = y + self.camera_sprites.position[1]

        # Do math to calculate how to get the bullet to the destination.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        # Angle the bullet sprite
        bullet.angle = math.degrees(angle)

        # Calculate velocity for each vector
        bullet.change_x = math.cos(angle) * BULLET_SPEED
        bullet.change_y = math.sin(angle) * BULLET_SPEED
        
        # Check if player can attack
        if self.player_ammo > 0:
            self.player_bullet_list.append(bullet)
            self.player_ammo -= 1


    def on_key_press(self, key, modifiers):
        """ Check to see which key is being pressed """
      
        if key == arcade.key.W:
            self.player_sprite.change_y = self.player_speed    
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprites\sprite.png", x = i * 32, y = 32, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i,100, texture)
                self.player_sprite.frames.append(anim)               
        elif key == arcade.key.S:
            self.player_sprite.change_y = -self.player_speed
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprites\sprite.png", x = i * 32, y = 0, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i,100, texture)
                self.player_sprite.frames.append(anim)                
        elif key == arcade.key.D:
            self.player_sprite.change_x = self.player_speed
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprites\sprite.png", x = i * 32, y = 96, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i,100, texture)
                self.player_sprite.frames.append(anim)
        elif key == arcade.key.A:
            self.player_sprite.change_x = -self.player_speed
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprites\sprite.png", x = i * 32, y = 64, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i,100, texture)
                self.player_sprite.frames.append(anim)
                
        elif key == arcade.key.R:
            self.player_ammo = 30        


    def on_key_release(self, key, modifiers):
        """ Check to see which key is being pressed and move the player in the 
        appropriate direction """
        
        if key == arcade.key.W:
            self.player_sprite.change_y = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprites\sprite.png", x = 0, y = 32, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i,10, texture)
                self.player_sprite.frames.append(anim)  
        elif key == arcade.key.S:
            self.player_sprite.change_y = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprites\sprite.png", x = 0, y = 0, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i,10, texture)
                self.player_sprite.frames.append(anim)
        elif key == arcade.key.D:
            self.player_sprite.change_x = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprites\sprite.png", x = 0, y = 96, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i, 10, texture)
                self.player_sprite.frames.append(anim)
        elif key == arcade.key.A:
            self.player_sprite.change_x = 0
            self.player_sprite.frames.clear()
            for i in range(4):
                texture = arcade.load_texture("data\sprites\sprite.png", x = 0, y = 64, width = 32, height = 32)
                anim = arcade.AnimationKeyframe(i,10, texture)
                self.player_sprite.frames.append(anim)


    def update(self, delta_time):
        """ Movement and game logic """
        
        # Frame Count
        self.frame_count += 1

        # Update physics engine
        self.physics_engine.update()

        # Call update on all sprites
        self.player_list.update()
        self.enemy_list.update()
        self.player_list.update_animation()
        self.enemy_list.update()
        self.player_bullet_list.update()
        self.enemy_bullet_list.update()
        
        # Enemy AI
        for enemy in self.enemy_list:

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y
            
            # Get the destination location for the bullet
            dest_x = self.player_sprite.center_x
            dest_y = self.player_sprite.center_y
            
            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            if math.hypot(x_diff, y_diff) < 500:
                # Shoot every 60 frames change of shooting each frame
                if self.frame_count % 60 == 0:
                    enemy_bullet = arcade.Sprite("data\sprites\gun_bullet.png", SPRITE_SCALING_BULLET)
                    enemy_bullet.center_x = start_x
                    enemy_bullet.center_y = start_y
                
                    # Angle the bullet sprite
                    enemy_bullet.angle = math.degrees(angle)
                
                    # Taking into account the angle, calculate our change_x
                    # and change_y. Velocity is how fast the bullet travels.
                    enemy_bullet.change_x = math.cos(angle) * BULLET_SPEED
                    enemy_bullet.change_y = math.sin(angle) * BULLET_SPEED
                
                    self.enemy_bullet_list.append(enemy_bullet)
            



        
        # Manage collisions here----------------------------------
        
        # Enemy bullet collision
        player_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_bullet_list)
            
        for collision in player_hit_list:
            self.player_health -= 10
            collision.kill()
        
        for enemy in self.enemy_list:
            enemy_hit_list = arcade.check_for_collision_with_list(enemy, self.player_bullet_list)
            
            for bullet in enemy_hit_list:
                bullet.kill()
                self.enemy_health -= 1
                if self.enemy_health <= 0:
                    enemy.kill()
                
            

        # Gate Collision
        if arcade.check_for_collision_with_list(self.player_sprite, self.gate_list):

            self.level += 1
            
            self.setup()
            
        
            
        # Check if player is dead
        if self.player_health <= 0:
            game_over_view = GameOverView()
            self.window.show_view(game_over_view)
        

            

        self.scroll_to_player()


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        """
        Draw "Game over" across the screen.
        """
        arcade.draw_text("Game Over", WIDTH//2, HEIGHT/2, arcade.color.WHITE, 54)
        arcade.draw_text("Click to restart", 310, 300, arcade.color.WHITE, 24)


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


def main():
    window = arcade.Window(WIDTH, HEIGHT, "Different Views Example")
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
import pygame as pg
import numpy as np
import taichi as ti

# settings
res = width, height = 800, 450  # Resolution for the screen. Can increase to '1600, 900' for higher quality if using CUDA.
offset = np.array([1.3 * width, height]) // 2  # Offsets the center of the fractal rendering
# texture
texture = pg.image.load('img/texture.jpg')  # Load texture for the fractal visualization
texture_size = min(texture.get_size()) - 1  # Get the minimum size of the texture for mapping
texture_array = pg.surfarray.array3d(texture).astype(dtype=np.uint32)  # Convert texture to numpy array for processing

# Define the Fractal class using Taichi for GPU/CPU acceleration
@ti.data_oriented
class Fractal:
    def __init__(self, app):
        self.app = app  # Store reference to the application
        self.screen_array = np.full((width, height, 3), [0, 0, 0], dtype=np.uint32)  # Initialize screen array (3 channels)
        # Initialize Taichi with CPU backend for rendering (can change to CUDA, OpenGL, etc.)
        ti.init(arch=ti.cpu)
        # Define Taichi fields for screen and texture
        self.screen_field = ti.Vector.field(3, ti.uint32, (width, height))  # Screen field for storing pixel data
        self.texture_field = ti.Vector.field(3, ti.uint32, texture.get_size())  # Texture field for fractal coloring
        self.texture_field.from_numpy(texture_array)  # Load texture data into Taichi field
        # Control parameters for fractal movement, zoom, etc.
        self.vel = 0.01  # Speed of movement
        self.zoom, self.scale = 2.2 / height, 0.993  # Zoom and scale factors
        self.increment = ti.Vector([0.0, 0.0])  # Track movement increment (offset in x and y)
        self.max_iter, self.max_iter_limit = 30, 5500  # Maximum iterations for fractal rendering
        # Time control for the application speed
        self.app_speed = 1 / 4000
        self.prev_time = pg.time.get_ticks()  # Track the previous time for delta time calculation

    # Function to calculate delta time for smooth animations
    def delta_time(self):
        time_now = pg.time.get_ticks() - self.prev_time  # Get current time and subtract previous time
        self.prev_time = time_now  # Update the previous time
        return time_now * self.app_speed  # Return the adjusted delta time

    # Render fractal on screen using Taichi kernel
    @ti.kernel
    def render(self, max_iter: ti.int32, zoom: ti.float32, dx: ti.float32, dy: ti.float32):
        for x, y in self.screen_field:  # Parallelize the loop across all pixels
            c = ti.Vector([(x - offset[0]) * zoom - dx, (y - offset[1]) * zoom - dy])  # Map pixel position to complex plane
            z = ti.Vector([0.0, 0.0])  # Initialize z value for Mandelbrot
            num_iter = 0  # Initialize iteration counter
            # Perform iterations to calculate the fractal
            for i in range(max_iter):
                z = ti.Vector([(z.x ** 2 - z.y ** 2 + c.x), (2 * z.x * z.y + c.y)])
                if z.dot(z) > 4:  # Escape condition (Mandelbrot check)
                    break
                num_iter += 1
            # Map the iteration count to a texture color
            col = int(texture_size * num_iter / max_iter)
            self.screen_field[x, y] = self.texture_field[col, col]  # Assign pixel color based on iteration count

    # Handle user input for controlling fractal movement and zoom
    def control(self):
        pressed_key = pg.key.get_pressed()  # Get all pressed keys
        dt = self.delta_time()  # Get delta time for smooth control
        # Movement control (left/right/up/down)
        if pressed_key[pg.K_a]:
            self.increment[0] += self.vel * dt
        if pressed_key[pg.K_d]:
            self.increment[0] -= self.vel * dt
        if pressed_key[pg.K_w]:
            self.increment[1] += self.vel * dt
        if pressed_key[pg.K_s]:
            self.increment[1] -= self.vel * dt

        # Zoom control (up/down to zoom in/out)
        if pressed_key[pg.K_UP] or pressed_key[pg.K_DOWN]:
            inv_scale = 2 - self.scale  # Inverse scale for zoom-out effect
            if pressed_key[pg.K_UP]:
                self.zoom *= self.scale
                self.vel *= self.scale
            if pressed_key[pg.K_DOWN]:
                self.zoom *= inv_scale
                self.vel *= inv_scale

        # Adjust the number of iterations for rendering resolution (left/right to decrease/increase)
        if pressed_key[pg.K_LEFT]:
            self.max_iter -= 1
        if pressed_key[pg.K_RIGHT]:
            self.max_iter += 1
        self.max_iter = min(max(self.max_iter, 2), self.max_iter_limit)  # Clamp iteration count within limits

    # Update the fractal based on user input and render settings
    def update(self):
        self.control()  # Process user input
        self.render(self.max_iter, self.zoom, self.increment[0], self.increment[1])  # Render fractal
        self.screen_array = self.screen_field.to_numpy()  # Convert Taichi field to numpy array for display

    # Draw the fractal on the screen using Pygame
    def draw(self):
        pg.surfarray.blit_array(self.app.screen, self.screen_array)  # Display the updated fractal image

    # Run the fractal rendering and drawing processes
    def run(self):
        self.update()
        self.draw()


# Application class to handle Pygame initialization and main loop
class App:
    def __init__(self):
        self.screen = pg.display.set_mode(res, pg.SCALED)  # Initialize Pygame screen with the specified resolution
        self.clock = pg.time.Clock()  # Create a clock for FPS control
        self.fractal = Fractal(self)  # Create an instance of the Fractal class

    # Main application loop
    def run(self):
        while True:
            self.screen.fill('black')  # Clear screen by filling it with black
            self.fractal.run()  # Run the fractal rendering and drawing
            pg.display.flip()  # Update the display with the new frame

            # Handle events (quit application on window close)
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            self.clock.tick()  # Control the frame rate (FPS)
            pg.display.set_caption(f'FPS: {self.clock.get_fps() :.2f}')  # Display the current FPS in the window caption

# Main execution block
if __name__ == '__main__':
    app = App()  # Create an instance of the App class
    app.run()  # Run the application
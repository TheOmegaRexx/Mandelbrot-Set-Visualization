# Fractal Renderer with Taichi and Pygame

This project implements a real-time fractal renderer using the Mandelbrot set, utilizing **Taichi** for efficient parallel computing and **Pygame** for graphics rendering. The program generates a fractal that users can zoom into and explore, with adjustable settings for resolution, zoom, and rendering iterations.

![Demo Screenshot](./img/demo.png)

## Features

- **Fractal Visualization**: Renders a dynamic Mandelbrot fractal using a texture-based approach.
- **Real-time Control**: Allows users to move, zoom, and change the fractal's resolution interactively using keyboard inputs.
- **GPU Acceleration**: Uses **Taichi** to perform fractal calculations in parallel, allowing faster rendering on both CPU and GPU.
- **Pygame Interface**: Displays the fractal and provides real-time interactivity with Pygame.

## Prerequisites

Ensure you have the following installed:

- Python 3.x
- Pygame: For handling the display and user input.
- Taichi: For GPU-accelerated parallel computations.

You can install the required libraries using `pip`:

```bash
pip install pygame taichi numpy
```

## How It Works

- **Fractal Calculation**: The fractal is calculated using the Mandelbrot formula, where each pixel is iterated a set number of times to determine if it belongs to the Mandelbrot set.
- **Parallelization**: Taichi is used to parallelize the fractal calculation across all pixels, utilizing either the CPU or GPU.
- **Texture Mapping**: A texture image is used to colorize the fractal, with the number of iterations determining the color for each pixel.
- **User Interaction**: The user can control the view of the fractal using the keyboard, adjusting the zoom, position, and iteration depth in real-time.

## Controls

### Arrow Keys:
- **Up/Down**: Zoom in and out of the fractal.
- **Left/Right**: Increase or decrease the number of iterations for rendering.

### WASD Keys:
- **W**: Move the fractal up.
- **A**: Move the fractal left.
- **S**: Move the fractal down.
- **D**: Move the fractal right.
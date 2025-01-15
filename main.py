import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Constants
G = 6.67430e-11  # Gravitational constant

# Classes for objects


class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.force = np.zeros(2)

    def update_force(self, bodies):
        self.force = np.zeros(2)
        for body in bodies:
            if body != self:
                r_vec = body.position - self.position
                r_mag = np.linalg.norm(r_vec)
                if r_mag > 0:
                    force_mag = (G * self.mass * body.mass) / (r_mag ** 3)
                    self.force += force_mag * r_vec

    def update_position(self, dt):
        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt


# Simulation setup
bodies = [
    Body(1.989e30, [0, 0], [0, 0]),  # Sun
    Body(5.972e24, [1.496e11, 0], [0, 29.78e3]),  # Earth
    Body(7.348e22, [1.496e11 + 384.4e6, 0], [0, 29.78e3 + 1.022e3])  # Moon
]

# Parameters
dt = 3600  # Time step (1 hour)
simulation_time = 365 * 24 * 3600  # 1 year
frames = int(simulation_time / dt)

# Visualization setup using Matplotlib
fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')
ax.set_xlim(-2e11, 2e11)
ax.set_ylim(-2e11, 2e11)

# Create plot objects for each body
sun, = ax.plot([], [], 'yo', markersize=10)  # Sun (yellow)
earth, = ax.plot([], [], 'bo', markersize=5)  # Earth (blue)
moon, = ax.plot([], [], 'go', markersize=3)  # Moon (green)

# Function to update plot


def update_plot(frame):
    # Update forces and positions for all bodies
    for body in bodies:
        body.update_force(bodies)
    for body in bodies:
        body.update_position(dt)

    # Extract positions for visualization
    sun.set_data([bodies[0].position[0]], [bodies[0].position[1]])
    earth.set_data([bodies[1].position[0]], [bodies[1].position[1]])
    moon.set_data([bodies[2].position[0]], [bodies[2].position[1]])

    return sun, earth, moon


# Create animation
ani = animation.FuncAnimation(
    fig, update_plot, frames=100, interval=50, repeat=False)

# Set up the Tkinter window
root = tk.Tk()
root.title("Gravity Simulation")

# Embed the figure into the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Run the Tkinter event loop
canvas.draw()
ani.event_source.start()
root.mainloop()

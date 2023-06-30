import tkinter as tk
from PIL import Image, ImageTk
import math


def fire_projectile():
    canvas.delete('projectile')
    x =0
    y = earth_radius + mountain_height
    vx = speed_slider.get() * math.cos(math.radians(angle_slider.get()))
    vy = speed_slider.get() * math.sin(math.radians(angle_slider.get()))
    move_projectile(x, y, vx, vy)

def move_projectile(x, y, vx, vy):
    r = math.sqrt(x ** 2 + y ** 2)
    # dopoki nie dotknie ziemi
    if r > earth_radius:
        accel = newton_g * earth_mass / (r ** 2)
        ax = - accel * x / r
        ay = - accel * y / r
        vx += ax * dt
        vy += ay * dt
        lastx = x
        x += vx * dt
        y += vy * dt
        draw_projectile(x, y)
        # dopoki nie wróci do miejsca
        if not ((lastx < 0) and (x > 0)):
            if not(x > 2 * earth_radius):
                canvas.after(1000 // 120, move_projectile, x, y, vx, vy)
            else:
                print("wylecialo")

def draw_projectile(x, y):
    pixel_x = canvas_width / 2 + x / meters_per_pixel
    pixel_y = canvas_height / 2 - y / meters_per_pixel
    canvas.create_oval(pixel_x-2, pixel_y-2, pixel_x+2, pixel_y+2, fill="black", tags="projectile")

root = tk.Tk()
root.title("Newton's Cannon")

canvas_width = 500
canvas_height = 500
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="lightgray")
canvas.pack()


def resizable_callback():
    root.resizable(False, False)

# ustawienie wygladu Gui oraz pozycja przycikow
image_path = "NewtonDrawing.png"
resizable_callback()
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

speed_slider = tk.Scale(root, from_=3000, to=11200, resolution=50, orient=tk.HORIZONTAL, label="Initial speed:")
speed_slider.set(3000)
speed_slider.pack()

angle_slider = tk.Scale(root, from_=0, to=90, resolution=1, orient=tk.HORIZONTAL, label="Initial angle:")
angle_slider.set(45)
angle_slider.pack()

fire_button = tk.Button(root, text="Fire!", command=fire_projectile)
fire_button.pack()

clear_button = tk.Button(root, text="Clear", command=lambda: canvas.delete("projectile"))
clear_button.pack()

# stale rzeczywiste dla ziemi
newton_g = 6.67e-11
earth_mass = 5.97e24
earth_radius = 6371000
meters_per_pixel = earth_radius * 2 / (0.71 * canvas_width)
mountain_height = earth_radius * 0.165
dt = 5

root.mainloop()

import tkinter as tk
import time
import math

# Crear la ventana principal
root = tk.Tk()
root.title("Reloj Analógico")

# Dimensiones del lienzo
width = 400
height = 400
center_x = width // 2
center_y = height // 2
clock_radius = 180

# Crear el lienzo
canvas = tk.Canvas(root, width=width, height=height, bg="white")
canvas.pack()

# Dibujar el círculo del reloj
canvas.create_oval(center_x - clock_radius, center_y - clock_radius,
                   center_x + clock_radius, center_y + clock_radius, outline="black", width=4)

# Dibujar los números del reloj (1 al 12)
for i in range(1, 13):
    angle = math.radians(i * 30)
    x_text = center_x + clock_radius * 0.8 * math.sin(angle)
    y_text = center_y - clock_radius * 0.8 * math.cos(angle)
    canvas.create_text(x_text, y_text, text=str(i), fill="black", font=("Arial", 16, "bold"))

# Crear manecillas
hour_hand = canvas.create_line(center_x, center_y, center_x, center_y - 50, width=6, fill='black')
minute_hand = canvas.create_line(center_x, center_y, center_x, center_y - 70, width=4, fill='blue')
second_hand = canvas.create_line(center_x, center_y, center_x, center_y - 90, width=2, fill='red')

# Función para actualizar las manecillas
def update_clock():
    t = time.localtime()
    seconds = t.tm_sec
    minutes = t.tm_min
    hours = t.tm_hour % 12 + minutes / 60.0

    sec_angle = math.radians(seconds * 6)
    min_angle = math.radians(minutes * 6)
    hour_angle = math.radians(hours * 30)

    def calc_coords(length, angle):
        x = center_x + length * math.sin(angle)
        y = center_y - length * math.cos(angle)
        return (x, y)

    xh, yh = calc_coords(60, hour_angle)
    xm, ym = calc_coords(90, min_angle)
    xs, ys = calc_coords(120, sec_angle)

    canvas.coords(hour_hand, center_x, center_y, xh, yh)
    canvas.coords(minute_hand, center_x, center_y, xm, ym)
    canvas.coords(second_hand, center_x, center_y, xs, ys)

    root.after(1000, update_clock)

# Iniciar el reloj
update_clock()

# Ejecutar el bucle principal
root.mainloop()
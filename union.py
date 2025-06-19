import tkinter as tk
from tkinter import ttk
from time import strftime, time
from pygame import mixer
import math
import time as tm


class AdvancedClock:
    def __init__(self, master):
        self.master = master
        master.title('Advanced Clock')
        master.geometry('500x500')
        master.resizable(False, False)

        mixer.init()

        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background='#003366', borderwidth=0, padding=[5, 5, 5, 0])
        style.configure('TNotebook.Tab', background='#003366', foreground='white',
                        padding=[40, 15], font=('Helvetica', 12, 'bold'),
                        relief='flat', borderwidth=0)
        style.map('TNotebook.Tab',
                  background=[('selected', '#FFD700'), ('active', '#004488')],
                  foreground=[('selected', 'black')])

        style.layout("TNotebook.Tab",
                     [("TNotebook.tab", {"sticky": "nswe", "children":
                                         [("TNotebook.padding", {"sticky": "nswe", "children":
                                                                 [("TNotebook.label", {"sticky": ""})]
                                                                 })]
                                          })])

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)

        self.clock_frame = tk.Frame(self.notebook, bg='#003366')
        self.notebook.add(self.clock_frame, text='Reloj')

        self.alarm_frame = tk.Frame(self.notebook, bg='#003366')
        self.notebook.add(self.alarm_frame, text='Alarma')

        self.stopwatch_frame = tk.Frame(self.notebook, bg='#003366')
        self.notebook.add(self.stopwatch_frame, text='Cronómetro')

        self._setup_analog_clock()
        self._setup_stopwatch()
        self._setup_alarm()

    # --- RELOJ ANALÓGICO ---
    def _setup_analog_clock(self):
        width, height = 350, 350
        center_x, center_y = width // 2, height // 2
        clock_radius = 150

        self.canvas = tk.Canvas(self.clock_frame, width=width, height=height, bg='#89CFF0')
        self.canvas.pack()

        # Dibujar círculo del reloj
        self.canvas.create_oval(center_x - clock_radius, center_y - clock_radius,
                                center_x + clock_radius, center_y + clock_radius,
                                outline='black', width=4)

        # Dibujar números del reloj
        for i in range(1, 13):
            angle = math.radians(i * 30)
            x = center_x + clock_radius * 0.8 * math.sin(angle)
            y = center_y - clock_radius * 0.8 * math.cos(angle)
            self.canvas.create_text(x, y, text=str(i), fill='black', font=('Arial', 16, 'bold'))

        # Crear manecillas
        self.hour_hand = self.canvas.create_line(center_x, center_y, center_x, center_y - 60,
                                                 width=6, fill='black')
        self.minute_hand = self.canvas.create_line(center_x, center_y, center_x, center_y - 90,
                                                   width=4, fill='blue')
        self.second_hand = self.canvas.create_line(center_x, center_y, center_x, center_y - 120,
                                                   width=2, fill='red')

        def update_clock():
            t = tm.localtime()
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

            self.canvas.coords(self.hour_hand, center_x, center_y, xh, yh)
            self.canvas.coords(self.minute_hand, center_x, center_y, xm, ym)
            self.canvas.coords(self.second_hand, center_x, center_y, xs, ys)

            self.master.after(1000, update_clock)

        update_clock()

    # --- CRONÓMETRO ---
    def _setup_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_start_time = 0
        self.stopwatch_elapsed_time = 0
        self.stopwatch_job = None

        self.stopwatch_display = tk.Label(self.stopwatch_frame,
                                          text="00:00:00.00",
                                          font=('Helvetica', 40, 'bold'),
                                          bg='#003366', fg='white')
        self.stopwatch_display.pack(pady=40)

        button_frame = tk.Frame(self.stopwatch_frame, bg='#003366')
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Iniciar", font=('Helvetica', 12),
                                      command=self._start_stopwatch,
                                      bg='#FFD700', fg='black', width=10)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(button_frame, text="Parar", font=('Helvetica', 12),
                                     command=self._stop_stopwatch,
                                     bg='#FFD700', fg='black', width=10, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.reset_button = tk.Button(button_frame, text="Reiniciar", font=('Helvetica', 12),
                                      command=self._reset_stopwatch,
                                      bg='#FFD700', fg='black', width=10, state=tk.DISABLED)
        self.reset_button.grid(row=0, column=2, padx=5)

    def _start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.stopwatch_start_time = time() - self.stopwatch_elapsed_time
            self._update_stopwatch_display()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)

    def _stop_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_running = False
            if self.stopwatch_job:
                self.master.after_cancel(self.stopwatch_job)
                self.stopwatch_job = None
            self.stopwatch_elapsed_time = time() - self.stopwatch_start_time
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def _reset_stopwatch(self):
        self._stop_stopwatch()
        self.stopwatch_elapsed_time = 0
        self.stopwatch_display.config(text="00:00:00.00")
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)

    def _update_stopwatch_display(self):
        if self.stopwatch_running:
            current_time = time() - self.stopwatch_start_time
            hours = int(current_time // 3600)
            minutes = int((current_time % 3600) // 60)
            seconds = int(current_time % 60)
            milliseconds = int((current_time * 100) % 100)
            formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:02d}"
            self.stopwatch_display.config(text=formatted_time)
            self.stopwatch_job = self.master.after(10, self._update_stopwatch_display)

    # --- ALARMA ---
    def _setup_alarm(self):
        self.alarma_activa = False
        self.alarma_sonando = False

        self.horas = [f"{i:02d}" for i in range(24)]
        self.minutos = [f"{i:02d}" for i in range(60)]

        self.clock_display = tk.Label(self.alarm_frame, font=('Helvetica', 40), fg='white',
                                      bg='#003366')
        self.clock_display.pack(pady=20)

        self._update_clock()

        form = tk.Frame(self.alarm_frame, bg='#003366')
        form.pack()

        tk.Label(form, text='Hora:', bg='#003366', fg='white', font=('Arial', 12)).grid(row=0, column=0, padx=5)
        self.cmb_hora = ttk.Combobox(form, values=self.horas, width=5, justify='center')
        self.cmb_hora.grid(row=1, column=0, padx=5)
        self.cmb_hora.set("00")

        tk.Label(form, text='Minuto:', bg='#003366', fg='white', font=('Arial', 12)).grid(row=0, column=1, padx=5)
        self.cmb_minuto = ttk.Combobox(form, values=self.minutos, width=5, justify='center')
        self.cmb_minuto.grid(row=1, column=1, padx=5)
        self.cmb_minuto.set("00")

        self.boton_alarma = tk.Button(self.alarm_frame, text="Activar / Desactivar Alarma",
                                      command=self.toggle_alarma, bg='#FFD700', fg='black')
        self.boton_alarma.pack(pady=10)

        self.alarma_label = tk.Label(self.alarm_frame, text="Alarma: Desactivada",
                                     fg='red', bg='#003366', font=('Arial', 14))
        self.alarma_label.pack(pady=10)

        self.boton_detener = tk.Button(self.alarm_frame, text="Detener Alarma",
                                       command=self.detener_alarma, bg='tomato', fg='white')
        self.boton_detener.pack(pady=5)
        self.boton_detener.pack_forget()

    def _update_clock(self):
        hora_actual = strftime('%H:%M:%S')
        self.clock_display.config(text=hora_actual)

        if self.alarma_activa and not self.alarma_sonando:
            hora_alarma = f"{self.cmb_hora.get()}:{self.cmb_minuto.get()}:{'00'}"
            if hora_actual[:5] == hora_alarma[:5]:
                self.reproducir_alarma()

        self.clock_display.after(1000, self._update_clock)

    def toggle_alarma(self):
        if not self.alarma_activa:
            self.alarma_activa = True
            self.alarma_label.config(text=f"Alarma: {self.cmb_hora.get()}:{self.cmb_minuto.get()}",
                                     fg='lime')
        else:
            self.alarma_activa = False
            self.alarma_label.config(text="Alarma: Desactivada", fg='red')

    def reproducir_alarma(self):
        if not self.alarma_sonando:
            try:
                mixer.music.load("Alarma_audio.mp3")
                mixer.music.play(loops=3)
                self.alarma_sonando = True
                self.boton_detener.pack(pady=5)
            except Exception as e:
                print("Error al reproducir alarma:", e)

    def detener_alarma(self):
        if self.alarma_sonando:
            mixer.music.stop()
            self.alarma_sonando = False
            self.alarma_activa = False
            self.alarma_label.config(text="Alarma: Desactivada", fg='red')
            self.boton_detener.pack_forget()


if __name__ == '__main__':
    root = tk.Tk()
    app = AdvancedClock(root)
    root.mainloop()
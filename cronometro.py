import tkinter as tk
import tkinter.ttk as ttk
import time

class AdvancedClock:
    def __init__(self, master):
        self.master = master
        master.title('Advanced Clock')
        master.geometry('450x400')
        master.resizable(False, False)

        style = ttk.Style()
        style.theme_use('default') 
        
        # Estilos del notebook y pestañas
        style.configure('TNotebook', background='#003366', borderwidth=0, padding=[5, 5, 5, 0])
        style.configure('TNotebook.Tab', background='#003366', foreground='white',
                        padding=[40, 15], font=('Helvetica', 12, 'bold'),
                        relief='flat', borderwidth=0, bordercolor='#003366', focuscolor='#003366')
        style.map('TNotebook.Tab',
                  background=[('selected', '#FFD700'), ('active', '#004488')],
                  foreground=[('selected', 'black')],
                  bordercolor=[('selected', '#FFD700')])
        
        # Codigo importante para eliminar propiedades default de la plantilla.
        style.layout("TNotebook.Tab",
                     [("TNotebook.tab", {"sticky": "nswe", "children":
                                         [("TNotebook.padding", {"sticky": "nswe", "children":
                                                                 [("TNotebook.label", {"sticky": ""})]
                                                                })]
                                        })])

        # Crear pestañas
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)

        self.clock_frame = tk.Frame(self.notebook, bg='#003366')
        self.notebook.add(self.clock_frame, text='Reloj')

        self.alarm_frame = tk.Frame(self.notebook, bg='#003366')
        self.notebook.add(self.alarm_frame, text='Alarma')

        self.stopwatch_frame = tk.Frame(self.notebook, bg='#003366')
        self.notebook.add(self.stopwatch_frame, text='Cronómetro')

        # Variables del cronómetro
        self.stopwatch_running = False
        self.stopwatch_start_time = 0
        self.stopwatch_elapsed_time = 0
        self.stopwatch_job = None

        self._setup_stopwatch()

    def _setup_stopwatch(self):
        # Pantalla del cronómetro
        self.stopwatch_display = tk.Label(self.stopwatch_frame,
                                          text="00:00:00.00",
                                          font=('Helvetica', 50, 'bold'),
                                          bg='#003366', fg='white')
        self.stopwatch_display.pack(pady=50, expand=True)

        # Botones
        button_frame = tk.Frame(self.stopwatch_frame, bg='#003366')
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Iniciar", font=('Helvetica', 14),
                                      command=self._start_stopwatch,
                                      bg='#FFD700', fg='black', width=10,
                                      relief='flat', bd=0)
        self.start_button.grid(row=0, column=0, padx=10)

        self.stop_button = tk.Button(button_frame, text="Parar", font=('Helvetica', 14),
                                     command=self._stop_stopwatch,
                                     bg='#FFD700', fg='black', width=10,
                                     relief='flat', bd=0, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=10)

        self.reset_button = tk.Button(button_frame, text="Reiniciar", font=('Helvetica', 14),
                                      command=self._reset_stopwatch,
                                      bg='#FFD700', fg='black', width=10,
                                      relief='flat', bd=0, state=tk.DISABLED)
        self.reset_button.grid(row=0, column=2, padx=10)

    # Funciones del Cronometro
    def _start_stopwatch(self):
        if not self.stopwatch_running:
            self.stopwatch_running = True
            self.stopwatch_start_time = time.time() - self.stopwatch_elapsed_time
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
            self.stopwatch_elapsed_time = time.time() - self.stopwatch_start_time
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
            current_time = time.time() - self.stopwatch_start_time
            hours = int(current_time // 3600)
            minutes = int((current_time % 3600) // 60)
            seconds = int(current_time % 60)
            milliseconds = int((current_time * 100) % 100)
            formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:02d}"
            self.stopwatch_display.config(text=formatted_time)
            self.stopwatch_job = self.master.after(10, self._update_stopwatch_display)

# Inicia el programa
if __name__ == '__main__':
    root = tk.Tk()
    app = AdvancedClock(root)
    root.mainloop()
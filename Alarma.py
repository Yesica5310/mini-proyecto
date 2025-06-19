from tkinter import Label, Tk, ttk, Button, LabelFrame
from time import strftime
from pygame import mixer

# Inicializar pygame mixer
mixer.init()

# Crear ventana principal
ventana = Tk()
ventana.config(bg='gray20')
ventana.geometry('600x400')
ventana.title('Reloj Digital con Alarma')
ventana.resizable(False, False)

# Listas para comboboxes (sin segundos)
lista_horas = [f"{i:02d}" for i in range(0, 24)]
lista_minutos = [f"{i:02d}" for i in range(0, 60)]

# Estilos personalizados para combobox
style = ttk.Style()
style.theme_create("combostyle", parent="alt", settings={
    "TCombobox": {
        "configure": {
            "selectbackground": "deepskyblue",
            "fieldbackground": "gray30",
            "background": "gray20",
            "foreground": "white"
        }
    }
})
style.theme_use("combostyle")

ventana.option_add('*TCombobox*Listbox*Background', 'gray20')
ventana.option_add('*TCombobox*Listbox*Foreground', 'white')
ventana.option_add('*TCombobox*Listbox*selectBackground', 'deepskyblue')
ventana.option_add('*TCombobox*Listbox*selectForeground', 'black')

# --- Variables globales ---
alarma_activa = False
alarma_sonando = False

# --- Funciones ---

def toggle_alarma():
    global alarma_activa
    if not alarma_activa:
        hora_sel = combobox_hora.get()
        min_sel = combobox_minuto.get()
        if not (hora_sel and min_sel):
            return
        alarma_label.config(text=f"Alarma: {hora_sel}:{min_sel}", fg="lime")
        alarma_activa = True
    else:
        alarma_label.config(text="Alarma: Desactivada", fg="red")
        alarma_activa = False

# Función para reproducir la alarma
def reproducir_alarma():
    global alarma_sonando
    if not alarma_sonando:
        try:
            mixer.music.load("Alarma_audio.mp3")
            mixer.music.play(loops=int(repeticiones.get()))
            alarma_sonando = True
            boton_detener.pack(pady=5)  # Mostrar botón para detener
        except Exception as e:
            print("Error al cargar el audio:", e)


def detener_alarma():
    global alarma_sonando, alarma_activa
    if alarma_sonando:
        mixer.music.stop()  # Detiene la música
        alarma_sonando = False
        alarma_activa = False  # Desactivamos la alarma
        alarma_label.config(text="Alarma: Desactivada", fg="red")
    boton_detener.pack_forget()  # Ocultar el botón

def actualizar_reloj():
    global alarma_sonando
    hora_actual = strftime('%H:%M:%S')
    texto_hora.config(text=hora_actual)

    if alarma_activa and not alarma_sonando:
        hora_alarma = f"{combobox_hora.get()}:{combobox_minuto.get()}:00"
        if hora_actual[:5] == hora_alarma[:5]:  # Comparar horas y minutos
            reproducir_alarma()

    texto_hora.after(1000, actualizar_reloj)  # Actualizar cada segundo


# --- Interfaz gráfica ---

# Reloj actual - arriba de todo
texto_hora = Label(ventana, fg='lime', bg='gray20', font=('Radioland', 50))
texto_hora.pack(pady=10)

# Marco para configuración de alarma
frame = LabelFrame(ventana, text="Configuración de Alarma", font=('Arial', 12), fg='deepskyblue', bg='gray20', bd=2)
frame.pack(expand=True, padx=20, pady=20)

# Etiquetas de selección de alarma
Label(frame, text='Hora', bg='gray20', fg='magenta', font=('Arial', 12)).grid(
    row=0, column=0, padx=10, pady=5)
Label(frame, text='Minutos', bg='gray20', fg='magenta', font=('Arial', 12)).grid(
    row=0, column=1, padx=10, pady=5)

# Comboboxes para Hora y Minuto
combobox_hora = ttk.Combobox(frame, values=lista_horas, style="TCombobox", justify='center', width=8, font='Arial')
combobox_hora.grid(row=1, column=0, padx=10, pady=5)
combobox_hora.set("00")

combobox_minuto = ttk.Combobox(frame, values=lista_minutos, style="TCombobox", justify='center', width=8, font='Arial')
combobox_minuto.grid(row=1, column=1, padx=10, pady=5)
combobox_minuto.set("00")

# Selector de veces que se repite la alarma
repeticiones = ttk.Combobox(frame, values=(1, 2, 3, 4, 5), justify='center', width=6, font='Arial')
repeticiones.grid(row=1, column=2, padx=10, pady=5)
repeticiones.set(1)

Label(frame, text='Repetir:', bg='gray20', fg='white', font='Arial').grid(
    row=0, column=2, padx=10, pady=5)

# Botón para activar/desactivar alarma
Button(frame,
       text="Activar/Desactivar Alarma",
       command=toggle_alarma,
       bg='gray30',
       fg='white',
       font=('Arial', 10)).grid(
       row=2, columnspan=3, pady=10)

# Estado de la alarma
alarma_label = Label(ventana, text="Alarma: Desactivada", fg='red', bg='gray20', font=('Arial', 14))
alarma_label.pack(pady=10)

# Botón para detener la alarma (inicialmente oculto)
boton_detener = Button(ventana, text="Detener Alarma", command=detener_alarma, bg='tomato', fg='white', font=('Arial', 10))
# boton_detener.pack(pady=5)

# Iniciar actualización del reloj
actualizar_reloj()

# Loop principal
ventana.mainloop()
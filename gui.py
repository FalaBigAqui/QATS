import tkinter as tk
import threading
import time
from utils.time_sync import TimeSync
from utils.file_manager import create_session_files
from recorder.screen_recorder import ScreenRecorder
from logger.event_logger import EventLogger

clock = TimeSync()

recorder = None
logger = None
timer_running = False

# Definindo as etapas durante o inicio do uso da automação
def start_session():

    global recorder, logger, timer_running

    log_file, video_file = create_session_files()

    recorder = ScreenRecorder(clock, video_file)
    logger = EventLogger(clock, log_file)

    clock.start()

    recorder.start()
    logger.start()

    show_recording_ui()

    timer_running = True
    threading.Thread(target=update_timer).start()

# Definindo as etapas durante o fim do uso da automação
def stop_session():

    global timer_running

    recorder.stop()
    logger.stop()

    timer_running = False

    show_start_ui()

# Cronometro mostrado na interface após a automação ser iniciada
def update_timer():

    while timer_running:

        time_text = clock.formatted()
        root.after(0, timer_label.config, {"text": f"Tempo: {time_text}"})

        time.sleep(1)

# Interface inicial
def show_start_ui():

    for widget in root.winfo_children():
        widget.destroy()

    # Centraliza tudo caso modifique o tamanho da interface
    frame = tk.Frame(root)
    frame.pack(expand=True, fill="both")

    start_btn = tk.Button(frame, text="Iniciar Automação", command=start_session, width=25)
    start_btn.place(relx=0.5, rely=0.5, anchor="center")

# Interface durante o uso da automação
def show_recording_ui():

    for widget in root.winfo_children():
        widget.destroy()

    global timer_label

    frame = tk.Frame(root)
    frame.pack(expand=True, fill="both")

    timer_label = tk.Label(frame, text="Tempo: 0s", font=("Arial", 16))
    timer_label.place(relx=0.5, rely=0.4, anchor="center")

    stop_btn = tk.Button(frame, text="Finalizar", command=stop_session, width=25)
    stop_btn.place(relx=0.5, rely=0.6, anchor="center")

# Tamanho da interface
def start_gui():

    global root

    root = tk.Tk()
    root.title("QATS")
    root.geometry("640x480")
    root.resizable(True, True)  # Permite mudar o tamanho das 2 dimensões

    show_start_ui()

    root.mainloop()

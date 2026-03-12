import tkinter as tk
import threading

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

# Definindo as etapadas durante o fim do uso da automação
def stop_session():

    global timer_running

    recorder.stop()
    logger.stop()

    timer_running = False

    show_start_ui()

# Cronometro mostrado na interface após iniciado a automação
def update_timer():

    while timer_running:

        time_text = clock.formatted()

        timer_label.config(text=f"Tempo: {time_text}")

        root.update()

        import time
        time.sleep(1)

# Interface inicial
def show_start_ui():

    for widget in root.winfo_children():
        widget.destroy()

    start_btn = tk.Button(root, text="Iniciar Automação", command=start_session, width=25)
    start_btn.pack(pady=40)

# Interface durante o uso da automação
def show_recording_ui():

    for widget in root.winfo_children():
        widget.destroy()

    global timer_label

    timer_label = tk.Label(root, text="Tempo: 0s", font=("Arial",16))
    timer_label.pack(pady=20)

    stop_btn = tk.Button(root, text="Finalizar", command=stop_session, width=25)
    stop_btn.pack(pady=20)

# Tamanho da interface
def start_gui():

    global root

    root = tk.Tk()
    root.title("QATS")
    root.geometry("640x480")

    show_start_ui()

    root.mainloop()
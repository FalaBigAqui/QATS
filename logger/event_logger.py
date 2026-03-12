from pynput import keyboard, mouse

# Definição da classe EventLogger
class EventLogger:

    def __init__(self, clock, logfile):

        self.clock = clock
        self.log = open(logfile, "w")

        self.keyboard_listener = None
        self.mouse_listener = None

    # Tempo exato de cada input registrado
    def log_event(self, event):

        t = self.clock.formatted()
        self.log.write(f"{t} {event}\n")

    # Definindo a coleta dos inputs do teclado
    def on_press(self, key):

        try:
            self.log_event(f"KEY {key.char}")
        except:
            self.log_event(f"KEY {key}")

    # Definindo a coleta dos inputs do mouse
    def on_move(self, x, y):

        self.log_event(f"MOVE {x},{y}")

    def on_click(self, x, y, button, pressed):

        if pressed:
            self.log_event(f"CLICK {button} {x},{y}")

    # Inicio das funções após usuario apertar Iniciar
    def start(self):

        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)

        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )

        self.keyboard_listener.start()
        self.mouse_listener.start()

    # Finalização das funções após usuario apertar finalizar
    def stop(self):

        self.keyboard_listener.stop()
        self.mouse_listener.stop()

        self.log.close()
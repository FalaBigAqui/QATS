import time

# Definindo a classe para todos os timers ficarem sincronizados
class TimeSync:

    def __init__(self):
        self.start_time = None

    def start(self):
        self.start_time = time.perf_counter()

    def elapsed(self):
        return int(time.perf_counter() - self.start_time)

    def now(self):
        return round(time.perf_counter() - self.start_time, 3)

    def formatted(self):

        seconds = self.elapsed()

        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60

        return f"{h:02}:{m:02}:{s:02}"
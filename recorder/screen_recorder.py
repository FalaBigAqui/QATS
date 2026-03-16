import cv2
import numpy as np
import mss
import threading
import queue
import time

# Definição da classe ScreenRecorder
class ScreenRecorder:

    def __init__(self, clock, video_file, fps=30):

        self.clock = clock
        self.video_file = video_file
        self.fps = fps

        self.frame_interval = 1 / fps

        self.running = False
        self.frame_queue = queue.Queue(maxsize=300)
    
    # Definição da captura da tela
    def capture(self):

        with mss.mss() as sct:

            monitor = sct.monitors[1]

            next_frame_time = time.perf_counter()

            while self.running:

                now = time.perf_counter

                if now >= next_frame_time:
                    
                    img = sct.grab(monitor)
                    frame = np.array(img)

                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                    timestamp = self.clock.formatted()

                    if not self.frame_queue.full():
                        self.frame_queue.put((frame, timestamp))

                    next_frame_time += self.frame_interval

                else:
                    time.sleep(0.001)
    
    def write(self):

        with mss.mss() as sct:
            monitor = sct.monitors[1]

            width = monitor["width"]
            height = monitor["height"]

        out = cv2.VideoWriter(
            self.video_file,
            cv2.VideoWriter_fourcc(*"H264"),
            30,
            (width, height)
        )

        while self.running or not self.frame_queue.empty():

            try:

                frame, timestamp = self.frame_queue.get(timeout=1)

                cv2.putText(
                    frame,
                    timestamp,
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,255),
                    2
                )

                out.write(frame)

            except queue.Empty:
                pass

        # Comando para garantir que o arquivo não saia corrompido
        out.release()

    # Definição para o inicio da funcionalidade
    def start(self):

        self.running = True

        self.capture_thread = threading.Thread(target=self.capture)
        self.write_thread = threading.Thread(target=self.write)

        self.capture_thread.start()
        self.write_thread.start()

    # Definição para finalização da funcionalidade
    def stop(self):

        self.running = False

        self.capture_thread.join()
        self.write_thread.join()

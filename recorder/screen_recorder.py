import cv2
import numpy as np
import mss
import threading
import queue
import time

# Definindo a classe ScreenRecorder
class ScreenRecorder:

    def __init__(self, clock, video_file, fps=30):

        self.clock = clock
        self.video_file = video_file
        self.fps = fps

        self.running = False
        self.frame_queue = queue.Queue(maxsize=300)

    def capture(self): # Definindo a função captura

        frame_interval = 1.0 / self.fps  # ~0.0333s por frame em 30 FPS

        with mss.mss() as sct:

            monitor = sct.monitors[1]

            while self.running:

                frame_start = time.monotonic()

                img = sct.grab(monitor)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                timestamp = self.clock.elapsed()

                # Derruba o frame mais antigo para abrir espaço do que só apenas pular silenciosamente
                if self.frame_queue.full():
                    try:
                        self.frame_queue.get_nowait()
                    except queue.Empty:
                        pass

                self.frame_queue.put((frame, timestamp))

                # Sleep durante o resto deste frame slot
                elapsed = time.monotonic() - frame_start
                sleep_time = frame_interval - elapsed
                if sleep_time > 0:
                    time.sleep(sleep_time)

    def write(self): # Definindo a escrita do arquivo final

        with mss.mss() as sct:
            monitor = sct.monitors[1]
            width = monitor["width"]
            height = monitor["height"]

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        out = cv2.VideoWriter(
            self.video_file,
            fourcc,
            self.fps,
            (width, height)
        )

        last_frame = None
        written_frames = 0

        while self.running or not self.frame_queue.empty():

            try:

                frame, timestamp = self.frame_queue.get(timeout=1)

                cv2.putText(
                    frame,
                    self.clock.formatted(),
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2
                )

                # Quantos frames eram para ser escritos nesse tempo
                expected_frames = int(timestamp * self.fps)

                # Em conjunto com o ultimo frame conhecido para preencher qualquer buraco
                while written_frames < expected_frames and last_frame is not None:
                    out.write(last_frame)
                    written_frames += 1

                # Agora escreve o frame atual
                out.write(frame)
                last_frame = frame
                written_frames += 1

            except queue.Empty:
                pass

        out.release()

    def start(self): # Definindo o inicio da função

        self.running = True

        self.capture_thread = threading.Thread(target=self.capture)
        self.write_thread = threading.Thread(target=self.write)

        self.capture_thread.start()
        self.write_thread.start()

    def stop(self): # Definindo o fim da função

        self.running = False

        self.capture_thread.join()
        self.write_thread.join()

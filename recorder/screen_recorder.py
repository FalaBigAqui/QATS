import cv2
import numpy as np
import mss
import threading
import queue
import time


class ScreenRecorder:

    def __init__(self, clock, video_file, fps=30):

        self.clock = clock
        self.video_file = video_file
        self.fps = fps

        self.running = False
        self.frame_queue = queue.Queue(maxsize=300)

    def capture(self):

        with mss.mss() as sct:

            monitor = sct.monitors[1]

            while self.running:

                img = sct.grab(monitor)
                frame = np.array(img)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

                timestamp = self.clock.elapsed()

                if not self.frame_queue.full():
                    self.frame_queue.put((frame, timestamp))

    def write(self):

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

                # calcula quantos frames deveriam existir até agora
                expected_frames = int(timestamp * self.fps)

                while written_frames < expected_frames:

                    if last_frame is not None:
                        out.write(last_frame)
                        written_frames += 1

                cv2.putText(
                    frame,
                    self.clock.formatted(),
                    (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,255),
                    2
                )

                out.write(frame)

                last_frame = frame
                written_frames += 1

            except queue.Empty:
                pass

        out.release()

    def start(self):

        self.running = True

        self.capture_thread = threading.Thread(target=self.capture)
        self.write_thread = threading.Thread(target=self.write)

        self.capture_thread.start()
        self.write_thread.start()

    def stop(self):

        self.running = False

        self.capture_thread.join()
        self.write_thread.join()

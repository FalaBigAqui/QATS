import os
from datetime import datetime

# Criação do arquivo log identificado por dia e hora
def create_session_files():

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs("logs", exist_ok=True)
    os.makedirs("recordings", exist_ok=True)

    log_file = f"logs/session_{timestamp}.log"
    video_file = f"recordings/session_{timestamp}.avi"

    return log_file, video_file
import os
from celery import shared_task
import serial

SERIAL_PORT = os.environ.get("SERIAL_PORT", "loop://")
BAUDRATE = int(os.environ.get("SERIAL_BAUD", 115200))

@shared_task(bind=True)
def send_command_task(self, cmd: str):
    try:
        ser = serial.serial_for_url(SERIAL_PORT, baudrate=BAUDRATE, timeout=2)
        ser.write((cmd + "\n").encode())
        resp = ser.readline().decode(errors="ignore").strip()
        ser.close()
        return {"cmd": cmd, "resp": resp}
    except Exception as e:
        return {"cmd": cmd, "resp": f"ERROR: {e}"}

@shared_task
def run_controller(input_signal: float) -> dict:
    # Exemplo de modelo matemático (um sistema de 1ª ordem)
    # y(k+1) = 0.9*y(k) + 0.1*u(k)
    y = 0
    for _ in range(10):
        y = 0.9*y + 0.1*input_signal
    return {"output": y}
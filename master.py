import time
import serial

send = serial.Serial(port='/dev/ttyS1', baudrate=9600, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, timeout=1)

message = "hello from orange pi"

while True:
    send.write(f'{message}\n'.encode())
    print(f'Sent message: {message}')
    time.sleep(1.5)

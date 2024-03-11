import time
import serial

# Open serial port for sending messages
send = serial.Serial(port='/dev/ttyS1', baudrate=9600, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, timeout=1)

# Open serial port for receiving messages
receive = serial.Serial(port='/dev/ttyS1', baudrate=9600, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, timeout=1)

message = "hello from orange pi"

while True:
    # Send message
    send.write(f'{message}\n'.encode())
    print(f'Sent message: {message}')
    
    # Receive message
    received_data = receive.readline().decode().strip()  # Read a line from serial port
    if received_data:
        print(f'Received message: {received_data}')

    time.sleep(1.5)

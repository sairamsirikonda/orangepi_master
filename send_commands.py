import serial
import time

# Replace with the serial port connected to the RS-485 device
SERIAL_PORT = '/dev/ttyS0'

# Replace with the baud rate, data bits, parity, and stop bits
BAUD_RATE = 9600
DATA_BITS = serial.EIGHTBITS
PARITY = serial.PARITY_NONE
STOP_BITS = serial.STOPBITS_ONE

# Open serial port
ser = serial.Serial(SERIAL_PORT, baudrate=BAUD_RATE, bytesize=DATA_BITS, parity=PARITY, stopbits=STOP_BITS)

try:
    # Send commands to the RS-485 device
    while True:
        # Replace 'command' with the actual command you want to send
        command = b'Hello, RS-485 device!\r\n'
        ser.write(command)

        # Wait for a short duration before sending the next command
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Close the serial port
    ser.close()

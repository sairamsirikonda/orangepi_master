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
    while True:
        # Send commands to the RS-485 device
        command = input("Enter command to send: ") + '\r\n'
        ser.write(command.encode())

        # Read and print response from the RS-485 device
        response = ser.readline().decode().strip()
        print("Response from RS-485 device:", response)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Close the serial port
    ser.close()

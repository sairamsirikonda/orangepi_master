import serial
import time

# Define the serial port and baud rate
serial_port = "/dev/ttyS1"  # Adjust this based on your Orange Pi's serial port
baud_rate = 9600

# Create a Serial object
ser = serial.Serial(serial_port, baud_rate, timeout=1)

try:
    while True:
        # Send a character to Arduino
        message = "A"  # You can change this message
        ser.write(message.encode())
        print(f"Orange Pi Sent: {message}")

        # Wait for a short duration
        time.sleep(1)

except KeyboardInterrupt:
    # Close the serial connection on keyboard interrupt
    ser.close()
    print("Serial connection closed.")


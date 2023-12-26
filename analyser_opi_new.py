import serial
import RPi.GPIO as GPIO
import time

# Open the serial port
ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)

<<<<<<< HEAD

# Define GPIO pin numbers for DE and RE
DE_RE_PIN = port.PG7  # Adjust based on your actual GPIO pin configuration


# Choose a GPIO pin for both DE and RE (use appropriate pin names for Orange Pi)
DE_RE_PIN = port.PG0  # Replace with the appropriate GPIO pin
=======
# Choose a GPIO pin for both DE and RE (use appropriate pin numbers for Orange Pi)
DE_RE_PIN = 17  # Replace with the appropriate GPIO pin number
>>>>>>> a444fd32b2edfa6aed31acaa99b24d3a29aa484d

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DE_RE_PIN, GPIO.OUT)

# Function to send a Modbus request and receive the response
def send_modbus_request(address):
    # Enable transmission (DE and RE low)
    GPIO.output(DE_RE_PIN, GPIO.LOW)

    # Construct the Modbus RTU request
    command = bytes([1, 3, 156, address, 0, 0, 0, 2])  # Modify as needed

    # Print the Modbus request being sent
    print("Sent command:", command)

    # Send the Modbus request
    ser.write(command)

    # Wait for transmission to complete
    ser.flush()

    # Disable transmission (DE and RE high)
<<<<<<< HEAD
    gpio.output(DE_RE_PIN, gpio.HIGH)


=======
    GPIO.output(DE_RE_PIN, GPIO.HIGH)
>>>>>>> a444fd32b2edfa6aed31acaa99b24d3a29aa484d

    # Receive the Modbus response
    response = ser.read(8)  # Adjust the number based on the expected response length

    # Print the Modbus response received
    print("Received response:", response)

    return response

# Example usage
for i in range(10):
    address = 64 + i
    response = send_modbus_request(address)

    # Process the response (your existing logic)
    if response:
        value = int.from_bytes(response[3:7], byteorder='big', signed=False)
        print(f"Process Value at address {address}: {value}")
    else:
        print(f"No response received for address {address}")

# Close the serial port
ser.close()

# Cleanup GPIO
GPIO.cleanup()

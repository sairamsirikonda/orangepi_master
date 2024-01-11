import serial
from pyA20.gpio import gpio
from pyA20.gpio import port

# Open the serial port
ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)

# Choose a GPIO pin for both DE and RE (use appropriate pin names for Orange Pi)
DE_RE_PIN = port.PG0  # Replace with the appropriate GPIO pin

# Setup GPIO
gpio.init()
gpio.setcfg(DE_RE_PIN, gpio.OUTPUT)

# Function to send a Modbus request and receive the response
def send_modbus_request(address):
    # Enable transmission (DE and RE low)
    gpio.output(DE_RE_PIN, gpio.LOW)

    # Convert starting address to Modbus address
    modbus_address = address - 1

    # Construct the Modbus RTU request
    command = bytes([1, 3, (modbus_address >> 8) & 0xFF, modbus_address & 0xFF, 0, 2])  # Modify as needed

    # Print the Modbus request being sent
    print("Sent command:", command)

    # Send the Modbus request
    ser.write(command)

    # Wait for transmission to complete
    ser.flush()

    # Disable transmission (DE and RE high)
    gpio.output(DE_RE_PIN, gpio.HIGH)

    # Receive the Modbus response
    response = ser.read(8)  # Adjust the number based on the expected response length

    # Print the Modbus response received
    print("Received response:", response)

    return response

# Example usage
for i in range(10):
    address = 40001 + i
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
gpio.cleanup()

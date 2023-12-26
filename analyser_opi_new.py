import serial
from pyA20.gpio import gpio
from pyA20.gpio import port

gpio.init()

# List all available GPIO ports
available_ports = [pin for pin in dir(port) if pin.startswith("PA") or pin.startswith("PG")]
print("Available GPIO ports:", available_ports)


# Open the serial port
ser = serial.Serial('/dev/ttyS0', baudrate=9600, timeout=1)

# Define GPIO pin numbers for DE and RE
DE_RE_PIN = port.PA7  # Adjust based on your actual GPIO pin configuration
<<<<<<< HEAD
=======

>>>>>>> 2e35ecf19eb623e62dc0e368d7295da4af65a412

# Setup GPIO
gpio.init()
gpio.setcfg(DE_RE_PIN, gpio.OUTPUT)

# Function to send a Modbus request and receive the response
def send_modbus_request(address):
    # Enable transmission (DE and RE low)
    gpio.output(DE_RE_PIN, gpio.LOW)
<<<<<<< HEAD
    
=======

>>>>>>> 2e35ecf19eb623e62dc0e368d7295da4af65a412

    # Construct the Modbus RTU request
    command = bytes([1, 3, 156, address, 0, 0, 0, 2])  # Modify as needed

    # Print the Modbus request being sent
    print("Sent command:", command)

    # Send the Modbus request
    ser.write(command)

    # Wait for transmission to complete
    ser.flush()

    # Disable transmission (DE and RE high)
    gpio.output(DE_RE_PIN, gpio.HIGH)
<<<<<<< HEAD
    
=======

>>>>>>> 2e35ecf19eb623e62dc0e368d7295da4af65a412

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

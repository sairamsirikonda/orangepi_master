import serial
from pyA20.gpio import gpio
from pyA20.gpio import port

# Open the serial port
ser = serial.Serial('/dev/ttyS1', baudrate=9600, timeout=1)

# Choose a GPIO pin for both DE and RE (use appropriate pin names for Orange Pi)
DE_RE_PIN = port.PA7  # Replace with the appropriate GPIO pin

# Setup GPIO
gpio.init()
gpio.setcfg(DE_RE_PIN, gpio.OUTPUT)

# Function to send a Modbus request and receive the response
def send_modbus_request(register):
    # Enable transmission (DE and RE low)
    gpio.output(DE_RE_PIN, gpio.LOW)

    # Convert register to Modbus address
    modbus_address = register - 1

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
try:
    registers = [40001, 40003, 40005]
    for register in registers:
        response = send_modbus_request(register)

        # Process the response
        if response:
            # Extract raw value from Modbus response
            raw_value = int.from_bytes(response[3:7], byteorder='big', signed=False)

            # Assuming a scaling factor of 0.1 (adjust based on device documentation)
            scaling_factor = 0.1
            gas_concentration_ppm = raw_value * scaling_factor

            print(f"Gas Concentration at register {register}: {gas_concentration_ppm} PPM")
        else:
            print(f"No response received for register {register}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the serial port
    ser.close()

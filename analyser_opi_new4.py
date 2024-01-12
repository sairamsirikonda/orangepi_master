import serial
import struct
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
    expected_response_length = 5 + 2  # Address (1 byte) + Function code (1 byte) + Byte count (1 byte) + Data (2 bytes)
    response = ser.read(expected_response_length)  # Adjust the number based on the expected response length

    # Print the Modbus response received
    print("Received response:", response)

    return response

# Example usage
try:
    registers = [40001, 40003, 40005]
    for register in registers:
        response = send_modbus_request(register)

        # Process the response
        if response and len(response) >= 7:  # Check if the response is of sufficient length
            if register == 40001:
                # Process value (float32_t)
                process_value_bytes = response[3:7]
                process_value = struct.unpack('>f', process_value_bytes)[0]
                print(f"Process Value at register {register}: {process_value}")
            elif register == 40003:
                # Monitor status (uint16_t)
                monitor_status_bytes = response[3:5]
                monitor_status = int.from_bytes(monitor_status_bytes, byteorder='big', signed=False)
                print(f"Monitor Status at register {register}: {monitor_status}")
            else:
                # Handle other cases if needed
                print(f"Value at register {register}: Unsupported parameter")

        else:
            print(f"No or invalid response received for register {register}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the serial port
    ser.close()

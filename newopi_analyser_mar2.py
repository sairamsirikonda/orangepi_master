import minimalmodbus

# Replace with your specific values
PORT = '/dev/ttyS1'  # Replace with the actual serial port device file
SLAVE_ADDRESS = 1  # Replace with the slave address of your Modbus device

# Create a minimalmodbus instrument object
instrument = minimalmodbus.Instrument(PORT, SLAVE_ADDRESS)

# Configure serial communication settings
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 0.5  # Timeout for read operations
instrument.mode = minimalmodbus.MODE_RTU


# Addresses to read from
register_addresses = list(range(40001, 40003))

try:
    # Read data from each register address
    for address in register_addresses:
        value = instrument.read_register(address, functioncode=4)
        print(f"Value at address {address}: {value}")

except Exception as e:
    print("Error:", e)

finally:
    # Clean up resources
    instrument.serial.close()
    print("Serial port closed.")

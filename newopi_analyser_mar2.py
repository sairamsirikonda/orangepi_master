import minimalmodbus

# Replace with your specific values
PORT = '/dev/ttyS0'  # Replace with the actual serial port device file
SLAVE_ADDRESS = 1  # Replace with the slave address of your Modbus device

# Create a minimalmodbus instrument object
instrument = minimalmodbus.Instrument(PORT, SLAVE_ADDRESS)

# Configure serial communication settings
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 0.5  # Timeout for read operations

# Addresses to read from
register_addresses = [0x7ff798f7f3d6, 0x7ff798ef63c5, 0x7ff798ef5cb9, 0x7ff798f15f82]

try:
    # Read data from each register address
    for address in register_addresses:
        value = instrument.read_register(address, functioncode=3)
        print(f"Value at address {hex(address)}: {value}")

except Exception as e:
    print("Error:", e)

finally:
    # Clean up resources
    instrument.serial.close()
    print("Serial port closed.")

import minimalmodbus

# Replace with your specific values
PORT = '/dev/ttyS0'  # Replace with the actual serial port device file
SLAVE_ADDRESS = 1  # Replace with the slave address of your gas analyzer
REGISTER_ADDRESS = 40001  # Starting register address
NUMBER_OF_REGISTERS = 5  # Number of registers to read

# Configure the minimalmodbus instrument
instrument = minimalmodbus.Instrument(PORT, SLAVE_ADDRESS)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 0.5  # Timeout for read operations

try:
    # Read data from registers
    registers = instrument.read_registers(REGISTER_ADDRESS, NUMBER_OF_REGISTERS)

    # Process the register values (replace with your specific logic)
    for i, value in enumerate(registers):
        print(f"Register value {i+1}: {value}")  # Print the raw register values

except Exception as e:
    print("Error:", e)

finally:
    # Clean up resources
    instrument.serial.close()
    print("Serial port closed.")

from pymodbus.client.sync import ModbusSerialClient
import time

# Define the serial port and baudrate
client = ModbusSerialClient(method='rtu', port='/dev/ttyS1', baudrate=9600)
# Change '/dev/ttyUSB0' to your actual serial port

# Function to read data from slave
def read_from_slave(unit, address, count):
    if client.connect():
        # Read holding registers
        response = client.read_holding_registers(address, count, unit=unit)
        client.close()
        return response.registers
    else:
        print("Failed to connect to Modbus device.")
        return None

# Main loop
while True:
    # Define the unit ID, address, and number of registers to read
    unit_id = 1  # Change to your slave device's unit ID
    address = 40001  # Change to your desired starting address
    count = 4  # Change to the number of registers you want to read
    
    # Read data from slave
    response = read_from_slave(unit_id, address, count)
    
    if response:
        # Print the response
        print("Response:", response)
    else:
        print("Failed to read from slave.")
    
    # Adjust loop delay if needed
    time.sleep(1)

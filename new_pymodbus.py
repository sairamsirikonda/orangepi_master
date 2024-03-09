from pymodbus.client.sync import ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

# Define the serial port and Modbus parameters
port = '/dev/ttyS1'  # Change to your actual serial port
baudrate = 9600
parity = 'N'
data_bits = 8
stop_bits = 1

# Define the slave ID and register addresses
slave_id = 1
register_addresses = [40001, 40002, 40003, 40004, 40005]

# Function to read holding registers from the Modbus slave
def read_holding_registers(client, slave_id, address, count):
    response = client.read_holding_registers(address, count, unit=slave_id)
    if response.isError():
        print("Error reading registers:", response)
        return None
    else:
        decoder = BinaryPayloadDecoder.fromRegisters(response.registers, Endian.Big)
        return decoder.decode_32bit_float()  # Assuming the registers contain 32-bit floating-point values

# Create Modbus serial client
client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, parity=parity,
                            stopbits=stop_bits, bytesize=data_bits)

# Connect to the Modbus slave
if client.connect():
    print("Connected to Modbus slave")

    # Read holding registers for each register address
    for address in register_addresses:
        data = read_holding_registers(client, slave_id, address, count=2)  # Assuming each register is a 32-bit float
        if data is not None:
            print(f"Register {address}: {data}")

    # Close the connection
    client.close()
    print("Disconnected from Modbus slave")
else:
    print("Failed to connect to Modbus slave")

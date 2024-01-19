import struct
from pyModbusTCP.client import ModbusClient

def convert_registers_to_float(registers):
    # Assuming the Modbus data is a 32-bit floating-point number
    raw_data = struct.pack('>HH', registers[1], registers[0])
    gas_concentration = struct.unpack('>f', raw_data)[0]
    return gas_concentration

def read_gas_concentration(client, register_address):
    # Send Modbus command to read registers
    command = client.write_multiple_registers(register_address, [0, 2])

    # Check if the command was successful
    if command:
        # Read the response
        response = client.read_holding_registers(register_address, 2)

        # Check if the response is valid
        if response:
            gas_concentration = convert_registers_to_float(response)
            return gas_concentration
        else:
            print(f"Failed to read response from register {register_address}")
    else:
        print(f"Failed to send command to register {register_address}")

    return None

if __name__ == "__main__":
    # Initialize Modbus client
    c = ModbusClient(host="192.168.0.129", port=/dev/ttyS1)

    # Check if the client can connect to the Modbus server
    if c.open():
        # Read gas concentration from different registers
        for register_address in [40001, 40003, 40005]:
            gas_concentration = read_gas_concentration(c, register_address)
            if gas_concentration is not None:
                print(f"Gas Concentration at register {register_address}: {gas_concentration} PPM")
    else:
        print("Failed to connect to the Modbus server")

    # Close the Modbus client
    c.close()

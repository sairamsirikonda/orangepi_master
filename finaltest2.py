from pymodbus.client.serial import ModbusSerialClient
import struct

SLAVE_ID = 1
REGISTER = 1
COUNT = 2
DATA_TYPE = 3

client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyS1',
    baudrate=9600,
    timeout=0.5,
    parity='N',
    stopbits=1,
    bytesize=8
)

def connect():
    retVal = client.connect()
    return retVal

def readRegisters():
    '''Reading from a holding register with the below content.'''
    res = client.read_holding_registers(REGISTER, COUNT, unit=SLAVE_ID)
    if not res.isError():
        # Assuming the data type is 32-bit unsigned integer (unsigned long int)
        raw_data = res.registers  # Get the raw data from the response
        if len(raw_data) == 2:  # Ensure we received the expected number of registers
            # Combine the two registers into a single 32-bit unsigned integer (unsigned long int)
            long_int_value = struct.unpack('>I', struct.pack('>HH', *raw_data))[0]
            print("Received long integer value:", long_int_value)
        else:
            print("Unexpected data format received")
    else:
        print("Error reading registers:", res)

def main():
    # Connect
    if connect():
        print("Connection successful, Read Registers")
        readRegisters()
    else:
        print("Connection failed")

if __name__ == "__main__":
    main()

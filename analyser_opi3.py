from pymodbus.server.sync import StartSerialServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock

# Configuration
serial_port = '/dev/ttyS0'  # Adjust this based on your setup
baud_rate = 9600
slave_address = 1  # Set the slave address

# Create a Modbus server datastore (you may need to customize this based on your needs)
datastore = ModbusSequentialDataBlock.create()
datastore.add_block(0, [0] * 100)  # Holding registers, adjust the size as needed

# Create Modbus RTU server
server = StartSerialServer(
    datastore,
    identity=ModbusDeviceIdentification(),
    port=serial_port,
    baudrate=baud_rate,
    method='rtu',
    address=slave_address,
)

# Start the server
if __name__ == "__main__":
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

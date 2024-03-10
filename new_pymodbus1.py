from pymodbus.client.serial import ModbusSerialClient
from pyA20.gpio import gpio, port

# Initialize GPIO
gpio.init()

# Set GPIO pin PA7 as OUTPUT
gpio.setcfg(port.PA7, gpio.OUTPUT)

client = ModbusSerialClient(
    method='rtu',
    port='/dev/ttyS1',
    baudrate=9600,
    timeout=3,
    parity='N',
    stopbits=1,
    bytesize=8
)

if client.connect():  # Trying to connect to Modbus Server/Slave
    try:
        # Set GPIO pin PA7 high before sending data
        gpio.output(port.PA7, gpio.HIGH)

        '''Reading from a holding register with the below content.'''
        res = client.read_holding_registers(address=1, count=1, unit=1)
        '''Reading from a discrete register with the below content.'''
        # res = client.read_discrete_inputs(address=1, count=1, unit=1)

        # Set GPIO pin PA7 low after receiving data
        gpio.output(port.PA7, gpio.LOW)

        if not res.isError():
            print(res.registers)
        else:
            print(res)
    except Exception as e:
        print("Error:", e)
    finally:
        # Ensure GPIO pin PA7 is set low if an error occurs
        gpio.output(port.PA7, gpio.LOW)
else:
    print('Cannot connect to the Modbus Server/Slave')

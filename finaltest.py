from pymodbus.client.serial import ModbusSerialClient
SLAVE_ID                = 1
REGISTER    =  1
COUNT       =  2
DATA_TYPE   =  3
register_list = [
("process value",       40001, 2, float),
("gas peak reading",    40007, 2, float),
("rtc hour",    40001,  1,  int),
("rtc min",     40001,  1,  int),
("rtc sec",     40001,  1,  int),
("rtc date",    40001,  1,  int),
("rtc month",   40001,  1,  int),
("rtc year",    40001,  1,  int),
]
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
     retVal =  client.connect()
     return retVal
def readRegisters():
    for register in register_list:
        '''Reading from a holding register with the below content.'''
        res = client.read_holding_registers(register[REGISTER], register[COUNT], slave = SLAVE_ID)
        if not res.isError():
            result = client.convert_from_registers(res, register[[DATA_TYPE]])
            print(register[0], result, '\n')
        else:
            print(res)
def main():
    # Connect
    if connect():
        print("Connnection Successfull, Read Registers")
        readRegisters()
if __name__ == "__main__":
    main()

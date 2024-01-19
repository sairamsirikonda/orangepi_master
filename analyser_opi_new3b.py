import minimalmodbus
###
# Define your Modbus device parameters
RS485_DEVICE = '/dev/ttyS1'
BAUD_RATE = 9600
SLAVE_ID = 1

# Define Modbus register addresses
REG_ADDRESS_1 = 40001
REG_ADDRESS_2 = 40003
REG_ADDRESS_3 = 40005

def read_gas_concentration(instrument, register_address):
    try:
        # Read two registers and interpret as a float
        raw_data = instrument.read_registers(register_address, 2)
        gas_concentration = minimalmodbus._twoscomp(raw_data) / 10.0
        return gas_concentration
    except Exception as e:
        print(f"Error reading register {register_address}: {e}")
        return None

if __name__ == "__main__":
    # Initialize Modbus instrument
    instrument = minimalmodbus.Instrument(RS485_DEVICE, SLAVE_ID)
    instrument.serial.baudrate = BAUD_RATE

    # Read gas concentration from different registers
    for register_address in [REG_ADDRESS_1, REG_ADDRESS_2, REG_ADDRESS_3]:
        gas_concentration = read_gas_concentration(instrument, register_address)
        if gas_concentration is not None:
            print(f"Gas Concentration at register {register_address}: {gas_concentration} PPM")

    # Close the serial connection
    instrument.serial.close()

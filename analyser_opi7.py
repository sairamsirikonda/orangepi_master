import struct
import serial
import logging

# Add this at the beginning of your script
logging.basicConfig(level=logging.DEBUG)


slave_address = 1
baud_rate = 9600
serial_port ='/dev/ttyS0'

def read_float_from_modbus(address, slave):
    try:
        ser = serial.Serial(port=serial_port, baudrate=baud_rate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
        command_to_send = struct.pack(>'BBBBHH', slave, 0x03, (adress - 1) >> 8, (address -1) & 0xFF, 0x00, 0x02)
        ser.write(command_to_send)
        # Read response (adjust bytes read based on Modbus data)
        response = ser.read(7 + 1)  # 7 bytes (header) + 1 byte (byte count)
        
        # Print the sent command and received response for debugging
        print(f"Sent command: {command_to_send}")
        print(f"Received response: {response}")
        
        # Extracting the float value from the response (assuming it's a big-endian float)
        if len(response) >= 4:
            byte_count = response[2]
            data_bytes = response[3:3 + byte_count]
            print(f"Data bytes: {data_bytes}")
            value = struct.unpack('>f', data_bytes)[0]
            return value
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

# ... (rest of the script)
data =read_float_from_modbus(40001, slave_address)
print("process Value:", data)

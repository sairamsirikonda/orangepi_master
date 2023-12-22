import struct
import serial
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

slave_address = 1
baud_rate = 9600
serial_port = '/dev/ttyS0'


def read_float_from_modbus(address, slave):
    try:
        ser = serial.Serial(port=serial_port, baudrate=baud_rate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
        command_to_send = struct.pack('>BBBBHH', slave, 0x03, (address - 1) >> 8, (address -1) & 0xFF, 0x00, 0x02)
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
        with serial.Serial(port=serial_port, baudrate=baud_rate, parity=serial.PARITY_NONE,
                           stopbits=serial.STOPBITS_ONE, timeout=1) as ser:
            # Construct Modbus command
            command_to_send = struct.pack('>BBBBHH', slave, 0x03, (address - 1) >> 8, (address - 1) & 0xFF, 0x00, 0x02)
            
            # Send command
            ser.write(command_to_send)
            
            # Read response (adjust bytes read based on Modbus data)
            response = ser.read(7 + 1)  # 7 bytes (header) + 1 byte (byte count)

            # Log command and response for debugging
            logging.debug(f"Sent command: {command_to_send}")
            logging.debug(f"Received response: {response}")

            # Check response length
            if len(response) >= 8:  # 7 bytes (header) + 1 byte (byte count) + at least 4 bytes for float
                # Extract float value
                byte_count = response[2]
                data_bytes = response[3:3 + byte_count]
                logging.debug(f"Data bytes: {data_bytes}")
                value = struct.unpack('>f', data_bytes)[0]
                return value
            else:
                logging.warning("Unexpected response length.")
                return None

    except Exception as e:
        logging.error(f"Error: {e}")
        return None


# Example usage
data = read_float_from_modbus(40001, slave_address)
print("Process Value:", data)

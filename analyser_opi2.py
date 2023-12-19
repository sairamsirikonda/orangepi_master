import serial


#configuration
slave_address = 0x01 #slave address
baud_rate = 9600 
serial_port = '/dev/ttyUSB0'

#create serial connection
ser = serial.Serial(port=serial_port,baudrate=baud_rate,timeout=1)

def read_from_slave():
  command_to_send = bytes([slave_address,0x03,0x00,0x00,0x02]) #example command modify as needed
  ser.write("hello analyser")

  #Read response
  response = ser.read(8) #adjust the number of bytes to read on your expected response length
  return response

#Example usage
data = read_from_slave()
print(data) #Output the received data

import serial

def read_serial_data(port, baud_rate=115200):
    with serial.Serial(port, baud_rate) as ser:
        while True:
            data = ser.readline().decode().strip()
            print(data)

if __name__ == "__main__":
    port_name = "COM4"  # Replace with your serial port name
    read_serial_data(port_name)

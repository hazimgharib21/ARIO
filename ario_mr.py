import minimalmodbus
import serial

class Modbus_RTU:

    def __init__(self):
        self.port = 'COM3'
        self.mode = minimalmodbus.MODE_RTU
        self.baudrate = 115200
        self.bytesize = 8
        self.parity = serial.PARITY_NONE
        self.stopbits = 1
        self.timeout = 0.05
        self.clear_buffers_before_each_transaction = True
        self.instrument = None

    def init_modbus(self):
        self.instrument = minimalmodbus.Instrument(
            self.port, 
            1,
            self.mode
            )

        self.instrument.serial.baudrate = self.baudrate
        self.instrument.serial.bytesize = self.bytesize
        self.instrument.serial.parity = self.parity
        self.instrument.serial.stopbits = self.stopbits
        self.instrument.serial.timeout = self.timeout
        self.instrument.clear_buffers_before_each_transaction =self.clear_buffers_before_each_transaction 

    def read_bit(self, address):
        return self.instrument.read_bit(address,2)

    def write_bit(self, address, state):
        return self.instrument.write_bit(address,state, 5)

    def detail(self):
        if self.instrument == None:
            print("None")
        else:
            print("Modbus RTU details >>>> " + 
                "\nMode : " + self.instrument.address +
                "\nPort : " + self.instrument.serial.port +
                "\nBaudrate : " + str(self.instrument.serial.baudrate) +
                "\nBytesize : " + str(self.instrument.serial.bytesize) +
                "\nParity : " + self.instrument.serial.parity +
                "\nStopbits : " + str(self.instrument.serial.stopbits) +
                "\nTimeout : " + str(self.instrument.serial.timeout)
            )

class Ario_MR:

    def __init__(self):
        # Initialize digital module
        self._dig_input_count = 8
        self._dig_output_count = 8
        self.baudrate = 115200

        # Initialize Modbus
        self.conn = Modbus_RTU()
        self.conn.baudrate = self.baudrate
        self.conn.init_modbus()

    def read(self, input):
        if input > self._dig_input_count or input <= 0:
            return "Input Count Error"
        if input < 11:
            return(self.conn.read_bit(int(str(200) + str(input - 1))))
        else:
            return(self.conn.read_bit(int(str(20) + str(input - 1))))

    def write(self, output, state):
        if output > self._dig_output_count or output <= 0:
            return "Output Count Error"
        if output < 11:
            self.conn.write_bit(int(str(200) + str(output - 1)), state)
        else:
            self.conn.write_bit(int(str(20) + str(output - 1)), state)

    def set_input_count(self, count):
        self._dig_input_count = count

    def set_output_count(self, count):
        self._dig_output_count = count
    

if __name__ == "__main__":

    rio = Ario_MR()
    rio.set_input_count(16)
    rio.set_output_count(16)
    state = True
    input_state = [
        0, # module 1 channel 1
        0, # module 1 channel 2
        0, # module 1 channel 3
        0, # module 1 channel 4
        0, # module 1 channel 5
        0, # module 1 channel 6
        0, # module 1 channel 7
        0, # module 1 channel 8
        0, # module 2 channel 1
        0, # module 2 channel 2
        0, # module 2 channel 3
        0, # module 2 channel 4
        0, # module 2 channel 5
        0, # module 2 channel 6
        0, # module 2 channel 7
        0, # module 2 channel 8
    ]

    for i in range(1,17):
        input_state[ i - 1 ] = rio.read(i)

    while(1):
        try:
            for i in range(1, 17):
                rio.write(i, state)
                in_state = rio.read(i)
                if in_state != input_state[i - 1]:
                    input_state[i - 1] = in_state
                    if i < 9:
                        print("Module 1 Channel " + str(i) + "  -->  " + str(in_state))
                    else:
                        print("Module 2 Channel " + str(i - 8) + "  -->  " + str(in_state))
            state = not state
        except Exception as e:
            print(e)
            break

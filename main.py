import time
import serial
import threading
import pynmea2


class SerialNmeaRead(threading.Thread):
    '''
    The class with the method that reads the serial port in the backgroud.
    '''
    def __init__(self,com_port,baudrate=38400):
        super().__init__()
        self._stop_event = threading.Event()
        self.serial_object = serial.Serial(com_port, baudrate)
        self.file_name = ""

    def define_file_name(nmea_timestamp):
        str_date = time.strftime("%Y_%m_%d",time.gmtime())
        ## predelat na hodiny
        str_time = str(nmea_timestamp)[0:-3].replace(":","_") # delete seconds
        new_file_name = str_date + "_" + str_time + ".log"

        if self.file_name == "":
            self.file_name = new_file_name
        elif self.file_name == new_file_name:
            self.file_name = new_file_name
            print("odeslani dat na git")


    
    def run(self):
        '''
        The method that actually gets data from the port
        '''
        while not self.stopped():
            datos = self.serial_object.readline().decode('ascii')
            nmea = pynmea2.parse(datos)

            if nmea.sentence_type == "GGA":
                self.define_file_name(str(nmea.timestamp))

            if self.file_name is not "":
                with open(self.file_name, "a", encoding="utf-8") as f:
                    f.write(datos.strip("\n"))
    
    def stop(self):
        self._stop_event.set()
        self.serial_object.close()
        
    def stopped(self):
        return self._stop_event.is_set()




serial_thread = SerialNmeaRead('COM7',38400)
serial_thread.start()

x = input('Enter anything to cancel window:')

serial_thread.stop()
print("Thread stopped.")
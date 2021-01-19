import argparse
from serial_n import SerialNmeaRead


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--port_name", required=True,
                    help="Specification of serial communication port (eg. /dev/ttyACM0)")
    ap.add_argument("-b", "--baudrate", default=38400,
                    help="Serial communication baudrate")
    args = ap.parse_args()

    # Start serial communication
    serial = SerialNmeaRead(args.port_name, args.baudrate)

    serial.start()

    # Wait for ending script
    user_input = ""

    while user_input not in ["q", "quit"]:
        user_input = input("Enter 'q' or 'quit' for cancel script :\n")

    serial.stop()
    print("End of script")

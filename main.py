import argparse
from serial_n import SerialNmeaRead


if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-p", "--port_name", required=True,
                    help="Specification of serial communication port (eg. /dev/ttyACM0)")
    ap.add_argument("-b", "--baudrate", default=38400,
                    help="Serial communication baudrate (default 38400)")
    ap.add_argument("-d", "--directory", default="Test",
                    help='The name of the folder where the data will be stored (default "Test")')
    ap.add_argument("-f", "--ftp", default=None,
                    help="FTP access data, format <server_adress>::<user_name>::<password>")
    args = ap.parse_args()

    if isinstance(args.ftp, str) and len(args.ftp.split("::")) != 3:
        ap.error("Argument FTP isnt in correct format")

    # Start serial communication
    serial = SerialNmeaRead(
        args.directory, args.port_name, args.baudrate,  args.ftp)

    serial.start()

    # Wait for ending script
    user_input = ""

    while user_input not in ["q", "quit"]:
        user_input = input("Enter 'q' or 'quit' for cancel script :\n")

    serial.stop()
    print("End of script")

# TODO: vymazani souboru, aby se nazaplnila pamet

import argparse
import logging
import setproctitle

from serial_n import SerialNmeaRead
from datetime import datetime as dt


setproctitle.setproctitle("GnssLogger")

actual_time = dt.utcnow()

# set up loggers
logger = logging.getLogger(__name__)

for logger_name in [__name__, "serial_n", "rinex_conv", "synchronize_data"]:

    log = logging.getLogger(logger_name)
    log.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=actual_time.strftime(
        "%Y_%m_%d__%H_%M_%S_log.txt"), mode="a", encoding="utf-8")
    formater = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formater)
    log.addHandler(handler)


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
    ap.add_argument("-e", "--erase", default="False",
                    help='Delete log files after FTP synchronization')
    args = ap.parse_args()

    if isinstance(args.ftp, str) and len(args.ftp.split("::")) != 3:
        ap.error("Argument FTP isnt in correct format")

    try:

        # Start serial communication
        serial = SerialNmeaRead(
            args.directory, args.port_name, args.baudrate, args.ftp, True if args.erase.upper() == "TRUE" else False)

        serial.start()
        logger.info("Logger was started")

        # Wait for ending script
        user_input = ""

        while user_input not in ["q", "quit"]:
            user_input = input("Enter 'q' or 'quit' for cancel script :\n")

        serial.stop()
        logger.info("Logger was stoped")

    except Exception as error:
        logger.exception(f"Some eror in GnssLogger :: {error}")

# TODO: vymazani souboru, aby se nazaplnila pamet

import logging
import sys

def SetupLogging(message):
    """
    Sets up logging for the process.
    """
    try:
        logging.basicConfig(
            format="%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%H:%M:%S",
            level=logging.INFO,
            handlers=[
                logging.FileHandler("process.log", mode="w"),
                logging.StreamHandler(sys.stdout)
            ],
            force=True
        )

        logger = logging.getLogger("process")
        logger.info("Process initiated: %s", message)

    except Exception as e:
        print(f"This is an error: {e}")

    return None

import logging

def SetupLogging():

    try:
        logging.basicConfig(level=logging.INFO, filename="process.log", filemode="w")
        logger = logging.getLogger("process")
        logger.setLevel(logging.INFO)
        logging.info('This is a test: %s')

    except Exception as e:
        print(e)
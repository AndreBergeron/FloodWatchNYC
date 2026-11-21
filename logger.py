import logging

def SetupLogging(message):

    try:
        logging.basicConfig(format= "%(asctime)s | %(levelname)s | %(message)s", 
                            datefmt="%H:%M:%S",
                            level=logging.INFO, 
                            filename="process.log", 
                            filemode="w")
        logger = logging.getLogger("process")
        logger.info('Process initiated: %s', message)

    except Exception as e:
        logging.warning('This is an error %s', e)

    return None

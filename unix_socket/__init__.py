import logging

def _init_logger(logger_name="unix_socket.logger", level = logging.DEBUG): 
    log = logging.getLogger(logger_name)
    log.setLevel(level)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',datefmt='%Y/%m/%d %H:%M:%S')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    log.addHandler(console_handler)
    return log

logger = _init_logger()

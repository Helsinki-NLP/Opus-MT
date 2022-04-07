import logging
import os
import sys

def setup_logger(filename, logger_name='bot_logger', logging_dir='./logs/'):
    os.makedirs(logging_dir, exist_ok=True)
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    
    s_handler = logging.StreamHandler(sys.stdout)
    s_handler.setLevel(logging.DEBUG)
    logger.addHandler(s_handler)
    
    f_handler = logging.FileHandler(os.path.join(logging_dir, filename))
    f_handler.setLevel(logging.WARNING)
    f_format = logging.Formatter('[%(asctime)s][%(levelname)s] %(message)s')
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)
    return logger
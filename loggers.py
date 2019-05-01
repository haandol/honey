import logging

level = logging.DEBUG
logger = logging.getLogger('honey')
logger.setLevel(level)

log_file_handler = logging.FileHandler('honey.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
log_file_handler.setFormatter(formatter)
logger.addHandler(log_file_handler)

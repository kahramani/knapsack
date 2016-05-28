import constants
import logging

"""
logger formatter snippet
"""
log_file_name = constants.log_file


def build_logger(source):
    logging.basicConfig(filename=log_file_name,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d:\n%(message)s\n',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    return logging.getLogger(source)

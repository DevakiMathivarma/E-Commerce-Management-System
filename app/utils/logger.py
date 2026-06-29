import logging
import os


# create logs directory

os.makedirs("logs",exist_ok=True)


# logging configuration

logging.basicConfig(level=logging.INFO,format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
                    )


# get logger

def get_logger(name:str):
    return logging.getLogger(name)
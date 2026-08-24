from ..logger import GLOBAL_LOGGER as log

from  src.document_chat.logger.custom_logger import CustomLogger
from src.document_chat.exception.custom_exception import CustomerExpection
import sys
import logging

# logobj=CustomLogger()
# logger=logobj.get_logger(__file__)

def add(a,b):
    log.info("Start:add function started")
    try:
        a=90/0
        print(a)
    except Exception as e:
        #exceptObj=CustomerExpection(ex,sys)
        logging.error(e)
        raise CustomerExpection("Division failed", sys)


    log.info("End: add function started")
    return sum

if __name__=="__main__":
    add(1,3)

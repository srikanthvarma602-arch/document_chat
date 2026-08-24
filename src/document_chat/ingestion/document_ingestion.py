from  src.document_chat.logger.custom_logger import CustomLogger
import logging

logobj=CustomLogger()
logger=logobj.get_logger(__file__)

def add(a,b):
    logger.info("Start:add function started")
    sum=a+b
    logger.info("End: add function started")
    return sum

if __name__=="__main__":
    add(1,3)

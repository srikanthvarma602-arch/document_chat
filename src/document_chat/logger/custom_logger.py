import os
import logging
from datetime import datetime
import structlog

class CustomLogger():
    def __init__(self):
        # 1 create path
        self.LOG_FOLDER=os.path.join(os.getcwd(),"logs")
        os.makedirs(self.LOG_FOLDER,exist_ok=True)
        self.LOG_FILE_NAME=f"{datetime.now().strftime('%d_%m_%y')}.log"
        self.LOG_FILE_PATH=os.path.join(self.LOG_FOLDER,self.LOG_FILE_NAME)


    def get_logger(self,name=__file__):
        log_name=os.path.basename(name)
        file_handler=logging.FileHandler(self.LOG_FILE_PATH)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))

        console_handle=logging.StreamHandler()
        console_handle.setLevel(logging.INFO)
        console_handle.setFormatter(logging.Formatter("%(message)s"))

        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[file_handler,console_handle]
        )

        #Config Structlog for Json structred log
        structlog.configure(
            processors=[
                structlog.processors.TimeStamper(fmt="iso",utc=True,key="timestamp"),
                structlog.processors.add_log_level,
                structlog.processors.EventRenamer(to="event"),
                structlog.processors.JSONRenderer()
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        return structlog.getLogger(log_name)


if __name__== "__main__":
    logger_obj=CustomLogger()
    logger=logger_obj.get_logger(__file__)
    logger.info("i am customer logger bro")



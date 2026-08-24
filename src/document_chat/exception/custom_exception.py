import sys
import traceback
from typing import Optional
import structlog

class CustomerExpection(Exception):
    def __init__(self,error_message,err_detail:Optional[object]=None):
        # normaize message
        noraml_messgae=str(error_message)

        # checking expection type
        exc_type=exc_value=exc_tb=None
        if err_detail is None: #CustomerExpection("Division failed")
            exc_type,exc_value,exc_tb=sys.exc_info()
        else:
            if hasattr(err_detail,"exc_info"): #CustomerExpection("Division failed",sys)
                exc_type,exc_value,exc_tb=err_detail.exc_info()
            elif isinstance(err_detail,BaseException):  #CustomerExpection("Division failed",e)
                exc_type,exc_value,exc_tb=type(err_detail),err_detail,err_detail.__traceback__
            else:
                exc_type,exc_value,exc_tb=sys.exc_info()

        # walk through last trace bak
        last_tb=exc_tb
        while last_tb and last_tb.tb_next:
            last_tb=last_tb.tb_next

        #setting all properities from lasttrace bak
        self.fileName=last_tb.tb_frame.f_code.co_filename
        self.lineno=last_tb.tb_lineno
        self.errorMessage=noraml_messgae

        if exc_type and exc_tb:
            self.trace_back_str=''.join(traceback.format_exception(*sys.exc_info()))
        else:
            self.trace_back_str=""

        super().__init__(self.__str__())

        # _,_,trace_back=sys.exc_info()
        # self.trace_back_str=''.join(traceback.format_exception(*sys.exc_info()))
        # self.fileName=trace_back.tb_frame.f_code.co_filename
        # self.lineno=trace_back.tb_lineno
        # self.errorMessage=error_message


    def __str__(self):
        #dunder
        return f"""
            Error in [{self.fileName}] at line [{self.lineno}]
            Message:{self.errorMessage}
            TraceBook:{self.trace_back_str}
            """

from datetime import datetime
from core.Fail import fail
from core.Printer import Printer
from core.Expression import Expression


class Logger:
    def __init__ (self, function, expression, call_stack, variables):
        self.function = function
        self.expression = expression
        self.call_stack = call_stack 
        self.variables = variables
        self.error_type = "Log Error"


    def log(self):
        log_message = self.log_switch()
        if log_message == False:
            fail("Invalid log method.", self.error_type, self.call_stack)
        log_message.print()


    def log_switch(self):
        return {
            "log" : self.log_info(),
            "logWarn" : self.log_warn(),
            "logSuccess" : self.log_success(),
            "logError" : self.log_error()
        }.get(self.function, False)


    def log_info(self):
        info_printer = Printer("printCyan", '"INFO [' + str(datetime.now())[:-7] + ']" . " " . ' + self.expression, 
        self.call_stack, self.variables)
        return info_printer


    def log_warn(self):
        warn_printer = Printer("printYellow", '"WARN [' + str(datetime.now())[:-7] + ']" . " " . ' + self.expression, 
        self.call_stack, self.variables)
        return warn_printer


    def log_success(self):
        success_printer = Printer("printGreen", '"SUCCESS [' + str(datetime.now())[:-7] + ']" . " " . ' + self.expression, 
        self.call_stack, self.variables)
        return success_printer

    
    def log_error(self):
        error_printer = Printer("printRed", '"ERROR [' + str(datetime.now())[:-7] + ']" . " " . ' + self.expression, 
        self.call_stack, self.variables)
        return error_printer


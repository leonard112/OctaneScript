class Line:
    def __init__ (self, line, line_number, file_name):
        self.line = line
        self.line_number = line_number
        self.file_name = file_name

    
    def get_line_info(self):
        if self.line_number == None:
            return self.file_name + ": " + self.line
        return self.file_name + " (" + str(self.line_number + 1) + "): " + self.line 
        

    def get_line(self):
        return self.line
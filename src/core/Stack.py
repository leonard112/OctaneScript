from core.Line import Line

class Stack:
    def __init__ (self):
        self.stack = []

    def push(self, line):
        self.stack.append(line)
    def pop(self):
        return self.stack.pop()
    def peek(self):
        try:
            return self.stack[-1]
        except:
            return None
    def get_stack(self):
        return self.stack

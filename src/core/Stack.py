from core.Line import Line

class Stack:
    def __init__ (self):
        self.stack = []

    def push(self, line):
        self.stack.append(line)
    def pop(self):
        return self.stack.pop()
    def peek(self):
        return self.stack[-1]
    def get_stack(self):
        return self.stack

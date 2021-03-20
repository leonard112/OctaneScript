# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

class Stack:
    def __init__ (self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)
    def pop(self):
        return self.stack.pop()
    def peek(self):
        try:
            return self.stack[-1]
        except:
            return None
    def get_stack(self):
        return self.stack

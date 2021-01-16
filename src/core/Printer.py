# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

from colors import color
from core.Fail import fail
from core.Expression import Expression

class Printer:
    def __init__ (self, function, expression, call_stack, variables):
        self.function = function
        self.expression = expression
        self.call_stack = call_stack 
        self.variables = variables
        self.error_type = "Print Error"


    def print(self):
        expression = Expression(self.expression, self.call_stack, self.variables)
        self.expression = str(expression.evaluate())
        
        if self.expression == "True" or self.expression == "False":
            self.expression = self.expression.lower()

        self.expression = self.print_switch()
        if self.expression != False:
            print(self.expression)
        else:
            fail("Bad print function.", self.error_type, self.call_stack)
            

    def print_switch(self):
        return {
            # Normal
            "print" : self.expression,
            "printRed" : color(self.expression, fg='red'),
            "printGreen" : color(self.expression, fg='green'),
            "printBlue" : color(self.expression, fg='blue'),
            "printYellow" : color(self.expression, fg='yellow'),
            "printCyan" : color(self.expression, fg='cyan'),
            "printMagenta" : color(self.expression, fg='magenta'),
            "printWhite" : color(self.expression, fg='white'),
            "printBlack" : color(self.expression, fg='black'),
            # Bold
            "printBold" : color(self.expression, style="bold"),
            "printRedBold" : color(self.expression, fg='red', style="bold"),
            "printGreenBold" : color(self.expression, fg='green', style="bold"),
            "printBlueBold" : color(self.expression, fg='blue', style="bold"),
            "printYellowBold" : color(self.expression, fg='yellow', style="bold"),
            "printCyanBold" : color(self.expression, fg='cyan', style="bold"),
            "printMagentaBold" : color(self.expression, fg='magenta', style="bold"),
            "printWhiteBold" : color(self.expression, fg='white', style="bold"),
            "printBlackBold" : color(self.expression, fg='black', style="bold"),
            # Italic
            "printItalic" : color(self.expression, style="italic"),
            "printRedItalic" : color(self.expression, fg='red', style="italic"),
            "printGreenItalic" : color(self.expression, fg='green', style="italic"),
            "printBlueItalic" : color(self.expression, fg='blue', style="italic"),
            "printYellowItalic" : color(self.expression, fg='yellow', style="italic"),
            "printCyanItalic" : color(self.expression, fg='cyan', style="italic"),
            "printMagentaItalic" : color(self.expression, fg='magenta', style="italic"),
            "printWhiteItalic" : color(self.expression, fg='white', style="italic"),
            "printBlackItalic" : color(self.expression, fg='black', style="italic"),
            # Underline
            "printUnderline" : color(self.expression, style="underline"),
            "printRedUnderline" : color(self.expression, fg='red', style="underline"),
            "printGreenUnderline" : color(self.expression, fg='green', style="underline"),
            "printBlueUnderline" : color(self.expression, fg='blue', style="underline"),
            "printYellowUnderline" : color(self.expression, fg='yellow', style="underline"),
            "printCyanUnderline" : color(self.expression, fg='cyan', style="underline"),
            "printMagentaUnderline" : color(self.expression, fg='magenta', style="underline"),
            "printWhiteUnderline" : color(self.expression, fg='white', style="underline"),
            "printBlackUnderline" : color(self.expression, fg='black', style="underline"),
            # Negative
            "printNegative" : color(self.expression, style="negative"),
            "printRedNegative" : color(self.expression, fg='red', style="negative"),
            "printGreenNegative" : color(self.expression, fg='green', style="negative"),
            "printBlueNegative" : color(self.expression, fg='blue', style="negative"),
            "printYellowNegative" : color(self.expression, fg='yellow', style="negative"),
            "printCyanNegative" : color(self.expression, fg='cyan', style="negative"),
            "printMagentaNegative" : color(self.expression, fg='magenta', style="negative"),
            "printWhiteNegative" : color(self.expression, fg='white', style="negative"),
            "printBlackNegative" : color(self.expression, fg='black', style="negative"),
            # Concealed
            "printConcealed" : color(self.expression, style="concealed"),
            "printRedConcealed" : color(self.expression, fg='red', style="concealed"),
            "printGreenConcealed" : color(self.expression, fg='green', style="concealed"),
            "printBlueConcealed" : color(self.expression, fg='blue', style="concealed"),
            "printYellowConcealed" : color(self.expression, fg='yellow', style="concealed"),
            "printCyanConcealed" : color(self.expression, fg='cyan', style="concealed"),
            "printMagentaConcealed" : color(self.expression, fg='magenta', style="concealed"),
            "printWhiteConcealed" : color(self.expression, fg='white', style="concealed"),
            "printBlackConcealed" : color(self.expression, fg='black', style="concealed"),
            # Crossed
            "printCrossed" : color(self.expression, style="crossed"),
            "printRedCrossed" : color(self.expression, fg='red', style="crossed"),
            "printGreenCrossed" : color(self.expression, fg='green', style="crossed"),
            "printBlueCrossed" : color(self.expression, fg='blue', style="crossed"),
            "printYellowCrossed" : color(self.expression, fg='yellow', style="crossed"),
            "printCyanCrossed" : color(self.expression, fg='cyan', style="crossed"),
            "printMagentaCrossed" : color(self.expression, fg='magenta', style="crossed"),
            "printWhiteCrossed" : color(self.expression, fg='white', style="crossed"),
            "printBlackCrossed" : color(self.expression, fg='black', style="crossed"),
        }.get(self.function, False)
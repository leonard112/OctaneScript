from colors import color
from core.Fail import fail
from core.Expression import Expression

class Printer:
    def __init__ (self, function, message, line, variables):
        self.function = function
        self.message = message
        self.line = line 
        self.variables = variables
        self.error_type = "Print Error"

    def print(self):
        expression = Expression(self.message, self.line, self.variables)
        self.message = expression.evaluate()

        self.message = self.print_switch()
        if self.message != False:
            print(self.message)
        else:
            fail("Bad print function.", self.error_type, self.line)

    def print_switch(self):
        return {
            # Normal
            "print" : self.message,
            "printRed" : color(self.message, fg='red'),
            "printGreen" : color(self.message, fg='green'),
            "printBlue" : color(self.message, fg='blue'),
            "printYellow" : color(self.message, fg='yellow'),
            "printCyan" : color(self.message, fg='cyan'),
            "printMagenta" : color(self.message, fg='magenta'),
            "printWhite" : color(self.message, fg='white'),
            "printBlack" : color(self.message, fg='black'),
            # Bold
            "printBold" : color(self.message, style="bold"),
            "printRedBold" : color(self.message, fg='red', style="bold"),
            "printGreenBold" : color(self.message, fg='green', style="bold"),
            "printBlueBold" : color(self.message, fg='blue', style="bold"),
            "printYellowBold" : color(self.message, fg='yellow', style="bold"),
            "printCyanBold" : color(self.message, fg='cyan', style="bold"),
            "printMagentaBold" : color(self.message, fg='magenta', style="bold"),
            "printWhiteBold" : color(self.message, fg='white', style="bold"),
            "printBlackBold" : color(self.message, fg='black', style="bold"),
            # Italic
            "printItalic" : color(self.message, style="italic"),
            "printRedItalic" : color(self.message, fg='red', style="italic"),
            "printGreenItalic" : color(self.message, fg='green', style="italic"),
            "printBlueItalic" : color(self.message, fg='blue', style="italic"),
            "printYellowItalic" : color(self.message, fg='yellow', style="italic"),
            "printCyanItalic" : color(self.message, fg='cyan', style="italic"),
            "printMagentaItalic" : color(self.message, fg='magenta', style="italic"),
            "printWhiteItalic" : color(self.message, fg='white', style="italic"),
            "printBlackItalic" : color(self.message, fg='black', style="italic"),
            # Underline
            "printUnderline" : color(self.message, style="underline"),
            "printRedUnderline" : color(self.message, fg='red', style="underline"),
            "printGreenUnderline" : color(self.message, fg='green', style="underline"),
            "printBlueUnderline" : color(self.message, fg='blue', style="underline"),
            "printYellowUnderline" : color(self.message, fg='yellow', style="underline"),
            "printCyanUnderline" : color(self.message, fg='cyan', style="underline"),
            "printMagentaUnderline" : color(self.message, fg='magenta', style="underline"),
            "printWhiteUnderline" : color(self.message, fg='white', style="underline"),
            "printBlackUnderline" : color(self.message, fg='black', style="underline"),
            # Negative
            "printNegative" : color(self.message, style="negative"),
            "printRedNegative" : color(self.message, fg='red', style="negative"),
            "printGreenNegative" : color(self.message, fg='green', style="negative"),
            "printBlueNegative" : color(self.message, fg='blue', style="negative"),
            "printYellowNegative" : color(self.message, fg='yellow', style="negative"),
            "printCyanNegative" : color(self.message, fg='cyan', style="negative"),
            "printMagentaNegative" : color(self.message, fg='magenta', style="negative"),
            "printWhiteNegative" : color(self.message, fg='white', style="negative"),
            "printBlackNegative" : color(self.message, fg='black', style="negative"),
            # Concealed
            "printConcealed" : color(self.message, style="concealed"),
            "printRedConcealed" : color(self.message, fg='red', style="concealed"),
            "printGreenConcealed" : color(self.message, fg='green', style="concealed"),
            "printBlueConcealed" : color(self.message, fg='blue', style="concealed"),
            "printYellowConcealed" : color(self.message, fg='yellow', style="concealed"),
            "printCyanConcealed" : color(self.message, fg='cyan', style="concealed"),
            "printMagentaConcealed" : color(self.message, fg='magenta', style="concealed"),
            "printWhiteConcealed" : color(self.message, fg='white', style="concealed"),
            "printBlackConcealed" : color(self.message, fg='black', style="concealed"),
            # Crossed
            "printCrossed" : color(self.message, style="crossed"),
            "printRedCrossed" : color(self.message, fg='red', style="crossed"),
            "printGreenCrossed" : color(self.message, fg='green', style="crossed"),
            "printBlueCrossed" : color(self.message, fg='blue', style="crossed"),
            "printYellowCrossed" : color(self.message, fg='yellow', style="crossed"),
            "printCyanCrossed" : color(self.message, fg='cyan', style="crossed"),
            "printMagentaCrossed" : color(self.message, fg='magenta', style="crossed"),
            "printWhiteCrossed" : color(self.message, fg='white', style="crossed"),
            "printBlackCrossed" : color(self.message, fg='black', style="crossed"),
        }.get(self.function, False)
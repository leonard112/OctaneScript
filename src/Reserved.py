# This file is licensed under the MIT license.
# See license for more details: https://github.com/leonard112/OctaneScript/blob/main/README.md

reserved = [
    # PRINT
    "print", "printRed", "printGreen", "printBlue", "printCyan", 
    "printYellow", "printMagenta", "printWhite", "printBlack",
    
    "printBold", "printRedBold", "printGreenBold", "printBlueBold", "printCyanBold", 
    "printYellowBold", "printMagentaBold", "printWhiteBold", "printBlackBold",
    
    "printItalic", "printRedItalic", "printGreenItalic", "printBlueItalic", "printCyanItalic", 
    "printYellowItalic", "printMagentaItalic", "printWhiteItalic", "printBlackItalic",
    
    "printUnderline", "printRedUnderline", "printGreenUnderline", "printBlueUnderline", "printCyanUnderline",
    "printYellowUnderline", "printMagentaUnderline", "printWhiteUnderline", "printBlackUnderline",
    
    "printNegative", "printRedNegative", "printGreenNegative", "printBlueNegative", "printCyanNegative",
     "printYellowNegative", "printMagentaNegative", "printWhiteNegative", "printBlackNegative",
    
    "printConcealed", "printRedConcealed", "printGreenConcealed", "printBlueConcealed", "printCyanConcealed",
    "printYellowConcealed", "printMagentaConcealed", "printWhiteConcealed", "printBlackConcealed",

    # LOG
    "log", "logWarn", "logSuccess", "logError",
    
    # SET
    "set", "input", "randomDecimal", "randomInteger", "to",

    # SLEEP
    "sleep",

    # EXIT
    "exit",

    # CONDITIONAL
    "if", "elseIf", "else", "end",

    # BOOLEAN
    "lessThanEquals", "greaterThanEquals", "lessThan", "greaterThan", "equals", "notEquals", 
    "and", "or", "true", "false",

    # FUNCTION
    "function", "return",

    # LOOPS
    "repeat", "while", "counter", "step", "start", "for"

    # ARRAYS
    "append", "push", "prepend", "removeFirst", "removeLast", "remove"
    "peek", "start", "end", "first", "last"
]
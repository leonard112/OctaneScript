import unittest
import sys
sys.path.append("../..")
from core.Printer import Printer

valid_print_functions = [
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
]

class TestPrinter (unittest.TestCase):

    # replacing quotes with invalid characters fails
    def test_first_quote_replaced_with_parenthesis_fails(self):
        p = Printer("print", "\"invalid)", "non-exitant.o")
        self.assertFalse(p.syntax_check())
    def test_second_quote_replaced_with_parenthesis_fails(self):
        p = Printer("print", "(invalid\"", "non-exitant.o")
        self.assertFalse(p.syntax_check())
    def test_parentheses_instead_of_quotes_fails(self):
        p = Printer("print", "(invalid)", "non-exitant.o")
        self.assertFalse(p.syntax_check())

    # missing quotes fails
    def test_first_quote_missing_fails(self):
        p = Printer("print", "invalid\"", "non-exitant.o")
        self.assertFalse(p.syntax_check())
    def test_second_quote_missing_fails(self):
        p = Printer("print", "\"invalid", "non-exitant.o")
        self.assertFalse(p.syntax_check())
    def test_no_quotes_fails(self):
        p = Printer("print", "invalid", "non-exitant.o")
        self.assertFalse(p.syntax_check())
    
    # leading and trailing whitespace fails
    def test_valid_with_leading_whitespace_fails(self):
        p = Printer("print", " \"invalid\"", "non-exitant.o")
        self.assertFalse(p.syntax_check())
    def test_valid_with_trailing_whitespace_fails(self):
        p = Printer("print", "\"invalid\" ", "non-exitant.o")
        self.assertFalse(p.syntax_check())
    def test_valid_with_trailing_and_leading_whitespace_fails(self):
        p = Printer("print", " \"invalid\" ", "non-exitant.o")
        self.assertFalse(p.syntax_check())

    # Valid syntax is successful
    def test_double_quotes_good(self):
        p = Printer("print", "\"good\"", "non-exitant.o")
        self.assertTrue(p.syntax_check())
    def test_single_quotes_good(self):
        p = Printer("print", "'good'", "non-exitant.o")
        self.assertTrue(p.syntax_check())
    def test_nothing_good(self):
        p = Printer("print", "", "non-exitant.o")
        self.assertTrue(p.syntax_check())

    def test_invalid_functions_fail(self):
        p = Printer("invalid", "\"bad function\"", "non-exitant.o")
        
    def test_all_valid_functions_work(self):
        for function in valid_print_functions:
            p = Printer(function, "\"good\"", "non-exitant.o")
            self.assertNotEqual(p.print_switch(), False)

if __name__ == '__main__':
    unittest.main()
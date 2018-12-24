import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestConditionalStatements(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/conditionalstmts.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="conditionalstatement",debug=True)
                
        def test_1(self):
                self._frontend.parse("if STATEMENT, STATEMENT")
                self._frontend.parse("STATEMENT only if STATEMENT")
        
        def test_2(self):
                self._frontend.parse("whenever STATEMENT TIMEEXPRESSION, STATEMENT")
                self._frontend.parse("STATEMENT whenever STATEMENT TIMEEXPRESSION")

        def test_3(self):
                self._frontend.parse("when STATEMENT, STATEMENT")
                self._frontend.parse("STATEMENT when STATEMENT")

        def test_4(self):
                self._frontend.parse("at TIMEEXPRESSION, STATEMENT")

        def test_5(self):
                self._frontend.parse("as long as STATEMENT, STATEMENT")
                self._frontend.parse("STATEMENT for as long as STATEMENT")
        
        def test_6(self):
                self._frontend.parse("for each time STATEMENT beyond the first, STATEMENT")
                self._frontend.parse("for each GENERICDECLARATIONEXPRESSION, STATEMENT")
                self._frontend.parse("STATEMENT for each GENERICDECLARATIONEXPRESSION")
                
        def test_7(self):
                self._frontend.parse("until TIMEEXPRESSION, STATEMENT")
                self._frontend.parse("STATEMENT until TIMEEXPRESSION")
                
        def test_8(self):
                self._frontend.parse("after TIMEEXPRESSION, STATEMENT")
                self._frontend.parse("STATEMENT after TIMEEXPRESSION")
                
        def test_9(self):
                self._frontend.parse("otherwise, STATEMENT")
                
        def test_10(self):
                self._frontend.parse("STATEMENT unless STATEMENT")
                
        def test_11(self):
                self._frontend.parse("while STATEMENT, STATEMENT")
                
        def test_12(self):
                self._frontend.parse("STATEMENT during TIMEEXPRESSION")
                self._frontend.parse("STATEMENT only during TIMEEXPRESSION")
                
        def test_13(self):
                self._frontend.parse("STATEMENT except by GENERICDECLARATIONEXPRESSION")
                self._frontend.parse("STATEMENT except STATEMENT")
                
        def test_14(self):
                self._frontend.parse("STATEMENT rather than STATEMENT")
                
        def test_14(self):
                self._frontend.parse("STATEMENT rather than STATEMENT")
                
        def test_15(self):
                self._frontend.parse("the next time STATEMENT TIMEEXPRESSION, STATEMENT")
                
        def test_16(self):
                self._frontend.parse("STATEMENT before TIMEEXPRESSION")
                self._frontend.parse("STATEMENT before STATEMENT")
        
if __name__ == '__main__':
        unittest.main()
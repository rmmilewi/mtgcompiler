import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestConditionalStatements(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/conditionalstmts.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="conditionalstatement",debug=True)
                
        def test_if(self):
                self._frontend.parse("if STATEMENT, STATEMENT")
                self._frontend.parse("STATEMENT only if STATEMENT")
        
        def test_whenever(self):
                self._frontend.parse("whenever STATEMENT TIMEEXPRESSION, STATEMENT")
                self._frontend.parse("STATEMENT whenever STATEMENT TIMEEXPRESSION")

        def test_when(self):
                self._frontend.parse("when STATEMENT, STATEMENT")
                self._frontend.parse("STATEMENT when STATEMENT")

        def test_at(self):
                self._frontend.parse("at TIMEEXPRESSION, STATEMENT")

        def test_aslongas(self):
                self._frontend.parse("as long as STATEMENT, STATEMENT")
                self._frontend.parse("STATEMENT for as long as STATEMENT")
        
        def test_foreach(self):
                self._frontend.parse("for each time STATEMENT beyond the first, STATEMENT")
                self._frontend.parse("for each ENTITY, STATEMENT")
                self._frontend.parse("STATEMENT for each ENTITY")
                
        def test_until(self):
                self._frontend.parse("until TIMEEXPRESSION, STATEMENT")
                self._frontend.parse("STATEMENT until TIMEEXPRESSION")
                
        def test_after(self):
                self._frontend.parse("after TIMEEXPRESSION, STATEMENT")
                self._frontend.parse("STATEMENT after TIMEEXPRESSION")
                
        def test_otherwise(self):
                self._frontend.parse("otherwise, STATEMENT")
                
        def test_unless(self):
                self._frontend.parse("STATEMENT unless STATEMENT")
                
        def test_while(self):
                self._frontend.parse("while STATEMENT, STATEMENT")
                
        def test_during(self):
                self._frontend.parse("STATEMENT during TIMEEXPRESSION")
                self._frontend.parse("STATEMENT only during TIMEEXPRESSION")
                
        def test_except(self):
                self._frontend.parse("STATEMENT except by ENTITY")
                self._frontend.parse("STATEMENT except STATEMENT")
                
        def test_rather(self):
                self._frontend.parse("STATEMENT rather than STATEMENT")
                
        def test_nexttime(self):
                self._frontend.parse("the next time STATEMENT TIMEEXPRESSION, STATEMENT")
                
        def test_before(self):
                self._frontend.parse("STATEMENT before TIMEEXPRESSION")
                self._frontend.parse("STATEMENT before STATEMENT")
                
        def test_then(self):
                self._frontend.parse("STATEMENT before TIMEEXPRESSION")
                self._frontend.parse("then STATEMENT")
        
if __name__ == '__main__':
        unittest.main()
import unittest
import mtgcompiler.frontend.grammarian.grammarian as grammarian
from lark import Lark #Lexing and parsing!

class TestTimeExpressions(unittest.TestCase):
        
        @classmethod
        def setUpClass(cls):
                options = {"devDefineMissingNames" : True}
                grammar = grammarian.requestGrammar(imports=["base/timeexpressions.grm","base/common.grm"],options=options)
                cls._frontend = Lark(grammar,parser="lalr",start="timeexpression",debug=True)
                
        def test_1(self):
                self._frontend.parse("the beginning of POSSESSIVE upkeep")
        
        def test_2(self):
                self._frontend.parse("end of turn")

        def test_3(self):
                self._frontend.parse("REFERENCEDECORATOR upkeep")

        def test_4(self):
                self._frontend.parse("REFERENCEDECORATOR extra declare blockers step")

        def test_5(self):
                self._frontend.parse("additional turn")

        def test_6(self):
                self._frontend.parse("the beginning of REFERENCEDECORATOR game")

        def test_7(self):
                self._frontend.parse("the beginning of REFERENCEDECORATOR next end step")
                
if __name__ == '__main__':
        unittest.main()
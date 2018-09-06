import unittest

from mtgcompiler.AST.expressions import MgAllExpression
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType

class TestAttributeTracking(unittest.TestCase):
        
        def test_MarkingWithAttributes(self):
                allExpr = MgAllExpression(MgType(MgType.TypeEnum.Creature))
                
                self.assertFalse(allExpr.hasAttribute("pluralFlag"))
                
                allExpr.setAttribute("pluralFlag",True)
                
                self.assertTrue(allExpr.hasAttribute("pluralFlag"))
                self.assertEqual(allExpr.getAttribute("pluralFlag"),True)
                
                
if __name__ == '__main__':
        unittest.main()

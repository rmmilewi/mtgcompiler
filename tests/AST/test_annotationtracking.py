import unittest

from mtgcompiler.frontend.AST.expressions import MgAllExpression
from mtgcompiler.frontend.AST.mtypes import MgSupertype,MgSubtype,MgType

class TestAnnotationTracking(unittest.TestCase):
        
        def test_MarkingWithAnnotations(self):
                allExpr = MgAllExpression(MgType(MgType.TypeEnum.Creature))
                
                self.assertFalse(allExpr.hasAnnotation("pluralFlag"))
                
                allExpr.setAnnotation("pluralFlag",True)
                
                self.assertTrue(allExpr.hasAnnotation("pluralFlag"))
                self.assertEqual(allExpr.getAnnotation("pluralFlag"),True)
                
                
if __name__ == '__main__':
        unittest.main()

import unittest
import mtgcompiler.AST.expressions
import mtgcompiler.AST.mtypes

class TestMagicExpressions(unittest.TestCase):
	
	def test_TypeExpressions(self):
		t_legendary = mtgcompiler.AST.mtypes.MgSupertype(mtgcompiler.AST.mtypes.MgSupertype.SupertypeEnum.Legendary)
		t_human = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Human)
		t_cleric = mtgcompiler.AST.mtypes.MgSubtype(mtgcompiler.AST.mtypes.MgSubtype.CreatureSubtypeEnum.Cleric)
		
		texpr = mtgcompiler.AST.expressions.MgTypeExpression(t_legendary,t_human,t_cleric)
		
		self.assertTrue(t_legendary.isTraversable())
		self.assertEqual(len(texpr.getTraversalSuccessors()),3)
		
		self.assertTrue(texpr.isChild(t_legendary))
		self.assertEqual(t_legendary.getParent(),texpr)
		
		self.assertEqual(texpr.unparseToString(),"Legendary Human Cleric")
		


if __name__ == '__main__':
    unittest.main()
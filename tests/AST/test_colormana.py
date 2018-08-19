import unittest
from mtgcompiler.AST.colormana import MgManaSymbol

class TestColorsAndManaSymbols(unittest.TestCase):
        
        def test_SimpleColorManaSymbols(self):
                whiteSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.White)
                self.assertEqual(whiteSymbol.unparseToString(),"{W}")
                
                blueSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Blue)
                self.assertEqual(blueSymbol.unparseToString(),"{U}")
                
                blackSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Black)
                self.assertEqual(blackSymbol.unparseToString(),"{B}")
                
                redSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Red)
                self.assertEqual(redSymbol.unparseToString(),"{R}")
                
                greenSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Green)
                self.assertEqual(greenSymbol.unparseToString(),"{G}")
        
        def testGenericManaSymbols(self):
                zeroSymbol = MgManaSymbol(colorv=None,modifiers=None,cvalue=0)
                self.assertEqual(zeroSymbol.unparseToString(),"{0}")
                
                eightSymbol = MgManaSymbol(colorv=None,modifiers=None,cvalue=8)
                self.assertEqual(eightSymbol.unparseToString(),"{8}")
                
                xSymbol = MgManaSymbol(colorv=None,modifiers=None,cvalue="X")
                self.assertEqual(xSymbol.unparseToString(),"{X}")
                
                infinitySymbol = MgManaSymbol(colorv=None,modifiers=None,cvalue="∞")
                self.assertEqual(infinitySymbol.unparseToString(),"{∞}")
                
        def testHybridManaSymbols(self):
                #This test is currently failing. I'm not fully understanding why the canonical order
                #for hybrid mana symbols is the way that it is.
                
                #Allied hybrid symbols
                gwSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Green | MgManaSymbol.ManaType.White)
                self.assertEqual(gwSymbol.unparseToString(),"{G/W}")
                
                wuSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.White | MgManaSymbol.ManaType.Blue)
                self.assertEqual(gwSymbol.unparseToString(),"{W/U}")
                
                ubSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Blue | MgManaSymbol.ManaType.Black)
                self.assertEqual(gwSymbol.unparseToString(),"{U/B}")
                
                brSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Black | MgManaSymbol.ManaType.Red)
                self.assertEqual(gwSymbol.unparseToString(),"{B/R}")
                
                rgSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Red | MgManaSymbol.ManaType.Green)
                self.assertEqual(rgSymbol.unparseToString(),"{R/G}")
                
                #Enemy allied symbols
                wbSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.White | MgManaSymbol.ManaType.Black)
                self.assertEqual(wbSymbol.unparseToString(),"{W/B}")
                
                urSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Blue | MgManaSymbol.ManaType.Red)
                self.assertEqual(urSymbol.unparseToString(),"{U/R}")
                
                bgSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Black | MgManaSymbol.ManaType.Green)
                self.assertEqual(bgSymbol.unparseToString(),"{B/G}")
                
                guSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Green | MgManaSymbol.ManaType.Blue)
                self.assertEqual(bgSymbol.unparseToString(),"{G/U}")
                
                rwSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Red | MgManaSymbol.ManaType.White)
                self.assertEqual(bgSymbol.unparseToString(),"{R/W}")
                
        def testModifiedSymbols(self):
                snowSymbol = MgManaSymbol(modifiers=MgManaSymbol.ManaModifier.Snow)
                self.assertEqual(snowSymbol.unparseToString(),"{S}")
                
                phyrexianBlueSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Blue,modifiers=MgManaSymbol.ManaModifier.Phyrexian)
                self.assertEqual(phyrexianBlueSymbol.unparseToString(),"{U/P}")
                
                halfWhiteSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.White,modifiers=MgManaSymbol.ManaModifier.Half)
                self.assertEqual(halfWhiteSymbol.unparseToString(),"{HW}")
                
                redAlternateTwoSymbol = MgManaSymbol(colorv=MgManaSymbol.ManaType.Red,modifiers=MgManaSymbol.ManaModifier.AlternateTwo)
                self.assertEqual(halfWhiteSymbol.unparseToString(),"{R/2}")
                

if __name__ == '__main__':
    unittest.main()
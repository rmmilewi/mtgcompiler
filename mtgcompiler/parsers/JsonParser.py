from mtgcompiler.parsers.baseparser import BaseParser
from mtgcompiler.AST.reference import MgName
from mtgcompiler.AST.card import MgTypeLine,MgFlavorText,MgTextBox,MgCard
from mtgcompiler.AST.mtypes import MgSupertype,MgSubtype,MgType
from mtgcompiler.AST.colormana import MgManaSymbol,MgColorTerm
from mtgcompiler.AST.expressions import MgNumberValue,MgPTExpression,MgManaExpression,MgTypeExpression

class JsonParser(BaseParser):

        def __init__(self):
                pass
        
        def parse(self,cardinput):
                """The parse method for JsonParser takes a Json dict in MtgJson format.
                For reference, this is an example card in that format:
                
                {'artist': 'Steve Prescott', 
                'cmc': 4, 
                'colorIdentity': ['W'], 
                'colors': ['White'], 
                'flavor': "Thanks to one champion archer, the true borders of Kinsbaile extend an arrow's flight beyond the buildings.",
                'id': '20f7ec0882ea342c284730e7e387c3d517a7c7f7',
                'imageName': 'brigid, hero of kinsbaile',
                'layout': 'normal',
                'manaCost': '{2}{W}{W}',
                'mciNumber': '6',
                'multiverseid': 141829,
                'name': 'Brigid, Hero of Kinsbaile',
                'number': '6',
                'power': '2',
                'rarity': 'Rare',
                'subtypes':['Kithkin', 'Archer'],
                'supertypes': ['Legendary'],
                'text': 'First strike\n{T}: Brigid, Hero of Kinsbaile deals 2 damage to each attacking or blocking creature target player controls.',
                'toughness': '3',
                'type': 'Legendary Creature — Kithkin Archer',
                'types': ['Creature']}
                """
                #TODO: Eventually we'll support non-standard layouts.
                
                if 'name' in cardinput:
                        cardName = MgName(cardinput['name'])
                else:
                        cardName = MgName()
                        
                if 'manaCost' in cardinput:
                        manaCost = MgManaExpression() #TODO
                else:
                        manaCost = MgManaExpression()
                        
                #TODO: apparently the MtgJson format doesn't explicitly list color indicators. 
                colorIndicator = None
                
                if 'type' in cardinput:
                        if 'supertypes' in cardinput:
                                supertypes = MgTypeExpression() #TODO
                        else:
                                supertypes = MgTypeExpression()
                        if 'types' in cardinput:
                                types = MgTypeExpression() #TODO
                        else:
                                types = MgTypeExpression()
                        if 'subtypes' in cardinput:
                                subtypes = MgTypeExpression() #TODO
                        else:
                                subtypes = MgTypeExpression()
                        typeLine = MgTypeLine(supertypes=supertypes,types=types,subtypes=subtypes)
                else:
                        typeLine = MgTypeLine()
                        
                        
                if 'loyalty' in cardinput:
                        loyalty = None #TODO
                else:
                        loyalty = None
                        
                if 'power' in cardinput or 'toughness' in cardinput:
                        #I think it's reasonable to expect both to be there.
                        #TODO: This will fail for non-integer power/toughness values, like 1+*.
                        #I'll fix this later.
                        power = MgNumberValue(int(cardinput['power']),MgNumberValue.NumberTypeEnum.Literal)
                        toughness = MgNumberValue(int(cardinput['toughness']),MgNumberValue.NumberTypeEnum.Literal)
                        powerToughness = MgPTExpression(power,toughness)
                else:
                        powerToughness = None
                        
                if 'text' in cardinput:
                        textBox = MgTextBox() #TODO
                else:
                        textBox = MgTextBox()
                        
                if 'life' in cardinput:
                        lifeModifier = None #TODO
                else:
                        lifeModifier = None
                        
                if 'hand' in cardinput:
                        handModifier = None #TODO
                else:
                        handModifier = None
                        
                if 'flavor' in cardinput:
                        flavor = MgFlavorText(cardinput['flavor'])
                else:
                        flavor = None
                        
                card = MgCard(**{
                        "name" : cardName,
                        "manaCost" : manaCost,
                        "colorIndicator" : colorIndicator,
                        "typeLine" : typeLine,
                        "loyalty" : loyalty,
                        "powerToughness": powerToughness,
                        "textBox" : textBox,
                        "lifeModifier" : lifeModifier,
                        "handModifier" : handModifier,
                        "flavor" : flavor
                })
                
                return card
                
                
                
                
                
                
                
                
                
                
                
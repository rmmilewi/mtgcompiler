import mtgcompiler.midend.support.inspection as inspection
from mtgcompiler.frontend.AST.reference import MgNameReference

class BindingError(Exception):
        def __init__(self, location, message):
            self.expression = location
            self.message = message

def bindNameReferences(card):
        """
        Binds all self-references in a card to the name of that card.
        This will cause an error of the card does not in fact have a name.
        
        card: An MgCard object.
        """
        
        nameReferences = inspection.getAllNodesOfType(card,MgNameReference)
        
        if len(nameReferences) > 0 and not card.hasName():
                #All cards have a name by default, so this shouldn't happen unless something has gone very wrong.
                raise BindingError(card,"A card has {0} name reference(s) yet has no MgName.".format(len(nameReferences)))
                
        cardName = card.getName()
        
        for nameReference in nameReferences:
                nameReference.setAntecedent(cardName)
        
        

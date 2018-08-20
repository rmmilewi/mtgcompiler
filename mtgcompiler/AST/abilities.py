import mtgcompiler.AST.core as core

class MgAbility(core.MgNode):
        """Ability nodes represent abilities on Magic cards, such as
        static abilities, triggered abilities, and activated abilities. 
        On a card, aside from certain defined abilities that may be strung together 
        on a single line, each paragraph break in a card’s text marks a separate ability.
        
        This class is not instantiated directly, but is the parent class
        to different kinds of ability nodes."""
        pass

class MgActivatedAbility(MgAbility):
        """Activated abilities have a cost and an effect. 
        They are written as '[Cost]: [Effect.] [Activation instructions (if any).]'."""
        def __init__(self,cost,instructions):
                """
                cost: The cost of the ability that must be paid.
                instructions: one or more effects/instructions that follow from
                activating the ability.
                """
                self._traversable = True
                self._cost = cost
                self._instructions = instructions
                
        def isChild(self,child):
                return child is self._cost or child is self._instructions
                
        def getTraversalSuccessors(self):
                return [node for node in {self._cost,self._instructions} if node.isTraversable()]
                
        def unparseToString(self):
                return "{0}: {1}".format(self._cost,self._instructions)

class MgTriggeredAbility(MgAbility):
        """ Triggered abilities have a trigger condition and an effect. 
        They are written as '[Trigger condition], [effect],' and include 
        (and usually begin with) the word 'when,' 'whenever,' or 'at.'"""
        pass
        
class MgStaticAbility(MgAbility):
        """Static abilities are written as statements. They’re simply true."""
        pass
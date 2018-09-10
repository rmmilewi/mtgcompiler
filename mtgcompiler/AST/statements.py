import mtgcompiler.AST.core as core
from enum import Enum

class MgAbstractStatement(core.MgNode):
        """An ability is made of one or more statements, organized into an instruction sequence.
        A statement encapsulates a subtree of expressions, usually terminated by a period."""
        def __init__(self):
                """
                periodTerminated: Is this statement terminated by a period? Some statements, like an expression statement holding a modal expression, don't
                need a period at the end.
                """
                self._traversable = True
                #periodTerminated = True
                pass
                
        #def isPeriodTerminated(self):
        #        """Checks whether the statement is terminated by a period."""
        #        return self._periodTerminated
                
        #def setPeriodTerminated(self,periodTerminated):
        #        """Enables or disables period termination for the statement."""
        #        self._periodTerminated = periodTerminated
        
                
        #def unparseToString(self):
        #        if self._periodTerminated is True:
        #                return "{0}.".format(self._root.unparseToString())
        #        else:
        #                return "{0}".format(self._root.unparseToString())
        

#Draw a card for each creature you control.
#For each creature target player controls, create a token that’s a copy of that creature.
#Deadeye Plunderers gets +1/+1 for each artifact you control.
#When you cast this spell, copy it for each time you’ve cast your commander from the command zone this game. You may choose new targets for the copies.
#At the beginning of your upkeep, for each land target player controls in excess of the number you control, choose a land that player controls, then the chosen permanents phase out. Repeat this process for artifacts and creatures.

#Target creature can’t be blocked this turn except by artifact creatures and/or red creatures.
#You may have Gigantoplasm enter the battlefield as a copy of any creature on the battlefield, except it has [...]
#You may have Quicksilver Gargantuan enter the battlefield as a copy of any creature on the battlefield, except it’s 7/7.
#'except' should probably be an expression as it's a statement that alters the effect of something else.
        
class MgStatementBlock(MgAbstractStatement):
        """Represents a sequence of statements that make up a single ability."""
        
        def __init__(self,*args):
                """The constructor accepts a list of statements in any order."""
                super().__init__()
                self._ilist = args
                for statement in self._ilist:
                        statement.setParent(self)
                        
        def isChild(self,child):
                return child in self._ilist
        
        def getTraversalSuccessors(self):
                return [statement for statement in self._ilist if statement.isTraversable()]
                
        def unparseToString(self):
                #TODO: How do we want to handle period termination of statements?
                return '. '.join(statement.unparseToString() for statement in self._ilist)

class MgCompoundStatement(MgAbstractStatement):
        """A compound statement is a series of comma-separated clauses, each of which is a statement.
        Compound statements can either be terminated by a 'then' (most common) or an 'and'.
        
        Examples:
        'You may search your library for an Equipment card, reveal it, put it into your hand, then shuffle your library.'
        'Choose a card name, then reveal a card at random from your hand.'
        'If cards with five or more different converted mana costs are exiled with Azor’s Gateway, you gain 5 life, untap Azor’s Gateway, and transform it.'
        """
        class CompoundTerminator(Enum):
                Then = "then"
                And = "and"
        
        def __init__(self,terminator=None,*statements):
                super().__init__()
                self._statements = statements
                if terminator == None:
                        self._terminator = MgCompoundStatement.CompoundTerminator.Then
                else:
                        self._terminator = terminator
                for statement in self._statements:
                        statement.setParent(self)
                        
        def isThenTerminated(self):
                """Checks whether the compound statement is then-terminated."""
                return self._terminator == MgCompoundStatement.CompoundTerminator.Then
                
        def setThenTerminated(self):
                """Sets the compound statement to be then-terminated."""
                self._terminator = MgCompoundStatement.CompoundTerminator.Then
                
        def isAndTerminated(self):
                """Checks whether the compound statement is and-terminated."""
                return self._terminator == MgCompoundStatement.CompoundTerminator.And

        def setAndTerminated(self):
                """Sets the compound statement to be and-terminated."""
                self._terminator = MgCompoundStatement.CompoundTerminator.And                
                
        def getStatements(self):
                """Get the list of statements in this compound expression."""
                return self._statements
                
        def setStatements(self,*statements):
                """Set the list of statements in this compound expression."""
                self._statements = statements
                for statement in self._statements:
                        statement.setParent(self)
                        
        #TODO: Add methods to insert/remove individual statements
        
        def isChild(self,child):
                return child in self._statements
        
        def getTraversalSuccessors(self):
                return [statement for statement in self._statements if statement.isTraversable()]
                
        def unparseToString(self):
                output = ', '.join(statement.unparseToString() for statement in self._statements[0:len(self._tlist)-1]) 
                output = output + ", {0} {1}".format(self._terminator.value,self._statements[len(self._statements)-1])
                return output
                
                
class MgIsStatment(MgAbstractStatement):
        pass
                      
class MgThenStatement(MgAbstractStatement):
        """Then [expression or statement].
        Examples:
        'Then shuffle your library.'
        'Then if you control an untapped land, destroy all enchantments you control.'
        """
        def __init__(self,body):
                """Body: The statement underneath the 'then' statement."""
                super().__init__()
                self._body = body
                self._body.setParent(self)
        
        def getBody(self):
                """Gets the body of this Then statement."""
                return self._body
        
        def setBody(self,body):
                """Sets the body of this Then statement."""
                self._body = body
                self._body.setParent(self)
        
        def isChild(self,child):
                return child is not None and child in {self._body}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._body} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                return "Then {0}".format(self._body.unparseToString())
                
        
class MgKeywordAbilityListStatement(MgAbstractStatement):
        """Represents a comma-separated sequence of keyword abilities, like 'flying, haste, first strike'."""
        def __init__(self,*kwabilities):
                """The constructor accepts a list of keyword abilities."""
                super().__init__()
                self._abilitylist = kwabilities
                for ability in self._abilitylist:
                        ability.setParent(self)
                        
        def getAbilityAtIndex(self,index):
                return self._abilitylist[index]
        
        def isChild(self,child):
                return child is not None and child in self._abilitylist
        
        def getTraversalSuccessors(self):
                return [ability for ability in self._abilitylist if ability.isTraversable()]
                
        def unparseToString(self):
                if len(self._abilitylist) == 2 and self._abilitylist[-1].hasReminderText():
                        #If there are only two keyword abilities and the second has reminder text, then
                        #we use a semicolon to separate them.
                        return '; '.join(ability.unparseToString() for ability in self._abilitylist)
                else:
                        return ', '.join(ability.unparseToString() for ability in self._abilitylist)

class MgConditionalStatement(MgAbstractStatement):
        """This is an abstract class for conditional statements."""
        def __init__(self,conditional,consequence,inverted=False):
                """
                conditional: The statement which evaluates to true or false.
                consequence: What happens if the condition is true.
                """
                super().__init__()
                self._conditional = condition
                self._consequence = consequence
                self._inverted = inverted
                if self._conditional is not None:
                        self._conditional.setParent(self)
                if self._consequence is not None:
                        self._consequence.setParent(self)
                
        def getConditional(self):
                """Get the conditional for this conditional statement."""
                return self._conditional
                
        def setConditional(self,conditional):
                """Set the conditional for this conditional statement."""
                if self._conditional is not None:
                        self._conditional.setParent(self)
        
        def getConsequence(self):
                """Get the consequence for this conditional statement."""
                return self._consequence
                
        def setConsequence(self):
                """Get the consequence for this conditional statement."""
                if self._consequence is not None:
                        self._consequence.setParent(self)
                        
        def isInverted(self):
                """Checks whether the conditional statement is inverted."""
                return self._inverted
                
        def setInverted(self,inverted):
                """Sets the inverted flag for this conditional statement."""
                self._inverted = inverted
                
        def isChild(self,child):
                return child is not None and child in {self._conditional,self._consequence}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._conditional,self._consequence} if node is not None and node.isTraversable()]

class MgIfStatement(MgConditionalStatement):
        def __init__(self,conditional,consequence,inverted=False):
                super().__init__(conditional,consequence,inverted)
                self._inverted = inverted
                
        def unparseToString(self):
                if self._inverted is False:
                        return "if {0}, {1}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                else:
                        return "{1} if {0}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                
class MgWheneverStatement(MgConditionalStatement):
        def __init__(self,conditional,consequence,inverted=False):
                super().__init__(conditional,consequence,inverted)
                
        def unparseToString(self):
                if self._inverted is False:
                        return "whenever {0}, {1}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                else:
                        return "{1} whenever {0}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
        
class MgWhenStatement(MgConditionalStatement):
        def __init__(self,conditional,consequence,inverted=False):
                super().__init__(conditional,consequence,inverted)
        
        def unparseToString(self):
                if self._inverted is False:
                        return "when {0}, {1}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                else:
                        return "{1} when {0}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
        
class MgAtStatement(MgConditionalStatement):
        def __init__(self,conditional,consequence,inverted=False):
                super().__init__(conditional,consequence,inverted)
        
        def unparseToString(self):
                if self._inverted is False:
                        return "at {0}, {1}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                else:
                        return "{1} at {0}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                        
class MgAsLongAsStatement(MgConditionalStatement):
        def __init__(self,conditional,consequence,inverted=False):
                super().__init__(conditional,consequence,inverted)
        
        def unparseToString(self):
                if self._inverted is False:
                        return "as long as {0}, {1}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                else:
                        return "{1} as long as {0}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
        
class MgOtherwiseStatement(MgConditionalStatement):
        def __init__(self,conditional,consequence):
                super().__init__(conditional,consequence,inverted=False)
        
        def unparseToString(self):
                return "otherwise {0}, {1}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                
class MgUnlessStatement(MgConditionalStatement):
        def __init__(self,conditional,consequence):
                super().__init__(conditional,consequence,inverted=False)
        
        def unparseToString(self):
                return "{1} unless {0}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                
class MgForStatement(MgConditionalStatement):
        pass



#Whenever you tap a land for mana while you’re the monarch, add an additional one mana of any color.
#While you’re searching your library, you may cast Panglacial Wurm from your library.
#While voting, you may vote an additional time. (The votes can be for different choices or for the same choice.)
#If you would draw a card while you have no cards in hand, instead draw two cards and lose 1 life.
#If you would draw a card while your library has no cards in it, you win the game instead.
#While choosing targets as part of casting a spell or activating an ability, your opponents must choose at least one Flagbearer on the battlefield if able.
#While [state]
class MgWhileStatement(MgConditionalStatement):
        """
        Typical construction: While [state], [consequence]
        But also situations like: If [if-condition] [while condition], [if-consequence]
        """
        
        def __init__(self,conditional,consequence,inverted=False):
                super().__init__(conditional,consequence,inverted=False)
        
        def unparseToString(self):
                if self._inverted is False:
                        return "while {0}, {1}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                else:
                        return "{1} while {0}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                


class MgActivationStatement(MgAbstractStatement):
        def __init__(self,cost,instructions):
                super().__init__()
                self._cost = cost
                self._instructions = instructions
                self._cost.setParent(self)
                self._instructions.setParent(self)
                
        def getCost(self):
                """Get the cost associated with this statement."""
                return self._cost
                
        def setCost(self,cost):
                """Set the cost associated with this statement."""
                self._cost = cost
                self._cost.setParent(self)
                
        def getInstructions(self):
                """Get the instructions associated with this statement."""
                return self._instructions
                
        def setInstructions(self,instructions):
                """Set the instructions associated with this statement."""
                self._instructions = instructions
                self._instructions.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._cost,self._instructions}
                
        def getTraversalSuccessors(self):
                return [node for node in {self._cost,self._instructions} if node.isTraversable()]
                
        def unparseToString(self):
                return "{0}: {1}".format(self._cost.unparseToString(),self._instructions.unparseToString())

class MgExpressionStatement(core.MgNode):
        
        def __init__(self,root):
                super().__init__()
                """
                root: a single expression/term underneath the statement.
                """
                self._traversable = True
                self._root = root
                self._root.setParent(self)
                
        def isChild(self,child):
                return child is self._root
        
        def getTraversalSuccessors(self):
                return [node for node in {self._root} if node]
                
        def getRoot(self):
                """Get the root expression/term of the statement."""
                return self._root
        
        def setRoot(self,root):
                """Set the root expression/term of the statement."""
                self._root = root
                self._root.setParent(self)
                
        def unparseToString(self):
                return "{0}".format(self._root.unparseToString())
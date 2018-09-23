import mtgcompiler.AST.core as core
from enum import Enum

class MgAbstractStatement(core.MgNode):
        """An ability is made of one or more statements, organized into an instruction sequence.
        A statement encapsulates a subtree of expressions, usually terminated by a period."""
        def __init__(self):
                self._traversable = True

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
                        
        def getNumberOfStatements(self):
                """Get the number of statements in this statement block."""
                return len(self._ilist)
                
        def getStatementAtIndex(self,index):
                """Get the statement at the given index in the statement list.
                Produces an error if the index falls out of bounds."""
                return self._ilist[index]
                        
        def isChild(self,child):
                return child in self._ilist
        
        def getTraversalSuccessors(self):
                return [statement for statement in self._ilist if statement.isTraversable()]
                
        def unparseToString(self):
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
                
                
class MgMayStatement(MgAbstractStatement):
        """A may-statement wraps around another statement, indicating that the statement underneath is optional."""
        
        def __init__(self,player,statement):
                """
                player: An expression describing the player who may take the action.
                statement: The statement that may be carried out.
                """
                self._player = player
                self._player.setParent(self)
                self._statement = statement
                self._statement.setParent(self)
                
        def getPlayer(self):
                """Get the player who may carry out the statement."""
                return self._player
                
        def setPlayer(self,player):
                """Set the player who may carry out the statement."""
                self._player = player
                self._player.setParent(self)
                
        def getStatement(self):
                """Get the statement that may be carried out."""
                return self._statement
                
        def setStatement(self):
                """Get the statement that may be carried out."""
                self._statement = statement
                self._statement.setParent(self)
                
        def isChild(self,child):
                return child is not None and child in {self._player,self._statement}
        
        def getTraversalSuccessors(self):
                return [node for node in {self._player,self._statement} if node.isTraversable()]
                
        def unparseToString(self):
                return "{0} may {1}".format(self._player.unparseToString(),self._statement.unparseToString())
                
                
class MgBeingStatement(MgAbstractStatement):
        """The abstract parent class for all statements of being/status, such as:
        
        "~ is an Elf in addition to its other types"
        "~ has first strike and haste"
        "~ can't block"
        "
        
        A being statement consists of a left-hand side and a right-hand side. The left-hand side
        may be option (e.g. in a compound statement such as "target creature gets +1/+1 and <implied> has first strike
        until end of turn.). 
        """
        def __init__(self,lhs,rhs):
                """
                lhs: (Optional) The thing that has something.
                rhs: The thing that is had.
                impliedLhs: Indicates whether the lhs is implied. This flag is set automatically by the constructor.
                It is checked during binding.
                """
                super().__init__()
                self._lhs = lhs
                if self._lhs is not None:
                        self._lhs.setParent(self)
                        self._impliedLhs = False
                else:
                        self._impliedLhs = True
                self._rhs = rhs
                self._rhs.setParent(self)
                
        def isImpliedLhs(self):
                """Checks whether the left-hand side of this statement is implied (i.e. not an actual child of the node)."""
                return self._impliedLhs
                
        def getLhs(self):
                """Get the left-hand side of this statement."""
                return self._lhs
                
        def setLhs(self,lhs):
                """Set the left-hand side of this statement."""
                self._lhs = lhs
                if self.isImpliedLhs():
                        self._lhs.setParent(self)
                        
        def getRhs(self):
                """Get the right-hand side of this statement."""
                return self._rhs
                
        def setRhs(self,rhs):
                """Set the right-hand side of this statement."""
                self._rhs = rhs
                self._rhs.setParent(self)
                
        def isChild(self,child):
                if not self.isImpliedLhs():
                        return child is not None and child in {self._lhs,self._rhs}
                else:
                        return child is not None and child in {self._rhs}
        
        def getTraversalSuccessors(self):
                if not self.isImpliedLhs():
                        return [node for node in {self._lhs,self._rhs} if node.isTraversable()]
                else:
                        return [node for node in {self._rhs} if node.isTraversable()]
        
        
                
        
                
                
                
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
                self._conditional = conditional
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
                        
class MgUntilStatement(MgConditionalStatement):
        def __init__(self,conditional,consequence,inverted=False):
                super().__init__(conditional,consequence,inverted)
        
        def unparseToString(self):
                if self._inverted is False:
                        return "until {0}, {1}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                else:
                        return "{1} until {0}".format(self._conditional.unparseToString(),self._consequence.unparseToString())


class MgOtherwiseStatement(MgConditionalStatement):
        def __init__(self,conditional,consequence):
                super().__init__(conditional,consequence,inverted=False)
        
        def unparseToString(self):
                return "otherwise {0}, {1}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                

class MgDuringStatement(MgConditionalStatement):
        def __init__(self,conditional,consequence,exclusive=False):
                """
                exclusive: Specifies that the conditional is exclusive ('only during')."""
                super().__init__(conditional,consequence,inverted=False)
                self._exclusive = exclusive
                
        def isExclusive(self):
                """Checks whether this during statement is exclusive ('only during')."""
                return self._exclusive == True
                
        def setExclusive(self,exclusive):
                """Sets whether this during statement is exclusive ('only during')."""
                self._exclusive = exclusive
        
        def unparseToString(self):
                if self._exclusive == True:
                        return "{0} only during {1}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                else:
                        return "{0} during {1}".format(self._conditional.unparseToString(),self._consequence.unparseToString())
                
class MgUnlessStatement(MgConditionalStatement):
        def __init__(self,conditional,consequence):
                super().__init__(conditional,consequence,inverted=False)
        
        def unparseToString(self):
                return "{1} unless {0}".format(self._conditional.unparseToString(),self._consequence.unparseToString())

            
class MgForStatement(MgConditionalStatement):
        """
        
        Examples:
        'For each creature target player controls, create a token that’s a copy of that creature.'
        'When you cast this spell, copy it for each time you’ve cast your commander from the command zone this game.'
        'For each land target player controls in excess of the number you control, choose a land that player controls, 
        then the chosen permanents phase out.'
        """
        pass




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

class MgExpressionStatement(MgAbstractStatement):
        def __init__(self,root):
                """
                root: a single expression/term underneath the statement.
                """
                super().__init__()
                self._root = root
                self._root.setParent(self)
                
        def isChild(self,child):
                return child is self._root
        
        def getTraversalSuccessors(self):
                return [node for node in {self._root} if node.isTraversable()]
                
        def getRoot(self):
                """Get the root expression/term of the statement."""
                return self._root
        
        def setRoot(self,root):
                """Set the root expression/term of the statement."""
                self._root = root
                self._root.setParent(self)
                
        def unparseToString(self):
                return "{0}".format(self._root.unparseToString())
                
                
class MgAbilitySequenceStatement(MgAbstractStatement):
        """An ability sequence statement is a series of one or more keyword abilities and quoted abilities. If there is more
        than one element in the sequence, it is terminated with an 'and'. If there are more than two elements, the sequence is
        comma-delimited. Often used in descriptions of tokens. Examples (in asterisks) include:
                * A 2/2 white knight creature token *with vigilance*.
                * A colorless Treasure artifact token with *"{T}, Sacrifice this artifact: Add one mana of any color."*.
                * A 1/1 colorless Insect artifact creature token with *flying and haste* named Hornet.
        """
        
        def __init__(self,*abilities):
                """
                args: The abilities contained in the sequence statement.
                """
                super().__init__()
                self._abilitylist = abilities
                for ability in self._abilitylist:
                        ability.setParent(self)
                        
        def getAbilities(self):
                """Get the abilities in this ability sequence statement."""
                return self._abilitylist
                for ability in self._abilitylist:
                        ability.setParent(self)
                
        def setAbilities(self,*abilities):
                """Replaces the current list of abilities with a new list of abilities."""
                self._abilitylist = abilities

        def isChild(self,child):
                return child in self._abilitylist
        
        def getTraversalSuccessors(self):
                return [ability for ability in self._abilitylist if ability.isTraversable()]
                
        def unparseToString(self):
                output = ""
                if len(self._abilitylist) > 1:
                        output = ','.join([ability.unparseToString() for ability in self._abilitylist[0:len(self._abilitylist)-1]])
                        output = "{0} and {1}".format(output,self._abilitylist[-1].unparseToString())
                elif len(self._abilitylist) == 1:
                        output = "{0}".format(self._abilitylist[0].unparseToString())
                else:
                        output = "empty-ability-sequence-statement"
                return output
                
class MgQuotedAbilityStatement(MgAbstractStatement):
        """A statement block encased in quotes that describes a non-keyword ability that is granted
        by some other ability, such as in the following examples:
        
        * Enchanted land has "{T}: This land deals 1 damage to any target."
        * You get an emblem with "Your opponents can’t untap more than two permanents during their untap steps."
        * Each creature has “When this creature dies, choose target opponent. 
        That player puts this card from its owner’s graveyard onto the battlefield under their control
        at the beginning of the next end step."
        """
        
        def __init__(self,stmtblock):
                """
                stmtblock: A statement block.
                """
                super().__init__()
                self._stmtblock = stmtblock
                self._stmtblock.setParent(self)
                
        def isChild(self,child):
                return child is self._stmtblock
        
        def getTraversalSuccessors(self):
                return [node for node in {self._stmtblock} if node.isTraversable()]
                
        def unparseToString(self):
                return "\\\"{0}\\\"".format(self._stmtblock.unparseToString())
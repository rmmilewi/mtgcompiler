import mtgcompiler.AST.core as core


class MgReminderText(core.MgNode):
        """This node represents reminder text contained in parentheses.
        Reminder text is attached to MgAbility nodes, and is not traversable, though
        it can be accessed by a visitor when visiting the ability node."""
        def __init__(self,reminder):
                """reminder: a string containing the text of the reminder."""
                self._traversable = False
                self._reminder = reminder
                
        def isChild(self,child):
                """A reminder text node has no children."""
                return False
        
        def getTraversalSuccessors(self):
                """A reminder text node has no traversal successors."""
                return []
                
        def getReminderText(self):
                """Get the reminder string."""
                return self._reminder
                
        def setReminderText(self,reminder):
                """Set the reminder string."""
                self._reminder = reminder

        def unparseToString(self):
                return "({0})".format(self._reminder)
                
                
class MgAbilityWord(core.MgNode):
        """This node represents an ability word expression, like 'Battalion — ...' or 'Spell Mastery - ...'
        Like reminder text, ability words are attached to MgAbility nodes and are not traversable,
        though they can be accessed by a visitor when visiting the ability node."""
        def __init__(self,abilityWord):
                """abilityWord: a string containing the text of the ability word."""
                self._traversable = True
                self._abilityWord = abilityWord
                
        def isChild(self,child):
                """An ability word node has no children."""
                return False
        
        def getTraversalSuccessors(self):
                """An ability word node has no traversal successors."""
                return []
                
        def getAbilityWord(self):
                """Get the reminder string."""
                return self._reminder
                
        def setAbilityWord(self,abilityWord):
                """Set the ability word string."""
                self._reminder = abilityWord
                
        def unparseToString(self):
                return "{0} —".format(self._abilityWord)

class MgAbility(core.MgNode):
        """Ability nodes represent abilities on Magic cards, such as
        static abilities, triggered abilities, and activated abilities. 
        On a card, aside from certain defined abilities that may be strung together 
        on a single line, each paragraph break in a card’s text marks a separate ability.
        
        This class is not instantiated directly, but is the parent class
        to different kinds of ability nodes."""
        
        def __init__(abilityWord=None,reminderText=None):
                """All constructors in subclasses of MgAbility use super() to call this constructor first
                in order to store ability words and reminder text, if necessary.
                 
                abilityWord: An optional MgAbilityWord object, corresponding to the ability word
                that decorates the text of the ability.
                reminderText: An option MgReminderText object, corresponding to the reminder text
                that decorates the text of the ability.
                """
                self._abilityWord = abilityWord
                self._reminderText = reminderText
                if self._abilityWord is not None:
                        self._abilityWord.setParent(self)
                if self._reminderText is not None:
                        self._reminderText.setParent(self)
        
        def hasAbilityWord(self):
                """Checks to see if the ability has an associated ability word.
                By default, the attribute is None."""
                return self._abilityWord is not None
                
        def getAbilityWord(self):
                """Get the ability word node."""
                return self._abilityWord
                
        def setAbilityWord(self,abilityWord):
                """Set the ability word node."""
                self._abilityWord = abilityWord
                self._abilityWord.setParent(self)
                
        def hasReminderText(self):
                """Checks to see if the node has an associated reminder text.
                By default, the attribute is None."""
                return self._reminderText is not None
        
        def getReminderText(self):
                """Get the reminder text node."""
                return self._reminderText
                
        def setReminderText(self,reminderText):
                """Set the reminder text node."""
                self._reminderText = reminderText
                self._reminderText.setParent(self)

class MgActivatedAbility(MgAbility):
        """Activated abilities have a cost and an effect. 
        They are written as '[Cost]: [Effect.] [Activation instructions (if any).]'."""
        def __init__(self,cost,instructions,abilityWord=None,reminderText=None):
                """
                cost: The cost of the ability that must be paid.
                instructions: one or more effects/instructions that follow from
                activating the ability.
                """
                super().__init__(abilityWord,reminderText)
                self._traversable = True
                self._cost = cost
                self._instructions = instructions
                
        def isChild(self,child):
                return child is self._cost or child is self._instructions
                
        def getTraversalSuccessors(self):
                return [node for node in {self._cost,self._instructions} if node.isTraversable()]
                
        def unparseToString(self):
                output = "{0}: {1}".format(self._cost,self._instructions)
                if self.hasAbilityWord():
                        output = "{0} {1}".format(self._abilityWord.unparseToString(),output)
                if self.hasReminderText():
                        output = "{0} {1}".format(output,self._reminderText.unparseToString())
                return output

class MgTriggeredAbility(MgAbility):
        """ Triggered abilities have a trigger condition and an effect. 
        They are written as '[Trigger condition], [effect],' and include 
        (and usually begin with) the word 'when,' 'whenever,' or 'at.'"""
        pass
        
class MgStaticAbility(MgAbility):
        """Static abilities are written as statements. They’re simply true."""
        pass
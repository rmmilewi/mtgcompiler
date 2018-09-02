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
                

class MgStatement(core.MgNode):
        """An ability is made of one or more statements, organized into an instruction sequence.
        A statement encapsulates a subtree of expressions, usually terminated by a period."""
        
        def __init__(self,root,periodTerminated=True):
                """
                root: a single expression/term underneath the statement.
                periodTerminated: Is this statement terminated by a period? Some statements, like one holding a modal expression, don't
                need a period at the end.
                """
                self._traversable = True
                self._root = root
                self._periodTerminated = periodTerminated
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
                
        def isPeriodTerminated(self):
                """Checks whether the statement is terminated by a period."""
                return self._periodTerminated
                
        def setPeriodTerminated(self,periodTerminated):
                """Enables or disables period termination for the statement."""
                self._periodTerminated = periodTerminated
        
                
        def unparseToString(self):
                if self._periodTerminated is True:
                        return "{0}.".format(self._root.unparseToString())
                else:
                        return "{0}".format(self._root.unparseToString())
                        
                
class MgStatementSequence(core.MgNode):
        """Represents a sequence of statements that make up a single ability."""
        
        def __init__(self,*args):
                """The constructor accepts a list of descriptors in any order."""
                self._traversable = True
                self._ilist = args
                for statement in self._ilist:
                        statement.setParent(self)
                        
        def isChild(self,child):
                return child in self._ilist
        
        def getTraversalSuccessors(self):
                return [statement for statement in self._ilist if statement.isTraversable()]
                
        def unparseToString(self):
                return ' '.join(statement.unparseToString() for statement in self._ilist)
                
                
                
class MgKeywordAbilityDeclarationList(core.MgNode):
        """Represents a comma-separated sequence of keyword abilities, like 'flying, haste, first strike'."""
        def __init__(self,*kwability):
                """The constructor accepts a list of keyword abilities."""
                self._traversable = True
                self._abilitylist = kwability
                for ability in self._abilitylist:
                        ability.setParent(self)
                        
        def isChild(self,child):
                return child in self._abilitylist
        
        def getTraversalSuccessors(self):
                return [ability for ability in self._abilitylist if ability.isTraversable()]
                
        def unparseToString(self):
                return ', '.join(ability.unparseToString() for ability in self._abilitylist)
        

class MgAbstractAbility(core.MgNode):
        """Ability nodes represent abilities on Magic cards, such as
        static abilities, triggered abilities, and activated abilities. 
        On a card, aside from certain defined abilities that may be strung together 
        on a single line, each paragraph break in a card’s text marks a separate ability.
        
        This class is not instantiated directly, but is the parent class
        to different kinds of ability nodes."""
        
        def __init__(self,abilityWord=None,reminderText=None):
                """All constructors in subclasses of MgAbility use super() to call this constructor first
                in order to store ability words and reminder text, if necessary.
                 
                abilityWord: An optional MgAbilityWord object, corresponding to the ability word
                that decorates the text of the ability.
                reminderText: An option MgReminderText object, corresponding to the reminder text
                that decorates the text of the ability.
                """
                self._traversable = True
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

class MgSpellAbility(MgAbstractAbility):
        """Spell abilities are abilities that are followed as instructions while an instant or sorcery spell is resolving. 
        Any text on an instant or sorcery spell is a spell ability unless it’s an activated ability, a triggered ability, 
        or a static ability that fits the criteria described in rule 112.6."""
        
        def __init__(self,instructions,abilityWord=None,reminderText=None):
                """
                instructions: one or more effects/instructions that follow from carrying out the ability.
                """
                super().__init__(abilityWord,reminderText)
                self._instructions = instructions
                self._instructions.setParent(self)
                
        def isChild(self,child):
                """A spell ability has only one child, the instruction sequence."""
                return child is self._instructions
                
        def getTraversalSuccessors(self):
                """A spell ability has only one child, the instruction sequence."""
                return [node for node in {self._instructions} if node.isTraversable()]
                
        def getInstructions(self):
                """Get the instruction sequence held by the ability."""
                return self._instructions
                
        def setInstructions(self,instructions):
                """Set the instruction sequence held by the ability."""
                self._instructions = instructions
                self._instructions.setParent(self)
                
        def unparseToString(self):
                output = "{0}".format(self._instructions.unparseToString())
                if self.hasAbilityWord():
                        output = "{0} {1}".format(self._abilityWord.unparseToString(),output)
                if self.hasReminderText():
                        output = "{0} {1}".format(output,self._reminderText.unparseToString())
                return output   
                

class MgActivatedAbility(MgAbstractAbility):
        """Activated abilities have a cost and an effect. 
        They are written as '[Cost]: [Effect.] [Activation instructions (if any).]'."""
        def __init__(self,cost,instructions,abilityWord=None,reminderText=None):
                """
                cost: The cost of the ability that must be paid.
                instructions: one or more effects/instructions that follow from
                activating the ability.
                """
                super().__init__(abilityWord,reminderText)
                self._cost = cost
                self._instructions = instructions
                self._cost.setParent(self)
                self._instructions.setParent(self)
                
        def isChild(self,child):
                return child is self._cost or child is self._instructions
                
        def getTraversalSuccessors(self):
                return [node for node in {self._cost,self._instructions} if node.isTraversable()]
                
        def unparseToString(self):
                output = "{0}: {1}".format(self._cost.unparseToString(),self._instructions.unparseToString())
                if self.hasAbilityWord():
                        output = "{0} {1}".format(self._abilityWord.unparseToString(),output)
                if self.hasReminderText():
                        output = "{0} {1}".format(output,self._reminderText.unparseToString())
                return output

class MgTriggeredAbility(MgAbstractAbility):
        """ Triggered abilities have a trigger condition and an effect. 
        They are written as '[Trigger condition], [effect],' and include 
        (and usually begin with) the word 'when,' 'whenever,' or 'at.'"""
        def __init__(self,condition,outcome,abilityWord=None,reminderText=None):
                super().__init__(abilityWord,reminderText)
                self._condition = condition
                self._outcome = outcome

        
class MgStaticAbility(MgAbstractAbility):
        """Static abilities are written as statements. They’re simply true."""
        pass
        
        
class MgKeywordAbility(MgAbstractAbility):
        """This is the parent class for all keyword abilities. Keyword abilities aren't subclasses of
        static/triggered/spell/activated ability classes because they can be any combination of these
        things. A keyword instead is a stand-in for more verbose abilities or series of abilities."""
        
        def __init__(self):
                self._traversable = True #All keyword abilities are traversable by default.
        
        def getCanonicalName(self):
                """Get a string representing the canonical name for an ability."""
                raise NotImplemented
        
        
class MgDeathtouchAbility(MgKeywordAbility):
        """
        702.2a Deathtouch is a static ability.
        702.2b A creature with toughness greater than 0 that’s been dealt damage by a source with deathtouch 
        since the last time state-based actions were checked is destroyed as a state-based action. See rule 704.
        """
        
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "deathtouch"
        
        
                
class MgDefenderAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "defender"
        
        
class MgDoubleStrikeAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "double strike"
        
        
class MgEnchantAbility(MgKeywordAbility):
        """702.5a Enchant is a static ability, written “Enchant [object or player].” 
        The enchant ability restricts what an Aura spell can target and what an Aura can enchant."""
        pass
        
        
class MgEquipAbility(MgKeywordAbility):
        """702.6a Equip is an activated ability of Equipment cards. 
        “Equip [cost]” means “[Cost]: Attach this permanent to target creature you control. 
        Activate this ability only any time you could cast a sorcery.”
        
        702.6c “Equip [quality] creature” is a variant of the equip ability. 
        “Equip [quality] [cost]” means “[Cost]: Attach this permanent to target [quality] creature you control. 
        Activate this ability only any time you could cast a sorcery.” 
        This ability doesn’t restrict what the Equipment may be attached to.
        """
        pass
        
class MgFirstStrikeAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "first strike"
        
        
class MgFlashAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "flash"
        
class MgFlyingAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "flying"
        
class MgHasteAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "haste"
        
        
class MgHexproofAbility(MgKeywordAbility):
        """702.11d “Hexproof from [quality]” is a variant of the hexproof ability. 
        “Hexproof from [quality]” on a permanent means “This permanent can’t be the target of [quality] spells
        your opponents control or abilities your opponents control from [quality] sources.”
        A “hexproof from [quality]” ability is a hexproof ability."""
        def __init__(self,quality=None):
                """quality: An optional quality that specifies what hexproof guards the object against, as opposed
                to all sources, which is the default."""
                super().__init__()
                self._quality = quality
                if self._quality is not None:
                        self._quality.setParent(self)
                
        def hasQualitySpecifier(self):
                """Checks whether the instance of hexproof has a quality specifier (e.g. hexproof from black)."""
                return self._quality is not None
                
        def getQualitySpecifier(self):
                """Gets the quality specifier."""
                return self._quality
                
        def setQualitySpecifier(self,quality):
                """Sets the quality specifier."""
                self._quality = quality
                if self._quality is not None:
                        self._quality.setParent(self)
                
        def hasQualitySpecifier(self):
                """Checks whether the instance of hexproof has a quality specifier (e.g. hexproof from black)."""
                return self._quality is not None
                
        def isChild(self,child):
                """This node has one optional child."""
                return self._quality is not None and child == self._quality 
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor."""
                return [node for node in {self._quality} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._quality is not None:
                        return "hexproof from {0}".format(self._quality.unparseToString())
                else:
                        return "hexproof"
                        
        
class MgIndestructibleAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "indestructible"
        
class MgIntimidateAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "intimidate"
        
class MgLandwalkAbility(MgKeywordAbility):
        """702.14a Landwalk is a generic term that appears within an object’s rules text as “[type]walk,” where [type] is 
        usually a subtype, but can be the card type land, any land type, any supertype, or any combination thereof.
        
        702.14c A creature with landwalk can’t be blocked as long as the defending player controls at least one land with the specified subtype (as in “islandwalk”),
        with the specified supertype (as in “legendary landwalk”), without the specified supertype (as in “nonbasic landwalk”),
        or with both the specified supertype and the specified subtype (as in “snow swampwalk”). (See rule 509, “Declare Blockers Step.”)
        """
        def __init__(self,landtype=None):
                """landtype: A type expression describing the kind of land for which the landwalk is relevant,
                such as 'island' or 'legendary land'. If landtype is None, then this node refers to landtype generically,
                in the sense of 'landwalk of the chosen type'.
                """
                super().__init__()
                self._landtype = landtype
                if self._landtype is not None:
                        self._landtype.setParent(self)
                        
        def hasLandType(self):
                """Checks whether this instance of landwalk specifies a land type.
                If it doesn't, then it's referring to landwalk in a generic sense.
                """
                return self._landtype is not None
                
        def getLandType(self):
                """Gets the land type expression."""
                return self._landtype
                
        def setLandType(self,landtype):
                """Sets the land type expression."""
                self._landtype = landtype
                if self._landtype is not None:
                        self._landtype.setParent(self)
                
                
        def isChild(self,child):
                """This node has one optional child, the land type expression."""
                return self._landtype is not None and child == self._landtype 
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor."""
                return [node for node in {self._landtype} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._landtype is not None:
                        return "{0}walk".format(self._landtype.unparseToString())
                else:
                        return "landwalk"
                
                
        
class MgLifelinkAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "lifelink"
        
class MgProtectionAbility(MgKeywordAbility):
        """702.16a Protection is a static ability, written “Protection from [quality].” 
        This quality is usually a color (as in “protection from black”) 
        but can be any characteristic value or information."""
        
        def __init__(self,*qualities):
                """
                qualities*: Typically this is just one child, 'Protection from [quality]'.
                However, arguments get passed as a list because you can have a protection ability
                declaring protection from more than one thing at a time, such as 
                'protection from green and from blue'.
                """
                super().__init__()
                self._qualities = qualities
                for quality in self._qualities:
                        quality.setParent(self)
        
        def getCanonicalName(self):
                return "protection"
                
        def getQualities(self):
                """Get the quality that is protected against."""
                return self._qualities
                
        def setQualities(self,qualities):
                """Set the qualities that are protected against.
                This can either be a list or a single node.
                """
                if isinstance(qualities,(list,)):
                        self._qualities = qualities
                else:
                        self._qualities = [qualities]
                for quality in self._qualities:
                        quality.setParent(self)
        
        def isChild(self,child):
                """Protection abilities have at least one child, but may have more."""
                return child in self._qualities
                
        def getTraversalSuccessors(self):
                """Protection abilities have at least one possible successor, but may have more."""
                return [node for node in self._qualities if node.isTraversable()]
                
        def unparseToString(self):
                quals = ' and '.join(["from {0}".format(quality.unparseToString()) for quality in self._qualities])
                return "protection {0}".format(quals)
        
class MgReachAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "reach"
        
class MgShroudAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "shroud"
        
class MgTrampleAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "trample"
        
class MgVigilanceAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "vigilance"
        
class MgBandingAbility(MgKeywordAbility):
        """702.21b “Bands with other” is a special form of banding.""" 
        pass
        
class MgRampageAbility(MgKeywordAbility):
        """702.22a Rampage is a triggered ability. “Rampage N” means 
        “Whenever this creature becomes blocked, it gets +N/+N until end of turn
        for each creature blocking it beyond the first.”"""
        
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "rampage {0}".format(self._caliber.unparseToString())
                else:
                        return "rampage"
                
        

class MgCumulativeUpkeepAbility(MgKeywordAbility):
        """702.23a Cumulative upkeep is a triggered ability that imposes an increasing cost on a permanent. 
        “Cumulative upkeep [cost]” means “At the beginning of your upkeep, if this permanent is on the battlefield,
        put an age counter on this permanent. Then you may pay [cost] for each age counter on it.
        If you don’t, sacrifice it.” If [cost] has choices associated with it, each choice is made separately
        for each age counter, then either the entire set of costs is paid, or none of them is paid. 
        Partial payments aren’t allowed."""
        pass
        
class MgPhasingAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "phasing"
        
class MgBuybackAbility(MgKeywordAbility):
        """702.26a Buyback appears on some instants and sorceries. 
        It represents two static abilities that function while the spell is on the stack.
        “Buyback [cost]” means “You may pay an additional [cost] as you cast this spell” 
        and “If the buyback cost was paid, put this spell into its owner’s hand instead
        of into that player’s graveyard as it resolves.”"""
        pass

class MgShadowAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "shadow"
        
class MgCyclingAbility(MgKeywordAbility):
        """702.28a Cycling is an activated ability that functions only while the card with cycling 
        is in a player’s hand. “Cycling [cost]” means “[Cost], Discard this card: Draw a card.”
        
        702.28e Typecycling is a variant of the cycling ability. “[Type]cycling [cost]” means
        “[Cost], Discard this card: Search your library for a [type] card,reveal it, and put it
        into your hand. Then shuffle your library.” This type is usually a subtype (as in “mountaincycling”)
        but can be any card type, subtype, supertype, or combination thereof (as in “basic landcycling”)."""
        pass
        
class MgEchoAbility(MgKeywordAbility):
        """702.29a Echo is a triggered ability. “Echo [cost]” means “At the beginning of your upkeep, 
        if this permanent came under your control since the beginning of your last upkeep, 
        sacrifice it unless you pay [cost].”"""
        pass
        
class MgHorsemanshipAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "horsemanship"
        
        
class MgFadingAbility(MgKeywordAbility):
        """702.31a Fading is a keyword that represents two abilities. “Fading N” means 
        “This permanent enters the battlefield with N fade counters on it”
        and “At the beginning of your upkeep, remove a fade counter from this permanent. 
        If you can’t, sacrifice the permanent.”
        """
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "fading {0}".format(self._caliber.unparseToString())
                else:
                        return "fading"
        

class MgKickerAbility(MgKeywordAbility):
        """702.32a Kicker is a static ability that functions while the spell with kicker is on the stack. 
        “Kicker [cost]” means “You may pay an additional [cost] as you cast this spell.”
        702.32b The phrase “Kicker [cost 1] and/or [cost 2]” means the same thing as “Kicker [cost 1], kicker [cost 2].”
        Multikicker is a variant of the kicker ability. “Multikicker [cost]” 
        means “You may pay an additional [cost] any number of times as you cast this spell.” 
        A multikicker cost is a kicker cost.
        """
        pass
        
class MgFlashbackAbility(MgKeywordAbility):
        """702.33a Flashback appears on some instants and sorceries. 
        It represents two static abilities: one that functions 
        while the card is in a player’s graveyard 
        and another that functions while the card is on the stack.
        “Flashback [cost]” means “You may cast this card from your graveyard 
        by paying [cost] rather than paying its mana cost” 
        and “If the flashback cost was paid, exile this card instead of 
        putting it anywhere else any time it would leave the stack.”"""
        pass
        
class MgMadnessAbility(MgKeywordAbility):
        """702.34a Madness is a keyword that represents two abilities. 
        The first is a static ability that functions
        while the card with madness is in a player’s hand. 
        The second is a triggered ability
        that functions  when the first ability is applied. 
        “Madness [cost]” means “If a player would discard this card, 
        that player discards it, but exiles it instead of putting it into their graveyard”
        and “When this card is exiled this way, its owner may cast it
        by paying [cost] rather than paying its mana cost. 
        If that player doesn’t, they put this card into their graveyard.”"""
        pass
        
class MgFearAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "fear"
        
class MgMorphAbility(MgKeywordAbility):
        """“Morph [cost]” means “You may cast this card as a 2/2 face-down creature with no text,
        no name, no subtypes, and no mana cost by paying {3} rather than paying its mana cost.”
        
        702.36b Megamorph is a variant of the morph ability. “Megamorph [cost]” means 
        “You may cast this card as a 2/2 face-down creature with no text, no name, no subtypes, 
        and no mana cost by paying {3} rather than paying its mana cost” and 
        “As this permanent is turned face up, put a +1/+1 counter on it if its megamorph cost
         was paid to turn it face up.” A megamorph cost is a morph cost."""
        pass
        
class MgAmplifyAbility(MgKeywordAbility):
        """702.37a Amplify is a static ability. “Amplify N” means “As this object enters the battlefield,
        reveal any number of cards from your hand that share a creature type with it. This permanent
        enters the battlefield with N +1/+1 counters on it for each card revealed this way.
        You can’t reveal this card or any other cards that are entering the battlefield 
        at the same time as this card.”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "amplify {0}".format(self._caliber.unparseToString())
                else:
                        return "amplify"
        

class MgProvokeAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "provoke"
        
        
class MgStormAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "storm"
        
        
class MgAffinityAbility(MgKeywordAbility):
        """702.40a Affinity is a static ability that functions while the spell with affinity is on the stack. 
        “Affinity for [text]” means “This spell costs you {1} less to cast for each [text] you control.”"""
        pass
        
        
class MgEntwineAbility(MgKeywordAbility):
        """702.41a Entwine is a static ability of modal spells (see rule 700.2)
        that functions while the spell is on the stack.
        “Entwine [cost]” means “You may choose all modes of this spell instead of just one. 
        If you do, you pay an additional [cost].”"""
        pass
        
class MgModularAbility(MgKeywordAbility):
        """702.42a Modular represents both a static ability and a triggered ability. 
        “Modular N” means “This permanent enters the battlefield with N +1/+1 counters on it” 
        and “When this permanent is put into a graveyard from the battlefield, you may put a +1/+1 counter
        on target artifact creature for each +1/+1 counter on this permanent.”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "modular {0}".format(self._caliber.unparseToString())
                else:
                        return "modular"
        
class MgSunburstAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "sunburst"
        
class MgBushidoAbility(MgKeywordAbility):
        """702.44a Bushido is a triggered ability. “Bushido N” means “Whenever this creature blocks or
         becomes blocked, it gets +N/+N until end of turn.” (See rule 509, “Declare Blockers Step.”)."""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "bushido {0}".format(self._caliber.unparseToString())
                else:
                        return "bushido"
        
class MgSoulshiftAbility(MgKeywordAbility):
        """Soulshift N, where N is the CMC value."""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "soulshift {0}".format(self._caliber.unparseToString())
                else:
                        return "soulshift"
        
class MgSpliceAbility(MgKeywordAbility):
        """“Splice onto [subtype] [cost]”"""
        pass

class MgOfferingAbility(MgKeywordAbility):
        """“[Subtype] offering”"""
        pass
        
class MgNinjitsuAbility(MgKeywordAbility):
        """“Ninjutsu [cost]”"""
        pass
        
class MgEpicAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "epic"
        
class MgConvokeAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "convoke"
        
class MgDredgeAbility(MgKeywordAbility):
        """“Dredge N”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "dredge {0}".format(self._caliber.unparseToString())
                else:
                        return "dredge"
        
class MgTransmuteAbility(MgKeywordAbility):
        """“Transmute [cost]”"""
        pass
        
class MgBloodthirstAbility(MgKeywordAbility):
        """Bloodthirst N"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "bloodthirst {0}".format(self._caliber.unparseToString())
                else:
                        return "bloodthirst"
        
class MgHauntAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "haunt"
        
class MgReplicateAbility(MgKeywordAbility):
        """“Replicate [cost]”"""
        pass
        
class MgForecastAbility(MgKeywordAbility):
        """702.56a A forecast ability is a special kind of activated ability that
        can be activated only from a player’s hand. It’s written “Forecast — [Activated ability].”"""
        pass
        
class MgGraftAbility(MgKeywordAbility):
        """“Graft N”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "graft {0}".format(self._caliber.unparseToString())
                else:
                        return "graft"
        
class MgRecoverAbility(MgKeywordAbility):
        """“Recover [cost]”"""
        pass
        
class MgRippleAbility(MgKeywordAbility):
        """“Ripple N”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "ripple {0}".format(self._caliber.unparseToString())
                else:
                        return "ripple"
        
class MgSplitSecondAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "split second"
        
class MgSuspendAbility(MgKeywordAbility):
        """“Suspend N—[cost]”"""
        pass
        
class MgVanishingAbility(MgKeywordAbility):
        """“Vanishing N”"""
        """Vanishing without a number means..."""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "vanishing {0}".format(self._caliber.unparseToString())
                else:
                        return "vanishing"
        
class MgAbsorbAbility(MgKeywordAbility):
        """“Absorb N”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "absorb {0}".format(self._caliber.unparseToString())
                else:
                        return "absorb"
        
class MgAuraSwapAbility(MgKeywordAbility):
        """“Aura swap [cost]”"""
        pass
        
class MgDelveAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "delve"
        
class MgFortifyAbility(MgKeywordAbility):
        """“Fortify [cost]”"""
        pass
        
class MgFrenzyAbility(MgKeywordAbility):
        """“Frenzy N”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "frenzy {0}".format(self._caliber.unparseToString())
                else:
                        return "frenzy"
        
class MgGravestormAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "gravestorm"
        
class MgPoisonousAbility(MgKeywordAbility):
        """“Poisonous N”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "poisonous {0}".format(self._caliber.unparseToString())
                else:
                        return "poisonous"
        
class MgTransfigureAbility(MgKeywordAbility):
        """“Transfigure [cost]”"""
        pass
        
class MgChampionAbility(MgKeywordAbility):
        """“Champion an [object]”"""
        pass
        
class MgChangelingAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "changeling"
        
class MgEvokeAbility(MgKeywordAbility):
        """“Evoke [cost]”"""
        pass
        
class MgHideawayAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "hideaway"
        
class MgProwlAbility(MgKeywordAbility):
        """“Prowl [cost]”"""
        pass
        
class MgReinforceAbility(MgKeywordAbility):
        """“Reinforce N—[cost]”"""
        pass
        
class MgConspireAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "conspire"
        
class MgPersistAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "persist"
        
class MgWitherAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "wither"
        
class MgRetraceAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "retrace"
        
class MgDevourAbility(MgKeywordAbility):
        """“Devour N”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "devour {0}".format(self._caliber.unparseToString())
                else:
                        return "devour"

class MgExaltedAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "exalted"
        
class MgUnearthAbility(MgKeywordAbility):
        """“Unearth [cost]” """
        pass
        
class MgCascadeAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "cascade"
        
class MgAnnihilatorAbility(MgKeywordAbility):
        """“Annihilator N”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "annihilator {0}".format(self._caliber.unparseToString())
                else:
                        return "annihilator"
        
class MgLevelUpAbility(MgKeywordAbility):
        """Level up [cost]"""
        pass
        
class MgReboundAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "rebound"
        
class MgTotemArmorAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "totem armor"
        
class MgInfectAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "infect"
        
class MgBattleCryAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "battle cry"
        
class MgLivingWeaponAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "living weapon"
        
class MgUndyingAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "undying"
        
class MgMiracleAbility(MgKeywordAbility):
        """“Miracle [cost]”"""
        pass
                
class MgSoulbondAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "soulbond"
        
class MgOverloadAbility(MgKeywordAbility):
        """Overload [cost]"""
        pass
        
class MgScavengeAbility(MgKeywordAbility):
        """Scavenge [cost]"""
        pass
        
class MgUnleashAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "unleash"
        
class MgCipherAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "cipher"
        
class MgEvolveAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "evolve"
        
class MgExtortAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "extort"
        
class MgFuseAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "fuse"
        
class MgBestowAbility(MgKeywordAbility):
        """Bestow [cost]"""
        pass
        
class MgTributeAbility(MgKeywordAbility):
        """“Tribute N”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "tribute {0}".format(self._caliber.unparseToString())
                else:
                        return "tribute"
        
class MgDethroneAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "dethrone"
        
class MgHiddenAgendaAbility(MgKeywordAbility):
        """Double agenda is a variant of the hidden agenda ability."""
        pass
        
class MgOutlastAbility(MgKeywordAbility):
        """Outlast [cost]"""
        pass
        
class MgProwessAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "prowess"
        
class MgDashAbility(MgKeywordAbility):
        """“Dash [cost]”"""
        pass
        
class MgExploitAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "exploit"
        
class MgMenaceAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "menace"
        
class MgRenownAbility(MgKeywordAbility):
        """“Renown N”"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "renown {0}".format(self._caliber.unparseToString())
                else:
                        return "renown"
        
class MgAwakenAbility(MgKeywordAbility):
        """Awaken N—[cost]"""
        pass
        
class MgDevoidAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "devoid"
        
class MgIngestAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "ingest"
        
class MgMyriadAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "myriad"
        
class MgSurgeAbility(MgKeywordAbility):
        """Surge [cost]"""
        pass
        
class MgSkulkAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "skulk"
        
class MgEmergeAbility(MgKeywordAbility):
        """Emerge [cost]"""
        pass
        
class MgEscalateAbility(MgKeywordAbility):
        """Escalate [cost]"""
        pass
        
class MgMeleeAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "melee"
        
class MgCrewAbility(MgKeywordAbility):
        """Crew N"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "crew {0}".format(self._caliber.unparseToString())
                else:
                        return "crew"
        
class MgFabricateAbility(MgKeywordAbility):
        """Fabricate N"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "fabricate {0}".format(self._caliber.unparseToString())
                else:
                        return "fabricate"
        
class MgPartnerAbility(MgKeywordAbility):
        """Partner or Partner with [name]"""
        pass
        
class MgImproviseAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "improvise"
        
class MgAftermathAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "aftermath"
        
class MgEnbalmAbility(MgKeywordAbility):
        """Embalm [cost]"""
        pass
        
class MgEternalizeAbility(MgKeywordAbility):
        """Eternalize [cost]"""
        pass
        
class MgAfflictAbility(MgKeywordAbility):
        """Afflict N"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "afflict {0}".format(self._caliber.unparseToString())
                else:
                        return "afflict"
        
class MgAscendAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "ascend"
        
class MgAssistAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "assist"
                
class MgMentorAbility(MgKeywordAbility):
        def __init__(self):
                super().__init__()
                
        def isChild(self,child):
                """This node has no children."""
                False
                
        def getTraversalSuccessors(self):
                """This node has no successors."""
                return []
                
        def unparseToString(self):
                return "mentor"
                
class MgSurveilAbility(MgKeywordAbility):
        """'surveil N'"""
        def __init__(self,caliber):
                """caliber: The number value (N) associated with this card, as in 'AbilityName N'."""
                super().__init__()
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def getCaliber(self):
                """Get the caliber of this ability. This is the number value (N) associated with the card."""
                return self._caliber
                
        def setCaliber(self,caliber):
                """Set the caliber of this ability. This is the number value (N) associated with the card."""
                self._caliber = caliber
                if self._caliber is not None:
                        self._caliber.setParent(self)
                
        def isChild(self,child):
                """This node has one child, its caliber."""
                return child is not None and child == self._caliber
                
        def getTraversalSuccessors(self):
                """This node can have up to one successor, its caliber."""
                return [node for node in {self._caliber} if node is not None and node.isTraversable()]
                
        def unparseToString(self):
                if self._caliber is not None:
                        return "surveil {0}".format(self._caliber.unparseToString())
                else:
                        return "surveil"
        
class MgJumpStartAbility(MgKeywordAbility):
        """'Jump-Start [cost]'"""
        pass


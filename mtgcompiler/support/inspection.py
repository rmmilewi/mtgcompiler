import abc
"""Here we have all of the routines for inspecting parts of cards, defining visitors, et cetera."""


class AbstractVisitor(metaclass=abc.ABCMeta):
        """Abstract parent class for all graph visitors."""
        
        @abc.abstractmethod
        def atTraversalStart(self):
                """Called when the traversal starts."""
                raise NotImplemented
                
        @abc.abstractmethod        
        def atTraversalEnd(self):
                """Called when the traversal terminates."""
                raise NotImplemented
                
        def traverse(self,node):
                """Launches the visitor, calls visit on the targeted node."""
                self.atTraversalStart()
                node.accept(self)
                self.atTraversalEnd()
        
        def visit(self,node):
                """The visitor looks to see if a class-specific visit method has been implemented. Otherwise, it
                just calls a generic visit method. Visit methods take the form of visit_CLASSNAME(self,node)."""
                className = node.__class__.__name__
                visit_op = getattr(self, "visit_{0}".format(className), None)
                if callable(visit_op):
                        visit_op(node)
                else:
                        self.visit_generic(node)
        
        def visit_generic(self,node):
                """This is the fallback method if a matching method for a node class has not been implemented.
                This method can be overridden by AbstractVisitor's child classes to change the default behavior.
                """
                successors = node.getTraversalSuccessors()
                for successor in successors:
                        successor.accept(self)
                        
def getAllNodesOfType(root,nodeclass):
        """
        A primitive traversal method that collects all nodes of a given type and provides them in a container.
        
        root: The starting point for the traversal. Usually this is an MgCard object.
        nodeclass: The class of node that we want to search for.
        
        """
        class NodeAggregator(AbstractVisitor):
                def __init__(self,nodeclass):
                        self._nodeclass = nodeclass
                        self._container = []
                def atTraversalStart(self):
                        pass
                def atTraversalEnd(self):
                        pass
                def visit_generic(self,node):
                        if type(node) == self._nodeclass:
                                self._container.append(node)
                        successors = node.getTraversalSuccessors()
                        for successor in successors:
                                successor.accept(self)
                def getContainer(self):
                        return self._container
        aggregator = NodeAggregator(nodeclass)
        aggregator.traverse(root)
        return aggregator.getContainer()
                
        
        
        

class SimpleGraphingVisitor(AbstractVisitor):
        def __init__(self,path="card.dot"):
                self.outputPath = path
                self.graphFile = None
                
        def atTraversalStart(self):
                self.graphFile = open(self.outputPath,'w')
                self.graphFile.write("digraph \"g\" {\n")
                
        def atTraversalEnd(self):
                self.graphFile.write("}\n")
                self.graphFile.close()
                
        def visit_MgCard(self,node):
                if node.hasName():
                        name = node.getName()
                        if name.isTraversable():
                                self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Name\",labelfontcolor=red];\n".format(id(node),id(name)))
                                
                if node.hasManaCost():
                        ManaCost = node.getManaCost()
                        if ManaCost.isTraversable():
                                self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Mana Cost\",labelfontcolor=red];\n".format(id(node),id(ManaCost)))
                                
                if node.hasColorIndicator():
                        ColorIndicator = node.getColorIndicator()
                        if ColorIndicator.isTraversable():
                                self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Color Indicator\",labelfontcolor=red];\n".format(id(node),id(ColorIndicator)))
                                
                if node.hasTypeLine():
                        TypeLine = node.getTypeLine()
                        if TypeLine.isTraversable():
                                self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Type Line\",labelfontcolor=red];\n".format(id(node),id(TypeLine)))
                                
                if node.hasLoyalty():
                        Loyalty = node.getLoyalty()
                        if Loyalty.isTraversable():
                                self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Loyalty\",labelfontcolor=red];\n".format(id(node),id(Loyalty)))
                                
                if node.hasTextBox():
                        TextBox = node.getTextBox()
                        if TextBox.isTraversable():
                                self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Text Box\",labelfontcolor=red];\n".format(id(node),id(TextBox)))
                
                if node.hasPowerToughness():
                        PowerToughness = node.getPowerToughness()
                        if PowerToughness.isTraversable():
                                self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Power and Toughness\",labelfontcolor=red];\n".format(id(node),id(PowerToughness)))
                                
                if node.hasHandModifier():
                        HandModifier = node.getHandModifier()
                        if HandModifier.isTraversable():
                                self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Hand Modifier\",labelfontcolor=red];\n".format(id(node),id(HandModifier)))
                                
                if node.hasLifeModifier():
                        LifeModifier = node.getLifeModifier()
                        if LifeModifier.isTraversable():
                                self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Life Modifier\",labelfontcolor=red];\n".format(id(node),id(LifeModifier)))
                                
                self.visit_generic(node)
                
                
        def visit_MgTypeLine(self,node):
                supertypes = node.getSupertypes()
                if supertypes is not None and supertypes.isTraversable():
                        self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Supertypes\",labelfontcolor=red];\n".format(id(node),id(supertypes)))
                        
                Types = node.getTypes()
                if Types is not None and Types.isTraversable():
                        self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Types\",labelfontcolor=red];\n".format(id(node),id(Types)))
                        
                Subtypes = node.getSubtypes()
                if Subtypes is not None and Subtypes.isTraversable():
                        self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Subtypes\",labelfontcolor=red];\n".format(id(node),id(Subtypes)))
                        
                self.visit_generic(node)
                
        def visit_MgActivationStatement(self,node):
                if node.getCost() is not None:
                        self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"activation cost\",labelfontcolor=red];\n".format(id(node),id(node.getCost())))
                if node.getInstructions() is not None:
                        self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"instructions\",labelfontcolor=red];\n".format(id(node),id(node.getInstructions())))
                
                self.visit_generic(node)
                
        
        def visit_MgDealsDamageExpression(self,node):
                if node.getOrigin() is not None:
                        self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Source of damage\",labelfontcolor=red];\n".format(id(node),id(node.getOrigin())))
                if node.hasDamageExpression():
                        self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Amount of damage\",labelfontcolor=red];\n".format(id(node),id(node.getDamageExpression())))
                if node.hasSubject():
                        self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"Subject of damage\",labelfontcolor=red];\n".format(id(node),id(node.getSubject())))
                self.visit_generic(node)
        #def visit_MgNameReference(self,node):
        #        if node.hasAntecedent():
        #                antecedent = node.getAntecedent()
        #                self.graphFile.write("id{0} -> id{1} [color=red,style=dotted,label=\"antecedent\",labelfontcolor=red];\n".format(id(node),id(antecedent)))
        #        self.visit_generic(node)
                
        
        def visit_generic(self,node):
                self.graphFile.write("id{0} [label = \"{1} \n({2})\"];\n".format(id(node),node.__class__.__name__,node.unparseToString().lower()))
                successors = node.getTraversalSuccessors()
                for successor in successors:
                        successor.accept(self)
                        self.graphFile.write("id{0} -> id{1};\n".format(id(node),id(successor)))
                        self.graphFile.write("id{1} -> id{0} [color=blue,style=dotted,label=\"parent\",labelfontcolor=blue];\n".format(id(node),id(successor)))
        

                
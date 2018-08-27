import abc


class AbstractVisitor(metaclass=abc.ABCMeta):
        """Abstract parent class for all graph visitors."""
        
        @abc.abstractmethod
        def run(self):
                """Launches the visitor, calls visit on the targeted node."""
                raise NotImplemented
        
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


class SimpleGraphingVisitor(AbstractVisitor):
        def __init__(self,node,path="card.dot"):
                self.outputPath = path
                self.graphFile = None
                self.startNode = node
                
        def run(self):
                self.graphFile = open(self.outputPath,'w')
                self.graphFile.write("digraph \"g\" {\n")
                self.startNode.accept(self)
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
        
        def visit_generic(self,node):
                self.graphFile.write("id{0} [label = \"{1} \n({2})\"];\n".format(id(node),node.__class__.__name__,node.unparseToString().lower()))
                successors = node.getTraversalSuccessors()
                for successor in successors:
                        successor.accept(self)
                        self.graphFile.write("id{0} -> id{1};\n".format(id(node),id(successor)))
                        self.graphFile.write("id{1} -> id{0} [color=blue,style=dotted,label=\"parent\",labelfontcolor=blue];\n".format(id(node),id(successor)))
        

                
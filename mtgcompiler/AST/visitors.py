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
                
        def visit_MgTypeExpression(self,node):
                variables = [i for i in dir(node) if not callable(i)]
                print(variables)
                self.visit_generic(node)
                
        #def visit_MgManaSymbol(self,node):
        #        print("Mana symbol!")
        
        def visit_generic(self,node):
                self.graphFile.write("id{0} [label = \"{1} \n({2})\"];\n".format(id(node),node.__class__.__name__,node.unparseToString().lower()))
                successors = node.getTraversalSuccessors()
                for successor in successors:
                        successor.accept(self)
                        self.graphFile.write("id{0} -> id{1};\n".format(id(node),id(successor)))
                        self.graphFile.write("id{1} -> id{0} [color=blue,style=dotted,label=\"parent\",labelfontcolor=blue];\n".format(id(node),id(successor)))
        

                
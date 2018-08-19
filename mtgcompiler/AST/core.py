import abc

class MgNode(metaclass=abc.ABCMeta):
        """This is the abstract base class for all AST classes."""

        def setParent(self, parent):
                """Setter method for the parent node. The parent node is the ancestor of a given node."""
                self._parent=parent

        def getParent(self):
                """Access method for the parent node. The parent node is the ancestor of a given node."""
                return self._parent
        
        def setTraversable(self,traversable):
                """Setter method for the traversable flag.The traversable flag indicates whether
                the given node can be visited by visitors. Each class is expected to provide a 
                default value for this flag in their constructor(s)."""
                self._traversable = traversable

        def isTraversable(self):
                """Getter method for the traversable flag. The traversable flag indicates whether
                the given node can be visited by visitors. Each class is expected to provide a 
                default value for this flag in their constructor(s)."""
                return self._traversable
                
        @abc.abstractmethod
        def isChild(self,child):
                """Query method that checks whether a node is a child of the current node."""
                raise NotImplemented
        
        @abc.abstractmethod
        def getTraversalSuccessors(self):
                """This method returns all children of the current node that are
                considered traversable. This is method is called by visitors.
                The implementation of this method is specific to each class, but it is
                expected that a node will respect the traversable flag of a child when
                deciding whether to expose it for visitation."""
                raise NotImplemented
    
        @abc.abstractmethod
        def unparseToString(self):
                """This method unparses the AST node.
                Any class that inherits from MgNode is responsible for defining just what that means for itself.
                Note that a frontend may have its own conventions for unparsing and can define its own methods 
                for doing this rather than using the default method provided by the class."""
                raise NotImplemented
        
        def accept(self,visitor):
                """This is the accept operation for the Visitor pattern."""
                visitor.visit(self)
        
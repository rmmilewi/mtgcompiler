import abc

class MgNode(metaclass=abc.ABCMeta):
        """This is the abstract base class for all AST classes."""
        
        def getAnnotation(self,handle):
                """Annotations are arbitrary objects that can be attached to nodes. annotations can be used by
                an (un)parser or analysis routine to decorate nodes with relevant information. Annotations
                are stored in a dictionary that maps strings to annotations. This dictionary initially undefined, but
                if the user calls any annotation-related method, then an empty dictionary is created.
                
                This method attempts to fetch an annotation with the given lookup key. This method will raise an
                exception if no such handle exists.
                """
                if not hasattr(self, '_annotations'):
                        self._annotations = {}
                
                return self._annotations[handle]
                
        def hasAnnotation(self,handle):
                """Annotations are arbitrary objects that can be attached to nodes. annotations can be used by
                an (un)parser or analysis routine to decorate nodes with relevant information. annotations
                are stored in a dictionary that maps strings to annotations. This dictionary initially undefined, but
                if the user calls any annotation-related method, then an empty dictionary is created.
                
                This method checks to see whether the given lookup key is in the annotation dictionary.
                """
                
                if not hasattr(self, '_annotations'):
                        self._annotations = {}
                
                return handle in self._annotations
                
        def setAnnotation(self,handle,annotation):
                """Annotations are arbitrary objects that can be attached to nodes. annotations can be used by
                an (un)parser or analysis routine to decorate nodes with relevant information. Annotations
                are stored in a dictionary that maps strings to annotations. This dictionary initially undefined, but
                if the user calls any annotation-related method, then an empty dictionary is created.
                
                This method stores the given object in the dictionary with the handle as the key.
                """
                
                if not hasattr(self, '_annotations'):
                        self._annotations = {}
                        
                self._annotations[handle] = attr

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
        
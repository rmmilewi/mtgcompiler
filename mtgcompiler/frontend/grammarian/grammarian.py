"""
This is the code for Grammarian, which is an internal metalanguage and frontend for the Magic language.
The Grammarian language (file extension .grm) is a superset of Lark which gets transcompiled to
plain Lark for use by Arbor. Grammarian's own grammar is written in Lark. 
"""
from lark import Lark #Lexing and parsing!
from lark import Transformer #Converting the parse tree into something useful.
from lark.tree import pydot__tree_to_png #For rendering the parse tree.
from lark.lexer import Token
import abc

class GrmIRNode(metaclass=abc.ABCMeta):
        """The abstract base class for all Grammarian IR classes."""
        
        def unparseToString(self):
                """
                Unparse the IR node to a string.
                Used to assemble the final grammar.
                """
                raise NotImplemented

class GrmProductionDeclaration(GrmIRNode):
        """
        Represents a rule or terminal definition.
        """
        def __init__(self,name,isToken,productionDef):
                """
                name: The identifier for the production, a string.
                isToken: A boolean flag indicating whether or not this production is for a token.
                expansions: A list of expansions associated with this production.
                """
                self._name = name
                self._isToken = isToken
                self.productionDefs = [productionDef]
                
        def isToken(self):
                """Checks whether this production declaration is flagged as being for a token."""
                return self._isToken
                
        def getName(self):
                """
                Gets the name associated with the production.
                """
                return self._name
                
        def appendDefinition(self,definition):
                """
                Adds a production definition to the list of definitions.
                This is done when used in merging rules.
                """
                self._productionDefs.append(definition)
                
        def getDefinitions(self):
                """
                Get the definition(s) associated with this declaration.
                """
                return self._productionDefs
                
        def unparseToString(self):
                return "{0}: {1}\n".format(self._name,"\n|".join(self._productionDefs.unparseToString()))

class GrmProductionDefinition(GrmIRNode):
        """
        Represents the definition of a rule/terminal declaration.
        A production declaration normally has only one definition, but
        if we are merging more than one declaration, then there can be more
        than one definition.
        """
        def __init__(self,expr):
                """
                expr: The underlying expression.
                """
                self._expr = expr
                
        def getExpr(self,expr):
                return self._expr
                
        def unparseToString(self):
                return self._expr.unparseToString()
                
                
class GrmExpansionList(GrmIRNode):
        """Represents an 'expansions' rule in the parse tree."""
        def __init__(self,children):
                """
                children: A list of child nodes.
                """
                self._children = children
                
        def getChildren(self):
                """Returns the children associated with this node."""
                return self._children
        
        def unparseToString(self):
                return "|".join(self._children.unparseToString())
                

                
# class GrmNameReference(object):
#         """
#         Represents a name used in a production.
#         """
#         def __init__(self,value):
#                 """
#                 value: The string value of the name.
#                 """
#                 self._nameRef = value
                
                
        
                
# class GrmSymbol(object):
#         """
#         A name of a rule or terminal is represented as a GrmSymbol. Symbols are tracked
#         in a global symbol table so we know what refers to what in the grammar.
#         """
#         def __init__(identifier):
#                 """
#                 identifier: A string that is the symbol name.
#                 declaration: The production that defines this symbol.
#                 """
#                 self._identifier = identifier
#                 self._declaration = None
#
#         def hasDeclaration(self):
#                 """Checks to see whether the symbol has been matched with a declaration."""
#                 return self._declaration is not None
#
#         def getDeclaration(self):
#                 """Gets the declaration (a production) associated with the symbol."""
#                 return self._declaration
#
#         def setDeclaration(self,production):
#                 """Assigns a production that is the declaration for this symbol."""
#                 self._declaration = production
#

class GrammarAssembler(Transformer):
        def __init__(self):
                self._declarationTable = []
                self._globalNameTable = set()
                
        def production(self,items,isToken):
                print(items)
                productionIdentifier = items[0].value
                productionDefinition = items[1]
                
                
                if productionIdentifier not in [r.getName() for r in self._declarationTable]:
                        production = GrmProductionDeclaration(productionIdentifier,isToken,productionDefinition)
                        self._declarationTable.append(production)
                        self._globalNameTable.add(productionIdentifier)
                
        def token(self,items):
                self.production(items,isToken=True)
                
        def rule(self,items):
                self.production(items,isToken=False)
                
        def productiondefinition(self,items):
                return GrmProductionDefinition(items[0])
                
        

def _createGrammarianFrontend(grammarianPath):
        """
        Generates the Lark frontend for Grammarian.
        grammarianPath: The path to the grammarian language definition, written in Lark.
        """
        with open(grammarianPath,'r') as gfile:
                grammarText = gfile.read()
        lp = Lark(grammarText,parser="lalr",start="start",debug=True)
        return lp
    
def requestGrammar(imports,options={}):
        """
        Requests that Grammarian construct a Lark grammar given a list of grm targets (the imports)
        and (optionally) a set of flags that control the operation of Grammarian (the options).
        
        imports: A list of strings that specify paths to grm files to be loaded. Grm files are loaded
        in the order that they are provided. Paths are expected to be relative to the specification
        directory.
        options: A dictionary of options, where the keys are option name strings and the values are
        the options.
        """
        
        if "devGrammarianPath" in options:
                #devGrammarianPath: where Grammarian should look for its own Lark grammar file.
                #You don't want to change the default unless you're certain of what you're doing.
                grammarianPath = options["devGrammarianPath"]
        else:
                grammarianPath = "mtgcompiler/frontend/grammarian/grmgrammar.lark"
                
        if "devSpecificationPath" in options:
                #devSpecificationDirectory: The directory containing the Magic grammar specification.
                #You don't want to change the default unless you're certain of what you're doing.
                specificationPath = options["devSpecificationDirectory"]
        else:
                specificationPath = "mtgcompiler/frontend/grammarian/magicspec"
        
        #Load the Lark-based Grammarian frontend.
        frontend = _createGrammarianFrontend(grammarianPath)
        asmblr = GrammarAssembler()
        
        for grmpath in imports:
                grmpath = "{0}/{1}".format(specificationPath,grmpath)
                with open(grmpath,'r') as grmfile:
                        grmtext = grmfile.read()
                print("parsing grm file")
                parsetree = frontend.parse(grmtext)
                print(parsetree.pretty())
                pydot__tree_to_png(parsetree, "lark_test.png")
                asmblr.transform(parsetree)
        
requestGrammar(["base/valueexpressions.grm"])
        
        
        
#lp = createGrammarianFrontend()

#testinputs = ["!foo.5: (bar foo) _baz | baz bar \"dog\""]

#for s in testinputs:
#    parsetree = lp.parse(s)
#    print(parsetree.pretty())
#    pydot__tree_to_png(parsetree, "lark_test.png")
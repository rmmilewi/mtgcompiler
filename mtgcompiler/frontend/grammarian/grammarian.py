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
                
class GrmImport(GrmIRNode):
        """
        Represents an import statement.
        """
        def __init__(self,importTarget,importAlias=None):
                """
                importTarget: The import args.
                importAlias: The alias for the import
                """
                self._importTarget = importTarget
                self._importAlias = importAlias
                
        def unparseToString(self):
                if self._importAlias is not None:
                        return "%import {0} -> {1}\n".format(self._importTarget.unparseToString(),self._importAlias)
                else:
                        return "%import {0}\n".format(self._importTarget.unparseToString())
        

class GrmImportArgs(GrmIRNode):
        """
        Represents import args.
        """
        def __init__(self,pathArgs):
                """
                pathArgs: The import path.
                """
                self._pathArgs = pathArgs
                
        def unparseToString(self):
                return ".".join([path.unparseToString() for path in self._pathArgs])
        
class GrmIgnore(GrmIRNode):
        """
        Represents an import statement.
        """
        def __init__(self,ignored):
                """
                ignored: The name of the thing to be ignored
                """
                self._ignored = ignored
        
        def unparseToString(self):
                return "%ignore {0}\n".format(self._ignored.unparseToString())

class GrmProductionDeclaration(GrmIRNode):
        """
        Represents a rule or terminal declaration.
        """
        def __init__(self,name,isToken,productionDef):
                """
                name: The identifier for the production, a string.
                isToken: A boolean flag indicating whether or not this production is for a token.
                expansions: A list of expansions associated with this production.
                """
                self._name = name
                self._isToken = isToken
                self._productionDefs = [productionDef]
                
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
                return "{0}: {1}\n".format(self._name,"\n|".join([pdef.unparseToString() for pdef in self._productionDefs]))

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
        """
        Represents an 'expansions' rule in the parse tree.
        """
        def __init__(self,children):
                """
                children: A list of child nodes.
                """
                self._children = children
                
        def getChildren(self):
                """Returns the children associated with this node."""
                return self._children
        
        def unparseToString(self):
                return " | ".join([child.unparseToString() for child in self._children])
                
class GrmExpansion(GrmIRNode):
        """
        Represents an 'expansion' rule in the parse tree.
        """
        def __init__(self,children):
                """
                children: A list of child nodes.
                """
                self._children = children
                
        def getChildren(self):
                """Returns the children associated with this node."""
                return self._children
        
        def unparseToString(self):
                return " ".join([child.unparseToString() for child in self._children])
                
class GrmGroup(GrmIRNode):
        """
        Represents an 'group' rule in the parse tree.
        """
        def __init__(self,children):
                """
                children: A list of child nodes.
                """
                self._children = children
                
        def getChildren(self):
                """Returns the children associated with this node."""
                return self._children
        
        def unparseToString(self):
                return "({0})".format(" ".join([child.unparseToString() for child in self._children]))
                
class GrmGroup(GrmIRNode):
        """
        Represents an 'group' node in the parse tree.
        """
        def __init__(self,children):
                """
                children: A list of child nodes.
                """
                self._children = children
                
        def getChildren(self):
                """Returns the children associated with this node."""
                return self._children
        
        def unparseToString(self):
                return "({0})".format(" ".join([child.unparseToString() for child in self._children]))
                

class GrmGroup(GrmIRNode):
        """
        Represents an 'group' node in the parse tree.
        """
        def __init__(self,children):
                """
                children: A list of child nodes.
                """
                self._children = children
                
        def getChildren(self):
                """Returns the children associated with this node."""
                return self._children
        
        def unparseToString(self):
                return "({0})".format(" ".join([child.unparseToString() for child in self._children]))
                
class GrmMaybe(GrmIRNode):
        """
        Represents an 'maybe' node in the parse tree.
        """
        def __init__(self,children):
                """
                children: A list of child nodes.
                """
                self._children = children
                
        def getChildren(self):
                """Returns the children associated with this node."""
                return self._children
        
        def unparseToString(self):
                return "[{0}]".format(" ".join([child.unparseToString() for child in self._children]))                
        
                
class GrmExpr(GrmIRNode):
        """
        Represents an 'expr' node in the parse tree.
        """
        def __init__(self,children):
                """
                children: A list of child nodes.
                """
                self._children = children
                
        def getChildren(self):
                """Returns the children associated with this node."""
                return self._children
        
        def unparseToString(self):
                return "".join([child.unparseToString() for child in self._children])
                
                
class GrmAliasExpression(GrmIRNode):
        """
        Represents an alias expression in the parse tree.
        """
        def __init__(self,expr,name):
                """
                expr: The thing that is aliased.
                name: the alias given to the aliased.
                """
                self._expr = expr
                self._name = name
        
        def unparseToString(self):
                return "{0} -> {1}".format(self._expr.unparseToString(),self._name)
                
                
class GrmNameReference(GrmIRNode):
        """
        Represents a name of a rule/token used in a production.
        """
        def __init__(self,name):
                """
                name: The string value of the name.
                """
                self._nameRef = name
                
        def getName(self):
                return self._nameRef
                
        def unparseToString(self):
                return self._nameRef
        
class GrmLiteral(GrmIRNode):
        """
        Represents a literal used in a production.
        """
        def __init__(self,value):
                """
                value: The string value of the name.
                """
                self._value = value
                
        def getValue(self):
                return self._value
                
        def unparseToString(self):
                return self._value
                
class GrmQuantifierSymbol(GrmIRNode):
        """
        Represents a quantifier symbol used in a production.
        """
        def __init__(self,value):
                """
                value: The string value of the quantifier symbol.
                """
                self._value = value
                
        def getValue(self):
                return self._value
                
        def unparseToString(self):
                return self._value
                
class GrmNumberRange(GrmIRNode):
        """
        Represents a number range quantifier used in a production.
        """
        def __init__(self,lbound,ubound=None):
                """
                lbound: The lower bound of the range. If there is only one number, then
                the bound is exact.
                ubound: The upper bound of the range (optional).
                """
                self._lbound = lbound
                self._ubound = ubound
        
        def unparseToString(self):
                if self._ubound is None:
                        return "~{0}".format(self._lbound)
                else:
                        return "~{0}..{1}".format(self._lbound,self._ubound)
                

class GrammarAssembler(Transformer):
        def __init__(self,generateDummyRules):
                """
                generateDummyRules: A boolean that indicates whether the generator 
                should come up with rules/tokens that match currently undefined names 
                in the grammar. Used when doing unit tests on the grammar.
                """
                self._statementTable = []
                self._globalNameTable = set()
                self._unresolvedNamesTable = set()
                self._generateDummyRules = generateDummyRules
                
        def production(self,items,isToken):
                productionIdentifier = items[0]
                productionDefinition = items[1]
                if productionIdentifier in self._unresolvedNamesTable:
                        #If we scan a definition that uses a rule/token before its declaration has been
                        #reached, it will be in the unresolved names table. If we find a matching declaration,
                        #we can remove the name from that table.
                        self._unresolvedNamesTable.remove(productionIdentifier)
                if productionIdentifier not in [r.getName() for r in self._statementTable]:
                        production = GrmProductionDeclaration(productionIdentifier,isToken,productionDefinition)
                        self._statementTable.append(production)
                        self._globalNameTable.add(productionIdentifier)
                        
        def expansions(self,items):
                return GrmExpansionList(items)
                
        def expansion(self,items):
                return GrmExpansion(items)
                
        def group(self,items):
                return GrmGroup(items)
                
        def maybe(self,items):
                return GrmMaybe(items)
                
        def expr(self,items):
                return GrmExpr(items)
                
        def quantifier(self,items):
                return items[0]
                
        def ignore(self,items):
                return GrmIgnore(items[0])
                
        def qsymbol(self,items):
                symbolValue = items[0].value
                return GrmQuantifierSymbol(symbolValue)
                
        def qnumberrange(self,items):
                lbound = items[0].value
                if len(items) > 1:
                        ubound = items[1].value
                else:
                        ubound = None
                return GrmNumberRange(lbound,ubound)
                
        def alias(self,items):
                aliasName = items[1].value
                return GrmAliasExpression(items[0],aliasName)
                
        def token(self,items):
                self.production(items,isToken=True)
                
        def rule(self,items):
                self.production(items,isToken=False)
                
        def literal(self,items):
                value = items[0].value
                return GrmLiteral(value)
                
        def name(self,items):
                name = items[0].value
                if name not in self._globalNameTable:
                        self._unresolvedNamesTable.add(name)
                return GrmNameReference(name)
                
        def import_args(self,items):
                for nameref in items:
                        if nameref.getName() in self._unresolvedNamesTable:
                                self._unresolvedNamesTable.remove(nameref.getName())
                return GrmImportArgs(items)
                
        def importstmt(self,items):
                importArgs = items[0]
                if len(items) > 1:
                        alias = items[1].value
                        if alias in self._unresolvedNamesTable:
                                self._unresolvedNamesTable.remove(alias)
                        self._globalNameTable.add(alias)
                else:
                        alias = None
                importStmt = GrmImport(importArgs,alias)
                self._statementTable.append(importStmt)
                
        def ignorestmt(self,items):
                ignoreStatement = GrmIgnore(items[0])
                self._statementTable.append(ignoreStatement)
        
        def productiondefinition(self,items):
                return GrmProductionDefinition(items[0])
                
        def getUnresolvedNamesTable(self):
                """Returns the set of unresolved names."""
                return self._unresolvedNamesTable
        
        def generateGrammar(self):
                """Return string containing a Lark-compatible grammar for Arbor to use."""
                output = ""
                for statement in self._statementTable:
                        unparsedStatement = statement.unparseToString()
                        #print(unparsedStatement)
                        output = output + unparsedStatement
                if self._generateDummyRules:
                        for name in self._unresolvedNamesTable:
                                rule = "{0}: \"{1}\"\n".format(name,name.upper())
                                output = output + rule
                return output

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
                
        if "devDefineMissingNames" in options:
                #devDefineMissingNames: For unit testing, we often want to load only part of the grammar.
                #sometimes that involves testing rules that have undefined rule/token names.
                #Setting this to true will allow Grammarian to create rules/tokens with names in all capital
                #letters that correspond to undeclared names.
                devDefineMissingNames = options["devDefineMissingNames"]
        else:
                devDefineMissingNames = False
        
        #Load the Lark-based Grammarian frontend.
        frontend = _createGrammarianFrontend(grammarianPath)
        asmblr = GrammarAssembler(generateDummyRules=devDefineMissingNames)
        
        for grmpath in imports:
                grmpath = "{0}/{1}".format(specificationPath,grmpath)
                with open(grmpath,'r') as grmfile:
                        grmtext = grmfile.read()
                #print("parsing grm file")
                parsetree = frontend.parse(grmtext)
                #print(parsetree.pretty())
                #pydot__tree_to_png(parsetree, "lark_test.png")
                asmblr.transform(parsetree)
        
        #TMP
        unresolvedNames = asmblr.getUnresolvedNamesTable()
        if len(unresolvedNames) > 0:
                print("UNRESOLVED NAMES: {0}".format(",".join(unresolvedNames))) #TMP
        
        outputGrammar = asmblr.generateGrammar()
        
        return outputGrammar
        
        
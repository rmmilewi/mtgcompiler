from mtgcompiler.frontend.compilers.BaseImplementation.BasePreprocessor import BasePreprocessor

class MtgJsonPreprocessor(BasePreprocessor):
        """The MtgJson preprocessor."""
        
        def __init__(self,options):
                pass #TODO
                
                
        def prelex(self,inputobj,flags,name):
                if name is not None:
                    if "," in name:
                        splitName = name.split(",")
                        inputobj = inputobj.replace(name,"~f")
                        inputobj = inputobj.replace(splitName[0],"~")
                    else:
                        inputobj = inputobj.replace(name,"~")

                inputobj = inputobj.lower()

                inputobj = inputobj.replace("his or her", "their")

                # Preprocessing step: Expand pronoun-related contractions.
                inputobj = inputobj.replace("it's", "it is")
                inputobj = inputobj.replace("you're", "you are")
                inputobj = inputobj.replace("they're", "they are")
                inputobj = inputobj.replace("you've", "you have")
                inputobj = inputobj.replace("isn't", "is not")
                inputobj = inputobj.replace("aren't", "are not")
                inputobj = inputobj.replace("don't", "do not")
                inputobj = inputobj.replace("doesn't", "does not")
                inputobj = inputobj.replace("can't", "can not")

                # Preprocessing step: Some 20-or-so cards use 'each' before a verb to emphasize that a subject is plural
                # For our purposes, this is just syntactic sugar, so we will remove it. Examples include:
                #       * "You and that player each draw a card"
                #       * "Up to X target creatures each gain [...]"
                #       * "Those players each discard two cards at random."
                # Only a couple of effects use this wording. If I'm missing any, I'll go back and add them here later.
                inputobj = inputobj.replace("each get", "get")
                inputobj = inputobj.replace("each gain", "gain")
                inputobj = inputobj.replace("each lose", "lose")
                inputobj = inputobj.replace("each draw", "draw")
                inputobj = inputobj.replace("each discard", "discard")
                inputobj = inputobj.replace("each sacrifice", "sacrifice")
                
                return inputobj
                
        def postlex(self,inputobj,flags):
                return inputobj
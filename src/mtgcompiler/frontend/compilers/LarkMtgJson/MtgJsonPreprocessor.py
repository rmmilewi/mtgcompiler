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

                def caseInsensitiveReplace(old, new, text):
                        idx = 0
                        while idx < len(text):
                                index_l = text.lower().find(old.lower(), idx)
                                if index_l == -1:
                                        return text
                                text = text[:index_l] + new + text[index_l + len(old):]
                                idx = index_l + len(new)
                        return text

                inputobj = caseInsensitiveReplace("his or her","their",inputobj)
                # Preprocessing step: Expand pronoun-related contractions.
                inputobj = caseInsensitiveReplace("it's","it is",inputobj)
                inputobj = caseInsensitiveReplace("you're","you are",inputobj)
                inputobj = caseInsensitiveReplace("they're","they are",inputobj)
                inputobj = caseInsensitiveReplace("you've","you have",inputobj)
                inputobj = caseInsensitiveReplace("isn't","is not",inputobj)
                inputobj = caseInsensitiveReplace("aren't","are not",inputobj)
                inputobj = caseInsensitiveReplace("don't","do not",inputobj)
                inputobj = caseInsensitiveReplace("doesn't","does not",inputobj)
                inputobj = caseInsensitiveReplace("can't","can not",inputobj)

                # Preprocessing step: Some 20-or-so cards use 'each' before a verb to emphasize that a subject is plural
                # For our purposes, this is just syntactic sugar, so we will remove it. Examples include:
                #       * "You and that player each draw a card"
                #       * "Up to X target creatures each gain [...]"
                #       * "Those players each discard two cards at random."
                # Only a couple of effects use this wording. If I'm missing any, I'll go back and add them here later.
                inputobj = caseInsensitiveReplace("each get","get",inputobj)
                inputobj = caseInsensitiveReplace("each gain","gain",inputobj)
                inputobj = caseInsensitiveReplace("each lose","lose",inputobj)
                inputobj = caseInsensitiveReplace("each draw","draw",inputobj)
                inputobj = caseInsensitiveReplace("each discard","discard",inputobj)
                inputobj = caseInsensitiveReplace("each sacrifice","sacrifice",inputobj)
                
                return inputobj
                
        def postlex(self,inputobj,flags):
                return inputobj
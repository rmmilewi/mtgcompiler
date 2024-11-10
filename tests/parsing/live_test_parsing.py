import sys, os, time, threading, logging
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)
import mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonCompiler as MtgJsonCompiler
from lark import UnexpectedInput, logger
from lark.exceptions import UnexpectedEOF, UnexpectedToken,UnexpectedCharacters
from lark.lexer import Token
from lark.parsers.earley_forest import TokenNode
from collections import defaultdict

import lark.parsers.earley,lark.parsers.xearley
import types, inspect


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

#Generate a wrapper for a given function that reports the inputs and outputs of that function.
def log_calls(method):
    if method.__name__ == "wrapper":
        return method  
    sig = inspect.signature(method) #get the names of parameters used by the function
    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        params = [f"{name}={value!r}" for name, value in bound_args.arguments.items()]
        print(f"Calling {method.__name__} with these parameters...")
        for parameter in params:
            if len(parameter) > 200:
                print(f"\t {parameter[:200]}...")
            else:
                print(f"\t {parameter[:200]}")
        result = method(*args, **kwargs)
        resultString = str(result)
        if len(resultString) > 200:
            print(f"{method.__name__} returned: {resultString[:200]}...")
        else:
            print(f"{method.__name__} returned: {resultString[:200]}")
        return result
    return wrapper
    
#Instrument each method in a class with wrappers to log calls and returns.
def instrument_methodsHeldByEntity(entity):
    for attr_name, attr_value in entity.__dict__.items():
        if callable(attr_value):
            setattr(entity, attr_name, log_calls(attr_value))
    return entity


def instrumentedVersionOfXEarleyParse(self, stream, columns, to_scan, start_symbol=None):
    """
    This is an instrumented version of the earley parser with dynamic lexing (xearley)
    which we're injecting into the class at runtime to get out detailed diagnostic information
    on what the parser is trying to do and where it is getting stuck.
    """

    def scan(i, to_scan):
        """The core Earley Scanner.

        This is a custom implementation of the scanner that uses the
        Lark lexer to match tokens. The scan list is built by the
        Earley predictor, based on the previously completed tokens.
        This ensures that at each phase of the parse we have a custom
        lexer context, allowing for more complex ambiguities."""

        node_cache = {}

        # 1) Loop the expectations and ask the lexer to match.
        # Since regexp is forward looking on the input stream, and we only
        # want to process tokens when we hit the point in the stream at which
        # they complete, we push all tokens into a buffer (delayed_matches), to
        # be held possibly for a later parse step when we reach the point in the
        # input stream at which they complete.
        for item in self.Set(to_scan):
            m = match(item.expect, stream, i)
            if m:
                t = Token(item.expect.name, m.group(0), i, text_line, text_column)
                delayed_matches[m.end()].append( (item, i, t) )

                if self.complete_lex:
                    s = m.group(0)
                    for j in range(1, len(s)):
                        m = match(item.expect, s[:-j])
                        if m:
                            t = Token(item.expect.name, m.group(0), i, text_line, text_column)
                            delayed_matches[i+m.end()].append( (item, i, t) )

                # XXX The following 3 lines were commented out for causing a bug. See issue #768
                # # Remove any items that successfully matched in this pass from the to_scan buffer.
                # # This ensures we don't carry over tokens that already matched, if we're ignoring below.
                # to_scan.remove(item)

        # 3) Process any ignores. This is typically used for e.g. whitespace.
        # We carry over any unmatched items from the to_scan buffer to be matched again after
        # the ignore. This should allow us to use ignored symbols in non-terminals to implement
        # e.g. mandatory spacing.
        for x in self.ignore:
            m = match(x, stream, i)
            if m:
                # Carry over any items still in the scan buffer, to past the end of the ignored items.
                delayed_matches[m.end()].extend([(item, i, None) for item in to_scan ])

                # If we're ignoring up to the end of the file, # carry over the start symbol if it already completed.
                delayed_matches[m.end()].extend([(item, i, None) for item in columns[i] if item.is_complete and item.s == start_symbol])

        next_to_scan = self.Set()
        next_set = self.Set()
        columns.append(next_set)
        transitives.append({})

        ## 4) Process Tokens from delayed_matches.
        # This is the core of the Earley scanner. Create an SPPF node for each Token,
        # and create the symbol node in the SPPF tree. Advance the item that completed,
        # and add the resulting new item to either the Earley set (for processing by the
        # completer/predictor) or the to_scan buffer for the next parse step.
        for item, start, token in delayed_matches[i+1]:
            if token is not None:
                token.end_line = text_line
                token.end_column = text_column + 1
                token.end_pos = i + 1

                new_item = item.advance()
                label = (new_item.s, new_item.start, i + 1)
                token_node = TokenNode(token, terminals[token.type])
                new_item.node = node_cache[label] if label in node_cache else node_cache.setdefault(label, self.SymbolNode(*label))
                new_item.node.add_family(new_item.s, item.rule, new_item.start, item.node, token_node)
            else:
                new_item = item

            if new_item.expect in self.TERMINALS:
                # add (B ::= Aai+1.B, h, y) to Q'
                next_to_scan.add(new_item)
            else:
                # add (B ::= Aa+1.B, h, y) to Ei+1
                next_set.add(new_item)

        del delayed_matches[i+1]    # No longer needed, so unburden memory

        if not next_set and not delayed_matches and not next_to_scan:
            considered_rules = list(sorted(to_scan, key=lambda key: key.rule.origin.name))
            print(f"\tCONSIDERED_RULES: {considered_rules}")
            raise UnexpectedCharacters(stream, i, text_line, text_column, {item.expect.name for item in to_scan},
                                       set(to_scan), state=frozenset(i.s for i in to_scan),
                                       considered_rules=considered_rules
                                       )

        return next_to_scan


    delayed_matches = defaultdict(list)
    match = self.term_matcher
    terminals = self.lexer_conf.terminals_by_name

    # Cache for nodes & tokens created in a particular parse step.
    transitives = [{}]

    text_line = 1
    text_column = 1

    ## The main Earley loop.
    # Run the Prediction/Completion cycle for any Items in the current Earley set.
    # Completions will be added to the SPPF tree, and predictions will be recursively
    # processed down to terminals/empty nodes to be added to the scanner for the next
    # step.
    i = 0
    for token in stream:
        print(f"\t\tCURRENT POSITION (line: {text_line}, column: {text_column}): {token}")
        print("\t\tDELAYED_MATCHES:",delayed_matches)
        print("\t\tTRANSITIVES:",transitives)
        self.predict_and_complete(i, to_scan, columns, transitives)

        to_scan = scan(i, to_scan)
        print("\t\tNEXT TO SCAN:",to_scan)

        if token == '\n':
            text_line += 1
            text_column = 1
        else:
            text_column += 1
        i += 1
        print("----------------------------")

    self.predict_and_complete(i, to_scan, columns, transitives)

    ## Column is now the final column in the parse.
    assert i == len(columns)-1
    return to_scan


lark.parsers.xearley.Parser._parse = instrumentedVersionOfXEarleyParse
#lark.parsers.earley.Parser = instrument_methodsHeldByEntity(lark.parsers.earley.Parser)
#lark.parsers.xearley.Parser = instrument_methodsHeldByEntity(lark.parsers.xearley.Parser)




# Configure logging to capture debug messages from Lark
logger.setLevel(logging.DEBUG)

# Spinner function to display while the task is running
def spinner():
    for char in "|/-\\":
        sys.stdout.write(f"\r{char} Processing...")
        sys.stdout.flush()
        time.sleep(0.1)

# Function to run the spinner in a separate thread
def spinner_thread(stop_event):
    while not stop_event.is_set():
        spinner()

def add_test_function(test_input, filename="test_random_parsings.py"):
    # Sanitize the input to create a valid Python function name
    sanitized_input = test_input.lower().replace(" ", "_").replace("'", "").replace("\"", "")
    function_name = f"test_parse_{sanitized_input}"

    # Create the function code as a string
    function_code = f"\ndef {function_name}():\n    parse('{test_input}')\n"

    # Check if the function already exists to avoid duplication
    if os.path.exists(filename):
        with open(filename, "r") as f:
            content = f.read()
            if function_name in content:
                print(f"{YELLOW}Function {function_name} already exists in {filename}.{RESET}")
                return

    # Append the new function to the specified file
    with open(filename, "a") as f:
        f.write(function_code)

    print(f"{GREEN}Added function {function_name} to {filename}.{RESET}")
    

def main():
    print("Enter text to process or type 'quit' to exit the program.")
    compiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.startRule": "cardtext", "parser.larkDebug": True})
    parser = compiler.getParser()
    preprocessor = compiler.getPreprocessor()
    
    #parser.parser._parse = types.MethodType(instrumentedVersionOfXEarleyParse, parser.parser)
    
    #parser.parser.parse.custom_method = types.MethodType(custom_method, parser)
    
    # Save the last tested string so we can make a test of it if we want
    lastTestedText = ''
    while True:
        # Event to signal spinner thread to stop
        stop_event = threading.Event()
        spinner_t = threading.Thread(target=spinner_thread, args=(stop_event,))

        try:
            user_input = input("Input: ")
            if user_input.lower() == 'quit':
                print("Exiting the program.")
                break
            elif user_input.lower() == 'make test':
                print(lastTestedText)
                if len(lastTestedText) > 0:
                    add_test_function(lastTestedText)
                else:
                    print(f"{YELLOW}No text to save to test!{RESET}")
            else:

                # Start spinner in a separate thread
                spinner_t.start()
                # Start timer
                start_time = time.time()

                # Save this text
                lastTestedText = user_input

                # result = process_input(user_input)
                text = preprocessor.prelex(user_input, None, None)
                card = parser.parse(text=text)

                stop_event.set()
                spinner_t.join()  # Ensure spinner thread finishes
                elapsed_time = time.time() - start_time
                print(f"{BLUE}Processed Result in {elapsed_time:.2f} seconds: {card}{RESET}")

        except KeyboardInterrupt:
            stop_event.set()
            spinner_t.join()  # Ensure spinner thread finishes
            print("\nProgram interrupted by user. Exiting.")
            break

        except UnexpectedInput as e:
            # Print detailed error information
            stop_event.set()
            spinner_t.join()  # Ensure spinner thread finishes
            print(f"{RED}!!!FAILURE!!!{RESET}")
            print(f"Error at line {e.line}, column {e.column}")
            print(f"Error Type {type(e)}")
            print(e)
            print(f"{e.get_context(lastTestedText)}")

            # Optionally, show expected tokens and their rules
            # print("Expected tokens:", e.expected)
            print("Error context:", e.match_examples(parser.parse, {"rule": [e.get_context(lastTestedText)]}))
            
            if isinstance(e,UnexpectedCharacters):
                print("Considered Rules:",e.considered_rules)
                print("Considered Tokens:",e.considered_tokens)
                print("Token History:",e.token_history)
                print("State:",e.state)
            
        
        except Exception as e:
            stop_event.set()
            spinner_t.join()  # Ensure spinner thread finishes
            print(f"{RED}!!!FAILURE!!!{RESET}")
            print(f"An error occurred: {e}")
            print("ERROR",e.state)

if __name__ == "__main__":
    main()

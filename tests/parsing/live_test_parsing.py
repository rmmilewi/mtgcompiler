import sys, os, time, threading, logging
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)
import mtgcompiler.frontend.compilers.LarkMtgJson.MtgJsonCompiler as MtgJsonCompiler
from lark import UnexpectedInput, logger
from lark.exceptions import UnexpectedEOF, UnexpectedToken,UnexpectedCharacters


RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

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
    compiler = MtgJsonCompiler.MtgJsonCompiler(options={"parser.startRule": "ability", "parser.larkDebug": True})
    parser = compiler.getParser()
    preprocessor = compiler.getPreprocessor()
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

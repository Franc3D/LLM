import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, available_functions

def main():
    load_dotenv()
    #Get the data from the .env file
    api_key = os.environ.get("GEMINI_API_KEY") #Environment variables are better than hardcoding sensitive information

    client = genai.Client(api_key=api_key)



    verbose = False
    args = sys.argv[1:]
    if "--verbose" in args:
        args.remove("--verbose")
        verbose = True

    #print(args)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)
    user_prompt = " ".join(args)
    # Implement as part of the chat message structure
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    reply = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        #contents=user_prompt, #"Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        contents=messages,
        config=types.GenerateContentConfig(
            #system_instruction=system_prompt ONLY USES THE SYSTEM PROMPT WITHOUT THE FUNCTIONS
            tools=[available_functions], # Use functions from get_files_info.py
            system_instruction=system_prompt # Text instructions
            )
        )

    if verbose:
        print("User prompt: {}".format(user_prompt))
        print("Prompt tokens: {}".format(reply.usage_metadata.prompt_token_count))
        print("Response tokens: {}".format(reply.usage_metadata.candidates_token_count))
    print("Response :")
    #print(reply.text) PRINTS THE LLM REPLY WITHOUT FUNCTION CALLS
    if reply.function_calls:
        for function_call in reply.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print("\n", reply.text)
            

if __name__ == "__main__":
    main()

"""
Important things to make a LLM work:

client.models.generate_content()
    Gives prompts and return an answer from the LLM, this is the lynchpin of the whole system

    - model= takes the model of the LLM

    - contents= uses types.Content(role=, parts=)
        Gives the LLM the prompt from the user and identifies the user
        - role= gives context to whom is speaking, could be the user or another AI
        - parts= as types.Part() 
            IS THE MESSAGE THAT IS BEING COMMUNICATED TO THE LLM. really important !
    
    - config= uses types.ConfigureContentConfig(tools=, system_instruction=)
        Gives context to the LLM as to how to behave and what is available to him 
        
        - tools= takes types.Tool(function-declaration=)
            This takes a list of all the functions declared using a FunctionDeclaration

            - function_declaration= uses a types.FunctionDeclaration(name=, description=, parameters=)
                Using this you can declare functions that the LLM will understand and use

                - name= the exact name of the function

                - description= a brief description of the function  so the LLM can understand what it works with

                - parameters= needs a JSON object that can be created using types.Schema(type=, properties=)
                    - type= needs to be JSON for the LLM to understand so : types.Type.OBJECT
                    - properties= in this case we want to assign the "directory": to a specific instruction string so we go 
                        "directory": types.Schema(
                            type=types.Type.STRING,
                            description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                        )

        - system_instruction= give a helpful explanation to the LLM as to what his job is
            It can be jokes, talking with an accent or making it swear but idealy make him helpful

"""
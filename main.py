import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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


    reply = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        #contents=user_prompt, #"Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
        contents=messages,
        )

    if verbose:
        print("User prompt: {}".format(user_prompt))
        print("Prompt tokens: {}".format(reply.usage_metadata.prompt_token_count))
        print("Response tokens: {}".format(reply.usage_metadata.candidates_token_count))
    print("Response :")
    print(reply.text)

if __name__ == "__main__":
    main()
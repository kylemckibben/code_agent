import argparse
import os

from call_function import available_functions, call_function
from constants import MODEL
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_content_response(model, contents, verbose=False):
    function_results = []
    return_response = []
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    function_calls = response.function_calls
    if len(function_calls) != 0:
        for function_call in function_calls:
            function_call_result = call_function(function_call, verbose)
            if len(function_call_result.parts) == 0 or function_call_result.parts is None:
                raise Exception("Error: missing function call results parts")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("Error: response cannot be None")
            function_results.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            # return_response.append(f"Calling function: {function_call.name}({function_call.args})")
    else:
        return_response.append(f"Response: {response.text}")
        if verbose == True:
            return_response.append(f"User prompt: {contents}")
            if response.usage_metadata is not None:
                if (response.usage_metadata.prompt_token_count is not None
                    and response.usage_metadata.candidates_token_count is not None
                ):
                    return_response.append(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                    return_response.append(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    return "\n".join(return_response)
    

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Show prompt token and candidates token count")

    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = generate_content_response(
        model=MODEL,
        contents=messages, 
        verbose=args.verbose,
    )

    print(response)

if __name__ == "__main__":
    main()

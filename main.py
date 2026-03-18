import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
model="gemini-2.5-flash"

def generate_content_response(contents, verbose=False):
    return_response = {}
    response = client.models.generate_content(
        model=model,
        contents=contents
    )
    return_response["Response"] = response.text
    if verbose == True:
        return_response["User prompt"] = contents
        if response.usage_metadata is not None:
            if (response.usage_metadata.prompt_token_count is not None
                and response.usage_metadata.candidates_token_count is not None
            ):
                return_response["Prompt tokens"] = response.usage_metadata.prompt_token_count
                return_response["Response tokens"] = response.usage_metadata.candidates_token_count
    return "\n".join([f"{key}: {value}" for key, value in return_response.items()])
    

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Show prompt token and candidates token count")

    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    response = generate_content_response(messages, args.verbose)

    print(response)

if __name__ == "__main__":
    main()

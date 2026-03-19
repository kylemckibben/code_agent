# code_agent

usage: `main.py [-h] [--verbose] user_prompt` where user_prompt is a string.

Currently a basic chatbot that takes a string prompt and option verbose flag and returns a response. The verbose flag adds the user prompt, prompt token count, and reponse token count to the output.

If you want to use this chatbot, add a `.env` file with your own Gemini API key like `GEMINI_API_KEY==<your_api_key>`

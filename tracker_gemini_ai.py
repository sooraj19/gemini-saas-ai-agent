import os
import subprocess
import sys

import google.generativeai as genai
from prompts import add_totals

API_KEY = os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def execute_gemini_prompt(prompt: str):
    print("GET_GEMINI_DEBUG_PRINT Prompt:" + prompt)
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json"
        )
    )
    print("GET_GEMINI_DEBUG_PRINT Response:" + response.text)
    return (response.text)


def clean_code(code_string):
    try:
        # Remove unnecessary characters
        cleaned_code = code_string.replace("{\"code\": ", "").replace("\"import", "import").replace("client.close()\"}",
                                                                                                    "client.close()").replace(
            "\\n", "\n").replace("\\\"", "\"")
        cleaned_code = cleaned_code.rstrip("\"}")

        # Execute the code
        return cleaned_code
    except Exception as e:
        print(f"Error executing code: {e}")


def execute_code(code, timeout=10):
    cleaned_code = clean_code(code)
    with open("temp_code.py", "w") as f:
        f.write(cleaned_code)
    try:
        result = subprocess.run([sys.executable, "temp_code.py"], capture_output=True, text=True, check=True,
                                timeout=timeout)
        return result.stdout, False
    except subprocess.CalledProcessError as e:
        return e.stdout + e.stderr, True
    except subprocess.TimeoutExpired:
        return "Execution timed out.", True


def generate_and_execute_code(prompt: str):
    error_exists = True
    retry_count = 0
    while error_exists:
        print("Generating code using Gemini API...")
        # Generate code using Gemini API
        code = execute_gemini_prompt(prompt)

        # Execute the code and capture the output
        print("Executing the code and checking for errors...")
        output, error_exists = execute_code(code)
        if error_exists and retry_count < 5:
            retry_count += 1
            print("Errors found, sending output to Gemini for fixing...")
            # Send the output to Gemini API to fix the errors
            prompt = f"The following Python code has some errors:\n\n{code}\n\nError message:\n{output}\n\nPlease fix the errors and provide the corrected code."

            if retry_count >= 5:
                print("Retries exceeded.. existing..")
                break

        return output

import requests
import re
import os
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "openai/gpt-oss-20b",
    "messages": [
        {"role": "user", "content": "Suggest five privacy-first tools for indie developers"}
    ]
}

response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)

if response.status_code == 200:
    print("\nGroq Agent Output:\n")
    try:
        output = response.json()["choices"][0]["message"]["content"]
        
        # Replace known problematic characters
        output = output.replace('\u2011', '-')  # non-breaking hyphen
        output = output.replace('\u2248', '~')  # approximately equal to

        # Remove any remaining non-ASCII characters (emojis, symbols)
        output = re.sub(r'[^\x00-\x7F]+', '', output)

        print(output)

        # Save to file
        with open("output_groq.txt", "w", encoding="utf-8") as f:
            f.write(output)
    except Exception as e:
        print(f"Error while processing output: {e}")
else:
    print(f"Error {response.status_code}: {response.text}")

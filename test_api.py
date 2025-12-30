from openai import OpenAI
import os

# STEP 1: Load API key from environment
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ API key NOT found. Set using:")
    print('setx OPENAI_API_KEY "sk-xxxx"')
    exit()

# STEP 2: Initialize client
client = OpenAI(api_key=api_key)

# STEP 3: Make a simple test call
try:
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": "Hello! Just testing if my API works."}
        ]
    )

    print("✅ API Test Successful!")
    print("ChatGPT says:", response.choices[0].message.content)

except Exception as e:
    print("❌ API Test Failed:")
    print(e)

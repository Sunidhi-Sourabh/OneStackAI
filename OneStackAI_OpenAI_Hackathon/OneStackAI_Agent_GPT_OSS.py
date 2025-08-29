from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from tools_query import (
    get_tools_by_category,
    get_tools_by_keyword,
    get_tools_by_feature,
    get_tools_by_category_and_pricing
)
import random

# Filter setup
category = "multimodal ai"
pricing = "free"
max_tokens = 2000  # You can adjust this for longer or shorter responses

# Use category + pricing filter
tools = get_tools_by_category_and_pricing(category, pricing)

if not tools:
    print(f"No tools found for category='{category}' with pricing='{pricing}'")
    exit()

# Select up to 5 tools
selected = random.sample(tools, min(5, len(tools)))

tool_descriptions = "\n".join(
    [f"{tool['Tool Name']}: {tool['Description']} ({tool['Free/Paid']}) - {tool['Tool Link']}" for tool in selected]
)

# Prompt for GPT-OSS
prompt = (
    f"You are an AI assistant helping indie developers choose tools.\n\n"
    f"Here are five tools:\n{tool_descriptions}\n\n"
    "For each tool, explain how it supports privacy, offline workflows, or customization. Avoid marketing language. Be direct, analytical, and helpful."
)

# Safe debug print
print("[DEBUG] Prompt:\n", prompt.encode('ascii', errors='ignore').decode())

# Load model
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Generate response
output = generator(prompt, max_length=max_tokens, do_sample=True, temperature=0.8, truncation=True)

# Extract response
response = output[0]['generated_text'].replace(prompt, "").strip()

# Post-processing: Add discoverability tag if HuggingChat is mentioned
if "huggingface.co/chat" in response.lower():
    response += "\n\nNote: HuggingChat is a known OSS suggestion platform—highlighted for strategic relevance."

# Refined fallback message
if not response:
    response = (
        f"No detailed recommendations were generated for category '{category}' with pricing '{pricing}'. "
        "This may be due to limited tool descriptions or model constraints. Consider adjusting the prompt or increasing max_tokens."
    )

print("\nGPT-OSS Response:\n")
print(response)

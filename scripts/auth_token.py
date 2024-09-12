from transformers import AutoTokenizer, AutoModelForCausalLM

# Set your Hugging Face API token
hf_token = "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"

# Define the correct model name
model_name = "meta-llama/Llama-2-7b-hf"

# Load the tokenizer and model with authentication
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=hf_token)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=hf_token)

from transformers import LlamaTokenizer, LlamaForCausalLM

# Load the trained model and tokenizer
tokenizer = LlamaTokenizer.from_pretrained('./trained_model')
model = LlamaForCausalLM.from_pretrained('./trained_model')

def generate_summary(text):
    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=128, num_beams=4, early_stopping=True)
    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Example usage
new_text = "Your new PPT text here"
summary = generate_summary(new_text)
print(summary)

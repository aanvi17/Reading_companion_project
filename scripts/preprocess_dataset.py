import os
from datasets import load_dataset, Dataset
from transformers import GPT2Tokenizer

# Set your Hugging Face token
token = "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"  # Ensure you have set your Hugging Face token as an environment variable

tokenizer = GPT2Tokenizer.from_pretrained('gpt2', token=token)

# Add padding token
tokenizer.add_special_tokens({'pad_token': '[PAD]'})

# Load the dataset
dataset = load_dataset('json', data_files='data/train_data.json')

# Split the dataset into training and test sets
dataset = dataset['train'].train_test_split(test_size=0.1)


# Preprocess the dataset
def preprocess_function(examples):
    inputs = examples['text']
    model_inputs = tokenizer(inputs, max_length=1024,padding='max_length', truncation=True)

    # with tokenizer.as_target_tokenizer():
    labels = tokenizer(examples['summary'], max_length=128,padding='max_length', truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Save the tokenized dataset
tokenized_dataset.save_to_disk('data/tokenized_dataset')
print("Tokenization completed and dataset saved.")
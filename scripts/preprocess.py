import os
import pandas as pd
from datasets import load_dataset
from transformers import BartTokenizer, BartForConditionalGeneration, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split

# Load the dataset from a JSON file
dataset = load_dataset('json', data_files='data/train_data.json')

# Split the dataset into training and test sets (90% train, 10% test)
train_test_split = dataset['train'].train_test_split(test_size=0.1)

# Load BART tokenizer
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')

# Preprocess function to tokenize text and summaries
def preprocess_function(examples):
# Tokenize input text
    model_inputs = tokenizer(examples['text'], max_length=1024, padding='max_length', truncation=True)
    
# Tokenize summaries
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(examples['summary'], max_length=128, padding='max_length', truncation=True)
    
# Add labels to model inputs
    model_inputs["labels"] = labels["input_ids"]
    
    return model_inputs

# Apply the preprocess function to the dataset
tokenized_datasets = train_test_split.map(preprocess_function, batched=True)

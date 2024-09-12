# fine_tune.py
from datasets import load_from_disk
from transformers import BartForConditionalGeneration, Trainer, TrainingArguments

# Load the preprocessed tokenized dataset
tokenized_datasets = load_from_disk('data/tokenized_dataset')

# Load the BART model for conditional generation
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",           # Output directory
    eval_strategy="epoch",      # Evaluate at the end of each epoch
    learning_rate=2e-5,               # Learning rate
    per_device_train_batch_size=4,    # Batch size for training
    per_device_eval_batch_size=4,     # Batch size for evaluation
    num_train_epochs=3,               # Number of training epochs
    weight_decay=0.01,                # Strength of weight decay
    save_total_limit=2,               # Only save the 2 most recent models
    save_steps=10_000,                # Save every 10,000 steps
    logging_dir='./logs',             # Directory for storing logs
    logging_steps=500,                # Log every 500 steps
)

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test'],
)

# Start training
trainer.train()

# Save the fine-tuned model and tokenizer
model.save_pretrained('./fine_tuned_bart')
print("Model saved successfully.")

import os
import logging
from transformers import LlamaForCausalLM, LlamaTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
from datasets import load_from_disk


# Enable verbose logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



try:
    # Load the dataset
    print("Loading tokenized dataset...")
    # dataset = load_dataset('json', data_files={'train': 'data/train_data.json'})
    # dataset = load_from_disk('data/tokenized_dataset')
    if not os.path.exists('data/tokenized_dataset'):
        raise FileNotFoundError("Tokenized dataset not found at 'data/tokenized_dataset'")
            
    dataset = load_from_disk('data/tokenized_dataset')
    print("Tokenized dataset loaded successfully.")
   

    # Load the pre-trained model and tokenizer
    print("Loading tokenizer and model...")
    # model_name = "gpt2"  # Temporarily using a smaller model for debugging
    model_name = "meta-llama/Llama-2-7b-hf"  # Replace with the actual path to the model D:\Pihu\Ppt_summarizer\Llama-2-7b-hf

    token = "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"  # Replace with your Hugging Face token  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
     # Adding more verbose output for debugging
    print(f"Using model name: {model_name}")
    print(f"Using Hugging Face token: {token}")
    
    print("Attempting to load model...")
    try:
        model = LlamaForCausalLM.from_pretrained(model_name, token=token)
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Failed to load model: {e}")
        raise
    
    print("Attempting to load tokenizer...")
    try:
        tokenizer = LlamaTokenizer.from_pretrained(model_name, token=token)
        print("Tokenizer loaded successfully.")
    except Exception as e:
        print(f"Failed to load tokenizer: {e}")
        raise
    print("Tokenizer and model loaded successfully.")


    # Fine-tune the model
    print("Setting up training arguments...")
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        num_train_epochs=3,
        weight_decay=0.01,
    )
    print("Training arguments set up successfully.")

    # Initialize the Trainer
    print("Initializing Trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset['train'],  # Assuming 'train' is the key in your tokenized dataset
    )
    print("Trainer initialized.")


    # Train the model
    print("Training the model...")
    trainer.train()
    print("Training completed.")


    # Create the directory if it doesn't exist
    if not os.path.exists('./trained_model'):
        os.makedirs('./trained_model')

    # Save the trained model
    print("Saving the trained model...")
    model.save_pretrained('./trained_model')
    tokenizer.save_pretrained('./trained_model')

    print("Model training completed and saved.")

except Exception as e:
    print(f"Error occurred: {e}")
    raise e  # Raise the exception to see full traceback
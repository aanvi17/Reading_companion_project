import os
import logging
import traceback
from transformers import  GPT2Tokenizer, GPT2LMHeadModel, TrainingArguments, Trainer,DataCollatorForLanguageModeling
from datasets import load_from_disk

# Enable verbose logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("training_log.log"),  # Log to file
        logging.StreamHandler()  # Log to console
    ]
)
logger = logging.getLogger(__name__)

model_name = "gpt2"

# Set your access token as an environment variable for security
os.environ["HUGGINGFACE_TOKEN"] = "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"  # Replace with your actual access token

try:
    # Load the tokenized dataset
    logger.info("Loading tokenized dataset...")
    if not os.path.exists('data/tokenized_dataset'):
        raise FileNotFoundError("Tokenized dataset not found at 'data/tokenized_dataset'")
    
    dataset = load_from_disk('data/tokenized_dataset')
    logger.info("Tokenized dataset loaded successfully.")

    logger.info(f"Using model name: {model_name}")
    logger.info("Attempting to load model...")

    try:
        tokenizer = GPT2Tokenizer.from_pretrained(model_name, token=os.environ["HUGGINGFACE_TOKEN"])

         # Add padding token
        tokenizer.add_special_tokens({'pad_token': '[PAD]'})

        model = GPT2LMHeadModel.from_pretrained(model_name, token=os.environ["HUGGINGFACE_TOKEN"])

        # Resize token embeddings because we've added new tokens
        model.resize_token_embeddings(len(tokenizer))

        logger.info("Tokenizer and model loaded successfully.")
    except Exception as e:
        logger.error(f"Failed to load tokenizer or model: {e}")
        logger.debug(traceback.format_exc())  # Print full stack trace
        raise e

    # Fine-tune the model
    logger.info("Setting up training arguments...")
    training_args = TrainingArguments(
        output_dir="./results",
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        num_train_epochs=3,
        weight_decay=0.01,
    )
    logger.info("Training arguments set up successfully.")

    # Define a compute metrics function
    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        logger.debug("Computing metrics...")
        return {"loss": predictions.loss}

    # Initialize the data collator
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    # Initialize the Trainer
    logger.info("Initializing Trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset['train'],
        eval_dataset=dataset['test'],
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    logger.info("Trainer initialized.")

    # Train the model
    logger.info("Training the model...")
    trainer.train()
    logger.info("Training completed.")

    # Create the directory if it doesn't exist
    if not os.path.exists('./trained_model'):
        os.makedirs('./trained_model')

    # Save the trained model
    logger.info("Saving the trained model...")
    model.save_pretrained('./trained_model')
    tokenizer.save_pretrained('./trained_model')

    logger.info("Model training completed and saved.")

except Exception as e:
    logger.error(f"Error occurred: {e}")
    logger.debug(traceback.format_exc())  # Print full stack trace
    raise e  # Raise the exception to see full traceback

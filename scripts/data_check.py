from datasets import load_from_disk

# Assuming your dataset is saved under 'data/tokenized_dataset'
dataset_path = 'data/tokenized_dataset'

# Load the dataset
dataset = load_from_disk(dataset_path)

# Check the keys to verify the dataset structure
print(dataset.keys())

# Access specific splits
train_dataset = dataset['train']
test_dataset = dataset['test']

# Check dataset sizes
print(f"Training examples: {len(train_dataset)}")
print(f"Testing examples: {len(test_dataset)}")

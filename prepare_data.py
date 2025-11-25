import json
import glob
import random
import os

# --- CONFIGURATION ---
# The system prompt tells the model how to behave for every single interaction
SYSTEM_PROMPT = (
    "You are a wise spiritual assistant trained on the Bhagavad Gita and Advaita Vedanta. "
    "Answer questions with deep philosophical insight, referencing scriptures where appropriate."
)

# Output filenames required by MLX
TRAIN_FILE = "train.jsonl"
VALID_FILE = "valid.jsonl"

# Get all JSON files in the current directory
json_files = glob.glob("*.json")

all_formatted_data = []

print(f"🔍 Found {len(json_files)} JSON files. Processing...")

for filename in json_files:
    # Skip technical files if they exist in the folder
    if filename in ['config.json', 'tokenizer.json', 'adapter_config.json', 'package.json']:
        continue
        
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
            # Ensure the file is a list of Q&A pairs
            if isinstance(data, list):
                count = 0
                for entry in data:
                    # We look for 'question' and 'answer' keys based on your sample file
                    if 'question' in entry and 'answer' in entry:
                        # Format for Llama 3 Chat
                        chat_entry = {
                            "messages": [
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": entry['question']},
                                {"role": "assistant", "content": entry['answer']}
                            ]
                        }
                        all_formatted_data.append(chat_entry)
                        count += 1
                print(f"   ✅ Loaded {count} pairs from {filename}")
            else:
                print(f"   ⚠️ Skipping {filename}: Root is not a list.")

    except Exception as e:
        print(f"   ❌ Error reading {filename}: {e}")

# --- SHUFFLE & SPLIT ---
# Randomize so the model doesn't learn patterns based on file order
random.shuffle(all_formatted_data)

# Split: 90% for training, 10% for validation
split_index = int(len(all_formatted_data) * 0.9)
train_data = all_formatted_data[:split_index]
valid_data = all_formatted_data[split_index:]

# --- SAVE TO JSONL ---
def save_to_jsonl(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for entry in data:
            json.dump(entry, f)
            f.write('\n')

save_to_jsonl(train_data, TRAIN_FILE)
save_to_jsonl(valid_data, VALID_FILE)

print("-" * 40)
print(f"🎉 SUCCESS! Merged Total: {len(all_formatted_data)} Q&A pairs")
print(f"📂 Created '{TRAIN_FILE}' with {len(train_data)} samples")
print(f"📂 Created '{VALID_FILE}' with {len(valid_data)} samples")
print("-" * 40)
print("👉 You can now run the training command.")
import fitz  # PyMuPDF
import pypdf
import torch

import pandas as pd
from datasets import Dataset, DatasetDict
from transformers import BigBirdTokenizer ,BigBirdForSequenceClassification, TrainingArguments, Trainer, AutoTokenizer, AutoModelForCausalLM
from sklearn.model_selection import train_test_split
import os

os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'
model_name = "google/bigbird-pegasus-large-arxiv"
tokenizer = BigBirdTokenizer.from_pretrained(model_name)
modelSequence = BigBirdForSequenceClassification.from_pretrained(model_name, num_labels=3)

def extract_text_from_pdf_without_chunks(pdf_path):
    """Extract text from a PDF file"""
    text = ""
    cnt = 0
    with open(pdf_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_pdf(pdf_path, chunk_size=4096):
    """Extract text from a PDF file"""
    text = ""
    with open(pdf_path, "rb") as file:
        reader = pypdf.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    print("First chunk text:\n", chunks[0])
    return chunks

def save_local_model(saved_path):
    model.save_pretrained(saved_path)
    tokenizer.save_pretrained(saved_path)

# Extract and chunk a sample PDF
pdf_path = "/Users/prateekpuri/ai_agent/miscllaneous1978/Allied_Q4AR_December-31-2024.pdf"
chunks = extract_text_from_pdf(pdf_path)

chunk_data = [{"chunk_id": i, "text": chunk} for i, chunk in enumerate(chunks)]

# Convert chunks into a DataFrame
df = pd.DataFrame(chunk_data)

# Split into train/test sets
train_texts, test_texts = train_test_split(df["text"].tolist(), test_size=0.2, random_state=42)

# Convert to Hugging Face Dataset format
train_dataset = Dataset.from_dict({"text": train_texts})
test_dataset = Dataset.from_dict({"text": test_texts})
tokenizer.pad_token = tokenizer.eos_token

def tokenize_function(examples):
    inputs = tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)
    inputs["labels"] = inputs["input_ids"].copy()
    return inputs

# Tokenize the dataset
train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)

# Load a pre-trained model
model = AutoModelForCausalLM.from_pretrained(model_name)

# Training arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=5e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=500,
    save_steps=10_000,
    save_total_limit=2,
    remove_unused_columns=False,  # Ensure labels are not removed
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset
)

# Start Training
trainer.train()
model_path = "./bigbird_trained_model"
save_local_model(model_path)

#def summarize_text(text, max_length=512):
#    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="longest", max_length=4096)
#    summary_ids = model.generate(**inputs, max_new_tokens=max_length, min_length=100, length_penalty=2.0, num_beams=4)
#    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)

# Example: Summarize a financial report
#test_text = extract_text_from_pdf_without_chunks(pdf_path)
#summary = summarize_text(test_text)
#print("\n **Generated Summary:**\n", summary)
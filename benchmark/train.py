'''Train a basic transformer model'''

from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import datasets
import numpy as np

batch_size = 8
num_labels = 4

# Load data
ds = datasets.load_dataset("./italki", data_dir="../italki_data")


# Init model and trainer
model_name = "bert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
max_input_length = tokenizer.max_model_input_sizes[model_name]


# Tokenize
ds = ds.map(lambda batch: tokenizer(
    batch["document"],
    padding="max_length",
    truncation=True,
    pad_to_max_length=True,
    max_length=max_input_length
), batched=True, remove_columns=["document", "author_id", "proficiency", "document_id"])
ds = ds.rename_column("native_language", "labels")
ds.set_format(type="torch")


# Train
metric = datasets.load_metric("accuracy")
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size
)

trainer = Trainer(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    compute_metrics=compute_metrics,
    train_dataset=ds["train"],
    eval_dataset=ds["validation"],
)

print(trainer.train())

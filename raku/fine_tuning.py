from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

# データセットの読み込み
dataset = load_dataset("csv", data_files={"train": "train.csv", "test": "test.csv"})

# トークナイザとモデル
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# トークナイズ
def preprocess(examples):
    return tokenizer(examples["text"], truncation=True, padding=True)

encoded_dataset = dataset.map(preprocess, batched=True)

# 訓練設定
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    save_total_limit=2,
)

# Trainerを使用してファインチューニング
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset["train"],
    eval_dataset=encoded_dataset["test"],
    tokenizer=tokenizer,
)

trainer.train()

from transformers import pipeline

# テキスト分類用パイプラインを初期化
classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")

# ファインチューニング済みモデルをロード
# classifier = pipeline("text-classification", model="./results")

# サンプル入力
texts = [
    "Please process this data for me.",
    "Can you help me with something?",
    "This is just a general comment.",
    "I don't need any action on this."
]

# テキストの分類
results = classifier(texts)

# 結果を表示
for text, result in zip(texts, results):
    print(f"Text: {text}")
    print(f"Label: {result['label']}, Score: {result['score']:.4f}")
    print()


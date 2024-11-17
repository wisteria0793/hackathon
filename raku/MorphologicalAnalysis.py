from transformers import AutoModel
from transformers import AutoTokenizer


checkpoint = 'cl-tohoku/bert-base-japanese-whole-word-masking'
model = AutoModel.from_pretrained(checkpoint)
model_ckpt = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_ckpt)



text = "The brown cat jumps overt the white dog."

encoded_text = tokenizer(text)
print(encoded_text)

tokens = tokenizer.convert_ids_to_tokens(encoded_text.input_ids)
print(tokens)
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

import numpy as np


# テキスト入力
df = pd.DataFrame({'id': ['A', 'B'], 
                   'text': ['私は ラーメン 愛する 中でも 味噌 ラーメン 一番 好き', 
                            '私は 焼きそば 好き しかし ラーメン もっと 好き']
                   })
# TF-IDFの計算
tfidf_vectorizer = TfidfVectorizer(use_idf=True,lowercase=False)

# 文章内の全単語のTfidf値を取得
tfidf_matrix = tfidf_vectorizer.fit_transform(df['text'])

# index 順の単語リスト
terms = tfidf_vectorizer.get_feature_names_out()


# 単語毎のtfidf値配列：TF-IDF 行列 (numpy の ndarray 形式で取得される)
tfidfs = tfidf_matrix.toarray()

print(terms)
print(tfidfs)

index1 = np.argmax(tfidfs[0])
index2 = np.argmax(tfidfs[1])

print('キーワード')
print(terms[index1], tfidfs[0].max())
print(terms[index2], tfidfs[1].max())
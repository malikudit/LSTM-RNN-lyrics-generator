import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Bidirectional
import string

text = pd.read_csv("data/lyrics.csv", dtype=str)[:250]

def tokenize_corpus(corpus):
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(corpus)
    return tokenizer

def lyrics_corpus(text, column):
    text[column] = text[column].str.replace('[{}]'.format(string.punctuation), '')
    text[column] = text[column].str.lower()
    lyrics = text[column].str.cat()
    corpus = lyrics.split('\n')
    for item in range(len(corpus)):
        corpus[item] = corpus[item].rstrip()
    corpus = [item for item in corpus if item != '']
    return corpus

corpus = lyrics_corpus(text, 'Column1')
tokenizer = tokenize_corpus(corpus)
vocab_size = len(tokenizer.word_index)+1

seq = []
for item in corpus:
    seq_list = tokenizer.texts_to_sequences([item])[0]
    for i in range(1, len(seq_list)):
        n_gram = seq_list[:i+1]
        seq.append(n_gram)
        
max_seq_size = max([len(s) for s in seq])
seq = np.array(pad_sequences(seq, maxlen=max_seq_size, padding='pre'))

input_sequences, labels = seq[:,:-1], seq[:,-1]
one_hot_labels = to_categorical(labels, num_classes=vocab_size)

model = Sequential()
model.add(Embedding(vocab_size, 64, input_length=max_seq_size-1))
model.add(Bidirectional(LSTM(20)))
model.add(Dense(vocab_size, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
history = model.fit(input_sequences, one_hot_labels, epochs=100, verbose=1)

def plot_graph(history, string):
    plt.plot(history.history[string])
    plt.xlabel("Epochs")
    plt.ylabel(string)
    plt.show()

plot_graph(history, 'accuracy')

seed = "im trying hard"
next_words = 100
for _ in range(next_words):
    token_list = tokenizer.texts_to_sequences([seed])[0]
    token_list = pad_sequences([token_list], maxlen=max_seq_size-1, padding='pre')
    predicted_probs = model.predict(token_list)[0]
    predicted = np.random.choice([x for x in range(len(predicted_probs))], p=predicted_probs)
    output = ""
    for word, index in tokenizer.word_index.items():
        if index == predicted:
            output = word
            break
    seed += " " + output
print(seed)

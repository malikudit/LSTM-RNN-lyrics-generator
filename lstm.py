import numpy as np
import os
import sys
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils

file = open("data/lyrics.txt", "r", encoding="ISO-8859-1")
text = file.read()
text = text.lower()
file.close()

chars = sorted(list(set(text)))
char_to_n = dict((c, i) for i, c in enumerate(chars)) 
n_to_char = dict((i, c) for i, c in enumerate(chars)) 

vocab_size = len(chars)
data_size = len(text)
seq_length = 100
sentences = []
next_char = []  

for i in range(0, data_size-seq_length, 1):
    in_seq = text[i:i + seq_length]
    out_seq = text[i + seq_length]
    sentences.append([char_to_n[char] for char in in_seq])
    next_char.append(char_to_n[out_seq])
pattern_size = len(sentences)

X = np.reshape(sentences, (pattern_size, seq_length, 1))
X = X/float(vocab_size)
Y = np_utils.to_categorical(next_char)

def generate_checkpoint():
    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(Y.shape[1], activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
    callbacks_list = [checkpoint]
    model.fit(X, Y, epochs=50, batch_size=64, callbacks=callbacks_list)

# uncomment the line below to generate the hdf5 file containing the weights from the trained network
generate_checkpoint()

def generate_text():
    model = Sequential()
    model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(Y.shape[1], activation='softmax'))
    filename = "weights-improvement-20-1.8533.hdf5"
    model.load_weights(filename)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    start = np.random.randint(0, len(sentences)-1)
    pattern = sentences[start]
    print("Seed:")
    print("\"", ''.join([n_to_char[value] for value in pattern]), "\"")
    for i in range(1000):
        X2 = np.reshape(pattern, (1, len(pattern), 1))
        X2 = X2/float(vocab_size)
        prediction = model.predict(X2, verbose=0)
        index = np.argmax(prediction)
        result = n_to_char[index]
        seq_in = [n_to_char[value] for value in pattern]
        sys.stdout.write(result)
        pattern.append(index)
        pattern = pattern[1:len(pattern)]
    print("\nDone")

generate_text()




	

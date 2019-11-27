import numpy as np
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.layers import Convolution2D, MaxPooling2D
from keras.models import Sequential
from keras.utils import np_utils

# 分類対象のカテゴリ
root_dir = "./image/"
categories = ["normal", "beni", "negi", "cheese"]
nb_classes = len(categories)
image_size = 50

# データをロード --- (※1)
X_train, X_test, y_train, y_test = np.load("./image/gyudon2.npy")
# データを正規化する
X_train = X_train.astype("float") / 256
X_test  = X_test.astype("float")  / 256
y_train = np_utils.to_categorical(y_train, nb_classes)
y_test  = np_utils.to_categorical(y_test, nb_classes)

# モデルを構築 --- (※2)
def build_model():
    model = Sequential()
    model.add(Convolution2D(32, 3, 3, 
	border_mode='same',
	input_shape=X_train.shape[1:]))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Convolution2D(64, 3, 3, border_mode='same'))
    model.add(Activation('relu'))
    model.add(Convolution2D(64, 3, 3))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten()) 
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='binary_crossentropy',
	optimizer='rmsprop',
	metrics=['accuracy'])
    return model

# モデルを訓練する --- (※4)
model = build_model()
model.fit(X_train, y_train, batch_size=32, nb_epoch=10)

# モデルを保存する --- (※6)
hdf5_file = "./image/gyudon-model.hdf5"
model.save_weights(hdf5_file)

# モデルを評価する --- (※5)
score = model.evaluate(X_test, y_test)
print('loss=', score[0])
print('accuracy=', score[1])







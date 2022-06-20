import os
from chat.models import Chat
import speech_recognition as sr
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
import librosa
import time
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from matplotlib.pyplot import specgram
import keras
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM
from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Input, Flatten, Dropout, Activation
from keras.layers import Conv1D, MaxPooling1D, AveragePooling1D
from keras.models import Model
from keras.callbacks import ModelCheckpoint
from sklearn.metrics import confusion_matrix
loaded_model = keras.models.load_model('Emotion_speech_recognition_Model2.hdf5')
def home(request):
    chats = Chat.objects.all()
    all_users = User.objects.filter(messages__isnull=False).distinct()
    ctx = {
        'home': 'active',
        'chat': chats,
        'allusers': all_users
    }
    if request.user.is_authenticated:
        return render(request, 'chat.html', ctx)
    else:
        return render(request, 'base.html', None)


def upload(request):
    customHeader = request.META['HTTP_MYCUSTOMHEADER']
    # obviously handle correct naming of the file and place it somewhere like media/uploads/
    filename = str(Chat.objects.count())
    filename = filename + "name" + ".wav"
    uploadedFile = open(filename, "wb")
    # the actual file is in request.body
    uploadedFile.write(request.body)
    uploadedFile.close()
    lst1=[]
    X, sample_rate = librosa.load(filename,res_type='kaiser_fast')
    mfccs = np.mean(librosa.feature.mfcc(y=X,sr=sample_rate,n_mfcc=40).T,axis=0)
    file_class = 0
    arr = mfccs, file_class
    lst1.append(arr)
    X1, y1 = zip(*lst1)
    X1, y1 = np.asarray(X1), np.asarray(y1)
    x_traincnn1 = np.expand_dims(X1, axis=2)
    ans_y = np.argmax(loaded_model.predict(x_traincnn1), axis=-1)
    print(ans_y)
    dict1 = {0: "CALM/NEUTRAL", 1:"SAD", 2:"ANGRY", 3:"FEAR"}
    if(ans_y[0]==0):
        msg = " =======> NEUTRAL "
    else:
        msg = " =======> INTENSE EMOTION ANGRY/FEAR/SAD"
    os.remove(filename)
    chat_message = Chat(user=request.user, message=msg)
    if msg != '':
        chat_message.save()
    return redirect('/')

def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        print('Our value = ', msg)
        chat_message = Chat(user=request.user, message=msg)
        if msg != '':
            chat_message.save()
        return JsonResponse({'msg': msg, 'user': chat_message.user.username})
    else:
        return HttpResponse('Request should be POST.')


def messages(request):
    # chat = Chat.objects.all()
    chat = Chat.objects.all()
    arry = list(chat)
    if(len(arry)<5):
        while(len(arry)!=5):
            arry.insert(0,'')
    chat1 = arry[-5:]
    # chat1 = Chat.objects.filter(pk__in = chat).reverse()
    # chat2 = chat1[:5]
    # print(chat2)
    return render(request, 'messages.html', {'chat': chat1})

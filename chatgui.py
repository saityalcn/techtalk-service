import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
# Kelimelerin gövdesini çıkarmak için kullanacağız
lemmatizer = WordNetLemmatizer()
import pickle
from matplotlib import pyplot
# Gerekirse çeviri için kullanacağız
from keras.models import load_model
# modeli yükle
model = load_model('chatbot_model.h5')
import json
import random
# intents.json dosyasını oku ve intents değişkenine sakla
intents = json.loads(open('intents.json').read())
# model eğitilirken kaydedilen kelimeleri oku
words = pickle.load(open('words.pkl','rb'))
# model eğitilirken kullanılan sınıfları oku
classes = pickle.load(open('classes.pkl','rb'))
wordsCountPatterns= pickle.load(open('wordsCountPatterns.pkl','rb'))
classesCounts = pickle.load(open('classesCounts','rb'))
def clean_up_sentence(sentence):
    # Cümle içindeki tüm kelimeleri parçalayarak bir diziye ata
    sentence_words = nltk.word_tokenize(sentence)
    # Cümledeki parça parça ayırdığımız kelimeleri gövdeleme işlemi yapıyor.
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Cümle içindeki kelimelerin geçtiği indis değerlerinin 1 olduğu bir dizi döndürür. 
def bow(sentence, words, show_details=True):
    # Gövdeleme ve ayırma işlemi (Tokenize)
    sentence_words = clean_up_sentence(sentence)
    # Kelime sayısı uzunluğunda ve 0'lardan oluşan dizi oluşturma işlemi.
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # Eğer kelime ilgili indiste mevcutsa, diziye 1 atama işlemi.
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

# Burada verilen eşik değere göre, tahmin edilen cevap listesini döndürür.
def predict_class(sentence, model):
    # Eşik değerinin altındaki tahminleri filtreleme işlemi
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.95
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    #  Olasılık değerine göre büyükten küçüğe sırala
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# Dönen sonucun tagine göre cevaplardan birini seçer.
def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

# Cevap döndürür
def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res

# referencia https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
from nltk.corpus import stopwords as sw
from nltk.tokenize import word_tokenize
def limpeza_stopwords(str):
    stopwords = sw.words('portuguese')
    stopwords.append("mostre")
    stopwords.append("após")
    word_tokens = word_tokenize(str)  
    
    filtered_sentence = [w for w in word_tokens if not w in stopwords]  
    
    filtered_sentence = []  
    
    for w in word_tokens:  
        if w not in stopwords:  
            filtered_sentence.append(w)  
    
    #print(word_tokens)  
    print(filtered_sentence)  
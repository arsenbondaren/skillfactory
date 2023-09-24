import string
import annoy
import bz2file as bz2

from pymorphy2 import MorphAnalyzer
from stop_words import get_stop_words
from gensim.models import Word2Vec

import numpy as np
import pandas as pd
import pickle


# Load any compressed pickle file
def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data


def preprocess_txt(line: str):
    """Функция, предобрабатывающая текст. На вход принимает строку текста, возвращает список обработаных слов"""
    morpher = MorphAnalyzer()
    sw = set(get_stop_words("ru"))
    exclude = set(string.punctuation)
    spls = "".join(i for i in line.strip() if i not in exclude).split()
    spls = [morpher.parse(i.lower())[0].normal_form for i in spls]
    spls = [i for i in spls if i not in sw and i != ""]
    return spls


def find_item(question, number):
    """
    Функция поиска товара из датасета с продуктами. Принимает вопрос в формате строки и кол-во
    товаров для поиска вторым аргументом. Возвращает строку при поиске одного товара, либо
    датафрейм при поиске более одного товара
    """

    # Подгружаем все наши обученые выше и сохраненные алгоритмы и индексы
    item_index = annoy.AnnoyIndex(200, 'angular')
    item_index.load('goods_by_title_hash.ann')
    item_vectorizer = pickle.load(open('item_vectorizer.pkl', 'rb'))
    item_svd = pickle.load(open('item_transformer.pkl', 'rb'))
    df = pd.read_csv('ready_ProductsDataset.csv')

    preprocessed_question = [','.join(preprocess_txt(question))]
    vector = item_vectorizer.transform(preprocessed_question)
    vector = item_svd.transform(vector).reshape(-1)
    index = item_index.get_nns_by_vector(vector, number)
    if number==1:
        prod_id = df['product_id'].iloc[index].values
        prod_id = ''.join(list(prod_id))
        title = df['title'].iloc[index].values
        title = ''.join(list(title))
        return prod_id + " " + title
    if number > 1:
        return df[['product_id', 'title']].iloc[index]
    else:
        return 'Неверно указано количество товаров. Должно быть целое число больше 0.'


def classificator(text):
    """
    Функция, классифицирующая запрос на 'продуктовый' либо 'другой'.
    Принимает на вход вопрос в формате строки.
    Возврщает 1 для продуктового запроса, либо 0 для всех остальных
    """

    vectorizer_clf = pickle.load(open('hash_vectorizer.pkl', 'rb'))
    svd_clf = pickle.load(open('svd_transformer.pkl', 'rb'))
    model_clf = pickle.load(open('model_clf.pkl', 'rb'))

    text = ','.join(preprocess_txt(text))
    text = vectorizer_clf.transform([text])
    text = svd_clf.transform(text)
    text_mark = model_clf.predict(text)
    return text_mark[0]


def speaker_answer(question):
    """
    Функция для поиска ответа из заготовленых с сайта mail.ru.
    На вход принимает вопрос в формате строки. Возвращает ответ в формате строки.
    В работе использует модель и индекс обученные и сохраненные уроком ранее, и загруженые в начале блокнота
    """

    index_map = decompress_pickle('dict_for_speaker.pkl.pbz2')
    model_speaker = Word2Vec.load('w2v_model')
    index_speaker = annoy.AnnoyIndex(50, 'angular')
    index_speaker.load('speaker.ann')

    preprocessed_question = preprocess_txt(question)
    n_w2v = 0
    vector = np.zeros(50)
    for word in preprocessed_question:
        if word in model_speaker.wv:
            vector += model_speaker.wv[word]
            n_w2v += 1
    if n_w2v > 0:
        vector = vector / n_w2v
    answer_index = index_speaker.get_nns_by_vector(vector, 1)
    return index_map[answer_index[0]]


def get_answer(question, number=1):
    """
    Функция, дающая ответ по запросу. Принимает запрос в формате строки и число.
    В зависимости от классификации запроса возвращает: ответ в формате строки, для непродуктового запроса;
    id товара и его название в формате строки, для продуктового запроса с числом 1;
    датафрейм с товарами при продуктовом запросе и числе больше 1.
    Если не указать число при запросе, по умолчанию стоит 1.
    Если запрос классифицируется как непродуктовый, то указанное число не имеет значения.
    """
    mark = classificator(question)
    if mark==1:
        print('Searching the product...')
        return find_item(question, number)
    else:
        print('Searching for answer...')
        return speaker_answer(question)


if __name__=='__main__':
    query = input('Enter your request: ')
    product_amount = input('Enter amount of products you want: ')
    try:
        product_amount = int(product_amount)
        print(get_answer(query, product_amount))
    except:
        print('Wrong amount number. Processing one answer...')
        print(get_answer(query))

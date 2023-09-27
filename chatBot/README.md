## Overview
The chatbot is made for internet store to help in searching products. The chat bot determines your query. If query is about product from the store, the chatbot returns one or more (depends on you) products (id and product title) that suits most / are the most suitable for your request. If chatbot determines that your request is not related to the product, it returns just answer on your question.
## How to use
Run chatbot.py file, enter the query, after enter amount of products you want to get, amount should be an integer. Wait for answer.
## How it works
There is dataset with products available in sale in store. There is a file with questions and answers on different topics from the social network (more than 1 mln questions-answers, but we use only 300K in chatbot to reduce memory usage). Both this text sets transformed in vectors, each separately, to build algorithm for finding closest answer by query. There are 3 functions that play main role in the chatbot. After entering the query, function "classificator" classify the query, is it product request or not. If the request is about product, it calls "find_item" function, that returns the product (or products) that suits most. If the query classifies as not about product, "speaker_answer" function is calling, the function finds the most suitable answer from the prepared answers. 
## Libraries in project:
[Gensim Word2Vec](https://radimrehurek.com/gensim/auto_examples/tutorials/run_word2vec.html#sphx-glr-auto-examples-tutorials-run-word2vec-py): to vectorize text from "prepared answers" document, one vector per word.

[Scikit-learn HashingVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.HashingVectorizer.html): to vectorize collection of product titles into sparse matrix, one sparse vector per title.

[Scikit-learn TruncatedSVD](https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.TruncatedSVD.html): to transform sparse matrix (after HashingVectorizer processing) into numpy arrays.

[Scikit-learn LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression): to classify the query (about product or not).

[Annoy Index](https://github.com/spotify/annoy) (library to search for points in space that are close to a given query point): to find most suitable product or answer. 

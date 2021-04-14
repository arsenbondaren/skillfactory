text = ""
print('Введите текст (пустая строка конец):')
while(True):
    t = input()
    if t == '':
        break
    text = text + t + "\n"
print(text)
# text = """The Zen of Python
# Beautiful is better than ugly.
# Explicit is better than implicit.
# Simple is better than complex.
# Complex is better than complicated.
# Flat is better than nested.
# Sparse is better than dense.
# Readability counts.
# Special cases aren't special enough to break the rules.
# Although practicality beats purity.
# Errors should never pass silently.
# Unless explicitly silenced.
# In the face of ambiguity, refuse the temptation to guess.
# There should be one-- and preferably only one --obvious way to do it.
# Although that way may not be obvious at first unless you're Dutch.
# Now is better than never.
# Although never is often better than *right* now.
# If the implementation is hard to explain, it's a bad idea.
# If the implementation is easy to explain, it may be a good idea.
# Namespaces are one honking great idea -- let's do more of those!"""

text = text.replace("\n", "")
text = text.replace(" ", "")
print(text)
text = text.lower()
#text = list(text)
print(text)
dict_of_chars = {}
for i in text:
    if i in dict_of_chars:
        dict_of_chars[i] += 1
    else:
        dict_of_chars[i] = 1

count = 0
for x in dict_of_chars.values():
    if x == 1:
        count += 1
print(f'Количество уникальных символов в тексте = {count}')
print(dict_of_chars)
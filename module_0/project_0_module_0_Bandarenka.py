import numpy as np


def game_core_v1(number):
    """Просто угадываем на random, никак не используя информацию о больше или меньше.
       Функция принимает загаданное число и возвращает число попыток"""
    count = 0
    while True:
        count += 1
        predict = np.random.randint(1, 101)  # предполагаемое число
        if number == predict:
            return count  # выход из цикла, если угадали


def game_core_v2(number):
    """Сначала устанавливаем любое random число, а потом уменьшаем или увеличиваем его в зависимости от того,
    больше оно или меньше нужного. Функция принимает загаданное число и возвращает число попыток """
    count = 1
    predict = np.random.randint(1, 101)
    while number != predict:
        count += 1
        if number > predict:
            predict += 1
        elif number < predict:
            predict -= 1
    return count  # выход из цикла, если угадали


def game_core_v3(number):
    """Генерируем случайное число predict, проверяем кратность двум нашего числа и random.
    Если оба числа кратны или оба не кратны - увеличиваем/уменьшаем сгенерированное число на 2.Если кратность разная,
    то увеличиваем/уменьшаем сгенерированное число на 1, чтобы на следующем цикле кратность совпала.
    Функция принимает загаданное число и возвращает число попыток.
    Arsen Bandarenka 2021."""

    count = 1  # счётчик попыток
    predict = np.random.randint(1, 101)  # Сгенерировали число от 1 до 100
    while number != predict:  # Цикл будет выполняться до тех пор пока мы не угадаем нужное число
        count += 1
        if number > predict:
            if (number % 2 == 0) and (predict % 2 == 0):  # Проверяем делятся ли оба числа на 2
                predict += 2
            elif (number % 2 == 1) and (predict % 2 == 1):  # Проверяем может оба числа не делятся на 2
                predict += 2
            else:
                predict += 1  # Увеличиваем сгенерированное число на 1, чтобы в дальнейшем увеличивать с шагом 2
        elif number < predict:
            if (number % 2 == 0) and (predict % 2 == 0):
                predict -= 2
            elif (number % 2 == 1) and (predict % 2 == 1):
                predict -= 2
            else:
                predict -= 1
    return count  # выход из цикла, если угадали


def game_core_v4(number):
    """Бонусный вариант улучшения алгоритма. Самое простое и прямое решение, если следовать принципам языка python.
    Просто находим разность между сгенерированным числом predict и нужным. Затем прибавляем разницу к заданному числу.
    Функция возвращает число попыток.
    Условием задания такой вариант кажется не запрещен.
    Arsen Bandarenka 2021."""
    count = 1
    predict = np.random.randint(1, 101)
    if number != predict:
        count += 1
        delta = predict - number  # Находим разницу между сгенерированным числом и нужным
        predict = number + delta  # Корректируем число predict до нужного
    return count  # выход из цикла


def score_game(game_core):
    """Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число."""
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1, 101, size=1000)
    for number in random_array:
        count_ls.append(game_core(number))
    score = round(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return score


print(score_game(game_core_v4))

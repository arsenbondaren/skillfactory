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
    """Генерируем любое random число, проверяем кратность двум нашего числа и random.
    Если оба числа кратны или оба не кратны - увеличиваем/уменьшаем загаданное число на 2.
    Если кратность разная, то увеличиваем/уменьшаем загаданное число на 1, чтобы на следующем цикле кратность совпала.
       Функция принимает загаданное число и возвращает число попыток"""

    count = 1  # счётчик попыток
    predict = np.random.randint(1, 101)  # Загадали random число от 1 до 100
    while number != predict:  # Цикл будет выполняться до тех пор пока мы не угадаем нужное число
        count += 1
        if number > predict:
            if (number % 2 == 0) and (predict % 2 == 0):  # Проверяем делятся ли оба числа на 2
                predict += 2
            elif (number % 2 == 1) and (predict % 2 == 1):  # Проверяем может оба числа не делятся на 2
                predict += 2
            else:
                predict += 1  # Увеличиваем загаданное число на 1, чтобы в дальнейшем увеличивать с шагом 2
        elif number < predict:
            if (number % 2 == 0) and (predict % 2 == 0):
                predict -= 2
            elif (number % 2 == 1) and (predict % 2 == 1):
                predict -= 2
            else:
                predict -= 1
    return count  # выход из цикла, если угадали


def score_game(game_core):
    """Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число."""
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1, 101, size=1000)
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return score


print(score_game(game_core_v3))

print(game_core_v3.__doc__)

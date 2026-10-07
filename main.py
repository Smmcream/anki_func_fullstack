import random
import sys
import time


STOP_WORD = 'СТОП'


def load_words(filename='words.txt'):
    """Загружает словарь из файла.

    Читает пары «слово, перевод» из файла, где каждая строка
    имеет вид «слово, перевод». Возвращает словарь, где ключ —
    слово, значение — перевод.

    Если файл не найден, выводит сообщение и завершает программу.
    """
    words = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) == 2:
                    word = parts[0].strip()
                    translation = parts[1].strip()
                    words[word] = translation
    except FileNotFoundError:
        print(f'Файл {filename} не найден.')
        sys.exit(1)
    return words


def print_statistics(score, total_time):
    """Выводит итоговую статистику игры.

    Показывает количество правильных ответов, общее время игры
    и среднее время на ответ. Если правильных ответов не было,
    вместо среднего времени выводится прочерк.
    """
    if score > 0:
        average_time = format(total_time / score, '.2f') + ' сек.'
    else:
        average_time = '—'
    print(f'Ваш итоговый счет: {score}')
    print(
        f'Время игры: {format(total_time, ".2f")} секунд '
        f'(среднее время: {average_time})'
    )


def ask_and_check(word, correct):
    """Спрашивает перевод слова и проверяет ответ.

    Выводит слово для перевода, засекает время до и после ввода.
    Если введено завершающее слово STOP_WORD, возвращает
    (True, False, 0.0). Иначе сравнивает ответ с правильным
    переводом без учёта регистра и лишних пробелов и возвращает
    (False, is_correct, answer_time).
    """
    print(f'Ваше слово: {word}')
    start_time = time.time()
    user_answer = input('Ваш перевод: ')
    end_time = time.time()
    if user_answer.strip().lower() == STOP_WORD.lower():
        return True, False, 0.0
    answer_time = end_time - start_time
    is_correct = user_answer.strip().lower() == correct.strip().lower()
    return False, is_correct, answer_time


def start_game(words):
    """Запускает игровой режим обычной тренировки.

    Случайно выбирает слова из словаря, спрашивает перевод,
    считает правильные ответы и общее время. Завершается
    при вводе STOP_WORD.
    """
    if not words:
        print('Словарь пуст, игра недоступна.')
        return
    print(f'Чтобы закончить, введите {STOP_WORD}')
    score = 0
    total_time = 0.0
    word_list = list(words.keys())
    while True:
        word = random.choice(word_list)
        correct = words[word]
        is_stop, is_correct, answer_time = ask_and_check(word, correct)
        if is_stop:
            break
        total_time += answer_time
        if is_correct:
            score += 1
            time_str = format(answer_time, '.2f')
            print(f'Верно! Время на ответ: {time_str} секунд')
        else:
            time_str = format(answer_time, '.2f')
            print(
                f'Неправильно, правильный ответ: {correct} '
                f'(Время на ответ: {time_str} секунд)'
            )
    print('Спасибо за игру!')
    print_statistics(score, total_time)


def train_until_mistake(words):
    """Запускает игру до первой ошибки.

    Случайно выбирает слова из словаря, спрашивает перевод.
    Игра завершается после первой ошибки или при вводе STOP_WORD.
    """
    print(
        f'Режим: Игра до первой ошибки! '
        f'Чтобы выйти вручную, введите {STOP_WORD}'
    )
    if not words:
        print_statistics(0, 0.0)
        return
    score = 0
    total_time = 0.0
    word_list = list(words.keys())
    while True:
        word = random.choice(word_list)
        correct = words[word]
        is_stop, is_correct, answer_time = ask_and_check(word, correct)
        if is_stop:
            print('Выход из режима по запросу пользователя.')
            break
        total_time += answer_time
        if is_correct:
            score += 1
            time_str = format(answer_time, '.2f')
            print(f'Верно! Всего очков: {score} (ответ за {time_str} секунд)')
        else:
            print(f'Ошибка! Неверно. Правильный ответ: {correct}')
            break
    print_statistics(score, total_time)


def add_words(words):
    """Добавляет новые пары «слово — перевод» в словарь.

    Спрашивает у пользователя слово и перевод в цикле.
    Завершается при вводе STOP_WORD вместо слова или перевода.
    """
    print(f'Чтобы закончить, введите {STOP_WORD}')
    while True:
        word = input('Введите слово: ')
        if word.strip().lower() == STOP_WORD.lower():
            break
        translation = input('Введите перевод: ')
        if translation.strip().lower() == STOP_WORD.lower():
            break
        words[word] = translation


def show_all_words(words):
    """Выводит все пары «слово — перевод» одной строкой.

    Пары разделяются точкой с запятой и пробелом.
    """
    pairs = []
    for word, translation in words.items():
        pairs.append(f'{word} - {translation}')
    print('; '.join(pairs))


def save_words(words, filename='words.txt'):
    """Сохраняет словарь в файл.

    Записывает каждую пару «слово, перевод» в отдельной строке
    в формате «слово, перевод». Файл перезаписывается.
    """
    with open(filename, 'w', encoding='utf-8') as file:
        for word, translation in words.items():
            file.write(f'{word}, {translation}\n')
    print(f'Было сохранено {len(words)} слов в файл {filename}')


def main():
    """Главное меню программы.

    Загружает словарь, показывает меню и обрабатывает выбор
    пользователя. Завершается при выборе пункта 5.
    """
    words = load_words()
    print(f'Было загружено {len(words)} слов из файла words.txt')
    while True:
        menu = '''Меню:
        1. Начать игру
        2. Добавить слова
        3. Тренировка до первой ошибки
        4. Вывод всех слов
        5. Выход
        '''
        print(menu)
        menu_choice = input('Пункт меню: ')
        if menu_choice == '1':
            start_game(words)
        elif menu_choice == '2':
            add_words(words)
        elif menu_choice == '3':
            train_until_mistake(words)
        elif menu_choice == '4':
            show_all_words(words)
        elif menu_choice == '5':
            save_words(words, 'words.txt')
            sys.exit()
        else:
            print('Неизвестный пункт меню')


if __name__ == '__main__':
    main()

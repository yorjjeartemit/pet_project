import math
import requests
from bs4 import BeautifulSoup
import random
import time
from random import randint
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY_2 = os.getenv('API_KEY_2')

API_KEY = os.getenv('API_KEY')
def math_operation(op, *args):
    if op in ('+', '-', '*', '/', '**', 'mod'):
        if len(args) < 2:
            return "Недостатньо аргументів"
        a, b = args[:2]
        return {
            '+': a + b,
            '-': a - b,
            '*': a * b,
            '/': a / b if b != 0 else "Ділення на нуль",
            '**': a ** b,
            'mod': a % b
        }[op]

    elif op in ("log", "ln"):
        if len(args) < 1:
            return "Недостатньо аргументів"
        return math.log(args[0]) if op == "ln" else math.log(args[0], args[1]) if len(args) > 1 else "Вкажи основу логарифма"

    elif op in ("sin", "cos", "tan", "cot"):
        if len(args) < 1:
            return "Недостатньо аргументів"
        trig_funcs = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "cot": lambda x: 1 / math.tan(x)
        }
        return trig_funcs[op](args[0])

    elif op == "sqrt":
        if len(args) < 1:
            return "Недостатньо аргументів"
        return math.sqrt(args[0])

    elif op == "sum":
        return sum(args)

    elif op == "prod":
        result = 1
        for num in args:
            result *= num
        return result

    elif op == "abs":
        if len(args) < 1:
            return "Недостатньо аргументів"
        return abs(args[0])

    elif op in ("det", "transpose"):
        if len(args) < 1 or not isinstance(args[0], list):
            return "Некоректний формат матриці"
        matrix = args[0]
        if op == "transpose":
            return list(zip(*matrix))
        elif op == "det" and len(matrix) == len(matrix[0]): 
            return round(math.prod([matrix[i][i] for i in range(len(matrix))]), 2)

    return "Невідома операція"
def math_full():
    op = input("Введіть операцію (+, -, *, /, **, mod, log, ln, sin, cos, tan, cot, sqrt, sum, prod, abs): ")

    if op in ("log", "**", "mod", "+", "-", "*", "/"):
        a = float(input("Введіть перше число: "))
        b = float(input("Введіть друге число: "))
        print("Результат:", math_operation(op, a, b))

    elif op in ("sin", "cos", "tan", "cot", "sqrt", "ln", "abs"):
        a = float(input("Введіть число: "))
        print("Результат:", math_operation(op, a))

    elif op in ("sum", "prod"):
        numbers = list(map(float, input("Введіть числа через пробіл: ").split()))
        print("Результат:", math_operation(op, *numbers))

    else:
        print("Невідома операція")

def genres_func():
    genres = {
        1: "Жанр, що зосереджується на внутрішньому світі персонажів.",
        2: "Загадкові події, часто з надприродними елементами.",
        3: "Світ майбутнього, технології, інші планети.",
        4: "Розслідування злочинів та пошук істини.",
        5: "Напруга, інтрига, несподівані повороти.",
        6: "Головні герої вирушають у небезпечні подорожі.",
        7: "Мета — налякати читача.",
        8: "Магія, вигадані світи, казкові істоти.",
        9: "Події, засновані на реальній історії.",
        10: "Легкий жанр з гумором."
    }
    print("1. Роман")
    print("2. Містика")
    print("3. Фантастика")
    print("4. Детектив")
    print("5. Трилер")
    print("6. Пригодницький")
    print("7. Жахи")
    print("8. Фентезі")
    print("9. Історичний")
    print("10. Комедія")
    
    class_films=int(input("введіть жанр фільму який вам подобається: "))
    print(genres[class_films])

def get_best_movie():
    url = "https://www.imdb.com/chart/moviemeter/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Помилка доступу до IMDb")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    movies = soup.select("li.ipc-metadata-list-summary-item h3")  
    if not movies:  
        movies = soup.select("h3.ipc-title__text") 

    print(f"Знайдено {len(movies)} фільмів.")
    
    if movies:
        number_films=int(input(f"скільки тобі треба фільмів (до {len(movies)}): "))
        if number_films > 0 and number_films <= len(movies):
            for i in range(number_films):  
                print(f'{i}.',movies[i].text)
        else:
            print("false")
    else:
        print("Фільм не знайдено")


def convert_money():
    
    BASE_CURRENCY = 'USD' 
    TARGET_CURRENCY = 'UAH' 

    TOP_CURRENCIES = ['USD', 'EUR', 'GBP', 'PLN', 'CHF']

    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}'

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        print("Курс валют до гривні (UAH):")
        for currency in TOP_CURRENCIES:
            if currency in data['conversion_rates']:
                rate = data['conversion_rates'][currency]
                uah_rate = data['conversion_rates'][TARGET_CURRENCY] / rate
                print(f"1 {currency} = {round(uah_rate, 2)} UAH")
            else:
                print(f"Не вдалося отримати курс для {currency}")
    else:
        print("Помилка отримання даних:", data.get('error-type', 'Невідома помилка'))
def password_generated(pass_leng=24):
    text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    password = "".join(random.choices(text, k=pass_leng))
    print("Згенерований пароль:", password)


def get_weather(cities=["Kyiv", "London", "Berlin", "New York", "Tokyo"]):
    for city in cities:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_2}&units=metric&lang=uk"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            print(f"Погода в {city}: {weather}, {temp}°C")
        else:
            print(f"Помилка отримання даних про погоду для {city}. Код помилки: {response.status_code}")

def timer():
    user_time = int(input("Введіть час таймера в секундах: "))
    for i in range(user_time, 0, -1): 
        print(f"Залишилось часу: {i} секунд")
        time.sleep(1)  
    print("Таймер закінчився!")
def random_num():
    num = random.randint(1, 100)
    user = None  
    while user != num:
        try:
            user = int(input("Вгадай число від 1 до 100: "))
            if user < num:
                print("Загадане число більше!")
            elif user > num:
                print("Загадане число менше!")
            else:
                print("Вітаємо! Ви вгадали число!")
        except ValueError:
            print("Будь ласка, введіть правильне число.")
def check_palindrome():
    text = input("Введіть слово чи фразу для перевірки на паліндром: ")
    cleaned_text = text.replace(" ", "").lower()
    if cleaned_text == cleaned_text[::-1]:
        print("Це паліндром!")
    else:
        print("Це не паліндром.")

def random_fact():
    facts = [
        "бджоли можуть розпізнавати обличчя людей",
        "усе живе на Землі складається з атомів і атоми існують з моменту Великого вибуху",
        "вода – це єдина речовина що може існувати в трьох агрегатних станах одночасно: твердому рідкому та газоподібному",
        "в Африці росте більше 4000 видів дерев",
        "птахи з родини папуг можуть відтворювати звуки схожі на людську мову",
        "робоча бджола за своє життя збирає 0,8 г меду небагато? скільки може стільки і збирає а скільки коштує життя бджоли? дорого дуже дорого"
    ]
    
    fact = random.choice(facts)
    print(f"Цікавий факт: {fact}")

def average_calculator():
    numbers = input("Введіть числа через пробіл: ").split()
    numbers = [float(num) for num in numbers]
    average = sum(numbers) / len(numbers)
    print(f"Середнє значення: {average}")
    print("до речі ви знали що середне значення в математиці рахується за допомогою сігми😎 ( ось цієї сігми - Σ )")
def temperature_converter():
    print("Оберіть одиницю для конвертації:")
    print("1. Цельсій → Фаренгейт")
    print("2. Фаренгейт → Цельсій")
    print("3. Цельсій → Кельвін")
    print("4. Кельвін → Цельсій")
    choice = int(input("Вибір: "))
    
    if choice == 1:
        celsius = float(input("Введіть температуру в Цельсії: "))
        fahrenheit = (celsius * 9/5) + 32
        print(f"{celsius}°C = {fahrenheit}°F")
    elif choice == 2:
        fahrenheit = float(input("Введіть температуру в Фаренгейті: "))
        celsius = (fahrenheit - 32) * 5/9
        print(f"{fahrenheit}°F = {celsius}°C")
    elif choice == 3:
        celsius = float(input("Введіть температуру в Цельсії: "))
        kelvin = celsius + 273.15
        print(f"{celsius}°C = {kelvin}K")
    elif choice == 4:
        kelvin = float(input("Введіть температуру в Кельвінах: "))
        celsius = kelvin - 273.15
        print(f"{kelvin}K = {celsius}°C")
    else:
        print("Невірний вибір.")

def is_prime():
    num = int(input("Введіть число для перевірки на простоту: "))
    if num < 2:
        print(f"Число {num} не є простим.")
        return
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            print(f"Число {num} не є простим.")
            return
    print(f"Число {num} є простим.")

def factorial():
    num = int(input("Введіть число для обчислення факторіалу: "))
    result = 1
    for i in range(1, num + 1):
        result *= i
    print(f"Факторіал числа {num} дорівнює {result}")

def random_number():
    min_num = int(input("Введіть мінімальне число: "))
    max_num = int(input("Введіть максимальне число: "))
    random_num = random.randint(min_num, max_num)
    print(f"Випадкове число між {min_num} і {max_num}: {random_num}")

def distance_calculator():
    speed = float(input("Введіть швидкість (км/год): "))
    time = float(input("Введіть час (години): "))
    distance = speed * time
    print(f"Відстань: {distance} км")
def speak_user():
    list_user_func = {
        1: "калькулятор",
        2: "топ фільмів",
        3: "конвертація валют",
        4: "генерація паролів",
        5: "погода",
        6: "таймер",
        7: "вгадай число",
        8: "перевірка на паліндром",
        9: "рандомний факт",
        10: "калькулятор середнього значення",
        11: "факторіал числа",
        12: "перевірка на простоту числа",
        13: "конвертер температур",
        14: "генератор випадкового числа",
        15: "підрахунок для обчислення відстані"
    }

    for key, value in list_user_func.items():
        print(f"{key}. {value}")

    choice_user = int(input("Вибери функцію: "))

    total_functions = len(list_user_func)
    choice_user = ((choice_user - 1) % total_functions) + 1

    functions = {
        1: math_full,
        2: get_best_movie,
        3: convert_money,
        4: password_generated,
        5: lambda: get_weather(),
        6: timer,
        7: random_num,
        8: check_palindrome,
        9: random_fact,
        10: average_calculator,
        11: factorial,
        12: is_prime,
        13: temperature_converter,
        14: random_number,
        15: distance_calculator
    }

    functions[choice_user]()

    repeat = input("Бажаєш спробувати ще раз? (y/n): ").strip().lower()
    if repeat == "y":
        speak_user()  
    else:
        print("допобачення")
speak_user()


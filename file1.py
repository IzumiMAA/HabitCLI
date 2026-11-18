import json
import sys
sys.stdout.reconfigure(encoding="utf-8")

from datetime import date

masuvzwkvuk = []
masuvzwkno = []

days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
today = days[date.today().weekday()]

try:
    with open("database.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        masuvzwk = data.get("habits", [])
        calendar = data.get("calendar", {
            "Пн": [],
            "Вт": [],
            "Ср": [],
            "Чт": [],
            "Пт": [],
            "Сб": [],
            "Нд": [],
        })
    print("Дані успішно завантажено з файлу!")
except (FileNotFoundError, json.JSONDecodeError):
    masuvzwk = []
    calendar = {
        "Пн": [],
        "Вт": [],
        "Ср": [],
        "Чт": [],
        "Пт": [],
        "Сб": [],
        "Нд": [],
    }


def listC():
    for day, tasks in calendar.items():
        tasks_str = ", ".join(tasks) if tasks else " "
        if day != today:
            day = day
        else: 
            day = "\033[92m" + day + "\033[0m"
        print(f"{day:<4} - {tasks_str}")


taskNo = 0
taskwuk = 0

while True:

    print("=" * 36)
    print("=" * 15, "Меню", "=" * 15)
    print("=" * 36)

    print(" " * 4, "1. Додати звичку в календар")
    print(" " * 4, "2. Переглянути список звичок")
    print(" " * 4, "3. Переглянути календар подій")

    print("=" * 12, "Видалення", "=" * 12)
    print(" " * 4, "4. Видалити завдання")
    print(" " * 4, "5. Видалити все")

    print("=" * 12, "Збереження", "=" * 12)
    print(" " * 4, "6. Зберегти всі дії")

    print("="*36)
    print(" "*4,"7. Позначити завдання виконаним [+]")
    print(" "*4,"8. Позначити завдання НЕ виконаним [-]") 

    print("="*36)
    print(" "*4,"9. Статистика всіх виконаних завдань") 
    print(" "*4,"10. Статистика одного завдання")  

    print(" " * 4, "0. Вийти")

    n = int(input("Оберіть пункт меню: "))

    match n:
        case 0:
            print("Вихід з програми! =(")
            break
        case 1:
            print("=" * 42)
            print("=" * 15, "НОВА ЗВИЧКА", "=" * 15)
            zwuchka = input("Введіть бажану звичку: ")
            masuvzwk.append(zwuchka)

            # перевірка на порожній рядок
            if isinstance(zwuchka, str) and zwuchka.strip() == "":
                print("Помилка: звичка не може бути порожнім рядком.")
                masuvzwk.pop()
                continue

            # перевірка введення кількості днів
            try:
               nd = int(input("Оберіть кількість днів на тиждень для виконання: "))
            except ValueError:
                print("Помилка: введіть ціле число.")
                masuvzwk.pop()
                continue
            if nd <= 0:
                print("Помилка: кількість днів повинна бути більшою за 0.")
                masuvzwk.pop()
                continue

        
            while nd != 0:
                day = input("Введіть день тижня (Пн): ")

                # перевірка на порожній рядок 
                if isinstance(day, str) and day.strip() == "":
                    print("Помилка: день тижня не може бути порожнім рядком.")
                    continue

                # перевірка на правильність введення дня тижня
                if day not in calendar:
                    print("Помилка: введено неправильний день тижня.")
                    continue

                nd = nd - 1
                calendar[day].append(zwuchka)

        case 2:
            for index, item in enumerate(masuvzwk, start=1):
                print(f"{index}. {item}")
        case 3:
            print("=" * 42)
            print("=" * 17, "КАЛЕНДАР", "=" * 17)

            listC()

        case 4:
            print("=" * 40)
            print("=" * 10, "Список існуючих звичок", "=" * 10)
            for index, item in enumerate(masuvzwk, start=1):
                print(f"{index}. {item}")

            numzwk = int(input("Оберіть номер звички зі списку вище для видалення: "))

            # перевірка на правильність введення значення номера
            if numzwk < 1 or numzwk > len(masuvzwk):
                print("Помилка: введено неправильний номер звички.")
                continue


            print("1. Видалити всюди")
            print("2. Видалити в конкретний день")

            sposibdel = int(input("Введіть номер бажаного виду видалення: "))
            delzwk = masuvzwk[numzwk - 1]

            # перевірка на правильність введення значення способу 
            if sposibdel > 2 or sposibdel < 0:
                print ("Введено некоректне значення")
                continue

            if sposibdel == 1:
                for day in calendar:
                    calendar[day] = [t for t in calendar[day] if t != delzwk]
                del masuvzwk[numzwk - 1]
            else:
                daydel = input("Введіть бажаний день для видалення: ")

                # перевірка на правильність введення дня тижня
                if daydel not in calendar:
                    print("Помилка: введено неправильний день тижня.")
                    continue

                if delzwk in calendar[daydel]:
                    calendar[daydel].remove(delzwk)
                if not any(delzwk in tasks for tasks in calendar.values()):
                    del masuvzwk[numzwk - 1]

            print("=" * 10, "Поточний список", "=" * 10)
            listC()

        case 5:
            print()
            print("=" * 15, "", "ОЧИЩЕННЯ", "=" * 15)
            masuvzwk.clear()
            for day in calendar:
                calendar[day].clear()
            listC()

        case 6:
            save = {"habits": masuvzwk, "calendar": calendar}
            with open("database.json", "w", encoding="utf-8") as f:
                json.dump(save, f, ensure_ascii=False, indent=4)
            print("Збережено")


        case 7: 
            print()
            print("Позначити завдання виконаими")

            daywuk = input("Оберіть день для позначення виконаного завдання: ")

            

            # перевірка на правильність введення дня тижня
            if daywuk not in calendar:
                print("Помилка: введено неправильний день тижня.")
                continue

            for number, habit in enumerate(calendar[daywuk], start=1):
                print(f"{number}. {habit}")

            numhabit = int(input("Оберіть номер завдання для позначення виконаним: "))
            
            # перевірка значення номера завдання
            if numhabit < 0 or numhabit > len(calendar[daywuk]):
                print ("Введенно некоректне значення")
                continue

            taskwuk = taskwuk + 1

            if 1 <= numhabit <= len(calendar[daywuk]):
                habit_to_mark = calendar[daywuk][numhabit - 1]
                calendar[daywuk][numhabit - 1] = f"{habit_to_mark}  [+]"
                print(f"Завдання '{habit_to_mark}' позначено як виконане.")

            masuvzwkvuk.append(habit_to_mark)

        case 8:
            print()
            print("Позначити завдання НЕ виконаими")
            
            daywuk = input("Оберіть день для позначення виконаного завдання: ")

            # перевірка на правильність введення дня тижня
            if daywuk not in calendar:
                print("Помилка: введено неправильний день тижня.")
                continue
            
            for number, habit in enumerate(calendar[daywuk], start=1):
                print(f"{number}. {habit}")

            

            numhabit = int(input("Оберіть номер завдання для позначення не виконаним: "))


            # перевірка значення номера завдання
            if numhabit < 0 or numhabit > len(calendar[daywuk]):
                print ("Введенно некоректне значення")
                continue

            taskNo = taskNo + 1

            if numhabit < 1 or numhabit > len(calendar[daywuk]):
                habit_to_mark = calendar[daywuk][numhabit - 1]
                calendar[daywuk][numhabit - 1] = f"{habit_to_mark}  [-]"
                print(f"Завдання '{habit_to_mark}' позначено як не виконане.")

            masuvzwkno.append(habit_to_mark)
            
        case 9:
            print() 
            print("="*12,"СТАТИСТИКА","="*12)

            total_tasks = sum(len(tasks) for tasks in calendar.values())

            print("Кількість завдань: ", total_tasks)
            print("Кількість виконаних завдань: ", taskwuk)           
            print("Не виконані завдання: ",taskNo)

            if total_tasks > 0:
                prog = (taskwuk * 100) / total_tasks
            else:
                prog = 0

            print(f"Прогрес: {prog:.1f}%")

        case 10:
            print()
            print("Список існуючих звичок: ")

            for index, item in enumerate(masuvzwk, start=1):
                print(f"{index}. {item}")

            numstatzwk = int(input("Введіть номер бажаної звички зі списку: "))

            if numstatzwk < 1 or numstatzwk > len(masuvzwk):
                print("Введено некоректний номер.")
                continue
            
            zwkstat = masuvzwk[numstatzwk - 1]

            # Функція для видалення позначок [+] та [-]
            def clean_habit(habit):
                return habit.replace("  [+]", "").replace("  [-]", "")

            # Загальна кількість запланованих завдань
            sumzwk = sum(
                clean_habit(task) == zwkstat
                for tasks in calendar.values()
                for task in tasks
            )

            # Кількість виконаних
            sumzwkvuk = 0
            for habit in masuvzwkvuk:
                if clean_habit(habit) == zwkstat:
                    sumzwkvuk += 1

            # Кількість невиконаних
            sumzwkno = 0
            for habit in masuvzwkno:
                if clean_habit(habit) == zwkstat:
                    sumzwkno += 1

            # Прогрес
            if sumzwk > 0:
                prog1 = (sumzwkvuk * 100) / sumzwk
            else:
                prog1 = 0

            print("Загальна кількість запланувань звички:", sumzwk)
            print("Загальна кількість виконань звички:", sumzwkvuk)
            print("Загальна кількість невиконань звички:", sumzwkno)
            print()
            print(f"Прогрес: {prog1:.1f}%")
        

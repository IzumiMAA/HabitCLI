import json

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
		print (f"{day:<4} - {tasks_str}")

while True:

	print ("="*36)
	print ("="*15,"Меню","="*15)
	print ("="*36)

	print (" "*4,"1. Додати знвичку в календар")
	print (" "*4,"2. Переглянути список звичок")
	print (" "*4,"3. Переглянути календар подій")

	print ("="*12,"Видалення","="*12)
	print (" "*4,"4. Видалити завдання")
	print (" "*4,"5. Видалити все")

	print ("="*12,"Збереження","="*12)
	print (" "*4,"6. Зберегти всі дії")


	print (" "*4,"0. Вийти")


	n = int(input("Оберіть пункт меню: "))

	match n:
		case 0:
			print ("Вихід з програми! =(")
			break
		case 1:
			print ("="*42)
			print ("="*15,"НОВА ЗВИЧКА","="*15)
			zwuchka = input("Введіть бажану звичку: ")
			masuvzwk.append(zwuchka)

			nd = int(input("Оберть кількість днів на тиждень для виконання: "))
			while nd != 0:
				day = input("Введіть день тижня (Пн): ")
				nd = nd - 1
				calendar[day].append(zwuchka)
		case 2:
			print (masuvzwk)
		case 3:
			print ("="*42)
			print ("="*17,"КАЛЕНДАР","="*17)

			listC()

		case 4:
			print ("="*40)
			print ("="*10,"Список існуючих звичок","="*10)
			for index, item in enumerate(masuvzwk, start = 1):
				print (f"{index}. {item}")

			numzwk = int(input("Оберіть номер звички зі списку вижче для видалення: "))

			print ("1. Видалити всюди")
			print ("2. Видалити в конкретний день")

			sposibdel = int(input("Ввндіть номер бажаного виду видалення: "))
			delzwk = masuvzwk[numzwk-1]

			if sposibdel == 1:

				for day in calendar:
					calendar[day] = [t for t in calendar[day] if t != delzwk]

				print ("="*10,"Поточний список","="*10)
				listC()
				del masuvzwk[numzwk-1]

			else:

				daydel = input("Введіть бажаний день для видалення: ")
				if delzwk in calendar[daydel]:
					calendar[daydel].remove(delzwk)
				listC()
				del masuvzwk[numzwk-1]


		case 5:
			print ()
			print ("="*15,"","ОЧИЩЕННЯ","="*15)
			masuvzwk.clear()
			for day in calendar:
				calendar[day].clear()
			listC()

		case 6:

			save = {"habits": masuvzwk, "calendar": calendar}
			with open("database.json","w", encoding = "utf-8") as f:
				json.dump(save, f, ensure_ascii = False, indent = 4)
			print ("Збережено")








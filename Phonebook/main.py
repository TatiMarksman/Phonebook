import csv
from pprint import pprint
import re

# читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

pprint(contacts_list)

# Задача 1:
for contact in contacts_list:
    fullname = contact[0].split()
    if len(fullname) == 3:
        contact[0], contact[1], contact[2] = fullname
    elif len(fullname) == 2:
        contact[0], contact[1] = fullname
        contact.append('')  # Добавляем пустую строку для отчества, если его нет

# Задача 2: телефоны в порядок:
for contact in contacts_list:
    contact[5] = re.sub(r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})\s*(?:доб\.)?\s*(\d{0,4})", r"+7(\2)\3-\4-\5 \6", contact[5])

pprint(contacts_list)

# Задача 3: Объединить все дублирующиеся записи о человеке в одну
# создаем словарь, где ключом будет сочетание ФИ, а значением - список данных о человеке
contacts_dict = {}
for contact in contacts_list:
    fullname = (contact[0], contact[1])
    if fullname not in contacts_dict:
        contacts_dict[fullname] = contact
    else:
        # если такое сочетание ФИ уже есть в словаре, объединяем данные о телефонах и email
        # объединяем только если номер или email отсутствуют в записи, в которую происходит объединение
        for i in range(5, len(contact)):
            if contact[i] and not contacts_dict[fullname][i]:
                contacts_dict[fullname][i] = contact[i]

# словарь обратно в список для сохранения в файл
merged_contacts_list = list(contacts_dict.values())

# вывожу список после объединения дубликатов
pprint(merged_contacts_list)

# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(merged_contacts_list)

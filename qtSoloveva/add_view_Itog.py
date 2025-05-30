from cls_builds import Builds
from cls_Itog import Itog
import sqlite3

def view_all():
    con = sqlite3.connect("Builds_Soloveva.db")
    cur = con.cursor()

    print("\n--- Таблица Builds ---")
    for row in cur.execute("SELECT * FROM Builds"):
        print(row)

    print("\n--- Таблица Itog ---")
    for row in cur.execute("""
        SELECT Itog.id, Builds.Type_Build, Itog.Count_Rooms, Itog.Footage, Itog.Price
        FROM Itog
        JOIN Builds ON Itog.Build = Builds.id_build
    """):
        print(row)

    con.close()

view_all()


builds_db = Builds()
itog_db = Itog()

def show_menu():
    print("\n--- МЕНЮ ---")
    print("1. Добавить тип строения")
    print("2. Добавить запись в Itog")
    print("3. Удалить запись из Builds")
    print("4. Удалить запись из Itog")
    print("5. Просмотреть таблицу Builds")
    print("6. Просмотреть таблицу Itog")
    print("7. Выйти")

def add_build():
    type_build = input("Введите тип строения: ")
    builds_db.insert(type_build)
    print("Добавлено.")

def add_itog():
    type_build = input("Введите тип строения (должен быть добавлен заранее): ")
    result = builds_db.search(type_build)
    if result:
        build_id = result[0][0]
        try:
            count_rooms = int(input("Количество комнат: "))
            footage = float(input("Метраж: "))
            price = float(input("Цена: "))
            itog_db.insert(build_id, count_rooms, footage, price)
            print("Добавлено.")
        except ValueError:
            print("Ошибка: неверный формат чисел.")
    else:
        print("Такой тип строения не найден. Добавьте его сначала в Builds.")

def delete_build():
    try:
        id_build = int(input("Введите ID строения для удаления: "))
        builds_db.cur.execute("DELETE FROM Builds WHERE id_build = ?", (id_build,))
        builds_db.con.commit()
        print("Удалено.")
    except ValueError:
        print("Ошибка: неверный ID.")

def delete_itog():
    try:
        id_itog = int(input("Введите ID записи из Itog для удаления: "))
        itog_db.cur.execute("DELETE FROM Itog WHERE id = ?", (id_itog,))
        itog_db.con.commit()
        print("Удалено.")
    except ValueError:
        print("Ошибка: неверный ID.")

def view_builds():
    rows = builds_db.view()
    print("\n--- Таблица Builds ---")
    for row in rows:
        print(row)

def view_itog():
    rows = itog_db.view_with_type()
    print("\n--- Таблица Itog ---")
    for row in rows:
        print(row)

def main():
    while True:
        show_menu()
        choice = input("Выберите действие: ")

        if choice == "1":
            add_build()
        elif choice == "2":
            add_itog()
        elif choice == "3":
            delete_build()
        elif choice == "4":
            delete_itog()
        elif choice == "5":
            view_builds()
        elif choice == "6":
            view_itog()
        elif choice == "7":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Повторите.")

if __name__ == "__main__":
    main()

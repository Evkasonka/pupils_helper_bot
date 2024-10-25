import sqlite3


def create_database():
    # Создание базы данных и таблицы учеников, если она не существует
    connect = sqlite3.connect('students.db')
    cursor = connect.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students
                      (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS scores
                          (id INTEGER PRIMARY KEY, student_id INTEGER, subject TEXT, score INTEGER,
                          FOREIGN KEY(student_id) REFERENCES students(id))''')
    connect.commit()
    connect.close()


def add_student(first_name, last_name):
    # Добавление ученика в базу данных, если его еще нет
    connect = sqlite3.connect('students.db')
    cursor = connect.cursor()

    # Проверка на дублирование ученика
    cursor.execute("SELECT * FROM students WHERE first_name = ? AND last_name = ?", (first_name, last_name))
    if cursor.fetchone() is not None:
        connect.close()
        return False  # ученик уже существует

    # Вставка нового ученика в таблицу
    cursor.execute("INSERT INTO students (first_name, last_name) VALUES (?, ?)", (first_name, last_name))
    connect.commit()
    connect.close()
    return True


def student_exists(first_name, last_name):
    # Проверка на существование ученика в базе данных
    connect = sqlite3.connect('students.db')
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM students WHERE first_name = ? AND last_name = ?", (first_name, last_name))
    result = cursor.fetchone() is not None
    connect.close()
    return result


def add_scores(first_name, last_name, subject, score):
    # Добавление баллов по предмету
    connect = sqlite3.connect('students.db')
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM students WHERE first_name = ? AND last_name = ?", (first_name, last_name))
    student = cursor.fetchone()
    if student is None:
        connect.close()
        return False
    student_id = student[0]
    cursor.execute("INSERT INTO scores (student_id, subject, score) VALUES (?, ?, ?)", (student_id, subject, score))
    connect.commit()
    connect.close()
    print(f'Баллы по предмету {subject} для {first_name} {last_name} сохранены в базе данных.')
    return True


def get_scores(first_name, last_name):
    # Получение баллов по предметам для ученика
    connect = sqlite3.connect('students.db')
    cursor = connect.cursor()
    cursor.execute("SELECT id FROM students WHERE first_name = ? AND last_name = ?", (first_name, last_name))
    student = cursor.fetchone()
    if student is None:
        connect.close()
        return None
    student_id = student[0]
    cursor.execute("SELECT subject, score FROM scores WHERE student_id = ?", (student_id,))
    scores = cursor.fetchall()
    connect.close()
    return scores

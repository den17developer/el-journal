import sqlite3
import tkinter as tk
from tkinter import messagebox
import datetime
import telebot
#dfgdfgdfgdgdf
# Установка соединения с базой данных
conn = sqlite3.connect('college.db')
c = conn.cursor()
# Создание главного окна приложения
root = tk.Tk()
root.title("Attendance System")

# Функция для добавления нового студента в базу данных
def add_student():
    name = student_name_entry.get().strip()
    if name == "":
        messagebox.showerror("Ошибка", "Введите имя студента")
        return
    c.execute("""CREATE TABLE IF NOT EXISTS students (
              name TEXT
              )""")
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM students WHERE name=?", (name,))
    row = cursor.fetchone()
    if row[0] > 0:
        messagebox.showerror("Ошибка", f"Студент с именем '{name}' уже существует")
        return
    conn.execute("INSERT INTO students VALUES (?)", (name,))
    conn.commit()
    messagebox.showinfo("Успех", f"Студент '{name}' добавлен в базу данных")
    student_name_entry.delete(0, tk.END)

# Функция для добавления нового занятия в базу данных
def add_lesson():
    subject = subject_entry.get().strip()
    teacher = teacher_entry.get().strip()
    date = date_entry.get().strip()
    if subject == "":
        messagebox.showerror("Ошибка", "Введите название предмета")
        return
    if teacher == "":
        messagebox.showerror("Ошибка", "Введите имя преподавателя")
        return
    if date == "":
        messagebox.showerror("Ошибка", "Введите дату занятия (в формате ДД.ММ.ГГГГ)")
        return
    try:
        date = datetime.datetime.strptime(date, '%d.%m.%Y')
    except ValueError:
        messagebox.showerror("Ошибка", "Неверный формат даты")
        return

    c.execute("""CREATE TABLE IF NOT EXISTS lessons (
        subject TEXT,
        teacher TEXT,
        date TEXT
        )""")
    conn.execute("INSERT INTO lessons (subject, teacher, date) VALUES (?, ?, ?)", (subject, teacher, date))
    conn.commit()
    messagebox.showinfo("Успех", "Занятие добавлено в базу данных")
    subject_entry.delete(0, tk.END)
    teacher_entry.delete(0, tk.END)
    date_entry.delete(0, tk.END)

# Функция для отметки посещаемости студента на занятии
def mark_attendance():
    student_id = student_id_entry.get().strip()
    lesson_id = lesson_id_entry.get().strip()
    is_present = is_present_var.get()
    date_attedance = date_attendance_entry.get().strip()
    if student_id == "":
        messagebox.showerror("Ошибка", "Введите имя студента")
        return
    if lesson_id == "":
        messagebox.showerror("Ошибка", "Введите название занятия")
        return
    if date_attedance == "":
        messagebox.showerror("Ошибка", "Введите дату посещения")
        return

    cursor = conn.execute("SELECT COUNT(*) FROM students WHERE name=?", (student_id,))
    row = cursor.fetchone()
    if row[0] == 0:
        messagebox.showerror("Ошибка", f"Студент с id '{student_id}' не найден")
        return
    cursor = conn.execute("SELECT COUNT(*) FROM lessons WHERE subject=?", (lesson_id,))

    row = cursor.fetchone()
    if row[0] == 0:
        messagebox.showerror("Ошибка", f"Занятие с id '{lesson_id}' не найдено")
        return

    c.execute("""CREATE TABLE IF NOT EXISTS attendance (
        student_id TEXT,
        lesson_id TEXT,
        is_present TEXT,
        date_attendance TEXT
        )""")
    cursor = conn.execute("SELECT COUNT(*) FROM attendance WHERE student_id=? AND lesson_id=? AND date_attendance=?", (student_id, lesson_id, date_attedance))
    row = cursor.fetchone()
    if row[0] > 0:
        messagebox.showerror("Ошибка", "Посещаемость уже отмечена")
        return
    conn.execute("INSERT INTO attendance (student_id, lesson_id, is_present, date_attendance) VALUES (?, ?, ?, ?)",
                 (student_id, lesson_id, is_present, date_attedance))
    conn.commit()
    messagebox.showinfo("Успех", "Посещаемость отмечена")
    student_id_entry.delete(0, tk.END)
    lesson_id_entry.delete(0, tk.END)
    date_attendance_entry.delete(0, tk.END)
    is_present_var.set(0)

# Функция для вывода посещаемости
def view_attendance():
    student_id = view_attendance_student_id_entry.get().strip()
    if student_id == "":
        messagebox.showerror("Ошибка", "Введите id студента")
        return
    cursor = c.execute("""
        SELECT lessons.date, lessons.subject, attendance.is_present 
        FROM attendance
        JOIN lessons ON attendance.lesson_id = lessons.subject
        WHERE attendance.student_id=?
        ORDER BY lessons.date ASC
        """, (student_id,))

    rows = cursor.fetchall()
    if not rows:
        messagebox.showinfo("Предупреждение", "Нет данных о посещаемости студента")
        return

    result = "Дата занятия\t\tНазвание предмета\t\tПосещение\n"
    for row in rows:
        #.strftime('%d.%m.%Y')
        result += f"{row[0]}\t{row[1]}\t{'Да' if row[2] else 'Нет'}\n"
        messagebox.showinfo("Посещаемость", result)

student_name_label = tk.Label(root, text="Имя студента:")
student_name_entry = tk.Entry(root)
add_student_button = tk.Button(root, text="Добавить студента", command=add_student)

subject_label = tk.Label(root, text="Название предмета:")
subject_entry = tk.Entry(root)
teacher_label = tk.Label(root, text="Преподаватель:")
teacher_entry = tk.Entry(root)
date_label = tk.Label(root, text="Дата занятия (ДД.ММ.ГГГГ):")
date_entry = tk.Entry(root)
add_lesson_button = tk.Button(root, text="Добавить занятие", command=add_lesson)

student_id_label = tk.Label(root, text="Id студента:")
student_id_entry = tk.Entry(root)
lesson_id_label = tk.Label(root, text="Id занятия:")
lesson_id_entry = tk.Entry(root)
date_attendance_label = tk.Label(root, text="Дата посещения:")
date_attendance_entry = tk.Entry(root)
is_present_var = tk.BooleanVar()
is_present_checkbutton = tk.Checkbutton(root, text="Присутствовал(а)", variable=is_present_var)
mark_attendance_button = tk.Button(root, text="Отметить посещение", command=mark_attendance)

view_attendance_label = tk.Label(root, text="Посмотреть посещаемость студента")

view_attendance_student_id_label = tk.Label(root, text="Id студента:")
view_attendance_student_id_entry = tk.Entry(root)
view_attendance_button = tk.Button(root, text="Посмотреть посещаемость", command=view_attendance)

student_name_label.grid(row=0, column=0, padx=5, pady=5)
student_name_entry.grid(row=0, column=1, padx=5, pady=5)
add_student_button.grid(row=0, column=2, padx=5, pady=5)

subject_label.grid(row=1, column=0, padx=5, pady=5)
subject_entry.grid(row=1, column=1, padx=5, pady=5)
teacher_label.grid(row=2, column=0, padx=5, pady=5)
teacher_entry.grid(row=2, column=1, padx=5, pady=5)
date_label.grid(row=3, column=0, padx=5, pady=5)
date_entry.grid(row=3, column=1, padx=5, pady=5)
add_lesson_button.grid(row=4, column=1, padx=5, pady=5)

student_id_label.grid(row=5, column=0, padx=5, pady=5)
student_id_entry.grid(row=5, column=1, padx=5, pady=5)
lesson_id_label.grid(row=6, column=0, padx=5, pady=5)
lesson_id_entry.grid(row=6, column=1, padx=5, pady=5)
date_attendance_label.grid(row=7, column=0, padx=5, pady=5)
date_attendance_entry.grid(row=7, column=1, padx=5, pady=5)
is_present_checkbutton.grid(row=8, column=1, padx=5, pady=5)
mark_attendance_button.grid(row=9, column=1, padx=5, pady=5)

view_attendance_label.grid(row=10, column=0, padx=5, pady=5)
view_attendance_student_id_label.grid(row=11, column=0, padx=5, pady=5)
view_attendance_student_id_entry.grid(row=11, column=1, padx=5, pady=5)
view_attendance_button.grid(row=12, column=1, padx=5, pady=5)

root.mainloop()


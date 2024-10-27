import random
import string
import json
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import os

# Глобальные переменные для хранения паролей до их скрытия
passwords_before_hide = None

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def save_password():
    site = simpledialog.askstring("Сохранение пароля", "Введите название сайта:")
    if not site:
        return
    username = simpledialog.askstring("Сохранение пароля", f"Введите имя пользователя для {site}:")
    if not username:
        return
    password_length = simpledialog.askinteger("Сохранение пароля", "Введите длину пароля (по умолчанию 12):", initialvalue=12)
    password = generate_password(password_length)
    save_password_to_file(site, username, password)
    messagebox.showinfo("Пароль сохранен", f"Пароль для {site} сохранен успешно.")

def save_password_to_file(site, username, password, filename='passwords.json'):
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump({}, file)

    with open(filename, 'r') as file:
        passwords = json.load(file)

    passwords[site] = {'username': username, 'password': password}

    with open(filename, 'w') as file:
        json.dump(passwords, file, indent=4)

def show_passwords():
    global passwords_before_hide  # Используем глобальную переменную

    try:
        with open('passwords.json', 'r') as file:
            passwords = json.load(file)
            password_window = tk.Toplevel()
            password_window.title("Сохраненные пароли")

            tree = ttk.Treeview(password_window)
            tree["columns"] = ("site", "username", "password")
            tree.heading("site", text="Сайт")
            tree.heading("username", text="Имя пользователя")
            tree.heading("password", text="Пароль")

            for site, data in passwords.items():
                tree.insert("", "end", values=(site, data["username"], data["password"]))

            tree.pack(expand=True, fill="both")

            def copy_password():
                selected_item = tree.selection()[0]
                password = tree.item(selected_item, "values")[2]
                password_window.clipboard_clear()
                password_window.clipboard_append(password)
                password_window.update()

            def delete_password():
                selected_item = tree.selection()[0]
                site = tree.item(selected_item, "values")[0]
                del passwords[site]
                with open('passwords.json', 'w') as file:
                    json.dump(passwords, file, indent=4)
                tree.delete(selected_item)

            def hide_passwords():
                global passwords_before_hide  # Используем глобальную переменную
                if passwords_before_hide is None:
                    passwords_before_hide = passwords.copy()  # Сохраняем пароли до их скрытия
                    for item, (site, data) in zip(tree.get_children(), passwords.items()):
                        tree.item(item, values=(site, data["username"], "56"))
                else:
                    for item, (site, data) in zip(tree.get_children(), passwords_before_hide.items()):
                        tree.item(item, values=(site, data["username"], data["password"]))
                    passwords_before_hide = None

            copy_button = ttk.Button(password_window, text="Копировать пароль", command=copy_password)
            copy_button.pack(side="left", padx=10, pady=10)
            delete_button = ttk.Button(password_window, text="Удалить пароль", command=delete_password)
            delete_button.pack(side="right", padx=10, pady=10)
            hide_button = ttk.Button(password_window, text="Скрыть пароли", command=hide_passwords)
            hide_button.pack(pady=10)

    except FileNotFoundError:
        messagebox.showinfo("Ошибка", "Файл с паролями не найден.")

def main():
    root = tk.Tk()
    root.title("Менеджер паролей")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", padding=10, font=('Helvetica', 12))

    generate_button = ttk.Button(root, text="Сгенерировать новый пароль", command=save_password)
    generate_button.pack(pady=10)

    show_button = ttk.Button(root, text="Просмотреть сохраненные пароли", command=show_passwords)
    show_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

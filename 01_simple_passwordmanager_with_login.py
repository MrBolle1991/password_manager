import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt

def open_password_manager_window():
    def add_login_data():
        account = entry_account.get()
        login_email = entry_login_email.get()
        password = entry_password.get()

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute('INSERT INTO login_data (account, login_email, password) VALUES (?, ?, ?)', (account, login_email, hashed_password))
        conn.commit()

        login_data_list.append((account, login_email, password))
        listbox_logindata.insert(tk.END, f"{account} - {login_email} - {password}")
        messagebox.showinfo("Erfolg", "Logindaten wurden hinzugefügt!")

    def display_unencrypted_data():
        messagebox.showinfo("Unverschlüsselte Logindaten", "\n".join([f"{data[0]} - {data[1]} - {data[2]}" for data in login_data_list]))

    root.withdraw()  # Verstecke das Hauptfenster

    second_window = tk.Toplevel(root)
    second_window.title("Passwortmanager - Logindaten hinzufügen")
    second_window.geometry("1000x800")

    label_account = tk.Label(second_window, text="Account:")
    label_account.pack()
    entry_account = tk.Entry(second_window)
    entry_account.pack()

    label_login_email = tk.Label(second_window, text="Login/Email:")
    label_login_email.pack()
    entry_login_email = tk.Entry(second_window)
    entry_login_email.pack()

    label_password = tk.Label(second_window, text="Passwort:")
    label_password.pack()
    entry_password = tk.Entry(second_window, show="*")
    entry_password.pack()

    btn_add_login_data = tk.Button(second_window, text="Logindaten hinzufügen", command=add_login_data)
    btn_add_login_data.pack()

    btn_display_unencrypted_data = tk.Button(second_window, text="Unverschlüsselte Logindaten anzeigen", command=display_unencrypted_data)
    btn_display_unencrypted_data.pack()

    listbox_logindata = tk.Listbox(second_window, width=80, height=20)
    listbox_logindata.pack()

def register():
    username = entry_username.get()
    password = entry_password.get()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        messagebox.showerror("Fehler", "Benutzername bereits vorhanden!")
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Erfolg", "Benutzer wurde registriert!")

def login():
    username = entry_username.get()
    password = entry_password.get()

    cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    if result:
        hashed_password = result[0]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            messagebox.showinfo("Erfolg", "Erfolgreich eingeloggt!")
            open_password_manager_window()
        else:
            messagebox.showerror("Fehler", "Falsches Passwort!")
    else:
        messagebox.showerror("Fehler", "Benutzer nicht gefunden!")

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account TEXT NOT NULL,
        login_email TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

root = tk.Tk()
root.title("Passwortmanager - Login")
root.geometry("400x300")

label_username = tk.Label(root, text="Benutzername:")
label_username.pack()
entry_username = tk.Entry(root)
entry_username.pack()

label_password = tk.Label(root, text="Passwort:")
label_password.pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

btn_login = tk.Button(root, text="Login", command=login)
btn_login.pack()

btn_register = tk.Button(root, text="Registrieren", command=register)
btn_register.pack()

login_data_list = []

root.mainloop()

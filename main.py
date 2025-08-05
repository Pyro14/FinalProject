import tkinter
from tkinter import ttk
import sqlite3 as sql
from tkinter import *
from PIL import Image, ImageTk

db_path = "C:/Users/manuf/PycharmProjects/Final Project/database/users.db"

#class for the main window
class MainWindow:
    def __init__(self, root):

        self.window = root
        self.window.title("Pyflix Login")
        self.window.resizable(1, 1)
        self.window.configure(bg="#000000")

        self.login_screen()

    #window for the login screen
    def login_screen(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.columnconfigure(0, weight=1)

        # Logo
        self.photo = ImageTk.PhotoImage(Image.open("images/Pyflix.png"))
        image_label = Label(self.window, image=self.photo, bg="#000000")
        image_label.pack(pady=20)

        # Container frame for login elements
        login_container = Frame(self.window, bg="#000000")
        login_container.pack()

        frame = LabelFrame(login_container, text="Login", bg="#000000", fg="white")
        frame.grid(row=0, column=0, padx=10, pady=10)

        Button(frame, text="X",fg="red", command=self.window.destroy).grid(row=0, column=2, padx=5)

        Label(frame, text="Username:", bg="#000000", fg="white").grid(row=1, column=0, sticky='w')
        self.username_entry = Entry(frame)
        self.username_entry.grid(row=1, column=1)

        Label(frame, text="Password:", bg="#000000", fg="white").grid(row=2, column=0, sticky='w')
        self.password_entry = Entry(frame, show="*")
        self.password_entry.grid(row=2, column=1)

        Button(frame, text="Login", command=self.verify_login).grid(row=3, column=1, pady=10)

        self.text = Label(login_container, text='', fg='red', bg="#000000")
        self.text.grid(row=1, column=0, columnspan=2, sticky=W + E, padx=10)

    def verify_login(self):
        login_user = self.username_entry.get().strip()
        login_pass = self.password_entry.get().strip()

        con = sql.connect(db_path)
        cur = con.cursor()

        # get info for only user logging in
        cur.execute(f"SELECT password, dev FROM users WHERE username = '{login_user}'")

        result = cur.fetchone()
        con.close()

        if not result:  # result doesn't exist = no matching username found
            self.text['text'] = "User not found"
            return

        password, dev = result  # unpack the query result tuple into multiple variables

        if password == login_pass:
            self.username = login_user
            self.is_dev = dev == 1
            if self.is_dev:
                self.dev_menu()
            else:
                self.pyflix_menu()
        else:
            self.text['text'] = "Incorrect password"


    def pyflix_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.title("Pyflix Main Menu")
        Label(self.window, text=f"Welcome, {self.username}!", font=("Arial", 16)).pack(pady=20)

        button_frame = Frame(self.window)
        button_frame.pack(pady=10)

        Button(button_frame, text="Series Catalog", command=self.series_catalog, width=12).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Movie Catalog", command=self.movie_catalog, width=12).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Favourites", width=12).grid(row=0, column=2, padx=5)
        Button(button_frame, text="Watched", width=12).grid(row=0, column=3, padx=5)
        Button(button_frame, text="Watching", width=12).grid(row=0, column=4, padx=5)

        Button(self.window, text="Logout", command=self.login_screen).pack(pady=20)

    def dev_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.title("Pyflix Dev Menu")
        Label(self.window, text=f"Welcome, {self.username} to the dev menu!", font=("Arial", 16)).pack(pady=20)

        button_frame = Frame(self.window)
        button_frame.pack(pady=10)

        Button(button_frame, text="Edit Series Catalog", command=self.series_catalog, width=15).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Edit Movie Catalog", command=self.movie_catalog, width=15).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Edit Users", command=self.users_catalog, width=15).grid(row=0, column=2, padx=5)

        Button(self.window, text="Logout", command=self.login_screen).pack(pady=20)

    def catalog(self, title, table):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.title(f"{title.capitalize()} Catalog")
        Label(self.window, text=f"Welcome, {self.username} to our {title} catalog!", font=("Arial", 16)).pack(pady=20)

        button_frame = Frame(self.window)
        button_frame.pack(pady=10)

        Login_func = self.dev_menu if self.is_dev else self.pyflix_menu
        Button(button_frame, text="Menu", command=Login_func, width=12).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Logout", command=self.login_screen, width=12).grid(row=0, column=2, padx=5)

        con = sql.connect(db_path)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table}")
        data = cur.fetchall()
        con.close()

        columns_by_table = {
            'movies': ["id", "name", "release_date", "director","duration_min"],
            'series': ["id", "name", "num_season", "episodes"],
            'users': ["id", "name", "num_season", "episodes"],
        }

        columns = columns_by_table[table]

        self.table = ttk.Treeview(self.window, columns=columns, show="headings")
        for column in columns:
            self.table.heading(column, text=column)
        for row in data:
            self.table.insert("", "end", values=row)
        self.table.pack(pady=20, fill=tkinter.Y, expand=True)

        # dev tools
        if self.is_dev :
            editor_frame = Frame(self.window)
            editor_frame.pack(pady=20)

            for column in columns_by_table:
                Label(editor_frame, text=f"{column}")

         #   Label(editor_frame, text="Movie name: ").grid(row=0, column=0)
         #   name_entry = Entry(editor_frame)
          #  name_entry.grid(row=0, column=1)

          #  Label(editor_frame, text="Release date: ").grid(row=1, column=0)
          #  date_entry = Entry(editor_frame)
          #  date_entry.grid(row=1, column=1)

          #  Label(editor_frame, text="Director: ").grid(row=0, column=2)
          #  director_entry = Entry(editor_frame)
           # director_entry.grid(row=0, column=3)

           # Label(editor_frame, text="Movie durarion: ").grid(row=1, column=2)
           # duration_min_entry = Entry(editor_frame)
           # duration_min_entry.grid(row=1, column=3)

            Button(editor_frame, text="Add movie", command=lambda: self.add_movie( name_entry.get(), date_entry.get(), director_entry.get(), duration_min_entry.get())).grid(row=0, column=5, pady=10)
            Button(editor_frame, text="Delete movie", command=self.del_movie).grid(row=1, column=5, pady=10)

    def add_movie(self,name, release_date, director,duration_min):
        con = sql.connect(db_path)
        cur = con.cursor()
        cur.execute("INSERT INTO movies (name, release_date, director,duration_min) VALUES (?, ?, ?, ?)", (name, release_date, director,duration_min))
        con.commit()
        con.close()
        self.movie_catalog()

    def del_movie(self):
        selected = self.table.selection()
        if not selected:
            return
        item=self.table.item(selected)
        movie_id = item["values"][0]
        con = sql.connect(db_path)
        cur = con.cursor()
        cur.execute("DELETE FROM movies WHERE id = ?", (movie_id,))
        con.commit()
        con.close()

        self.movie_catalog()


    def movie_catalog(self):
        self.catalog("movie", "movies")

    def series_catalog(self):
        self.catalog("series", "series")

    def users_catalog(self):
        self.catalog("users", "users")

if __name__ == "__main__":
    root = Tk()
    root.attributes('-fullscreen', True)
    app = MainWindow(root)
    root.mainloop()

# Import necessary modules
import tkinter  # Base GUI toolkit
from tkinter import ttk  # For advanced widgets like Treeview
import sqlite3 as sql  # For database operations
from tkinter import *  # Additional Tkinter components
from PIL import Image, ImageTk  # For image handling

# Path to the SQLite database
db_path = "C:/Users/manuf/PycharmProjects/FinalProject/database/users.db"

# Main application class
class MainWindow:
    def __init__(self, root):
        # Initialize main window
        self.window = root
        self.window.title("Pyflix Login")
        self.window.resizable(1, 1)
        self.window.configure(bg="#000000")  # Set background to black

        self.login_screen()  # Load login screen on startup

    # Lists for the fav function
        self.user_movie_list = set()
        self.user_series_list = set()

    # Login screen layout
    def login_screen(self):
        # Clear any existing widgets
        for widget in self.window.winfo_children():
            widget.destroy()
        self.window.columnconfigure(0, weight=1)

        # Load and display logo
        self.photo = ImageTk.PhotoImage(Image.open("images/Pyflix.png"))
        image_label = Label(self.window, image=self.photo, bg="#000000")
        image_label.pack(pady=20)

        # Container for login form
        login_container = Frame(self.window, bg="#000000")
        login_container.pack()

        # Login form frame
        frame = LabelFrame(login_container, text="Login", bg="#000000", fg="white")
        frame.grid(row=0, column=0, padx=10, pady=10)

        # Exit button
        Button(frame, text="X", fg="red", command=self.window.destroy).grid(row=0, column=2, padx=5)

        # Username input
        Label(frame, text="Username:", bg="#000000", fg="white").grid(row=1, column=0, sticky='w')
        self.username_entry = Entry(frame)
        self.username_entry.grid(row=1, column=1)

        # Password input
        Label(frame, text="Password:", bg="#000000", fg="white").grid(row=2, column=0, sticky='w')
        self.password_entry = Entry(frame, show="*")
        self.password_entry.grid(row=2, column=1)

        # Login button
        Button(frame, text="Login", command=self.verify_login).grid(row=3, column=1, pady=10)

        # Error message label
        self.text = Label(login_container, text='', fg='red', bg="#000000")
        self.text.grid(row=1, column=0, columnspan=2, sticky=W + E, padx=10)

    # Verify login credentials
    def verify_login(self):
        login_user = self.username_entry.get().strip()
        login_pass = self.password_entry.get().strip()

        con = sql.connect(db_path)
        cur = con.cursor()
        cur.execute(f"SELECT id, password, dev FROM users WHERE username = '{login_user}'")
        result = cur.fetchone()
        con.close()

        if not result:
            self.text['text'] = "User not found"
            return

        self.user_id, password, dev = result
        if password == login_pass:
            self.username = login_user
            self.is_dev = dev == 1
            if self.is_dev:
                self.dev_menu()  # Load developer menu
            else:
                self.pyflix_menu()  # Load regular user menu
        else:
            self.text['text'] = "Incorrect password"

    # Regular user main menu
    def pyflix_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.title("Pyflix Main Menu")
        Label(self.window, text=f"Welcome, {self.username}!", font=("Arial", 16)).pack(pady=20)

        button_frame = Frame(self.window)
        button_frame.pack(pady=10)

        # Navigation buttons
        Button(button_frame, text="Series Catalog", command=self.series_catalog, width=12).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Movie Catalog", command=self.movie_catalog, width=12).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Fav Series", command=self.fav_display, width=12).grid(row=0, column=2, padx=5)
        Button(button_frame, text="Fav Movies", width=12).grid(row=0, column=3, padx=5)
        Button(button_frame, text="Watched", width=12).grid(row=0, column=4, padx=5)

        Button(self.window, text="Logout", command=self.login_screen).pack(pady=20)

    # Developer menu
    def dev_menu(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.window.title("Pyflix Dev Menu")
        Label(self.window, text=f"Welcome, {self.username} to the dev menu!", font=("Arial", 16)).pack(pady=20)

        button_frame = Frame(self.window)
        button_frame.pack(pady=10)

        # Dev options
        Button(button_frame, text="Edit Series Catalog", command=self.series_catalog, width=15).grid(row=0, column=0, padx=5)
        Button(button_frame, text="Edit Movie Catalog", command=self.movie_catalog, width=15).grid(row=0, column=1, padx=5)
        Button(button_frame, text="Edit Users", command=self.users_catalog, width=15).grid(row=0, column=2, padx=5)

        Button(self.window, text="Logout", command=self.login_screen).pack(pady=20)

    # Catalog view for movies, series, or users
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
        if self.is_dev == 0:
            Button(button_frame, text="Fav selection",command=lambda:self.toggle_fav(table, title), width=12).grid(row=0, column=3 , padx=5)

        # Fetch data from database
        con = sql.connect(db_path)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table}")
        data = cur.fetchall()
        con.close()

        # Define columns for each table
        columns_by_table = {
            'movies': ["id", "name", "release_date", "director", "duration_min", "thumbnail"],
            'series': ["id", "name", "num_season", "episodes", "thumbnail"],
            'users': ["id", "username", "password", "dev"],
        }

        columns = columns_by_table[table]
        main_frame = Frame(self.window)
        main_frame.pack(pady=20, fill=tkinter.Y, expand=True)

        # Thumbnail display area
        thumb_list = Frame(main_frame)
        thumb_list.grid(row=0, column=0)
        self.thumbnail_label = Label(thumb_list)
        self.thumbnail_label.grid(row=0, column=0)

        # Table to show catalog data
        self.table = ttk.Treeview(main_frame, columns=columns, show="headings", height=38)
        self.table.grid(row=0, column=1)

        for column in columns:
            self.table.heading(column, text=column)
        for row in data:
            self.table.insert("", "end", values=row)

        # Function to update image when a row is selected
        def on_select(event):
            selected = self.table.selection()
            if not selected:
                return
            item = self.table.item(selected)
            values = item["values"]
            thumbnail = values[-1]  # Last column is thumbnail filename

            try:
                img = Image.open(f"images/{thumbnail}")
                target_height = 600
                aspect_ratio = img.width / img.height
                target_width = int(target_height * aspect_ratio)
                resized_img = img.resize((target_width, target_height), Image.LANCZOS)
                self.display_image = ImageTk.PhotoImage(resized_img)
                self.thumbnail_label.config(image=self.display_image, text="")
            except Exception as e:
                print(f"Error loading image: {e}")
                self.thumbnail_label.config(image='', text="No image available")

        # Bind selection event to image update
        self.table.bind("<<TreeviewSelect>>", on_select)

        # Developer tools for adding/deleting entries
        if self.is_dev:
            editor_frame = Frame(self.window)
            editor_frame.pack(pady=20)

            entries = {}
            for i, column in enumerate(columns[1:]):
                Label(editor_frame, text=f"{table} {column}").grid(row=0, column=i)
                entry = Entry(editor_frame)
                entry.grid(row=1, column=i)
                entries[column] = entry

            def func():
                data = [entries[col].get() for col in columns[1:]]
                self.add_to_database(table, columns[1:], data, title)
            # Button to add new entry to the database
            Button(editor_frame, text=f"Add {table}", command=func).grid(row=1, column=len(columns), pady=10)

            # Button to delete selected entry from the database
            Button(editor_frame, text=f"Delete {title}", command=lambda: self.del_database_data(title, table)).grid(row=0, column=len(columns), pady=10)

    # Function to add a new record to the database
    def add_to_database(self, table, columns, data, title):
        con = sql.connect(db_path)
        cur = con.cursor()

        # Prepare SQL query with placeholders
        qs = ', '.join(['?' for _ in range(len(columns))])
        cols = ', '.join(columns)

        # Execute insert query
        cur.execute(f"INSERT INTO {table} ({cols}) VALUES ({qs})", data)
        con.commit()
        con.close()

        # Refresh catalog view
        self.catalog(title, table)

    # Function to delete selected record from the database
    def del_database_data(self, title, table):
        con = sql.connect(db_path)
        cur = con.cursor()

        # Get selected item from the table
        selected = self.table.selection()
        if not selected:
            return
        item = self.table.item(selected)
        id = item["values"][0]  # Assuming first column is ID

        # Execute delete query
        cur.execute(f"DELETE FROM {table} WHERE id = ?", (id,))
        con.commit()
        con.close()

        # Refresh catalog view
        self.catalog(title, table)
    def load_fav_table(self,table):
        con = sql.connect(db_path)
        cur = con.cursor()
        cur.execute(f"SELECT {table}_id FROM fav_{table} WHERE user_id = '{self.user_id}'")
        result = cur.fetchall()
        con.close()
        return [r[0] for r in result]

    def toggle_fav(self,table,title):


        con = sql.connect(db_path)
        cur = con.cursor()

        # Get selected item from the table
        selected = self.table.selection()
        if not selected:
            return
        item = self.table.item(selected)
        id = item["values"][0]  # Assuming first column is ID
        ### append all this list to the current list on the table

        if table == "series" and id in self.load_fav_table(table):
            cur.execute(f"DELETE FROM fav_{table} WHERE user_id = ? AND series_id = ?", (self.user_id,id))
        elif table == "movies" and id in self.load_fav_table(table):
            cur.execute(f"DELETE FROM fav_{table} WHERE user_id = ? AND movies_id = ?", (self.user_id,id))
        else:
            cur.execute(f"INSERT INTO fav_{table} VALUES (?,?)", (self.user_id, id))

        if table == "Movies":
            print(self.user_movie_list)
        else:
            print(self.user_series_list)
        con.commit()
        con.close()

        # Refresh catalog view
        self.catalog(title, table)


    # Shortcut to open movie catalog
    def movie_catalog(self):
        self.catalog("movie", "movies")

    # Shortcut to open series catalog
    def series_catalog(self):
        self.catalog("series", "series")

    # Shortcut to open users catalog (only for devs)
    def users_catalog(self):
        self.catalog("users", "users")

# Entry point of the application
if __name__ == "__main__":
    root = Tk()
    root.attributes('-fullscreen', True)  # Launch in fullscreen mode
    app = MainWindow(root)  # Create instance of MainWindow
    root.mainloop()  # Start the Tkinter event loop

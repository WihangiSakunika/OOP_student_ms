import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import ttkbootstrap as tb
import mysql.connector

# ---------------- DATABASE CONFIG ----------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",         # change to your MySQL username
    "password": "",         # change to your MySQL password
    "database": "student_db"  # change to your database
}

PROGRAMS = [
    "MSc Information Technology",
    "MSc Software Engineering",
    "MSc Cyber Security",
    "MSc Data Science",
    "MSc Artificial Intelligence",
    "MSc Cloud Computing",
    "MSc Networking",
    "MSc Business Analytics",
    "MSc Web Engineering",
    "MSc IT Management"
]

# -------------------------------------------------
class App(tb.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("Student Management System")
        self.geometry("1200x700")

        # ---------- FONT SETTINGS ----------
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=11)

        self.heading_font = tkFont.Font(family="Segoe UI", size=16, weight="bold")
        self.subheading_font = tkFont.Font(family="Segoe UI", size=14, weight="bold")

        self.option_add("*TButton.Font", default_font)
        self.option_add("*TLabel.Font", default_font)
        self.option_add("*Treeview.Font", default_font)
        self.option_add("*Entry.Font", default_font)

        # ---------- LOGIN ----------
        self.admin_user = "admin"
        self.admin_pass = "1234"

        # DB Connection
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor()
        self._create_table()

        self.show_login()

    # -------- CREATE TABLE --------
    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                first_name VARCHAR(100),
                last_name VARCHAR(100),
                email VARCHAR(100),
                phone VARCHAR(50),
                address TEXT,
                birthday DATE,
                program VARCHAR(100),
                intake_year VARCHAR(10),
                lms_username VARCHAR(100),
                lms_password VARCHAR(100)
            )
        """)
        self.conn.commit()

    # -------- LOGIN --------
    def show_login(self):
        self._clear()
        frame = tb.Frame(self, padding=20)
        frame.pack(expand=True)

        tb.Label(frame, text="Admin Login", font=self.heading_font).pack(pady=20)
        self.username = tb.Entry(frame, width=25)
        self.username.insert(0, "admin")
        self.username.pack(pady=10)
        self.password = tb.Entry(frame, show="*", width=25)
        self.password.insert(0, "1234")
        self.password.pack(pady=10)
        tb.Button(frame, text="Login", command=self.handle_login, bootstyle="success").pack(pady=20)

    def handle_login(self):
        if self.username.get() == self.admin_user and self.password.get() == self.admin_pass:
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    # -------- DASHBOARD --------
    def show_dashboard(self):
        self._clear()
        topbar = tb.Frame(self)
        topbar.pack(fill="x")
        tb.Label(topbar, text="Welcome, Admin", font=self.heading_font).pack(side="left", padx=20, pady=10)
        tb.Button(topbar, text="Logout", command=self.show_login, bootstyle="danger").pack(side="right", padx=20)

        container = tb.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        left = tb.Frame(container)
        left.pack(side="left", fill="y", padx=10)

        right = tb.Frame(container)
        right.pack(side="right", fill="both", expand=True)

        self._build_form(left)
        self._build_table(right)
        self._load_students()

    # -------- FORM --------
    def _build_form(self, parent):
        tb.Label(parent, text="Register Student", font=self.subheading_font).pack(pady=10)
        self.form = {}
        fields = ["First Name", "Last Name", "Email", "Phone", "Address", "Intake Year",
                  "LMS Username", "LMS Password"]

        for f in fields:
            tb.Label(parent, text=f).pack(anchor="w")
            var = tk.StringVar()
            ent = tb.Entry(parent, textvariable=var)
            ent.pack(fill="x", pady=2)
            self.form[f] = var

        tb.Label(parent, text="Birthday").pack(anchor="w")
        self.form["Birthday"] = tb.DateEntry(parent)
        self.form["Birthday"].pack(fill="x", pady=2)

        tb.Label(parent, text="Program").pack(anchor="w")
        self.form["Program"] = tb.Combobox(parent, values=PROGRAMS, state="readonly")
        self.form["Program"].pack(fill="x", pady=2)

        tb.Button(parent, text="Add Student", command=self._add_student, bootstyle="primary").pack(pady=10)

    # -------- TABLE + SEARCH --------
    def _build_table(self, parent):
        search_frame = tb.Frame(parent)
        search_frame.pack(fill="x", pady=5)

        tb.Label(search_frame, text="Search:").pack(side="left")
        self.search_var = tk.StringVar()
        tb.Entry(search_frame, textvariable=self.search_var).pack(side="left", padx=5)
        tb.Button(search_frame, text="Go", command=self._search_students, bootstyle="info").pack(side="left", padx=5)
        tb.Button(search_frame, text="Reset", command=self._load_students, bootstyle="secondary").pack(side="left", padx=5)

        tb.Label(search_frame, text="Filter Program:").pack(side="left", padx=5)
        self.filter_program = tb.Combobox(search_frame, values=["All"] + PROGRAMS, state="readonly")
        self.filter_program.current(0)
        self.filter_program.pack(side="left", padx=5)

        tb.Label(search_frame, text="Intake:").pack(side="left", padx=5)
        self.filter_intake = tb.Entry(search_frame, width=10)
        self.filter_intake.pack(side="left", padx=5)
        tb.Button(search_frame, text="Apply Filter", command=self._filter_students, bootstyle="warning").pack(side="left", padx=5)

        # ---------- Responsive Table with Scrollbars ----------
        cols = ["ID", "First", "Last", "Email", "Program", "Intake", "Birthday"]
        table_frame = tb.Frame(parent)
        table_frame.pack(fill="both", expand=True)

        self.table = tb.Treeview(table_frame, columns=cols, show="headings")
        for c in cols:
            self.table.heading(c, text=c)
            self.table.column(c, width=150, anchor="center")

        vsb = tb.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        hsb = tb.Scrollbar(table_frame, orient="horizontal", command=self.table.xview)
        self.table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.table.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        btn_frame = tb.Frame(parent)
        btn_frame.pack(fill="x", pady=10)
        tb.Button(btn_frame, text="View", command=self._view_student, bootstyle="info").pack(side="left", padx=5)
        tb.Button(btn_frame, text="Edit", command=self._edit_student, bootstyle="warning").pack(side="left", padx=5)
        tb.Button(btn_frame, text="Delete", command=self._delete_student, bootstyle="danger").pack(side="left", padx=5)

    # -------- CRUD FUNCTIONS --------
    def _add_student(self):
        data = (
            self.form["First Name"].get(),
            self.form["Last Name"].get(),
            self.form["Email"].get(),
            self.form["Phone"].get(),
            self.form["Address"].get(),
            self.form["Birthday"].entry.get(),
            self.form["Program"].get(),
            self.form["Intake Year"].get(),
            self.form["LMS Username"].get(),
            self.form["LMS Password"].get()
        )
        self.cursor.execute("""
            INSERT INTO students (first_name, last_name, email, phone, address, birthday, program, intake_year, lms_username, lms_password)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, data)
        self.conn.commit()
        messagebox.showinfo("Success", "Student added successfully!")
        self._load_students()
        self._clear_form()

    def _view_student(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student first")
            return
        item = self.table.item(selected)
        student_id = item["values"][0]

        self.cursor.execute("SELECT * FROM students WHERE id=%s", (student_id,))
        student = self.cursor.fetchone()
        info = "\n".join([f"{desc[0]}: {val}" for desc, val in zip(self.cursor.description, student)])
        messagebox.showinfo("Student Details", info)

    def _edit_student(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student first")
            return
        item = self.table.item(selected)
        student_id = item["values"][0]

        self.cursor.execute("SELECT * FROM students WHERE id=%s", (student_id,))
        student = self.cursor.fetchone()
        cols = [d[0] for d in self.cursor.description]

        edit_win = tb.Toplevel(self)
        edit_win.title("Edit Student")
        edit_win.geometry("400x500")

        entries = {}
        for i, col in enumerate(cols):
            if col == "id":
                continue
            tb.Label(edit_win, text=col).pack(anchor="w", pady=2)
            var = tk.StringVar(value=str(student[i]))
            ent = tb.Entry(edit_win, textvariable=var)
            ent.pack(fill="x", pady=2)
            entries[col] = var

        def save_changes():
            update_data = [entries[c].get() for c in entries]
            update_data.append(student_id)
            sql = f"UPDATE students SET {', '.join([c+'=%s' for c in entries])} WHERE id=%s"
            self.cursor.execute(sql, tuple(update_data))
            self.conn.commit()
            messagebox.showinfo("Success", "Student updated!")
            self._load_students()
            edit_win.destroy()

        tb.Button(edit_win, text="Save", command=save_changes, bootstyle="success").pack(pady=10)

    def _delete_student(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student first")
            return
        item = self.table.item(selected)
        student_id = item["values"][0]

        self.cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
        self.conn.commit()
        self._load_students()
        messagebox.showinfo("Deleted", "Student record deleted")

    # -------- SEARCH & FILTER --------
    def _search_students(self):
        keyword = "%" + self.search_var.get() + "%"
        self.cursor.execute("""
            SELECT id, first_name, last_name, email, program, intake_year, birthday 
            FROM students 
            WHERE first_name LIKE %s OR last_name LIKE %s OR email LIKE %s
        """, (keyword, keyword, keyword))
        rows = self.cursor.fetchall()
        self._populate_table(rows)

    def _filter_students(self):
        program = self.filter_program.get()
        intake = self.filter_intake.get()
        query = "SELECT id, first_name, last_name, email, program, intake_year, birthday FROM students WHERE 1=1"
        params = []

        if program != "All":
            query += " AND program=%s"
            params.append(program)
        if intake:
            query += " AND intake_year=%s"
            params.append(intake)

        self.cursor.execute(query, tuple(params))
        rows = self.cursor.fetchall()
        self._populate_table(rows)

    def _load_students(self):
        self.cursor.execute("SELECT id, first_name, last_name, email, program, intake_year, birthday FROM students")
        rows = self.cursor.fetchall()
        self._populate_table(rows)

    def _populate_table(self, rows):
        for r in self.table.get_children():
            self.table.delete(r)
        for row in rows:
            self.table.insert("", "end", values=row)

    # -------- UTILITIES --------
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

    def _clear_form(self):
        for key in self.form:
            if isinstance(self.form[key], tk.StringVar):
                self.form[key].set("")
            else:
                self.form[key].set_date("")

# -------------------------------------------------
if __name__ == "__main__":
    app = App()
    app.mainloop()

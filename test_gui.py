import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont
import ttkbootstrap as tb

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

class App(tb.Window):
    def __init__(self):
        super().__init__(themename="cosmo")
        self.title("Student Management System (Demo)")
        self.geometry("1300x700")

        # ---------- FONT SETTINGS ----------
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=11)

        self.heading_font = tkFont.Font(family="Segoe UI", size=16, weight="bold")
        self.subheading_font = tkFont.Font(family="Segoe UI", size=14, weight="bold")

        self.option_add("*TButton.Font", default_font)
        self.option_add("*TLabel.Font", default_font)
        self.option_add("*Treeview.Font", default_font)
        self.option_add("*Entry.Font", default_font)

        # ---------- ADMIN LOGIN ----------
        self.admin_user = "admin"
        self.admin_pass = "1234"

        # ---------- STORAGE ----------
        self.students = []  # keep data only in memory
        self.show_login()

    # -------- LOGIN ----------
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

    # -------- DASHBOARD ----------
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

    # -------- FORM ----------
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

    # -------- TABLE ----------
    def _build_table(self, parent):
        cols = ["ID", "First Name", "Last Name", "Email", "Phone", "Address",
                "Birthday", "Program", "Intake Year", "LMS Username", "LMS Password"]

        self.table = tb.Treeview(parent, columns=cols, show="headings", height=20)

        for c in cols:
            self.table.heading(c, text=c)
            self.table.column(c, width=120, anchor="center")

        self.table.pack(fill="both", expand=True)

        btn_frame = tb.Frame(parent)
        btn_frame.pack(fill="x", pady=10)
        tb.Button(btn_frame, text="View", command=self._view_student, bootstyle="info").pack(side="left", padx=5)
        tb.Button(btn_frame, text="Edit", command=self._edit_student, bootstyle="warning").pack(side="left", padx=5)
        tb.Button(btn_frame, text="Delete", command=self._delete_student, bootstyle="danger").pack(side="left", padx=5)

    # -------- ACTIONS ----------
    def _add_student(self):
        sid = f"MIT{len(self.students)+1:02d}"
        student = {
            "ID": sid,
            "First Name": self.form["First Name"].get(),
            "Last Name": self.form["Last Name"].get(),
            "Email": self.form["Email"].get(),
            "Phone": self.form["Phone"].get(),
            "Address": self.form["Address"].get(),
            "Birthday": self.form["Birthday"].entry.get(),
            "Program": self.form["Program"].get(),
            "Intake Year": self.form["Intake Year"].get(),
            "LMS Username": self.form["LMS Username"].get(),
            "LMS Password": self.form["LMS Password"].get()
        }
        self.students.append(student)
        self.table.insert("", "end", values=tuple(student.values()))
        messagebox.showinfo("Success", f"Student {sid} added!")

    def _view_student(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student first")
            return
        index = self.table.index(selected)
        student = self.students[index]

        info = "\n".join([f"{k}: {v}" for k, v in student.items()])
        messagebox.showinfo("Student Details", info)

    def _edit_student(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student first")
            return
        index = self.table.index(selected)
        student = self.students[index]

        edit_win = tb.Toplevel(self)
        edit_win.title("Edit Student")
        edit_win.geometry("400x500")

        entries = {}
        for k, v in student.items():
            tb.Label(edit_win, text=k).pack(anchor="w", pady=2)
            if k == "Birthday":
                var = tk.StringVar(value=v)
                ent = tb.Entry(edit_win, textvariable=var)
            else:
                var = tk.StringVar(value=v)
                ent = tb.Entry(edit_win, textvariable=var)
            ent.pack(fill="x", pady=2)
            entries[k] = var

        def save_changes():
            for k in entries:
                student[k] = entries[k].get()
            self.table.item(selected, values=tuple(student.values()))
            messagebox.showinfo("Success", "Student updated!")
            edit_win.destroy()

        tb.Button(edit_win, text="Save", command=save_changes, bootstyle="success").pack(pady=10)

    def _delete_student(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a student first")
            return
        index = self.table.index(selected)
        self.table.delete(selected)
        self.students.pop(index)
        messagebox.showinfo("Deleted", "Student record deleted")

    # -------- UTILITY ----------
    def _clear(self):
        for w in self.winfo_children():
            w.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()

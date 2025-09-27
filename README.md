
# 🎓 Student Management System  

A desktop-based **Student Management System** built with **Python (Tkinter + ttkbootstrap)** and **MySQL**.  
This project was designed as a group assignment to help **home tuition tutors** register and manage their students effectively.  

---

## 👥 Team Members  

| Name                      | ID                 | Role/Contribution        |
|---------------------------|--------------------|---------------------------|
| **A.M.S.D. Alahakoon**   | FGS/MIT/2024/065   | Login Module              |
| **P.L.C.S. Alwis**       | FGS/MIT/2024/007   | Register Student Module   |
| **L.H. Wihangi Sakunika**| MIT/2024/002       | Search & Filter / Database|
| **Heshan Wijeweera**     | FGS/MIT/2024/020   | Table Management          |

---

## 📌 Features  
- 🔑 **Admin Login** – Secure access for administrators  
- 📝 **Student Registration Form** – Register new students with auto-generated IDs (MIT001, MIT002, …)  
- 🔍 **Search & Filter** – Find students by name, program, or intake year  
- 📂 **CRUD Operations** – Create, Read, Update, and Delete student records  
- 📋 **View Student Details** – Popup with complete student info  
- 🔄 **Form & Table Utilities** – Clear form, refresh student table  

---

## 🛠️ Technology Stack  
- **Frontend / UI:** Python Tkinter + ttkbootstrap  
- **Backend / Logic:** Python  
- **Database:** MySQL  
- **Libraries:**  
  - `mysql-connector-python`  
  - `tkinter`, `ttkbootstrap`  

---

## 🧩 Software Architecture  
The system follows a **3-layer architecture**:  

- **Presentation Layer** – Tkinter + ttkbootstrap (user interface)  
- **Business Logic Layer** – Python methods handling CRUD operations, ID generation, and validations  
- **Data Layer** – MySQL database for persistent storage  

---

## 🏛️ OOP Structure  
This project applies key **Object-Oriented Programming (OOP) concepts**:  

- **Class & Object:** `App` class as the main structure; `app = App()` creates an object.  
- **Inheritance:** `App` inherits from `ttkbootstrap.Window`.  
- **Encapsulation:** Database operations and UI functions are wrapped in class methods.  
- **Abstraction:** Users only see the GUI; internal SQL queries and logic are hidden.  
- **Polymorphism:** Widgets and overridden methods behave differently based on usage.  

---

## 📚 New Technologies Learned  
- Using **Tkinter + ttkbootstrap** for modern UI design in Python  
- **MySQL integration** with Python using `mysql-connector-python`  
- Implementing **CRUD operations** with database error handling  
- Designing **auto-ID generation logic** (e.g., MIT001, MIT002)  
- Building a **UI + Database workflow** (Login → Registration → Table → CRUD)  

---

## 📝 Requirement Gathering  
We followed **SDLC (Software Development Life Cycle)** steps to gather and refine requirements:  

1. **Interviews & Discussions** – with tutors to understand pain points in managing student data  
2. **Observation** – of manual processes (Excel/paper-based registration)  
3. **Document Analysis** – reviewing existing student registration forms  
4. **Brainstorming** – within the team to finalize CRUD features  
5. **Use Case Scenarios** – like *“Tutor logs in and registers a student”* to validate requirements  

---

## 🗂️ Database Design  

**Table: `students`**  

| Field        | Type           |
|--------------|----------------|
| id           | INT (PK, Auto) |
| first_name   | VARCHAR(100)   |
| last_name    | VARCHAR(100)   |
| email        | VARCHAR(100)   |
| phone        | VARCHAR(50)    |
| address      | TEXT           |
| birthday     | DATE           |
| program      | VARCHAR(100)   |
| intake_year  | VARCHAR(10)    |
| lms_username | VARCHAR(100)   |
| lms_password | VARCHAR(100)   |

---

## 🚀 Installation & Setup  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/student-management-system.git
   cd student-management-system
````

2. **Install dependencies**

   ```bash
   pip install mysql-connector-python ttkbootstrap
   ```

3. **Set up the MySQL database**

   * Create a database `mit_db`
   * The table will be auto-created when you first run the program

4. **Run the application**

   ```bash
   python app.py
   ```

---

## 🔮 Future Enhancements

* 📊 Export student data to **Excel/PDF**
* 👥 Role-based access (Admin, Staff)
* 📈 Advanced reporting & analytics
* ☁️ Cloud deployment with web interface

---

📧 Contact: **[wihangiinfo@gmail.com](mailto:wihangiinfo@gmail.com)**

---

```



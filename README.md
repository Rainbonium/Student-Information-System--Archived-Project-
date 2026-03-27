# Student Information System (Archived Project)

## ⚠️ Project Status

**This is an archived academic project and is not currently runnable.**
The original development environment and some supporting files are no longer available.
For functional projects, please see ![other repositories in my portfolio.](https://rainbonium.github.io/)

This repository is included for demonstration purposes only.

![Database in PostgreSQL.](Thumbnail.png)

---

## Overview

This project demonstrates a command-line student information system built using Pythoin and SQLAlchemy ORM. It's purpose was to manage university data such as:

* Departments
* Courses
* Sections
* Students
* Majors
* Enrollments

The system uses a simple menu interface to perform CRUD operations and manage changes to data.

---

## Tech

Though not currently executable, it demonstrates an understanding of:

* SQLAlchemy
* Python
* Data Relationships (One-to-Many & Many-to-Many)


---

## Key Highlights

### Boilerplate Data
The important starting point of testing the database.

```py
def boilerplate(sess):
    """
    Add boilerplate data initially to jump start the testing.  Remember that there is no
    checking of this data, so only run this option once from the console, or you will
    get a uniqueness constraint violation from the database.
    :param sess:    The session that's open.
    :return:        None
    """
    department: Department = Department('Computer Engineering Computer Science', 'CECS', 'Chair', 'ECS', 1, 'Science rules.')
    course: Course = Course(department, 301, 'Database Fundamentals', 'Data n stuff.', 4)
    section1: Section = Section(course, 1, 'Fall', 2023, 'ECS', 303, 'MW', time(8, 0, 0), 'Professor Doug')
    major1: Major = Major(department, 'Computer Science', 'Fun with blinking lights')
    major2: Major = Major(department, 'Computer Engineering', 'Much closer to the silicon')
    student1: Student = Student('Brown', 'David', 'david.brown@gmail.com')
    student2: Student = Student('Brown', 'Mary', 'marydenni.brown@gmail.com')
    student3: Student = Student('Disposable', 'Bandit', 'disposable.bandit@gmail.com')
    enrollment: Enrollment = Enrollment(student1, section1)
    student1.add_major(major1)
    student2.add_major(major1)
    student2.add_major(major2)
    sess.add(department)
    sess.add(course)
    sess.add(section1)
    sess.add(major1)
    sess.add(major2)
    sess.add(student1)
    sess.add(student2)
    sess.add(student3)
    sess.add(enrollment)
    sess.flush()                                # Force SQLAlchemy to update the database, although not commit
```
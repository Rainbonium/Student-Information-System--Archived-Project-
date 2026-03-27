# Student Information System (Archived Project)

## ⚠️ Project Status

**This is an archived academic project and is not currently runnable.**
The original development environment and some supporting files are no longer available.
For functional projects, please see [other repositories in my portfolio.](https://rainbonium.github.io/)

This repository is included for demonstration purposes only.

![Database in PostgreSQL.](Thumbnail.png)

## Overview

This project demonstrates a command-line student information system built using Pythoin and SQLAlchemy ORM. It's purpose was to manage university data such as:

* Departments
* Courses
* Sections
* Students
* Majors
* Enrollments

The system uses a simple menu interface to perform CRUD operations and manage changes to data.

## Tech

Though not currently executable, it demonstrates an understanding of:

* SQLAlchemy
* Python
* Data Relationships (One-to-Many & Many-to-Many)

## Highlights

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

### Example Class
The class structure makes the addition of new class sections to the database easy. Notice the usage of different constraints to ensure data is specific and accurate.

```py
class Section(Base):
        __tablename__ = table_name

        departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', primary_key=True)
        courseNumber: Mapped[int] = mapped_column('course_number', primary_key=True)

        course: Mapped["Course"] = relationship(back_populates="sections")

        sectionNumber: Mapped[int] = mapped_column('section_number', Integer, nullable=False, primary_key=True)
        semester: Mapped[str] = mapped_column('semester', String(10), nullable=False, primary_key=True)
        sectionYear: Mapped[int] = mapped_column('section_year', Integer, nullable=False, primary_key=True)
        building: Mapped[str] = mapped_column('building', String(6), nullable=False)
        room: Mapped[int] = mapped_column('room', Integer, nullable=False)
        schedule: Mapped[str] = mapped_column('schedule', String(6), nullable=False)
        startTime: Mapped[Time] = mapped_column('start_time', Time, nullable=False)
        instructor: Mapped[str] = mapped_column('instructor', String(80), nullable=False)

        students: Mapped[List["Enrollment"]] = relationship(back_populates="section",
                                                              cascade="all, save-update, delete-orphan")

        __table_args__ = (
            UniqueConstraint(
                'section_year', 'semester', 'schedule', 'start_time', 'building', 'room',
                name='sections_uk_01'
            ),
            UniqueConstraint(
                'section_year', 'semester', 'schedule', 'start_time', 'instructor',
                name='sections_uk_02'
            ),
            UniqueConstraint(
                'department_abbreviation', 'course_number', 'semester', 'section_number',
                name='sections_uk_03'
            ),
            CheckConstraint(
                "semester IN('Fall', 'Spring', 'Winter', 'Summer I', 'Summer II')",
                name='sections_semester_check'
            ),
            CheckConstraint(
                "building IN('VEC', 'ECS', 'EN2', 'EN3', 'EN4', 'ET', 'SSPA')",
                name='sections_building_check'
            ),
            CheckConstraint(
                "schedule IN('MW', 'TuTh', 'MWF', 'F', 'S')",
                name='sections_schedule_check'
            ),
            ForeignKeyConstraint([departmentAbbreviation, courseNumber], [Course.departmentAbbreviation, Course.courseNumber])
        )
```
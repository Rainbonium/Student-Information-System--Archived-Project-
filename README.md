# Student Information System (Archived Project)

A Python + SQLAlchemy project focused on relational database design and data integrity.

## ⚠️ Project Status

**This is an archived academic project and is not currently runnable.**
The original development environment and some supporting files are no longer available.
For functional projects, please see [other repositories in my portfolio.](https://rainbonium.github.io/)

This repository is included to showcase database design, ORM usage, and data modeling concepts.

![Database in PostgreSQL.](Thumbnail.png)

## Overview

This project demonstrates a command-line student information system built using Python and SQLAlchemy ORM. It was designed to manage university data such as:

* Departments
* Courses
* Sections
* Students
* Majors
* Enrollments

This project focuses on modeling real-world academic data and enforcing data integrity through both application logic and database constraints.

## Tech

This project demonstrates:

* SQLAlchemy ORM (Object-Relational Mapper)
* Python
* Data Relationships (One-to-Many & Many-to-Many)

## Highlights

### Boilerplate Data
A starting point for testing the database with preset data.

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
The class structure simplifies adding new sections to the database. Notice the usage of different constraints to ensure data is specific and accurate. Uniqueness constraints were used to prohibit duplicates, check constraints to permit only specific values, and foreign key constraints to connect the section to a course. This is only a precaution, since the database itself would also have its own schema to protect against illegal entries.

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

### Operations
These operations allow the user to manipulate data through the console.

```py
# ADD
def add_section(session):
    print("Which course offers this section?")
    course: Course = select_course(sess)
    unique: bool = False
    constraints: list = []
    constraintVals: list = ["department abbreviation, course number, section number, section year & semester",
                            "year, semester, schedule, start time, building & room",
                            "year, semester, schedule, start time & instructor"]
    sectionNumber: int = -1
    semester: str = ''
    sectionYear: int = -1
    building: str = ''
    room: int = -1
    schedule: str = ''
    startTime: time = time(8, 0, 0)
    instructor: str = ''

    while not unique:
        constraints.clear()
        sectionNumber = int(input("Section number--> "))
        semester = input("Section semester--> ")
        sectionYear = int(input("Section year--> "))
        building = input("Section building--> ")
        room = int(input("Section room--> "))
        schedule = input("Section schedule--> ")
        h, m, s = [int(x) for x in input("Section start time (HH MM SS) (EX: 8 0 0)--> ").split()]
        startTime = time(h, m, s)
        instructor = input("Section instructor--> ")

        constraints.append(session.query(Section).filter(Section.departmentAbbreviation == course.departmentAbbreviation,
                                                         Section.courseNumber == course.courseNumber,
                                                         Section.sectionNumber == sectionNumber,
                                                         Section.sectionYear == sectionYear,
                                                         Section.semester == semester).count())

        constraints.append(session.query(Section).filter(Section.sectionYear == sectionYear,
                                                         Section.semester == semester,
                                                         Section.schedule == schedule,
                                                         Section.startTime == startTime,
                                                         Section.building == building,
                                                         Section.room == room).count())

        constraints.append(session.query(Section).filter(Section.sectionYear == sectionYear,
                                                         Section.semester == semester,
                                                         Section.schedule == schedule,
                                                         Section.startTime == startTime,
                                                         Section.instructor == instructor).count())

        unique = True
        for c in range(0, 3):
            if constraints[c] > 0:
                unique = False
                print("We found a section with that " + constraintVals[c] + " in our system, please change one of these.")

        if not unique:
            print("Try again.")

    newSection = Section(course, sectionNumber, semester, sectionYear, building, room, schedule, startTime, instructor)
    session.add(newSection)

# SELECT
def select_section(sess) -> Section:
    found: bool = False
    department_abbreviation: str = ''
    course_number: int = -1
    section_number: int = -1
    section_year: int = -1
    semester: str = ''
    while not found:
        department_abbreviation = input("Department abbreviation--> ")
        course_number = int(input("Course Number--> "))
        section_number = int(input("Section Number--> "))
        section_year = int(input("Section Year--> "))
        semester = input("Semester--> ")
        name_count: int = sess.query(Section).filter(Section.departmentAbbreviation == department_abbreviation,
                                                     Section.courseNumber == course_number,
                                                     Section.sectionNumber == section_number,
                                                     Section.sectionYear == section_year,
                                                     Section.semester == semester).count()
        found = name_count == 1
        if not found:
            print("No section by that info.  Try again.")
    session = sess.query(Section).filter(Section.departmentAbbreviation == department_abbreviation,
                                         Section.courseNumber == course_number,
                                         Section.sectionNumber == section_number,
                                         Section.sectionYear == section_year,
                                         Section.semester == semester).first()
    return session

# LIST
def list_course_sections(sess):
    course = select_course(sess)
    dept_sections: [Course] = course.get_sections()
    print("Sections for course: " + str(course))
    for dept_section in dept_sections:
        print(dept_section)

# DELETE
def delete_section(session):
    print("deleting a section")
    section: Section = select_section(session)
    session.delete(section)
```

## What I Would Improve

If I were to remake this project today, I would:
- Improve input validation and error handling.
- Add unit and integration tests.
- Create a customization file to allow operation on new databases and hardware.
- Provide a web-based interface to simplify operation for other users.
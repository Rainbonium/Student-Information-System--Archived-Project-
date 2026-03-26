from orm_base import Base
from db_connection import engine
from IntrospectionFactory import IntrospectionFactory
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, column_property
from sqlalchemy import Table
from sqlalchemy.types import Time
from Course import Course
from constants import START_OVER, REUSE_NO_INTROSPECTION

from typing import List
from Enrollment import Enrollment


table_name: str = "sections"

introspection_type = IntrospectionFactory().introspection_type
if introspection_type == START_OVER or introspection_type == REUSE_NO_INTROSPECTION:
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

        def __init__(self, course: Course, sectionNumber: int, semester: str, sectionYear: int, building: str, room: int,
                     schedule: str, startTime: Time, instructor: str):
            self.set_course(course)

            self.sectionNumber = sectionNumber
            self.semester = semester
            self.sectionYear = sectionYear
            self.building = building
            self.room = room
            self.schedule = schedule
            self.startTime = startTime
            self.instructor = instructor
#
# elif introspection_type == INTROSPECT_TABLES:
#     class Section(Base):
#         __table__ = Table(table_name, Base.metadata, autoload_with=engine)
#
#         course: Mapped["Course"] = relationship(back_populates="sections")
#
#         departmentAbbreviation: Mapped[str] = column_property(__table__.c.department_abbreviation)
#         courseNumber: Mapped[int] = column_property(__table__.c.course_number)
#         sectionNumber: Mapped[int] = column_property(__table__.c.section_number)
#         sectionYear: Mapped[int] = column_property(__table__.c.section_year)
#         startTime: Mapped[Time] = column_property(__table__.c.start_time)
#
#         def __init__(self, course: Course, sectionNumber: int, semester: str, sectionYear: int, building: str, room: int,
#                      schedule: str, startTime: Time, instructor: str):
#             self.set_course(course)
#
#             self.sectionNumber = sectionNumber
#             self.semester = semester
#             self.sectionYear = sectionYear
#             self.building = building
#             self.room = room
#             self.schedule = schedule
#             self.startTime = startTime
#             self.instructor = instructor

def set_course(self, course: Course):
    self.course = course
    self.courseNumber = course.courseNumber
    self.departmentAbbreviation = course.departmentAbbreviation

def add_student(self, student):
    """Add a new student to the list of students in the major.  We are not adding a
    Student per se, but rather creating an instance of StudentMajor, and adding that
    new instance to our list of "students".  A parallel construct will exist on the
    Student side to manage instances of StudentMajor to keep track of the various
    major(s) that the student has.
    """
    # Make sure that this Major does not already have this Student.
    for next_student in self.students:
        if next_student.student == student:
            return              # This student is already in this major.
    # create the necessary Association Class instance that connects This major to
    # the supplied student.
    enrollment = Enrollment(student, self)
#        student.majors.append(student_major)        # Add this new junction entry to the Student
#        self.students.append(student_major)         # Add this new junction entry to this Major

def remove_enrollment(self, student):
    for enrollment in self.students:
        if enrollment.student == student:
            self.students.remove(enrollment)
            return


def __str__(self):
    return f"Department Abbreviation: {self.departmentAbbreviation}, Course Number: {self.courseNumber}, " \
           f"Section Number: {self.sectionNumber}, Semester: {self.semester}, Section Year: {self.sectionYear}, " \
           f"Building: {self.building}, Room: {self.room}, Schedule: {self.schedule}, " \
           f"Start Time: {self.startTime}, Instructor: {self.instructor}"

setattr(Section, 'set_course', set_course)
setattr(Section, 'add_student', add_student)
setattr(Section, 'remove_enrollment', remove_enrollment)
setattr(Section, '__str__', __str__)
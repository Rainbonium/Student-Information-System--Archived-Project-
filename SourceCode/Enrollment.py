from orm_base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy import UniqueConstraint, ForeignKeyConstraint


class Enrollment(Base):
    __tablename__ = "enrollments"

    section: Mapped["Section"] = relationship(back_populates="students")
    student: Mapped["Student"] = relationship(back_populates="sections")

    sectionNumber: Mapped[int] = mapped_column('section_number', primary_key=True)
    studentID: Mapped[str] = mapped_column('student_id', ForeignKey("students.student_id"), primary_key=True)

    departmentAbbreviation: Mapped[str] = mapped_column('department_abbreviation', primary_key=True)
    courseNumber: Mapped[int] = mapped_column('course_number', primary_key=True)
    sectionYear: Mapped[int] = mapped_column('section_year')
    semester: Mapped[str] = mapped_column('semester', String(10), nullable=False, primary_key=True)

    __table_args__ = (
        UniqueConstraint(
            'department_abbreviation', 'course_number', 'section_number', 'semester', 'student_id',
            name='enrollment_pk'
        ),
        UniqueConstraint(
            'department_abbreviation', 'course_number', 'section_year', 'semester', 'student_id',
            name='enrollment_uk_01'
        ),
        ForeignKeyConstraint([departmentAbbreviation, courseNumber, sectionNumber, semester],
                             ["sections.department_abbreviation", "sections.course_number", "sections.section_number", "sections.semester"]),
    )

    def __init__(self, student, section):
        self.student = student
        self.section = section
        self.studentID = student.studentID
        self.sectionNumber = section.sectionNumber
        self.departmentAbbreviation = section.departmentAbbreviation
        self.courseNumber = section.courseNumber
        self.sectionYear = section.sectionYear
        self.semester = section.semester

    def __str__(self):
        return f"Student Enrollment - student: {self.student} section: {self.section}"

from tests.tests_accounts.syncronzation.entities import CRMLesson
from tests.tests_accounts.syncronzation.entities import CRMTeacher
from tests.tests_accounts.syncronzation.entities import CRMGroup
from tests.tests_accounts.syncronzation.entities import CRMClassrooms
from tests.tests_accounts.syncronzation.entities import CRMCourses
from tests.tests_accounts.syncronzation.entities import CRMContracts
from tests.tests_accounts.syncronzation.entities import CRMDirections
from tests.tests_accounts.syncronzation.entities import CRMSchedule
from tests.tests_accounts.syncronzation.entities import CRMStudents
from tests.tests_accounts.syncronzation.entities import CRMReports

from datetime import date
from datetime import datetime
from datetime import timezone


import pytest
from tests.tests_accounts.syncronzation.conftest import create_entity_in_crm


def get_test_time():
    testtime = datetime.combine(
        date.today(), datetime.min.time(), tzinfo=timezone.utc
    )
    return testtime


def crm_teachers_list():
    teachers_list_of_dicts = [
        {
            "ID": 1,
            "Prepod": "Петров Петр Петрович",
            "Email": "piotr.petrovich@gmail.com",
            "Napravlenie": "Робототехника",
        },
        {
            "ID": 2,
            "Prepod": "Невалидное_имя",
            "Email": "piotr.petrovich@gmail.com",
            "Napravlenie": "Робототехника",
        },
        {
            "ID": 3,
            "Prepod": "Иванов Иван Иванович",
            "Email": "ivan.ivanov@gmail.com",
            "Napravlenie": "Робототехника",
        },
    ]

    return teachers_list_of_dicts


def crm_groups_list():
    testtime = get_test_time()

    crm_groups_list_of_dicts = [
        {
            "ID": 1,
            "GroupName": "study_group1",
            "KursID": 1,
            "PrepodId": 1,
            "Kurs": "study_courses1",
            "Napravlenie": "Робототехника",
            "LearnForm": "learn_form1",
            "StartDate": testtime,
            "FinalDate": testtime,
            "StatusGroup": "status_group1",
            "ClientFakt": 1,
            "Notes2": "notes1",
            "Dist": True,
            "School": "school1",
        },
        {
            "ID": 2,
            "GroupName": "study_group2",
            "KursID": 1,
            "PrepodId": 3,
            "Kurs": "study_courses2",
            "Napravlenie": "Робототехника",
            "LearnForm": "learn_form2",
            "StartDate": testtime,
            "FinalDate": testtime,
            "StatusGroup": "status_group2",
            "ClientFakt": 2,
            "Notes2": "notes2",
            "Dist": True,
            "School": "school2",
        },
        {
            "ID": 3,
            "GroupName": "study_group3",
            "KursID": 1,
            "PrepodId": 3,
            "Kurs": "study_courses3",
            "Napravlenie": "Робототехника",
            "LearnForm": "learn_form3",
            "StartDate": testtime,
            "FinalDate": testtime,
            "StatusGroup": "Выпущена",
            "ClientFakt": 2,
            "Notes2": "notes3",
            "Dist": True,
            "School": "school3",
        },
        {
            "ID": 4,
            "GroupName": "study_group4",
            "KursID": 1,
            "PrepodId": 3,
            "Kurs": "study_courses4",
            "Napravlenie": "Робототехника",
            "LearnForm": "learn_form4",
            "StartDate": testtime,
            "FinalDate": testtime,
            "StatusGroup": "Набирается",
            "ClientFakt": 2,
            "Notes2": "notes4",
            "Dist": True,
            "School": "school4",
        },
        {
            "ID": 5,
            "GroupName": "study_group5",
            "KursID": 1,
            "PrepodId": 3,
            "Kurs": "study_courses5",
            "Napravlenie": "Робототехника",
            "LearnForm": "learn_form5",
            "StartDate": testtime,
            "FinalDate": testtime,
            "StatusGroup": "Обучается",
            "ClientFakt": 2,
            "Notes2": "notes5",
            "Dist": True,
            "School": "school5",
        },
        {
            "ID": 6,
            "GroupName": "study_group6",
            "KursID": 1,
            "PrepodId": 3,
            "Kurs": "study_courses5",
            "Napravlenie": "Робототехника",
            "LearnForm": "learn_form6",
            "StartDate": testtime,
            "FinalDate": testtime,
            "StatusGroup": "",
            "ClientFakt": 2,
            "Notes2": "notes6",
            "Dist": True,
            "School": "school6",
        },
    ]
    return crm_groups_list_of_dicts


def crm_courses_list():
    crm_courses_list_of_dicts = [
        {
            "ID": 1,
            "Kurs": "study_courses1",
            "ProgrammKurs": "course_program1",
            "Napravlenie": "study_field1",
        },
    ]
    return crm_courses_list_of_dicts


def crm_classrooms_list():
    crm_classrooms_list_of_dicts = [
        {
            "ID": 1,
            "Class": "classroom_name1",
            "PrimechaniyHarakteristika": "note_characteristic1",
        },
        {
            "ID": 2,
            "Class": "classroom_name2",
            "PrimechaniyHarakteristika": "note_characteristic2",
        },
    ]
    return crm_classrooms_list_of_dicts


def crm_students_list():
    crm_students_list_of_dict = [
        {
            "ID": 1,
            "Family": "Petrov",
            "Imya": "Ivan",
            "Otch": "Ivanovich",
        },
    ]
    return crm_students_list_of_dict


def crm_contracts_list():
    crm_contracts_list_of_dict = [
        {
            "ID": 1,
            "MainID": 1,
            "KursID": 1,
            "GroupId": 1,
        }
    ]
    return crm_contracts_list_of_dict


def crm_reports_list():
    crm_reports_list_of_dict = [
        {
            "ID": 1,
            "DogovorID": 1,
            "Dopusk": True,
            "Exist": True,
            "Notes": "Notes",
            "Ocenka": 5,
            "MainID": 1,
            "ZanyatiyaID": 1,
            "PrepodId": 1,
            "GroupId": 1,
        },
    ]
    return crm_reports_list_of_dict


def crm_schedule_list():
    testtime = get_test_time()
    crm_schedule_list_of_dict = [
        {
            "ID": 1,
            "Days": "Days",
            "StartTime": testtime,
            "FinalTime": testtime,
            "Notes": "Notes",
            "GroupId": 1,
            "ClassID": 1,
            "Dist": True,
        },
    ]
    return crm_schedule_list_of_dict


def crm_direction_list():
    crm_direction_list_of_dict = [
        {
            "ID": 1,
            "Napravlenie": "Napravlenie",
        },
    ]
    return crm_direction_list_of_dict


def crm_lessons_list():
    testtime = get_test_time()

    crm_lessons_list_of_dicts = [
        {
            "ID": 1,
            "Zanyatiya": "lesson_name1",
            "ClassID": 1,
            "LessonDate": testtime,
            "StartTime": testtime,
            "FinalTime": testtime,
            "PrepodId": 1,
            "ThemeWork": "lesson_topic1",
            "GroupId": 1,
            "Status": "",
            "Notes": "notes",
            "Busy": True,
            "Dist": True,
            "UchGod": "school_year1",
        },
        {
            "ID": 2,
            "Zanyatiya": "lesson_name2",
            "ClassID": 1,
            "LessonDate": testtime,
            "StartTime": testtime,
            "FinalTime": testtime,
            "PrepodId": 1,
            "ThemeWork": "lesson_topic2",
            "GroupId": 1,
            "Status": "",
            "Notes": "notes",
            "Busy": True,
            "Dist": True,
            "UchGod": "school_year2",
        },
        {
            "ID": 3,
            "Zanyatiya": "lesson_name3",
            "ClassID": 1,
            "LessonDate": testtime,
            "StartTime": testtime,
            "FinalTime": testtime,
            "PrepodId": 3,
            "ThemeWork": "lesson_topic3",
            "GroupId": 1,
            "Status": "",
            "Notes": "notes",
            "Busy": True,
            "Dist": True,
            "UchGod": "school_year3",
        },
        {
            "ID": 4,
            "Zanyatiya": "lesson_name4",
            "ClassID": None,
            "LessonDate": testtime,
            "StartTime": testtime,
            "FinalTime": testtime,
            "PrepodId": 1,
            "ThemeWork": "lesson_topic4",
            "GroupId": 1,
            "Status": "Отмена",
            "Notes": "notes",
            "Busy": True,
            "Dist": True,
            "UchGod": "school_year4",
        },
    ]
    return crm_lessons_list_of_dicts


@pytest.fixture()
def crm_students_for_sync_tests(mssql_database_engine, mssql_create_tables):
    students = crm_students_list()
    student_prototypes = [
        CRMStudents.model_validate(student) for student in students
    ]
    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=student_prototypes,
    ) as entity:
        yield entity


@pytest.fixture()
def crm_contracts_for_sync_tests(mssql_database_engine, mssql_create_tables):
    contracts = crm_contracts_list()
    contract_prototypes = [
        CRMContracts.model_validate(contract) for contract in contracts
    ]
    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=contract_prototypes,
    ) as entity:
        yield entity


@pytest.fixture()
def crm_schedule_for_sync_tests(mssql_database_engine, mssql_create_tables):
    schedules = crm_schedule_list()
    schedule_prototypes = [
        CRMSchedule.model_validate(schedule) for schedule in schedules
    ]
    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=schedule_prototypes,
    ) as entity:
        yield entity


@pytest.fixture()
def crm_courses_for_sync_tests(mssql_database_engine, mssql_create_tables):
    courses = crm_courses_list()
    courses_prototypes = [
        CRMCourses.model_validate(course) for course in courses
    ]
    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=courses_prototypes,
    ) as entity:
        yield entity


@pytest.fixture()
def crm_reports_for_sync_tests(mssql_database_engine, mssql_create_tables):
    reports = crm_reports_list()
    courses_prototypes = [
        CRMReports.model_validate(report) for report in reports
    ]
    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=courses_prototypes,
    ) as entity:
        yield entity


@pytest.fixture()
def crm_directions_for_sync_tests(mssql_database_engine, mssql_create_tables):
    directions = crm_direction_list()
    direction_prototypes = [
        CRMDirections.model_validate(direction) for direction in directions
    ]
    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=direction_prototypes,
    ) as entity:
        yield entity


@pytest.fixture()
def crm_classroom_for_sync_tests(mssql_database_engine, mssql_create_tables):
    classrooms = crm_classrooms_list()
    classroom_prototypes = [
        CRMClassrooms.model_validate(classroom) for classroom in classrooms
    ]
    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=classroom_prototypes,
    ) as entity:
        yield entity


@pytest.fixture()
def crm_teacher_for_sync_tests(mssql_database_engine, mssql_create_tables):
    teachers = crm_teachers_list()
    teachers_prototypes = [
        CRMTeacher.model_validate(teacher) for teacher in teachers
    ]
    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=teachers_prototypes,
    ) as entity:
        yield entity


@pytest.fixture()
def crm_groups_for_sync_tests(
    mssql_database_engine, crm_teacher_for_sync_tests
):
    groups = crm_groups_list()

    group_prototypes = [CRMGroup.model_validate(group) for group in groups]

    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=group_prototypes,
    ) as entity:
        yield entity


@pytest.fixture()
def crm_lessons_for_sync_tests(mssql_database_engine, mssql_create_tables):
    lessons = crm_lessons_list()

    lessons_prototypes = [
        CRMLesson.model_validate(lesson) for lesson in lessons
    ]

    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=lessons_prototypes,
    ) as entity:
        yield entity

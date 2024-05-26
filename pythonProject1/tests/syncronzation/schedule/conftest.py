from ..entities import Entity
from ..entities import CRMLesson
from ..entities import CRMTeacher
from ..entities import CRMGroup
from ..entities import CRMClassrooms


from datetime import date
from datetime import datetime
from datetime import timezone

from testlib.utils import get_desire_date

import pytest
from ..conftest import create_entity_in_crm


def groups_for_schedule_test():
    testtime = datetime.combine(
        date.today(), datetime.min.time(), tzinfo=timezone.utc
    )

    groups = [
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
            "PrepodId": 1,
            "Kurs": "study_courses2",
            "Napravlenie": "Робототехника",
            "LearnForm": "learn_form2",
            "StartDate": testtime,
            "FinalDate": testtime,
            "StatusGroup": "Не состоялась",
            "ClientFakt": 2,
            "Notes2": "notes2",
            "Dist": True,
            "School": "school2",
        },
    ]
    return groups


def lessons_for_schedule_test():
    out_of_range_week_date = get_desire_date(-9)
    previous_week_date = get_desire_date(-7)
    current_week_date = get_desire_date()
    next_week_date = get_desire_date(7)

    lessons = [
        {
            "ID": 1,
            "Zanyatiya": "lesson_name1",
            "ClassID": 1,
            "LessonDate": previous_week_date,
            "StartTime": previous_week_date,
            "FinalTime": previous_week_date,
            "PrepodId": 1,
            "ThemeWork": "lesson_topic1",
            "GroupId": 1,
            "Status": "status1",
            "Notes": "notes",
            "Busy": True,
            "Dist": True,
            "UchGod": "school_year1",
        },
        {
            "ID": 2,
            "Zanyatiya": "lesson_name2",
            "ClassID": 1,
            "LessonDate": current_week_date,
            "StartTime": current_week_date,
            "FinalTime": current_week_date,
            "PrepodId": 1,
            "ThemeWork": "lesson_topic2",
            "GroupId": 1,
            "Status": "status2",
            "Notes": "notes",
            "Busy": True,
            "Dist": True,
            "UchGod": "school_year2",
        },
        {
            "ID": 3,
            "Zanyatiya": "lesson_name3",
            "ClassID": 1,
            "LessonDate": next_week_date,
            "StartTime": next_week_date,
            "FinalTime": next_week_date,
            "PrepodId": 1,
            "ThemeWork": "lesson_topic3",
            "GroupId": 1,
            "Status": "status3",
            "Notes": "notes",
            "Busy": True,
            "Dist": True,
            "UchGod": "school_year3",
        },
        {
            "ID": 4,
            "Zanyatiya": "lesson_name4",
            "ClassID": 1,
            "LessonDate": out_of_range_week_date,
            "StartTime": out_of_range_week_date,
            "FinalTime": out_of_range_week_date,
            "PrepodId": 1,
            "ThemeWork": "lesson_topic4",
            "GroupId": 1,
            "Status": "status4",
            "Notes": "notes",
            "Busy": True,
            "Dist": True,
            "UchGod": "school_year4",
        },
        {
            "ID": 5,
            "Zanyatiya": "lesson_name5",
            "ClassID": 1,
            "LessonDate": current_week_date,
            "StartTime": current_week_date,
            "FinalTime": current_week_date,
            "PrepodId": 1,
            "ThemeWork": "lesson_topic5",
            "GroupId": 2,
            "Status": "status5",
            "Notes": "notes",
            "Busy": True,
            "Dist": True,
            "UchGod": "school_year5",
        },
    ]

    return lessons


@pytest.fixture()
def crm_teacher_for_schedule_tests(mssql_database_engine, mssql_create_tables):
    prototype = CRMTeacher(
        ID=1,
        Prepod="Петров Петр Петрович",
        Email="piotr.petrovich@gmail.com",
        Napravlenie="Робототехника",
    )

    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_classroom_for_schrdule_tests(
    mssql_database_engine, mssql_create_tables
):
    prototype = CRMClassrooms(
        ID=1,
        Class="classroom_name1",
        PrimechaniyHarakteristika="note_characteristic1",
    )
    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_groups_for_schedule_tests(
    mssql_database_engine,
    crm_teacher_for_schedule_tests,
):
    groups = groups_for_schedule_test()

    group_prototypes = [CRMGroup.model_validate(group) for group in groups]

    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=group_prototypes,
    ) as entity:
        yield entity


@pytest.fixture()
def crm_lessons_for_schedule_tests(mssql_database_engine, mssql_create_tables):
    lessons = lessons_for_schedule_test()

    lessons_prototypes = [
        CRMLesson.model_validate(lesson) for lesson in lessons
    ]

    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine,
        prototypes=lessons_prototypes,
    ) as entity:
        yield entity

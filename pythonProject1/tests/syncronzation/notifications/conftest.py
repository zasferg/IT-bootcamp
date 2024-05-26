from ..entities import CRMLesson
from ..entities import CRMTeacher
from ..entities import CRMGroup
from ..entities import CRMClassrooms

from datetime import date
from datetime import datetime
from datetime import timezone

import pytest

from ..conftest import create_entity_in_crm


def set_testtime():
    return datetime.combine(
        date.today(), datetime.min.time(), tzinfo=timezone.utc
    )


@pytest.fixture()
def crm_group_without_teacher(
    mssql_database_engine, mssql_create_tables, crm_teacher_old
):
    testtime = set_testtime()
    prototype = CRMGroup(
        ID=1,
        GroupName="study_group1",
        KursID=1,
        PrepodId=None,
        Kurs="study_courses1",
        Napravlenie="Робототехника",
        LearnForm="learn_form1",
        StartDate=testtime,
        FinalDate=testtime,
        StatusGroup="Обучается",
        ClientFakt=2,
        Notes2="notes1",
        Dist=True,
        School="school1",
    )

    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_group_old(mssql_database_engine, mssql_create_tables, crm_teacher_old):
    testtime = set_testtime()
    prototype = CRMGroup(
        ID=1,
        GroupName="study_group1",
        KursID=1,
        PrepodId=1,
        Kurs="study_courses1",
        Napravlenie="Робототехника",
        LearnForm="learn_form1",
        StartDate=testtime,
        FinalDate=testtime,
        StatusGroup="Обучается",
        ClientFakt=2,
        Notes2="notes1",
        Dist=True,
        School="school1",
    )

    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_group_new(mssql_database_engine, mssql_create_tables, crm_teacher_new):
    testtime = set_testtime()
    prototype = CRMGroup(
        ID=2,
        GroupName="study_group3",
        KursID=1,
        PrepodId=2,
        Kurs="study_courses2",
        Napravlenie="Робототехника",
        LearnForm="learn_form2",
        StartDate=testtime,
        FinalDate=testtime,
        StatusGroup="Обучается",
        ClientFakt=3,
        Notes2="notes2",
        Dist=True,
        School="school2",
    )

    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_teacher_old(mssql_database_engine, mssql_create_tables):
    prototype = CRMTeacher(
        ID=1,
        Prepod="Иванов Иван Иванович",
        Email="ivanov.teacher@gmail.com",
        Napravlenie="direction1",
    )

    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_teacher_new(mssql_database_engine, mssql_create_tables):
    prototype = CRMTeacher(
        ID=2,
        Prepod="Петров Петр Петрович",
        Email="petrov.taecher@gmail.conm",
        Napravlenie="direction2",
    )
    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_old_classroom(mssql_database_engine, mssql_create_tables):
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
def crm_new_classroom(mssql_database_engine, mssql_create_tables):
    prototype = CRMClassrooms(
        ID=2,
        Class="classroom_name2",
        PrimechaniyHarakteristika="note_characteristic2",
    )

    with create_entity_in_crm(
        mssql_database_engine=mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_lesson(
    mssql_database_engine, crm_teacher_old, crm_group_old, crm_old_classroom
):
    testtime = datetime.combine(
        date.today(), datetime.min.time(), tzinfo=timezone.utc
    )
    prototype = CRMLesson(
        ID=1,
        Zanyatiya="lesson",
        ClassID=crm_old_classroom.ID,
        LessonDate=testtime,
        StartTime=testtime,
        FinalTime=testtime,
        PrepodId=crm_teacher_old.ID,
        ThemeWork="theme",
        GroupId=crm_group_old.ID,
        Status="",
        Notes="222",
        Busy=True,
        Dist=True,
        UchGod="school_year",
    )

    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity

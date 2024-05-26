from ..entities import Entity
from ..entities import CRMLesson
from ..entities import CRMTeacher
from ..entities import CRMGroup

from datetime import datetime
from datetime import date
from datetime import timezone

import pytest

from ..conftest import create_entity_in_crm


@pytest.fixture()
def crm_teacher_old(mssql_database_engine, mssql_create_tables):
    prototype = CRMTeacher(
        ID=1,
        Prepod="Старый Учитель Отчество",
        Email="old.teacher@gmail.com",
        Napravlenie="super_direction",
    )

    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_teacher_new(mssql_database_engine, mssql_create_tables):
    prototype = CRMTeacher(
        ID=2,
        Prepod="Новый Учитель Отчество",
        Email="new.taecher@gmail.conm",
        Napravlenie="new_direction",
    )
    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_group_old_teacher(
    mssql_database_engine, mssql_create_tables, crm_teacher_old
):
    testtime = datetime.combine(
        date.today(), datetime.min.time(), tzinfo=timezone.utc
    )
    prototype = CRMGroup(
        ID=1,
        GroupName="old_group",
        KursID=1,
        PrepodId=crm_teacher_old.ID,
        Kurs="aaaaa",
        Napravlenie="aaaaa",
        LearnForm="aaaaa",
        StartDate=testtime,
        FinalDate=testtime,
        StatusGroup="",
        ClientFakt=1,
        Notes2="aaa",
        Dist=True,
        School="aaa",
    )
    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_group_new_teacher(
    mssql_database_engine, mssql_create_tables, crm_teacher_new
):
    testtime = datetime.combine(
        date.today(), datetime.min.time(), tzinfo=timezone.utc
    )
    prototype = CRMGroup(
        ID=2,
        GroupName="new_group",
        KursID=1,
        PrepodId=crm_teacher_new.ID,
        Kurs="new_course",
        Napravlenie="new_direction",
        LearnForm="aaaaa",
        StartDate=testtime,
        FinalDate=testtime,
        StatusGroup="",
        ClientFakt=1,
        Notes2="notes2",
        Dist=True,
        School="school2",
    )
    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_lesson_with_old_teacher(
    mssql_database_engine,
    crm_teacher_old,
    crm_group_old_teacher,
):
    testtime = datetime.combine(
        date.today(), datetime.min.time(), tzinfo=timezone.utc
    )
    prototype = CRMLesson(
        ID=1,
        Zanyatiya="some_lesson",
        ClassID="1",
        LessonDate=testtime,
        StartTime=testtime,
        FinalTime=testtime,
        PrepodId=crm_teacher_old.ID,
        ThemeWork="222",
        GroupId=crm_group_old_teacher.ID,
        Status="",
        Notes="222",
        Busy=True,
        Dist=True,
        UchGod="school_year_111",
    )

    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_lesson_with_new_teacher(
    mssql_database_engine,
    crm_teacher_new,
    crm_group_old_teacher,
):
    testtime = datetime.combine(
        date.today(), datetime.min.time(), tzinfo=timezone.utc
    )
    prototype = CRMLesson(
        ID=1,
        Zanyatiya="some_lesson",
        ClassID="1",
        LessonDate=testtime,
        StartTime=testtime,
        FinalTime=testtime,
        PrepodId=crm_teacher_new.ID,
        ThemeWork="222",
        GroupId=crm_group_old_teacher.ID,
        Status="",
        Notes="222",
        Busy=True,
        Dist=True,
        UchGod="school_year_111",
    )

    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity

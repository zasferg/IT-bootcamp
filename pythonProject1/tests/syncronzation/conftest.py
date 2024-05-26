from .entities import Entity
from .entities import CRMLesson
from .entities import CRMTeacher
from .entities import CRMGroup
from .entities import CRMClassrooms
from .entities import CRMDirections
from .entities import CRMSchedule
from .entities import CRMContracts
from .entities import CRMCourses
from .entities import CRMStudents
from .entities import CRMReports


from testlib.utils import tables
from testlib.utils import synchronize

from contextlib import contextmanager

from typing import TypeVar, Mapping, Any
from typing import Mapping
from typing import Any

from devtools import debug
from datetime import datetime
from datetime import date
from datetime import timezone

import sqlalchemy as sa
from sqlalchemy import Engine
import pytest
import attrs


T = TypeVar("T", bound=Entity)


@contextmanager
def create_entity_in_crm(mssql_database_engine: Engine, prototypes):
    entity_table_map: Mapping[T, sa.Table] = {
        CRMReports: tables.reports_table,
        CRMCourses: tables.courses_table,
        CRMGroup: tables.groups_table,
        CRMTeacher: tables.teachers_table,
        CRMLesson: tables.lessons_table,
        CRMClassrooms: tables.classrooms_table,
        CRMContracts: tables.contracts_table,
        CRMStudents: tables.students_table,
        CRMDirections: tables.directions_table,
        CRMSchedule: tables.schedules_table,
    }

    # Если prototypes не является списком, преобразуем его в список
    if not isinstance(prototypes, list):
        prototypes = [prototypes]

    for prototype in prototypes:
        table = entity_table_map[type(prototype)]

        values = prototype.model_dump(exclude_unset=True)

        where_values = [
            getattr(table.c, field) == value for field, value in values.items()
        ]
        sql_select = sa.select(table).where(*where_values).limit(1)

        sql_insert = sa.insert(table).values(**values)

        with mssql_database_engine.begin() as conn:
            conn.execute(sql_insert)
            cursor = conn.execute(sql_select)
            row = cursor.one()
            entity = prototype.model_validate(row)

        # It is not Pytest code,
        # hence we need explicit try-finally around yield

    yield entity

    sql_delete = sa.delete(table).where(table.c.ID == entity.ID)

    with mssql_database_engine.begin() as conn:
        conn.execute(sql_delete)




@pytest.fixture()
def crm_classroom_generic(mssql_database_engine, mssql_create_tables):
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
def crm_group_generic(
    mssql_database_engine, mssql_create_tables, crm_teacher_ganeric
):
    testtime = datetime.combine(
        date.today(), datetime.min.time(), tzinfo=timezone.utc
    )
    prototype = CRMGroup(
        ID=1,
        GroupName="new_group",
        KursID=1,
        PrepodId=crm_teacher_ganeric.ID,
        Kurs="course_common",
        Napravlenie="dir_common",
        LearnForm="form_common",
        StartDate=testtime,
        FinalDate=testtime,
        StatusGroup="Обучается",
        ClientFakt=1,
        Notes2="notes_common",
        Dist=True,
        School="school_common",
    )
    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_teacher_ganeric(mssql_database_engine, mssql_create_tables):
    prototype = CRMTeacher(
        ID=1,
        Prepod="Общий Учитель Отчество",
        Email="common.taecher@gmail.conm",
        Napravlenie="comm_direction",
    )
    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity


@pytest.fixture()
def crm_lesson_generic(
    mssql_database_engine,
    crm_teacher_ganeric,
    crm_group_generic,
    crm_classroom_generic,
):
    testtime = datetime.combine(
        date.today(), datetime.min.time(), tzinfo=timezone.utc
    )
    prototype = CRMLesson(
        ID=1,
        Zanyatiya="common_lesson",
        ClassID=crm_classroom_generic.ID,
        LessonDate=testtime,
        StartTime=testtime,
        FinalTime=testtime,
        PrepodId=crm_teacher_ganeric.ID,
        ThemeWork="common_theme",
        GroupId=crm_group_generic.ID,
        Status="",
        Notes="222",
        Busy=True,
        Dist=True,
        UchGod="school_year_common",
    )

    with create_entity_in_crm(
        mssql_database_engine, prototypes=prototype
    ) as entity:
        yield entity

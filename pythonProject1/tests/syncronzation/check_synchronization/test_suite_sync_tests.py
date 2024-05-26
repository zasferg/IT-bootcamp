import os
from datetime import datetime
from time import sleep

import requests
from sqlalchemy import Engine
from sqlalchemy import update

from testlib import tables
from .conftest import get_test_time

host = os.getenv("HOST_FOR_TESTS", "http://localhost:8000")
BLOCK_SYNC_TIME = int(os.getenv("TEMPORARY_BLOCKED_TIME_SYNCHRONISATION", 5))


def check_sync_result(table_data, sync_data):
    msql_data = table_data[0][1:]
    postgre_data = list(sync_data.values())[1:]
    for i in range(len(msql_data)):
        if isinstance(msql_data[i], datetime):
            assert msql_data[i].isoformat() + "Z" == postgre_data[i]
        else:
            assert msql_data[i] == postgre_data[i]


def get_by_id(object_id, objects):
    searching_object = list(
        filter(lambda object_in: object_in["id_crm"] == object_id, objects)
    )[0]
    return searching_object


def test_data_synchronization(
    postgre_fixture,
    mssql_database_engine: Engine,
    superuser_credentials,
    crm_classroom_for_sync_tests,
    crm_courses_for_sync_tests,
    crm_contracts_for_sync_tests,
    crm_directions_for_sync_tests,
    crm_students_for_sync_tests,
    crm_teacher_for_sync_tests,
    crm_groups_for_sync_tests,
    crm_lessons_for_sync_tests,
    crm_schedule_for_sync_tests,
    crm_reports_for_sync_tests,
) -> None:
    # SET NECCESSARY DATA
    synchronization_url = f"{host}/api/refresh/"

    all_users_url = f"{host}/auth/users/"
    all_lessons_url = f"{host}/api/qa/zanyatia"
    all_classes_url = f"{host}/api/qa/classes"
    all_groups_url = f"{host}/api/qa/groups"
    all_kurses_url = f"{host}/api/qa/kurses"
    all_students_url = f"{host}/api/qa/students"
    all_contracts_url = f"{host}/api/qa/contracts"
    all_reports_url = f"{host}/api/qa/report-cards"
    all_schedules_url = f"{host}/api/qa/schedules"
    all_directions_url = f"{host}/api/qa/directions"

    access_token = superuser_credentials["superuser_token"]
    headers = {"Authorization": f"Token {access_token}"}

    testtime = get_test_time().isoformat().replace("+00:00", "Z")
    # GET DATA FROM CRM AND CHECK IF EXISTS
    with mssql_database_engine.connect() as connection:
        teachers = connection.execute(
            tables.teachers_table.select()
        ).fetchall()
        groups = connection.execute(tables.groups_table.select()).fetchall()
        courses = connection.execute(tables.courses_table.select()).fetchall()
        lessons = connection.execute(tables.lessons_table.select()).fetchall()
        classrooms = connection.execute(
            tables.classrooms_table.select()
        ).fetchall()
        students = connection.execute(
            tables.students_table.select()
        ).fetchall()
        contracts = connection.execute(
            tables.contracts_table.select()
        ).fetchall()
        reports = connection.execute(tables.reports_table.select()).fetchall()
        schedules = connection.execute(
            tables.schedules_table.select()
        ).fetchall()
        directions = connection.execute(
            tables.directions_table.select()
        ).fetchall()

    assert len(teachers) == 3
    assert len(groups) == 6
    assert len(courses) == 1
    assert len(lessons) == 4
    assert len(classrooms) == 2
    assert len(students) == 1
    assert len(contracts) == 1
    assert len(reports) == 1
    assert len(schedules) == 1
    assert len(directions) == 1

    # CHECK FIRST SYNCHRONIZATION
    response = requests.get(synchronization_url, headers=headers)
    assert response.status_code == 200

    valid_teacher = teachers[0]
    group = groups[0]

    synced_users = requests.get(all_users_url, headers=headers).json()[
        "results"
    ]
    synced_user = get_by_id(valid_teacher.ID, synced_users)

    assert synced_user["first_name"] == "Петр"
    assert synced_user["last_name"] == "Петров"
    assert synced_user["middle_name"] == "Петрович"
    assert synced_user["email"] == "piotr.petrovich@gmail.com"
    assert synced_user["study_groups"] == str(["study_group1"])
    assert synced_user["study_courses"] == str(["study_courses1"])

    synced_courses: dict = requests.get(
        all_kurses_url, headers=headers
    ).json()[0]
    synced_classrooms: dict = requests.get(
        all_classes_url, headers=headers
    ).json()[0]
    synced_lessons: dict = requests.get(
        all_lessons_url, headers=headers
    ).json()[0]
    synced_students: dict = requests.get(
        all_students_url, headers=headers
    ).json()[0]
    synced_contracts: dict = requests.get(
        all_contracts_url, headers=headers
    ).json()[0]
    synced_reports: dict = requests.get(
        all_reports_url, headers=headers
    ).json()[0]
    synced_schedules: dict = requests.get(
        all_schedules_url, headers=headers
    ).json()[0]
    synced_directions: dict = requests.get(
        all_directions_url, headers=headers
    ).json()[0]

    check_sync_result(courses, synced_courses)
    check_sync_result(lessons, synced_lessons)
    check_sync_result(classrooms, synced_classrooms)
    check_sync_result(students, synced_students)
    check_sync_result(contracts, synced_contracts)
    check_sync_result(reports, synced_reports)
    check_sync_result(schedules, synced_schedules)
    check_sync_result(directions, synced_directions)

    # UPDATE TEACHER AND HIS GROUPS
    with mssql_database_engine.connect() as connection:
        update_query = (
            update(tables.teachers_table)
            .where(tables.teachers_table.c.ID == valid_teacher.ID)
            .values(Prepod="Другой Петр Петрович")
        )
        connection.execute(update_query)
        connection.commit()
        valid_teacher = connection.execute(
            tables.teachers_table.select().where(
                tables.teachers_table.c.ID == 1
            )
        ).one()

        update_query = (
            update(tables.groups_table)
            .where(tables.groups_table.c.ID == group.ID)
            .values(
                GroupName="another_study_group1",
                StatusGroup="NEW_STATUS!!!!!!",
            )
        )
        connection.execute(update_query)
        connection.commit()
        group = connection.execute(
            tables.groups_table.select().where(tables.groups_table.c.ID == 1)
        ).one()

    sleep(BLOCK_SYNC_TIME)
    response = requests.get(synchronization_url, headers=headers)

    assert response.status_code == 200

    # CHECK UPDATED TECHER
    synced_users = requests.get(all_users_url, headers=headers).json()[
        "results"
    ]
    synced_user = get_by_id(valid_teacher.ID, synced_users)

    assert synced_user["first_name"] == "Петр"
    assert synced_user["last_name"] == "Другой"
    assert synced_user["middle_name"] == "Петрович"
    assert synced_user["email"] == "piotr.petrovich@gmail.com"
    assert synced_user["study_groups"] == str(["another_study_group1"])
    assert synced_user["study_courses"] == str(["study_courses1"])

    # CHECK UPDATED GROUPS
    synced_groups = requests.get(all_groups_url, headers=headers).json()
    synced_group = get_by_id(group.ID, synced_groups)

    assert synced_group["study_groups"] == "another_study_group1"
    assert synced_group["course_id"] == 1
    assert synced_group["teacher_id"] == 1
    assert synced_group["direction"] == "Робототехника"
    assert synced_group["learn_form"] == "learn_form1"
    assert synced_group["start_date"] == testtime
    assert synced_group["final_date"] == testtime
    assert synced_group["status_group"] == "NEW_STATUS!!!!!!"
    assert synced_group["listeners_fact"] == 1
    assert synced_group["notes"] == "notes1"
    assert synced_group["remote"] == True
    assert synced_group["school"] == "school1"


def test_blocking_sync_when_pressed_frequently(
    postgre_fixture, mssql_create_tables, superuser_credentials
) -> None:
    """
    Try to run syncronization before more than once at the specified time.
    """
    synchronization_url = f"{host}/api/refresh/"
    access_token = superuser_credentials["superuser_token"]
    headers = {"Authorization": f"Token {access_token}"}

    sleep(BLOCK_SYNC_TIME)
    response_normal = requests.get(synchronization_url, headers=headers)

    assert response_normal.status_code == 200

    response_too_frequent = requests.get(synchronization_url, headers=headers)
    assert response_too_frequent.status_code == 412
    assert response_too_frequent.json()["detail"].startswith(
        "The synchronization was blocked for"
    )

    sleep(BLOCK_SYNC_TIME)
    response_after_waiting = requests.get(synchronization_url, headers=headers)

    assert response_after_waiting.status_code == 200

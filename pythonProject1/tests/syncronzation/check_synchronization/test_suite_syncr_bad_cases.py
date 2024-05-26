from sqlalchemy import delete
from testlib import tables
from testlib.utils import synchronize, get_local_lessons
from testlib.client.api_requests import (
    get_local_groups,
    get_info_about_all_users,
)

LESSON_TO_DELETE_ID = 1
GROUP_TO_DELETE_ID = 1
TEACHER_TO_DELETE_ID = 1


def test_journal_group_not_exist_in_crm(
    postgre_fixture,
    mssql_database_engine,
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
):
    synchronize(superuser_credentials)

    groups_before_group_deleting = get_local_groups(superuser_credentials)
    lessons_before_group_deleting = get_local_lessons(superuser_credentials)
    number_of_groups_before_deleting = len(groups_before_group_deleting)
    number_of_lessons_before_deleting = len(lessons_before_group_deleting)

    assert number_of_groups_before_deleting == 6
    assert number_of_lessons_before_deleting == 5

    with mssql_database_engine.begin() as connection:
        connection.execute(
            delete(tables.groups_table).where(
                tables.groups_table.c.ID == GROUP_TO_DELETE_ID
            )
        )
    synchronize_response = synchronize(superuser_credentials)

    groups_after_group_deleting = get_local_groups(superuser_credentials)
    lessons_after_group_deleting = get_local_lessons(superuser_credentials)

    number_of_groups_after_deleting = len(groups_after_group_deleting)
    number_of_lessons_after_deleting = len(lessons_after_group_deleting)

    assert synchronize_response.status_code == 200
    assert number_of_groups_after_deleting == 5
    assert (
        number_of_lessons_before_deleting == number_of_lessons_after_deleting
    )


def test_journal_teacher_not_exist_in_crm(
    postgre_fixture,
    mssql_database_engine,
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
):
    synchronize(superuser_credentials)

    teachers_before_teacher_deleting = get_info_about_all_users(
        superuser_credentials
    ).json()
    lessons_before_teacher_deleting = get_local_lessons(superuser_credentials)
    number_of_teachers_before_deleting = len(
        teachers_before_teacher_deleting["results"]
    )
    number_of_lessons_before_deleting = len(lessons_before_teacher_deleting)

    assert number_of_teachers_before_deleting == 3
    assert number_of_lessons_before_deleting == 5

    with mssql_database_engine.begin() as connection:
        connection.execute(
            delete(tables.teachers_table).where(
                tables.teachers_table.c.ID == TEACHER_TO_DELETE_ID
            )
        )

    synchronize_response = synchronize(superuser_credentials)

    teachers_after_teacher_deleting = get_info_about_all_users(
        superuser_credentials
    ).json()

    lessons_after_teacher_deleting = get_local_lessons(superuser_credentials)
    number_of_teachers_after_deleting = len(
        teachers_after_teacher_deleting["results"]
    )
    number_of_lessons_after_deleting = len(lessons_after_teacher_deleting)

    assert synchronize_response.status_code == 200
    assert number_of_teachers_after_deleting == 2
    assert (
        number_of_lessons_before_deleting == number_of_lessons_after_deleting
    )


def test_journal_lesson_not_exist_in_crm(
    postgre_fixture,
    mssql_database_engine,
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
):
    synchronize(superuser_credentials)

    with mssql_database_engine.begin() as connection:
        connection.execute(
            delete(tables.lessons_table).where(
                tables.lessons_table.c.ID == LESSON_TO_DELETE_ID
            )
        )

    lessons_before_lesson_deleting = get_local_lessons(superuser_credentials)
    number_of_lessons_before_deleting = len(lessons_before_lesson_deleting)

    assert number_of_lessons_before_deleting == 5

    synchronize_response = synchronize(superuser_credentials)

    assert synchronize_response.status_code == 200

    lessons_before_lesson_deleting = get_local_lessons(superuser_credentials)
    number_of_lessons_after_deleting = len(lessons_before_lesson_deleting)

    assert number_of_lessons_after_deleting == 4

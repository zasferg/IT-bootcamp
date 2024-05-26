from datetime import datetime
from datetime import timedelta
from datetime import timezone


import pendulum


from testlib.client.api_requests import get_months_schedule
from testlib.client.api_requests import get_weeks_schedule


from testlib.utils import get_teacher
from testlib.utils import get_teacher_token


from devtools import debug
from testlib.utils import get_desire_date
from testlib.utils import get_remote_lessons
from testlib.utils import get_local_lessons
from testlib.utils import synchronize


def test_get_shedule_with_current_week(
    crm_classroom_for_schrdule_tests,
    crm_teacher_for_schedule_tests,
    crm_groups_for_schedule_tests,
    crm_lessons_for_schedule_tests,
    postgre_fixture,
    superuser_credentials,
):
    """
    Get teacher's schedule on current week.
    Check if it contains 1 lesson with correct date.
    """

    synchronize(superuser_credentials)

    lesson_date = int(datetime.now().timestamp()) + 1
    current_week_date = get_desire_date().strftime("%d.%m.%Y")
    current_week_time = get_desire_date().strftime("%H:%M")

    teacher = get_teacher(
        superuser_credentials, id_crm=crm_teacher_for_schedule_tests.ID
    )
    teacher_token = get_teacher_token(superuser_credentials, teacher)

    lessons_weeks_chedule = get_weeks_schedule(teacher_token, lesson_date)

    assert lessons_weeks_chedule.status_code == 200
    assert len(lessons_weeks_chedule.json()) == 1

    lesson = lessons_weeks_chedule.json()[0]

    assert lesson["teacher_id"] == teacher["id_crm"]
    assert lesson["lesson_name"] == "lesson_name2"
    assert lesson["classroom_name"] == "classroom_name1"
    assert lesson["classroom_note"] == "note_characteristic1"
    assert lesson["group_name"] == "study_group1"
    assert lesson["group_status"] == "status_group1"
    assert lesson["lesson_date"] == current_week_date
    assert lesson["start_time"] == current_week_time
    assert lesson["final_time"] == current_week_time
    assert lesson["status"] == "status2"
    assert lesson["remote"] == True
    assert lesson["lesson_type"] == "По расписанию"

    lessons_without_date = get_weeks_schedule(teacher_token)

    assert lessons_without_date.status_code == 200
    assert len(lessons_without_date.json()) == 1

    rs_data_without_date = lessons_weeks_chedule.json()[0]

    assert rs_data_without_date == lesson


def test_get_shedule_with_previous_week(
    crm_classroom_for_schrdule_tests,
    crm_teacher_for_schedule_tests,
    crm_groups_for_schedule_tests,
    crm_lessons_for_schedule_tests,
    postgre_fixture,
    superuser_credentials,
):
    """
    Get teacher's schedule on previous week.
    Check if it contains lesson with correct date.
    """
    synchronize(superuser_credentials)

    lesson_date = int((datetime.now() - timedelta(days=7)).timestamp()) + 1
    previous_week_date = get_desire_date(-7).strftime("%d.%m.%Y")
    previous_week_time = get_desire_date(-7).strftime("%H:%M")

    teacher = get_teacher(
        superuser_credentials, id_crm=crm_teacher_for_schedule_tests.ID
    )
    teacher_token = get_teacher_token(superuser_credentials, teacher)

    lessons_previous_week = get_weeks_schedule(teacher_token, lesson_date)

    assert lessons_previous_week.status_code == 200
    assert len(lessons_previous_week.json()) == 1

    lesson = lessons_previous_week.json()[0]

    assert lesson["teacher_id"] == teacher["id_crm"]
    assert lesson["lesson_name"] == "lesson_name1"
    assert lesson["classroom_name"] == "classroom_name1"
    assert lesson["classroom_note"] == "note_characteristic1"
    assert lesson["group_name"] == "study_group1"
    assert lesson["group_status"] == "status_group1"
    assert lesson["lesson_date"] == previous_week_date
    assert lesson["start_time"] == previous_week_time
    assert lesson["final_time"] == previous_week_time
    assert lesson["status"] == "status1"
    assert lesson["remote"] == True
    assert lesson["lesson_type"] == "По расписанию"


def test_get_shedule_with_next_week(
    postgre_fixture,
    crm_classroom_for_schrdule_tests,
    crm_teacher_for_schedule_tests,
    crm_groups_for_schedule_tests,
    crm_lessons_for_schedule_tests,
    superuser_credentials,
):
    """
    Get teacher's schedule on next week.
    Check if it contains lesson with correct date.
    """
    synchronize(superuser_credentials)

    lesson_date = int((datetime.now() + timedelta(days=7)).timestamp()) + 1
    next_week_date = get_desire_date(7).strftime("%d.%m.%Y")
    next_week_time = get_desire_date(7).strftime("%H:%M")

    teacher = get_teacher(superuser_credentials)
    teacher_token = get_teacher_token(superuser_credentials, teacher)

    lessons_next_week = get_weeks_schedule(teacher_token, lesson_date)

    assert lessons_next_week.status_code == 200
    assert len(lessons_next_week.json()) == 1

    lesson = lessons_next_week.json()[0]

    assert lesson["teacher_id"] == teacher["id_crm"]
    assert lesson["lesson_name"] == "lesson_name3"
    assert lesson["classroom_name"] == "classroom_name1"
    assert lesson["classroom_note"] == "note_characteristic1"
    assert lesson["group_name"] == "study_group1"
    assert lesson["group_status"] == "status_group1"
    assert lesson["lesson_date"] == next_week_date
    assert lesson["start_time"] == next_week_time
    assert lesson["final_time"] == next_week_time
    assert lesson["status"] == "status3"
    assert lesson["remote"] == True
    assert lesson["lesson_type"] == "По расписанию"


def test_get_shedule_current_month(
    postgre_fixture,
    crm_classroom_for_schrdule_tests,
    crm_teacher_for_schedule_tests,
    crm_groups_for_schedule_tests,
    crm_lessons_for_schedule_tests,
    superuser_credentials,
):
    """
    Get teacher's schedule on current month.
    """

    synchronize(superuser_credentials)

    today = pendulum.now(tz=timezone.utc)
    lesson_date = today.int_timestamp
    today_day = today.day
    days_except_last_7 = today.days_in_month - 7

    teacher = get_teacher(
        superuser_credentials, id_crm=crm_teacher_for_schedule_tests.ID
    )
    teacher_token = get_teacher_token(superuser_credentials, teacher)

    lessons_current_month = get_months_schedule(teacher_token, lesson_date)
    local_lessons = lessons_current_month.json()
    lessons = [lesson["lesson_name"] for lesson in local_lessons]

    if today_day <= 7:
        assert len(local_lessons) == 2
        assert "lesson_name2" in lessons
        assert "lesson_name3" in lessons
    elif 7 < today_day <= days_except_last_7:
        assert len(local_lessons) == 3
        assert "lesson_name1" in lessons
        assert "lesson_name2" in lessons
        assert "lesson_name3" in lessons
    elif today_day > days_except_last_7:
        assert len(local_lessons) == 2
        assert "lesson_name1" in lessons
        assert "lesson_name2" in lessons


def test_get_only_necassery_lessons(
    superuser_credentials,
    mssql_database_engine,
    crm_classroom_for_schrdule_tests,
    crm_teacher_for_schedule_tests,
    crm_groups_for_schedule_tests,
    crm_lessons_for_schedule_tests,
) -> None:
    """
    Create 5 lessons:
        - fisrt one with the date is not interesting to us
        - three - with the date we need
        - run refresh and check if we get only 4 lessons
    """

    synchronize(superuser_credentials)

    remote_lessons = get_remote_lessons(mssql_database_engine)
    local_lessons = get_local_lessons(superuser_credentials)
    assert len(remote_lessons) == 5
    assert len(local_lessons) == 4

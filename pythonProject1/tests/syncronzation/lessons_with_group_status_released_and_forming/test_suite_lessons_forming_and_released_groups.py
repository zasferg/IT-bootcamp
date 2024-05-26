from datetime import timedelta
import datetime
from datetime import datetime
from testlib.utils import get_desire_date
from testlib.utils import synchronize
from testlib.utils import get_local_lessons_by_crm_id
from testlib.utils import get_scheduled_lesson_by_name


def test_lesson_type_release_group_change_class_id(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_lesson,
    crm_lesson,
    crm_group_released,
    crm_classroom,
    crm_teacher_id_first,
):
    synchronize(superuser_credentials)
    lesson_scheduled = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson.ID
    )[0]

    assert lesson_scheduled["lesson_type"] == "По расписанию"

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, GroupId=crm_group_released.ID
    )
    lesson_released = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_lesson.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )
    assert lesson_released["lesson_type"] == "Группа выпущена"

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, ClassID=crm_classroom.ID
    )
    lesson_released_with_changed_class_id = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )
    assert (
        lesson_released_with_changed_class_id["lesson_type"]
        == "Группа выпущена"
    )


def test_lesson_type_release_group_change_status(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_lesson,
    crm_lesson,
    crm_group_released,
    crm_teacher_id_first,
):
    synchronize(superuser_credentials)

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, GroupId=crm_group_released.ID
    )

    released_lesson = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_lesson.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )
    assert released_lesson["lesson_type"] == "Группа выпущена"

    update_and_sync_lesson(crm_lesson_id=crm_lesson.ID, Status="Status2")
    released_lesson_with_changed_status = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )
    assert (
        released_lesson_with_changed_status["lesson_type"] == "Группа выпущена"
    )


def test_lesson_type_release_group_change_start_time(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_lesson,
    crm_lesson,
    crm_group_released,
    crm_teacher_id_first,
):
    synchronize(superuser_credentials)
    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, GroupId=crm_group_released.ID
    )

    released_lesson = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_lesson.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )
    assert released_lesson["lesson_type"] == "Группа выпущена"

    new_testtime = get_desire_date() + timedelta(minutes=1)
    update_and_sync_lesson(crm_lesson_id=crm_lesson.ID, StartTime=new_testtime)
    released_lesson_with_new_start_time = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert (
        released_lesson_with_new_start_time["lesson_type"] == "Группа выпущена"
    )


def test_lesson_type_release_group_change_prepod_id(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_lesson,
    crm_lesson,
    crm_group_released,
    crm_group_forming,
    crm_teacher_id_second,
):
    synchronize(superuser_credentials)
    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, GroupId=crm_group_released.ID
    )

    released_lesson = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_lesson.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )
    assert released_lesson["lesson_type"] == "Группа выпущена"

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, PrepodId=crm_teacher_id_second.ID
    )

    released_lesson_with_new_teacher = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_second.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert released_lesson_with_new_teacher["lesson_type"] == "Группа выпущена"


def test_lesson_type_release_group_change_lesson_date(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_lesson,
    crm_lesson,
    crm_group_released,
    crm_teacher_id_first,
):
    synchronize(superuser_credentials)
    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, GroupId=crm_group_released.ID
    )

    released_lesson = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_lesson.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )
    assert released_lesson["lesson_type"] == "Группа выпущена"

    new_lesson_date = int((datetime.now() + timedelta(days=7)).timestamp()) + 1
    new_testtime = get_desire_date(7)

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, LessonDate=new_testtime
    )

    released_lesson_with_new_lesson_date = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        date=new_lesson_date,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert (
        released_lesson_with_new_lesson_date["lesson_type"]
        == "Группа выпущена"
    )


def test_lesson_type_forming_group_change_class_id(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_lesson,
    crm_lesson,
    crm_group_forming,
    crm_classroom,
    crm_teacher_id_first,
):
    synchronize(superuser_credentials)

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, GroupId=crm_group_forming.ID
    )

    lesson_forming = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert lesson_forming["lesson_type"] == "Группа набирается"

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, ClassID=crm_classroom.ID
    )
    lesson_forming_with_changed_class_id = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )
    assert (
        lesson_forming_with_changed_class_id["lesson_type"]
        == "Группа набирается"
    )


def test_lesson_type_forming_group_change_status(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_lesson,
    crm_lesson,
    crm_group_forming,
    crm_teacher_id_first,
):
    synchronize(superuser_credentials)

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, GroupId=crm_group_forming.ID
    )

    lesson_forming = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_lesson.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert lesson_forming["lesson_type"] == "Группа набирается"

    update_and_sync_lesson(crm_lesson_id=crm_lesson.ID, Status="Status2")

    lesson_forming_with_new_status = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert lesson_forming_with_new_status["lesson_type"] == "Группа набирается"


def test_lesson_type_forming_group_change_start_time(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_lesson,
    crm_lesson,
    crm_group_forming,
    crm_teacher_id_first,
):
    synchronize(superuser_credentials)

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, GroupId=crm_group_forming.ID
    )

    lesson_forming = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert lesson_forming["lesson_type"] == "Группа набирается"

    new_testtime = get_desire_date() + timedelta(minutes=1)

    update_and_sync_lesson(crm_lesson_id=crm_lesson.ID, StartTime=new_testtime)

    lesson_forming_with_new_start_time = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert (
        lesson_forming_with_new_start_time["lesson_type"]
        == "Группа набирается"
    )


def test_lesson_type_forming_group_change_prepod_id(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_lesson,
    crm_lesson,
    crm_group_forming,
    crm_teacher_id_first,
    crm_teacher_id_second,
):
    synchronize(superuser_credentials)

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, GroupId=crm_group_forming.ID
    )

    lesson_forming = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert lesson_forming["lesson_type"] == "Группа набирается"

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, PrepodId=crm_teacher_id_second.ID
    )

    lesson_forming_with_new_teacher = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_second.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert (
        lesson_forming_with_new_teacher["lesson_type"] == "Группа набирается"
    )


def test_lesson_type_forming_group_change_lesson_date(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_lesson,
    crm_lesson,
    crm_group_forming,
    crm_teacher_id_first,
):
    synchronize(superuser_credentials)

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, GroupId=crm_group_forming.ID
    )

    lesson_forming = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert lesson_forming["lesson_type"] == "Группа набирается"

    new_lesson_date = int((datetime.now() + timedelta(days=7)).timestamp()) + 1
    new_testtime = get_desire_date(7)

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, LessonDate=new_testtime
    )

    lesson_forming_with_new_lesson_date = get_scheduled_lesson_by_name(
        superuser_credentials,
        date=new_lesson_date,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert (
        lesson_forming_with_new_lesson_date["lesson_type"]
        == "Группа набирается"
    )


def test_lesson_type_group_change_status_group(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_group,
    update_and_sync_lesson,
    crm_group_released,
    crm_group_is_studing,
    crm_lesson,
    crm_teacher_id_first,
):
    synchronize(superuser_credentials)

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson.ID, GroupId=crm_group_released.ID
    )

    lesson_released = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert lesson_released["lesson_type"] == "Группа выпущена"

    update_and_sync_group(
        crm_group_id=crm_group_released.ID, StatusGroup="Набирается"
    )

    lesson_forming = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert lesson_forming["lesson_type"] == "Группа набирается"

    update_and_sync_group(
        crm_group_id=crm_group_released.ID, StatusGroup="Обучается"
    )
    lesson_scheduled = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_id_first.ID,
        lesson_name=crm_lesson.Zanyatiya,
    )

    assert lesson_scheduled["lesson_type"] == "По расписанию"

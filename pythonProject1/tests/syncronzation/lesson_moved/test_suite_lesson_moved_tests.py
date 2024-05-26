from datetime import timedelta
import datetime
from datetime import datetime

from testlib.utils import get_desire_date
from testlib.utils import synchronize
from testlib.utils import get_local_lessons_by_crm_id
from testlib.utils import get_scheduled_lesson_by_name


def test_change_lesson_date(
    crm_group_generic,
    crm_teacher_ganeric,
    crm_lesson_generic,
    postgre_fixture,
    superuser_credentials,
    update_and_sync_lesson,
):
    new_testtime = get_desire_date(7)

    synchronize(superuser_credentials)

    update_and_sync_lesson(crm_lesson_generic.ID, LessonDate=new_testtime)

    local_lesson = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_generic.ID
    )
    moved_lesson = local_lesson[0]
    assert moved_lesson["lesson_type"] == "Перенос занятия"


def test_change_lesson_start_time(
    crm_group_generic,
    crm_teacher_ganeric,
    crm_lesson_generic,
    postgre_fixture,
    superuser_credentials,
    update_and_sync_lesson,
):
    new_testtime = get_desire_date() + timedelta(minutes=1)

    synchronize(superuser_credentials)

    update_and_sync_lesson(crm_lesson_generic.ID, StartTime=None)

    local_lesson = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_generic.ID
    )
    moved_lesson = local_lesson[0]
    from devtools import debug
    debug(moved_lesson)
    assert moved_lesson["lesson_type"] != "Перенос занятия"


def test_change_lesson_classroom(
    crm_group_generic,
    crm_teacher_ganeric,
    crm_lesson_generic,
    postgre_fixture,
    superuser_credentials,
    update_and_sync_lesson,
):
    new_testtime = get_desire_date() + timedelta(minutes=1)

    synchronize(superuser_credentials)

    old_local_lesson = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_generic.ID
    )
    old_lesson = old_local_lesson[0]
    assert old_lesson["class_id"] == crm_lesson_generic.ClassID
    new_class_id = 2
    update_and_sync_lesson(crm_lesson_generic.ID, ClassID=new_class_id)

    new_local_lesson = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_generic.ID
    )
    new_lesson = new_local_lesson[0]

    assert new_lesson["lesson_type"] == "Перенос занятия"
    assert new_lesson["class_id"] != old_lesson["class_id"]


def test_resync_moved_lessondate_statusgroup_null(
    postgre_fixture,
    mssql_database_engine,
    superuser_credentials,
    update_and_sync_lesson,
    crm_group_generic,
    crm_teacher_ganeric,
    crm_lesson_generic,
):
    """
    В этом тесте мы воспроизводим несколько действий:
        1.Создание урока с группой, статус которой "" (пустой/не заполнен)
        2.Изменение даты урока, в связи с чем lesson_type меняется с "По расписанию" на "Перенесенное"
        3.Имитация синхронизации второй раз, чтобы проверить, не перешел ли урок обратно в статус "По расписанию"
    """
    synchronize(superuser_credentials)

    local_lesson = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_generic.ID
    )[0]
    assert local_lesson["lesson_type"] == "По расписанию"
    assert local_lesson["status"] == ""

    new_testtime = get_desire_date(7)
    new_lesson_date = int((datetime.now() + timedelta(days=7)).timestamp()) + 1

    update_and_sync_lesson(crm_lesson_generic.ID, LessonDate=new_testtime)

    moved_lesson = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_generic.ID
    )[0]

    assert moved_lesson["lesson_type"] == "Перенос занятия"
    assert moved_lesson["status"] == ""

    synchronize(superuser_credentials)

    local_lesson_after_second_sync = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_generic.ID
    )[0]

    assert local_lesson_after_second_sync["lesson_type"] == "Перенос занятия"
    assert local_lesson_after_second_sync["status"] == ""


def test_resync_moved_starttime_statusgroup_obuchaetsya(
    crm_group_generic,
    crm_teacher_ganeric,
    crm_lesson_generic,
    postgre_fixture,
    superuser_credentials,
    update_and_sync_lesson,
):
    """
    В этом тесте мы воспроизводим несколько действий:
        1.Создание урока с группой, статус которой "Обучается"
        2.Изменение времени урока, в связи с чем lesson_type меняется с "По расписанию" на "Перенесенное"
        3.Имитация синхронизации второй раз, чтобы проверить, не перешел ли урок обратно в статус "По расписанию"
    """
    synchronize(superuser_credentials)

    local_lesson = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_ganeric.ID,
        lesson_name=crm_lesson_generic.Zanyatiya,
    )
    assert local_lesson["lesson_type"] == "По расписанию"
    assert local_lesson["group_status"] == "Обучается"

    new_testtime = get_desire_date() + timedelta(minutes=1)

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson_generic.ID, StartTime=new_testtime
    )
    local_lesson_moved = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_ganeric.ID,
        lesson_name=crm_lesson_generic.Zanyatiya,
    )

    assert local_lesson_moved["lesson_type"] == "Перенос занятия"
    assert local_lesson_moved["group_status"] == "Обучается"

    synchronize(superuser_credentials)

    local_lesson_moved_after_second_sync = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_ganeric.ID,
        lesson_name=crm_lesson_generic.Zanyatiya,
    )
    assert (
        local_lesson_moved_after_second_sync["lesson_type"]
        == "Перенос занятия"
    )
    assert local_lesson_moved_after_second_sync["group_status"] == "Обучается"


def test_resync_moved_lessondate_statusgroup_obuchaetsya(
    crm_group_generic,
    crm_teacher_ganeric,
    crm_lesson_generic,
    postgre_fixture,
    superuser_credentials,
    update_and_sync_lesson,
):
    """
    В этом тесте мы воспроизводим несколько действий:
        1.Создание урока с группой, статус которой "Обучается"
        2.Изменение даты урока, в связи с чем lesson_type меняется с "По расписанию" на "Перенесенное"
        3.Имитация синхронизации второй раз, чтобы проверить, не перешел ли урок обратно в статус "По расписанию"
    """
    synchronize(superuser_credentials)

    local_lesson = get_scheduled_lesson_by_name(
        superuser_credentials,
        teacher_id_crm=crm_teacher_ganeric.ID,
        lesson_name=crm_lesson_generic.Zanyatiya,
    )
    assert local_lesson["lesson_type"] == "По расписанию"
    assert local_lesson["group_status"] == "Обучается"

    new_testtime = get_desire_date(7)
    new_lesson_date = int((datetime.now() + timedelta(days=7)).timestamp()) + 1

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson_generic.ID, LessonDate=new_testtime
    )
    local_lesson_changed_lesson_date = get_scheduled_lesson_by_name(
        superuser_credentials,
        date=new_lesson_date,
        lesson_name=crm_lesson_generic.Zanyatiya,
    )

    assert local_lesson_changed_lesson_date["lesson_type"] == "Перенос занятия"
    assert local_lesson_changed_lesson_date["group_status"] == "Обучается"

    synchronize(superuser_credentials)

    local_lesson_moved_after_second_sync = get_scheduled_lesson_by_name(
        superuser_credentials,
        date=new_lesson_date,
        teacher_id_crm=crm_teacher_ganeric.ID,
        lesson_name=crm_lesson_generic.Zanyatiya,
    )
    assert (
        local_lesson_moved_after_second_sync["lesson_type"]
        == "Перенос занятия"
    )
    assert local_lesson_moved_after_second_sync["group_status"] == "Обучается"

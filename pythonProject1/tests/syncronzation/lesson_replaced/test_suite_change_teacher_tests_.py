from datetime import timedelta

from testlib.utils import get_desire_date
from testlib.utils import synchronize
from testlib.utils import get_local_lessons_by_crm_id
from testlib.utils import get_teacher


def test_change_teacher(
    crm_group_old_teacher,
    crm_group_new_teacher,
    crm_teacher_old,
    crm_teacher_new,
    crm_lesson_with_old_teacher,
    update_and_sync_lesson,
    superuser_credentials,
    postgre_fixture,
):
    """
    В этом тесте мы воспроизводим несколько действий:
        1.Непосредственно создание уроков "Я заменяю" и "Меня заменяют"
        2.Имитация синхронизации второй раз, что бы проверить,
          не перешел ли урок обратно в статус "По расписанию"
        3.Трансформация урока со статусом "Я заменяю" в "Перенесенное".
          Тип и статус урока "Я заменяю" должен остаться неизменным.
    """

    synchronize(superuser_credentials)

    teacher_old, teacher_new = [
        get_teacher(superuser_credentials, id_crm=crm.ID)
        for crm in [crm_teacher_old, crm_teacher_new]
    ]

    lessons = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_with_old_teacher.ID
    )
    assert len(lessons) == 1

    lesson_old = lessons[0]

    assert lesson_old["lesson_type"] == "По расписанию"

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson_with_old_teacher.ID,
        PrepodId=crm_teacher_new.ID,
    )
    local_lessons_after_changing_the_teacher = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_with_old_teacher.ID
    )

    assert len(local_lessons_after_changing_the_teacher) == 2

    lesson_new, lesson_old = local_lessons_after_changing_the_teacher

    assert lesson_old["lesson_type"] == "Меня заменяют"
    assert lesson_new["lesson_type"] == "Я заменяю"
    assert lesson_new["teacher_id"] == teacher_new["id_crm"]
    assert lesson_old["teacher_id"] == teacher_old["id_crm"]

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson_with_old_teacher.ID, Status=""
    )
    local_lesson_with_replaced_status_after_second_sync = (
        get_local_lessons_by_crm_id(
            superuser_credentials, id_crm=crm_lesson_with_old_teacher.ID
        )
    )
    lesson_new = local_lesson_with_replaced_status_after_second_sync[1]

    assert lesson_new["lesson_type"] != "По расписанию"

    new_testtime = get_desire_date() + timedelta(minutes=1)
    update_and_sync_lesson(
        crm_lesson_with_old_teacher.ID, StartTime=new_testtime
    )
    local_lesson_after_start_time_change = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_with_old_teacher.ID
    )
    lesson_new = local_lesson_after_start_time_change[1]

    assert lesson_new["lesson_type"] != "Перенесенное"
    assert lesson_new["lesson_type"] == "Я заменяю"


def test_replaced_lesson_cancel(
    crm_group_old_teacher,
    crm_group_new_teacher,
    crm_teacher_old,
    crm_teacher_new,
    crm_lesson_with_old_teacher,
    update_and_sync_lesson,
    superuser_credentials,
    postgre_fixture,
):
    """
    В данном тесте воспроизводится создание урока со статусом "Я заменяю" и "Меня заменяют"
    и трансформация их в уроки со статусом "Отмена"
    """

    synchronize(superuser_credentials)

    teacher_old, teacher_new = [
        get_teacher(superuser_credentials, id_crm=crm.ID)
        for crm in [crm_teacher_old, crm_teacher_new]
    ]

    update_and_sync_lesson(
        crm_lesson_id=crm_lesson_with_old_teacher.ID,
        PrepodId=crm_teacher_new.ID,
        Status="Отмена",
    )

    local_lessons_after_cancelled_status_assignment = (
        get_local_lessons_by_crm_id(
            superuser_credentials, id_crm=crm_lesson_with_old_teacher.ID
        )
    )

    lesson_new, lesson_old = local_lessons_after_cancelled_status_assignment

    assert len(local_lessons_after_cancelled_status_assignment) == 2
    assert lesson_old["teacher_id"] == teacher_old["id_crm"]
    assert lesson_old["lesson_type"] == "Отмена занятия"
    assert lesson_new["teacher_id"] == teacher_new["id_crm"]
    assert lesson_old["lesson_type"] == lesson_new["lesson_type"]


def test_get_new_lesson_replaced(
    crm_lesson_with_new_teacher,
    superuser_credentials,
    postgre_fixture,
):
    """В этом тесте мы создаем урок в котором учитель на закреплен за группой."""

    synchronize(superuser_credentials)
    local_lesson_after_creating_new_lesson_with_not_equal_group_teacher = (
        get_local_lessons_by_crm_id(
            superuser_credentials, id_crm=crm_lesson_with_new_teacher.ID
        )
    )
    assert (
        len(
            local_lesson_after_creating_new_lesson_with_not_equal_group_teacher
        )
        == 2
    )

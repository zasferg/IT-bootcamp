from datetime import timedelta

from testlib.utils import get_desire_date
from testlib.utils import synchronize
from testlib.utils import get_local_lessons_by_crm_id
from testlib.utils import get_cancelled_notifications


from devtools import debug


def test_cancell_lesson(
    crm_group_generic,
    crm_teacher_ganeric,
    crm_lesson_generic,
    update_and_sync_lesson,
    superuser_credentials,
    postgre_fixture,
):
    synchronize(superuser_credentials)

    update_and_sync_lesson(crm_lesson_generic.ID, Status="Отмена")

    lesson = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_generic.ID
    )
    lesson_cancelled = lesson[0]
    assert lesson_cancelled["lesson_type"] == "Отмена занятия"

    new_testtime_for_start_time = get_desire_date() + timedelta(minutes=1)
    new_testtime_for_lasson_date = get_desire_date(7)
    update_and_sync_lesson(
        crm_lesson_generic.ID,
        StartTime=new_testtime_for_start_time,
        LessonDate=new_testtime_for_lasson_date,
    )

    lesson = get_local_lessons_by_crm_id(
        superuser_credentials, id_crm=crm_lesson_generic.ID
    )
    lesson_cancelled = lesson[0]
    assert lesson_cancelled["lesson_type"] == "Отмена занятия"

    cancelled_lesson_notification = get_cancelled_notifications(
        superuser_credentials
    )
    assert len(cancelled_lesson_notification) == 2

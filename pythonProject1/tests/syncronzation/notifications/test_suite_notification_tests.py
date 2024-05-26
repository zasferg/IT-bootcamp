from datetime import date
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from sqlalchemy import select
from testlib import tables

from testlib.client.api_requests import get_notifications
from testlib.utils import synchronize

from ..entities import CRMGroup


class TestNotifacation:
    @staticmethod
    def select_from_mssql_db(mssql_database_engine, table, value):
        with mssql_database_engine.begin() as conn:
            sql_select = conn.execute(select(table).where(table.c.ID == value))
            row = sql_select.one()
            return row

    def test_change_status_group(
        self,
        postgre_fixture,
        mssql_database_engine,
        superuser_credentials,
        crm_group_old,
        update_and_sync_group,
    ):
        synchronize(superuser_credentials)

        update_and_sync_group(crm_group_old.ID, StatusGroup="Выпущена")

        sql_select = self.select_from_mssql_db(
            mssql_database_engine=mssql_database_engine,
            table=tables.groups_table,
            value=crm_group_old.ID,
        )

        crm_old_group_with_new_status_group = CRMGroup.model_validate(
            sql_select
        )
        message_expected = f'Ваша группа {crm_group_old.GroupName} перешла в статус "{crm_old_group_with_new_status_group.StatusGroup}"'
        message_returned = get_notifications(superuser_credentials)[-1][
            "message"
        ]

        assert message_returned == message_expected

    def test_teacher_appointed(
        self,
        postgre_fixture,
        superuser_credentials,
        crm_group_without_teacher,
        crm_teacher_new,
        update_and_sync_group,
    ):
        synchronize(superuser_credentials)
        update_and_sync_group(
            crm_group_id=crm_group_without_teacher.ID,
            PrepodId=crm_teacher_new.ID,
        )
        message_expected_teacher_appointed = (
            f"Вам запланировали группу {crm_group_without_teacher.GroupName}"
        )
        message_returned_teacher_appointed = get_notifications(
            superuser_credentials
        )[-1]["message"]

        assert (
            message_expected_teacher_appointed
            == message_returned_teacher_appointed
        )

    def test_lesson_cancelled(
        self,
        postgre_fixture,
        superuser_credentials,
        crm_group_old,
        crm_lesson,
        update_and_sync_lesson,
    ):
        testtime = datetime.combine(
            date.today(), datetime.min.time(), tzinfo=timezone.utc
        )

        synchronize(superuser_credentials)
        update_and_sync_lesson(crm_lesson.ID, Status="Отмена")
        expected_message = f"Занятие группы {crm_group_old.GroupName} от {testtime} отменено. {crm_lesson.Notes}"

        returned_message = get_notifications(superuser_credentials)[-1][
            "message"
        ]
        assert returned_message == expected_message

    def test_change_lessons_fields(
        self,
        postgre_fixture,
        superuser_credentials,
        crm_old_classroom,
        crm_new_classroom,
        crm_group_old,
        crm_lesson,
        update_and_sync_lesson,
    ):
        testtime = datetime.combine(
            date.today(), datetime.min.time(), tzinfo=timezone.utc
        )

        new_testtime = testtime + timedelta(days=1)

        synchronize(superuser_credentials)

        update_and_sync_lesson(crm_lesson.ID, LessonDate=new_testtime)
        expected_message_changed_lesson_date = f"Занятие группы {crm_group_old.GroupName} от {testtime} в помещении {crm_old_classroom.Class} с началом в {testtime} перенесено на: {new_testtime} в {testtime} в помещении {crm_old_classroom.Class}"
        returned_message_changed_lesson_date = get_notifications(
            superuser_credentials
        )[-1]["message"]

        assert (
            expected_message_changed_lesson_date
            == returned_message_changed_lesson_date
        )

        update_and_sync_lesson(crm_lesson.ID, StartTime=new_testtime)
        expected_message_changed_start_time = f"Занятие группы {crm_group_old.GroupName} от {new_testtime} в помещении {crm_old_classroom.Class} с началом в {testtime} перенесено на: {new_testtime} в {new_testtime} в помещении {crm_old_classroom.Class}"
        returned_message_changed_start_time = get_notifications(
            superuser_credentials
        )[-1]["message"]

        assert (
            expected_message_changed_start_time
            == returned_message_changed_start_time
        )

        update_and_sync_lesson(crm_lesson.ID, ClassID=crm_new_classroom.ID)
        expected_message_changed_classroom = f"Занятие группы {crm_group_old.GroupName} от {new_testtime} в помещении {crm_old_classroom.Class} с началом в {new_testtime} перенесено на: {new_testtime} в {new_testtime} в помещении {crm_new_classroom.Class}"
        returned_message_changed_classroom = get_notifications(
            superuser_credentials
        )[-1]["message"]

        assert (
            expected_message_changed_classroom
            == returned_message_changed_classroom
        )

    def test_change_teacher(
        self,
        postgre_fixture,
        superuser_credentials,
        crm_old_classroom,
        crm_teacher_old,
        crm_group_old,
        crm_teacher_new,
        crm_lesson,
        update_and_sync_lesson,
    ):
        testtime = datetime.combine(
            date.today(), datetime.min.time(), tzinfo=timezone.utc
        )

        synchronize(superuser_credentials)

        update_and_sync_lesson(crm_lesson.ID, PrepodId=crm_teacher_new.ID)

        expected_message_old_teacher = f"На занятии группы {crm_group_old.GroupName} от {testtime} Вас заменит преподаватель {crm_teacher_new.Prepod}. {crm_lesson.Notes}"
        expected_message_new_teacher = f"Вы назначены замещающим преподавателем на занятие для группы {crm_group_old.GroupName} от {testtime} с началом в {testtime} в помещении {crm_old_classroom.Class} вместо {crm_teacher_old.Prepod}. {crm_lesson.Notes}"

        notifications = get_notifications(superuser_credentials)

        returned_message_old_teacher = notifications[-1]["message"]
        returned_message_new_teacher = notifications[-2]["message"]

        assert returned_message_new_teacher == expected_message_new_teacher
        assert returned_message_old_teacher == expected_message_old_teacher

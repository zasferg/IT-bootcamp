def synchronize(self):
    week_ago = timezone.now() - timezone.timedelta(days=8)
    all_lessons_crm = LessonCRM.objects.filter(
        lesson_date__gt=week_ago
    )
    all_teachers_crm = TeacherCRM.objects.all()
    all_groups_crm = GroupCRM.objects.all()
    all_lessons_journal = Lesson.objects.all()
    all_groups_journal = Group.objects.all()

    all_lessons_crm_ids = {
        crm_lesson.id for crm_lesson in all_lessons_crm.all()
    }
    all_teachers_crm_ids = {
        crm_teacher.id for crm_teacher in all_teachers_crm.all()
    }
    all_groups_crm_ids = {
        crm_group.id for crm_group in all_groups_crm.all()
    }

    lesson_journal_query = all_lessons_journal.filter(
        ~Q(id_crm__in=all_lessons_crm_ids)
    )
    if lesson_journal_query.exists() and isinstance(
            all_lessons_journal, QuerySet
    ):
        lesson_journal_query.delete()

    try:
        for lesson_crm in all_lessons_crm:
            if not all_lessons_journal.filter(
                    id_crm=lesson_crm.id
            ).exists():
                group_journal = all_groups_journal.filter(
                    id_crm=lesson_crm.group_id
                ).values()
                if (
                        lesson_crm.teacher_id in all_teachers_crm_ids
                        and lesson_crm.group_id in all_groups_crm_ids
                ):
                    group_journal_teacher_id = (
                        group_journal.values_list(
                            "teacher_id", flat=True
                        )[0]
                    )

                    if (
                            group_journal
                            and (
                            group_journal_teacher_id
                            != lesson_crm.teacher_id
                    )
                            and lesson_crm.status
                            not in ["Отмена", "Отработка"]
                    ):
                        lesson_crm.status = "Я заменяю"
                        new_lesson_with_new_teacher = (
                            self.object_create(lesson_crm)
                        )
                        self.new_lessons.append(
                            new_lesson_with_new_teacher
                        )
                        lesson_crm.status = "Меня заменяют"
                        lesson_crm.teacher_id = (
                            group_journal_teacher_id
                        )
                        new_lesson_with_old_teacher = (
                            self.object_create(lesson_crm)
                        )
                        self.new_lessons.append(
                            new_lesson_with_old_teacher
                        )
                    else:
                        new_lesson = self.object_create(lesson_crm)
                        self.new_lessons.append(new_lesson)
                else:
                    message_with_not_valid_lesson = f"Занятие с id {lesson_crm.id} имеет невалидные данные."
                    RefreshPoint.create_notification(
                        self.new_notifications,
                        None,
                        message_with_not_valid_lesson,
                    )
                    pass
            else:
                if lesson_crm.status == "Отмена":
                    lesson_for_upgrade = all_lessons_journal.filter(
                        id_crm=lesson_crm.id
                    )
                    for lesson in lesson_for_upgrade:
                        if (
                                lesson.teacher_id in all_teachers_crm_ids
                                and lesson_crm.teacher_id
                                in all_teachers_crm_ids
                        ) and lesson.group_id in all_groups_crm_ids:
                            lesson_teacher_id = lesson.teacher_id
                            if not self.check_equality(
                                    lesson, lesson_crm
                            ):
                                upgraded_lesson = self.object_upgrade(
                                    lesson_crm, lesson
                                )
                                if (
                                        upgraded_lesson.teacher_id
                                        != lesson_teacher_id
                                ):
                                    upgraded_lesson.teacher_id = (
                                        lesson_teacher_id
                                    )
                                self.update_lessons.append(lesson)
                        else:
                            message_with_not_valid_lesson = f"Занятие с id {lesson.id_crm} имеет невалидные данные."
                            RefreshPoint.create_notification(
                                self.new_notifications,
                                None,
                                message_with_not_valid_lesson,
                            )
                            pass

                else:
                    some_lessons = all_lessons_journal.all().exclude(
                        status="Меня заменяют"
                    )
                    lesson_for_upgrade = some_lessons.get(
                        id_crm=lesson_crm.id
                    )
                    if (
                            lesson_for_upgrade.teacher_id
                            in all_teachers_crm_ids
                            and lesson_crm.teacher_id
                            in all_teachers_crm_ids
                            and lesson_for_upgrade.group_id
                            in all_groups_crm_ids
                    ):
                        if not self.check_equality(
                                lesson_for_upgrade, lesson_crm
                        ):
                            upgraded_lesson = self.object_upgrade(
                                lesson_crm, lesson_for_upgrade
                            )

                            self.update_lessons.append(upgraded_lesson)

                            if (
                                    upgraded_lesson.status
                                    == "Меня заменяют"
                            ):
                                lesson_crm.status = "Я заменяю"

                                new_lesson = self.object_create(
                                    lesson_crm
                                )

                                self.new_lessons.append(new_lesson)
                    else:
                        message_with_not_valid_lesson = f"Занятие с id {lesson_for_upgrade.id_crm} имеет невалидные данные."
                        RefreshPoint.create_notification(
                            self.new_notifications,
                            None,
                            message_with_not_valid_lesson,
                        )
                        pass

from medly_backend.db.session import get_session
from medly_backend.data_importer.course_importer import import_course
from medly_backend.data_importer.exam_importer import import_exams
from medly_backend.data_importer.practice_importer import import_practices
from medly_backend.data_importer.user_data_importer import import_user_data


def run_import():
    session = get_session()
    import_course(session)
    import_exams(session)
    import_practices(session)
    import_user_data(session)
    session.commit()


if __name__ == "__main__":
    run_import()

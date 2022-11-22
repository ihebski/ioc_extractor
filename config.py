import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Form
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'RandomKey-cabcjbjcbjdbcjbjbx!!!ecnm*****cdncjkdzc'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or\
        'sqlite:///' + os.path.join(basedir, 'database/cti_ioc_extract.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Upload
    UPLOAD_PATH = os.environ.get('UPLOAD_PATH') or 'files'
    UPLOAD_FOLDER = UPLOAD_PATH


    # logs
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

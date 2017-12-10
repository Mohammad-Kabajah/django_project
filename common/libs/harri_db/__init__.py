from common.libs.harri_request_handler import get_current_request_id
from django.conf import settings
import sqlalchemy
from sqlalchemy.orm import scoped_session

SQLA_ENGINE = "{driver}://{user}:{password}@{host}/{dbname}?charset=utf8".format(driver=settings.DATABASES['default']['ENGINE'].split('.', -1)[-1],
                                                                    user=settings.DATABASES['default']['USER'],
                                                                    password=settings.DATABASES['default']['PASSWORD'],
                                                                    host=settings.DATABASES['default']['HOST'],
                                                                    dbname=settings.DATABASES['default']['NAME'])


engine = sqlalchemy.create_engine(SQLA_ENGINE, echo=settings.SQLALCHEMY_ECHO, pool_recycle=7200, pool_size=10)
db_session = scoped_session(sqlalchemy.orm.sessionmaker(bind=engine), scopefunc=get_current_request_id)
#Session = sqlalchemy.orm.sessionmaker(bind=engine)


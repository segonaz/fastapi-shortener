from os import path
from pydantic import BaseSettings


class Settings(BaseSettings):
    alphabet: str
    url_prefix: str
    user_link_hash_length: int

    redis_host: str
    redis_port: str
    redis_db: int
    redis_exat: int

    postgres_user:  str
    postgres_password: str
    postgres_server: str
    postgres_db: str

    database_url: str = ''

    # Test settings
    is_test: bool = False
    test_redis_db: int = 16
    test_postgres_db: str
    test_postgres_server: str

    def set_database_for_test(self):
        # Replace databases then running tests
        self.postgres_server = self.test_postgres_server
        self.postgres_db = self.test_postgres_db
        self.redis_db = self.test_redis_db


dir_path = path.dirname(path.dirname(path.dirname(path.realpath(__file__))))

settings = Settings(
    _env_file=path.join(dir_path, '.env.example'),
    _env_file_encoding='utf-8',
)

# Если запущены тесты, заменяем базу данных на тестовую
if settings.is_test:
    settings.set_database_for_test()

settings.database_url = f"postgresql://{settings.postgres_user}:{settings.postgres_password}" \
                                        f"@{settings.postgres_server}:5432/{settings.postgres_db}"

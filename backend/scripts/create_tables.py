# Docker startup script
# Create tables for first run
from src.shortener.db import engine, Base # noqa

# For PyCharm
# from backend.src.shortener.db import engine, Base

print('Creating tables if need')
Base.metadata.create_all(bind=engine)
print('Done')

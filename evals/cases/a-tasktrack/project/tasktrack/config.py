import os


class Config:
    DATABASE_URL = os.environ["DATABASE_URL"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    SMTP_HOST = os.environ.get("SMTP_HOST", "localhost")
    TASKS_PER_PAGE = int(os.environ.get("TASKS_PER_PAGE", "20"))

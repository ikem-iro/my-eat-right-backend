from sqlmodel import Session
from utils.db_utils import engine


def get_session():
    with Session(engine) as session:
        return session
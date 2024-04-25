from sqlmodel import Session, select
from auth.dbschema import User



def get_user_by_email(email: str, session: Session):
    """
    Retrieve a user by their email from the database.

    Args:
        email (str): The email of the user to retrieve.
        session (Session): The database session to execute the query.

    Returns:
        User: The user object retrieved based on the email.
    """
    statement = select(User).where(User.email == email)
    result = session.exec(statement).first()
    return result


def get_user_by_id(id: str, session: Session):
    """
    Retrieve a user from the database by their ID.

    Parameters:
        id (str): The ID of the user to retrieve.
        session (Session): The database session to execute the query.

    Returns:
        User
    """
    statement = select(User).where(User.id == id)
    result = session.exec(statement).first()
    return result
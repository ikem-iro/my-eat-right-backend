from sqlmodel import Session, select
from auth.dbschema import User, BlacklistedTokens
from users.dbschema import Chats 



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


def get_user_by_id(id, session: Session):
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

def get_blacklisted_token(token: str, session: Session):
    statement = select(BlacklistedTokens).where(BlacklistedTokens.token == token)
    result = session.exec(statement).first()
    return result



def get_chat_history(id, session: Session):
    """
    Retrieve the chat history of a user from the database.

    Parameters:
        id (str): The ID of the user to retrieve the chat history for.
        session (Session): The database session to execute the query.

    Returns:
        List[Chats]: The list of chat messages for the user.
    """
    statement = select(Chats).where(Chats.user_id == id)
    result = session.exec(statement).all()
    return result
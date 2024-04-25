from fastapi import Request
import uuid
from datetime import datetime
from .dbschema import User, BlacklistedTokens
from fastapi.encoders import jsonable_encoder
from crud.crud import get_user_by_email, get_user_by_id, get_blacklisted_token
from utils.pass_utils import hash_password, compare_password_and_hash
from utils.token_utils import (
    create_access_token,
    create_password_reset_token,
    verify_password_reset_token,
    create_verify_email_token,
    verify_email_verification_token,
)
from utils.email_utils import (
    generate_reset_password_email,
    send_mail,
    generate_verification_email,
)


def create_new_user(user, session):
    """
    Creates a new user in the database.

    Parameters:
        user (User): The user object containing the user's information.
        session (Session): The database session to execute the query.

    Returns:
        dict: A dictionary containing the user's ID and the data returned by the send_mail function.
              If an error occurs, a dictionary with an 'error' key is returned.

    Raises:
        ValueError: If a user with the same email already exists in the database.
    """

    try:
        user_exists = get_user_by_email(user.email, session)
        if user_exists is not None:
            raise ValueError("User already exists.")
        user.password = hash_password(user.password)
        new_user = User(**user.dict())
        new_user.created_at = datetime.now()
        new_user.updated_at = datetime.now()
        token = create_verify_email_token(new_user.email)
        email_to_send = generate_verification_email(
            email_to=new_user.email, email=new_user.email, token=token
        )

        data = send_mail(
            email_to=new_user.email,
            subject=email_to_send.subject,
            html_content=email_to_send.html_content,
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return {"id": new_user.id, "data": data}
    except ValueError as e:
        return {"error": str(e)}


def log_user_in(user, session):
    """
    Logs in a user by checking if the user exists in the database and if the provided password matches the hashed password stored in the database. If the user exists and the password is correct, a JWT access token is generated and returned. If the user does not exist or the password is incorrect, a dictionary with an 'error' key is returned.

    Parameters:
        user (User): The user object containing the email and password of the user to be logged in.
        session (Session): The database session to execute the query.

    Returns:
        str: The JWT access token if the user exists and the password is correct.
        dict: A dictionary with an 'error' key if the user does not exist or the password is incorrect.
    """
    try:
        user_exists = get_user_by_email(user.email, session)
        if user_exists is None:
            raise ValueError("User does not exist.")
        if not compare_password_and_hash(user.password, user_exists.password):
            raise ValueError("Password is incorrect.")
        token = create_access_token(jsonable_encoder(user_exists.id))
        return {"Access_token": token, "is_active": user_exists.is_active}
    except ValueError as e:
        return {"error": str(e)}


def password_recovery(email, session):
    """
    Recovers the password for a user with the given email.

    Args:
        email (str): The email of the user whose password is being recovered.
        session (Session): The database session to execute the query.

    Returns:
        dict or str: If the password recovery is successful, returns the response data.
                     If there is an error during password recovery, returns a dictionary with an 'error' key.

    Raises:
        ValueError: If the user does not exist.

    """
    try:
        user_exists = get_user_by_email(email, session)
        if user_exists is None:
            raise ValueError("User does not exist.")
        token = create_password_reset_token(jsonable_encoder(user_exists.id))

        email_to_send = generate_reset_password_email(
            email_to=user_exists.email, email=email, token=token
        )

        data = send_mail(
            email_to=user_exists.email,
            subject=email_to_send.subject,
            html_content=email_to_send.html_content,
        )

        return data

    except ValueError as e:
        return {"error": str(e)}


def passwd_reset(new_password, session, token):
    """
    Resets the password for a user based on a provided token.

    Parameters:
        new_password: The new password to set for the user.
        session: The database session to execute the password reset operation.
        token: The token used for password reset.

    Returns:
        dict: A dictionary containing a success message if the password reset is successful.
              A dictionary with an 'error' key if there is an issue during the password reset process.
    """
    try:
        is_token_blacklisted = get_blacklisted_token(token, session)
        if is_token_blacklisted:
            raise ValueError("Token already blacklisted")
        password_to_change = new_password.new_password
        token_data = verify_password_reset_token(token)
        if token_data is None:
            raise ValueError("Invalid token.")
        user_exists = get_user_by_id(token_data, session)
        if user_exists is None:
            raise ValueError("User does not exist.")
        if user_exists.is_active == False:
            raise ValueError("User is not active.")
        is_password_invalid = compare_password_and_hash(
            password_to_change, user_exists.password
        )
        if is_password_invalid:
            raise ValueError("Password cannot be the same as current password")
        hash_new_password = hash_password(password_to_change)
        user_exists.password = hash_new_password
        user_exists.updated_at = datetime.now()
        session.add(user_exists)
        session.commit()
        session.refresh(user_exists)
        blacklisted_token = BlacklistedTokens(token=token)
        session.add(blacklisted_token)
        session.commit()
        session.refresh(blacklisted_token)
        return {"message": "Password reset successful"}
    except ValueError as e:
        return {"error": str(e)}


def send_verification_email(id, session):
    """
    Sends a verification email to the user with the given ID.

    Parameters:
        id (str): The ID of the user.
        session (Session): The database session to execute the query.

    Returns:
        dict : If the verification email is sent successfully, returns the response data.
                     If there is an error during email sending, returns a dictionary with an 'error' key.

    Raises:
        ValueError: If the user does not exist or the user is already active.
    """
    try:
        format_id_to_uuid = str(uuid.UUID(id))
        print(format_id_to_uuid)
        user_exists = get_user_by_id(format_id_to_uuid, session)
        if user_exists is None:
            raise ValueError("User does not exist.")
        if user_exists.is_active == True:
            raise ValueError("User is already active.")
        token = create_verify_email_token(jsonable_encoder(user_exists.email))
        email_to_send = generate_verification_email(
            email_to=user_exists.email, email=user_exists.email, token=token
        )

        data = send_mail(
            email_to=user_exists.email,
            subject=email_to_send.subject,
            html_content=email_to_send.html_content,
        )
        return data
    except ValueError as e:
        return {"error": str(e)}


def verify_user_email(token, session):
    """
    Verify the user's email based on the provided token.

    Parameters:
        session: The database session to execute the query.
        token: The token used to verify the user's email.

    Returns:
        A dictionary with a message key if the email verification is successful.
        If an error occurs, a dictionary with an error key is returned.
    """
    try:
        is_token_blacklisted = get_blacklisted_token(token, session)
        if is_token_blacklisted:
            raise ValueError("Token already blacklisted")
        token_data = verify_email_verification_token(token)
        if token_data is None:
            raise ValueError("Invalid token.")
        user_exists = get_user_by_email(token_data, session)
        if user_exists is None:
            raise ValueError("User does not exist.")
        if user_exists.is_active == True:
            raise ValueError("User is already active.")
        user_exists.is_active = True
        user_exists.updated_at = datetime.now()
        session.add(user_exists)
        session.commit()
        session.refresh(user_exists)
        blacklisted_token = BlacklistedTokens(token=token)
        session.add(blacklisted_token)
        session.commit()
        session.refresh(blacklisted_token)
        return {"message": "Email verified successfully"}
    except ValueError as e:
        return {"error": str(e)}


def log_user_out(token, session):
    try:
        is_token_blacklisted = get_blacklisted_token(token, session)
        if is_token_blacklisted:
            raise ValueError("Token already blacklisted")

        blacklisted_token = BlacklistedTokens(token=token)
        session.add(blacklisted_token)
        session.commit()
        session.refresh(blacklisted_token)
        return {"message": "Logged out successfully"}
    except ValueError as e:
        return {"error": str(e)}

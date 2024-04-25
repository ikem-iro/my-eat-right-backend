import jwt
from datetime import datetime, timedelta, timezone
from .config_utils import settings



def create_access_token(data: str) -> str:
    """
    Creates an access token with the provided data.

    Args:
        data (str): The data to be included in the access token.

    Returns:
        str: The encoded access token.

    Raises:
        None.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)
    to_encode = {"exp": expire, "data": data}
    encoded_jwt = jwt.encode(to_encode, settings.ACCESS_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_password_reset_token(data: str) -> str:
    """
    Creates a password reset token with the provided data.

    Args:
        data (str): The data to be included in the password reset token.

    Returns:
        str: The encoded password reset token.

    Raises:
        None.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES)
    to_encode = {"exp": expire, "data": data}
    encode_jwt = jwt.encode(to_encode, settings.PASSWORD_RESET_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt


def create_verify_email_token(data: str) -> str:
    """
    Creates a verify email token with the provided data.

    Args:
        data (str): The data to be included in the verify email token.

    Returns:
        str: The encoded verify email token.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.VERIFY_EMAIL_TOKEN_EXPIRES)
    to_encode = {"exp": expire, "data": data}
    encoded_jwt = jwt.encode(to_encode, settings.VERIFY_EMAIL_TOKEN_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password_reset_token(data: str):
    """
    Verify a password reset token and return the decoded data.

    Args:
        data (str): The password reset token to be verified.

    Returns:
        str or Exception: The decoded data if the token is valid, otherwise the exception message.

    Raises:
        None.
    """
    try:
        decode_token = jwt.decode(data, settings.PASSWORD_RESET_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decode_token["data"]
    except Exception:
        return None
    
def verify_email_verification_token(data: str):
    """
    Verify an email verification token and return the decoded data.

    Args:
        data (str): The email verification token to be verified.

    Returns:
        str or None: The decoded data if the token is valid, otherwise None.

    Raises:
        Exception: If there is an error decoding the token.
    """
    try:
        decode_token = jwt.decode(data, settings.VERIFY_EMAIL_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decode_token["data"]
    except Exception:
        return None

def verify_access_token(data: str):
    """
    Verify an access token and return the decoded data.

    Args:
        data (str): The access token to be verified.

    Returns:
        str or None: The decoded data if the token is valid, otherwise None.

    Raises:
        Exception: If there is an error decoding the token.
    """
    try:
        decode_token = jwt.decode(data, settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decode_token["data"]
    except Exception:
        return None

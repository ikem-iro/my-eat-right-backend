from passlib.context import CryptContext



password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")






def hash_password(password: str):
    """
    Hashes a given password using the bcrypt algorithm.

    Args:
        password (str): The password to be hashed.

    Returns:
        str: The hashed password.

    Raises:
        None.
    """
    return password_context.hash(password)


def compare_password_and_hash(password: str, hashed_password: str):
    """
    Compares a given password with a hashed password using the bcrypt algorithm.

    Args:
        password (str): The password to be compared.
        hashed_password (str): The hashed password to compare against.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.

    Raises:
        None.
    """
    return password_context.verify(password, hashed_password)
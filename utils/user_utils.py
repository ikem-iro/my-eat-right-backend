import random

def generate_username(first_name, last_name):
    """
    Generates a username using the user's first name, last name, and a random number.

    Parameters:
        first_name (str): The user's first name.
        last_name (str): The user's last name.

    Returns:
        str: The generated username.
    """
    random_number = random.randint(1, 999)
    username = f"{first_name.lower()}_{last_name.lower()}_{random_number}"
    return username



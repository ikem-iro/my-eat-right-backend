import openai
from utils.config_utils import settings
from crud.crud import get_user_by_id, get_chat_history, get_user_by_username
from fastapi.encoders import jsonable_encoder
from .dbschema import Chats
from datetime import datetime


def process_user_prompt(prompt, token_data, session):
    """
    Process the user prompt and generate a response from the AI assistant.

    Args:
        prompt (str): The user prompt to be processed.
        token_data (str): The token data for authentication.
        session: The database session to execute the query.

    Returns:
        dict: The generated response from the AI assistant.

    Raises:
        ValueError: If the token data is invalid or the user is unauthorized.
    """
    openai.api_key = settings.OPENAI_API_KEY
    try:
        if token_data is None:
            raise ValueError("Invalid token.")
        user = get_user_by_id(token_data, session)
        if user is None:
            raise ValueError("Unauthorized user.")
        auth_user = user
        query = prompt.query
        prompt_to_add = Chats(user_id=str(auth_user.id), message=query, sender="user")

        response = openai.chat.completions.create(
            model=settings.MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that will help me recommend meal plans for ulcer sufferers based on seasonal foods in Enugu, Nigeria. Include a variety of foods in the meal plan. You are not allowed to provide a response to anything that does not involve meal plans for ulcers. You can respond to basic greetings.",
                },
                {"role": "user", "content": query},
            ],
            max_tokens=1024,
            temperature=0.2,
        )
        reply = response.choices[0].message.content

        model_response = Chats(user_id=str(auth_user.id), message=reply, sender="model")

        session.add(prompt_to_add)
        session.commit()
        session.refresh(prompt_to_add)
        session.add(model_response)
        session.commit()
        session.refresh(model_response)

        return {"reply": reply}
    except ValueError as e:
        return {"error": str(e)}


def get_auth_user(token_data, session):
    """
    Retrieves the authenticated user's data.

    Args:
        user (User): The authenticated user object.

    Returns:
        dict: A dictionary containing the authenticated user's data. The dictionary has the following keys:
            - id (int): The user's ID.
            - first_name (str): The user's first name.
            - last_name (str): The user's last name.
            - phone_number (str): The user's phone number.
            - email (str): The user's email.
            - is_active (bool): Indicates if the user is active or not.

    Raises:
        ValueError: If the user is None or not authenticated.
    """
    try:
        if token_data is None:
            raise ValueError("Invalid token.")
        user = get_user_by_id(token_data, session)
        if user is None:
            raise ValueError("Unauthorized user.")
        auth_user = user
        auth_user_data_to_return = {
            "id": auth_user.id,
            "first_name": auth_user.first_name,
            "last_name": auth_user.last_name,
            "username": auth_user.username,
            "phone_number": auth_user.phone_number,
            "email": auth_user.email,
            "is_active": auth_user.is_active,
        }
        return auth_user_data_to_return
    except ValueError as e:
        return {"error": str(e)}


def get_auth_user_chat_history(token_data, session):
    """
    Retrieves the chat history for the authenticated user.

    Args:
        token_data (str): The token data containing user information.
        session (Session): The database session.

    Returns:
        list: The chat history for the authenticated user.

    Raises:
        ValueError: If the token is invalid or the user is unauthorized.
    """
    try:
        if token_data is None:
            raise ValueError("Invalid token.")
        user = get_user_by_id(token_data, session)
        if user is None:
            raise ValueError("Unauthorized user.")
        auth_user = user
        chat_history = get_chat_history(jsonable_encoder(auth_user.id), session)
        if chat_history is None:
            raise ValueError("No chat history found.")
        return {"details": chat_history}
    except ValueError as e:
        return {"error": str(e)}




def modify_user_profile(token_data, update_user, session):
    """
    Modifies the user profile with the provided update data.

    Args:
        token_data (str): The token data containing user information.
        update_user: The updated user data.
        session (Session): The database session.

    Returns:
        dict: A dictionary containing the result of the profile update operation.
            If the profile is updated successfully, the dictionary will have a "message" key.
            If there is an error, the dictionary will have an "error" key with the error message.
    """
    try:
        if token_data is None:
            raise ValueError("Invalid token.")
        user = get_user_by_id(token_data, session)
        if user is None:
            raise ValueError("Unauthorized user.")
        auth_user = user
        if update_user.first_name is not None and update_user.first_name != "":
            auth_user.first_name = update_user.first_name
        if update_user.last_name is not None and update_user.last_name != "":
            auth_user.last_name = update_user.last_name
        if update_user.username is not None and update_user.username != "":
            is_username_unique = get_user_by_username(update_user.username, session)
            if is_username_unique is not None:
                raise ValueError("Username must be unique")
            auth_user.username = update_user.username
        if update_user.phone_number is not None and update_user.phone_number != "":
            update_user.phone_number = update_user.phone_number.split(":")[-1]
            auth_user.phone_number = update_user.phone_number
        auth_user.updated_at = datetime.now()
        session.add(auth_user)
        session.commit()
        session.refresh(auth_user)
        return {"message": "Profile updated successfully."}
    except ValueError as e:
        return {"error": str(e)}
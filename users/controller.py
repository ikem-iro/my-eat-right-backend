import openai
from utils.config_utils import settings
from crud.crud import get_user_by_id, get_chat_history
from fastapi.encoders import jsonable_encoder
from .dbschema import Chats


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




def modify_user_profile(token_data, session):
    pass
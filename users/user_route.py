from .models import Prompt, UpdateUser
from fastapi import APIRouter, Response, Depends
from dependencies.db import get_session
from dependencies.user_deps import get_current_user
from sqlmodel import Session
from typing import Annotated
from .controller import process_user_prompt, get_auth_user, get_auth_user_chat_history, modify_user_profile


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/me/chat")
async def user_prompt(
    prompt: Prompt,
    token_data: Annotated[str, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    res: Response,
):
    """
    Handle a POST request to '/me/chat' endpoint.

    This function receives a prompt, a user object, a session object, and a response object as parameters.
    It processes the prompt using the `process_user_prompt` function, passing the prompt, user, and session as arguments.
    If the response contains an 'error' key, it sets the response status code to 403 and returns the response.
    Otherwise, it sets the response status code to 200 and returns the response.

    Parameters:
        - prompt (Prompt): The prompt object received from the request.
        - user (Annotated[User, Depends(get_current_user)]): The user object obtained from the current session.
        - session (Annotated[Session, Depends(get_session)]): The session object used for database operations.
        - res (Response): The response object used to send the HTTP response.

    Returns:
        - dict: The processed response from the `process_user_prompt` function.

    Raises:
        - None.
    """
    response = process_user_prompt(prompt, token_data, session)
    match response.get("error"):
        case "Invalid token.":
            res.status_code = 401
        case "Unauthorized User":
            res.status_code = 403
        case _:
            res.status_code = 200
    return response


@router.get("/me/profile")
async def user_profile(
    token_data: Annotated[str, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    res: Response,
):
    """
    Get the profile information of the authenticated user.

    Args:
        user (Annotated[User, Depends(get_current_user)]): The authenticated user object.
        res (Response): The response object used to send the HTTP response.

    Returns:
        dict: The profile information of the authenticated user. If an error occur, a dictionary with an 'error' key is returned.

    Raises:
        None.

    """
    response = get_auth_user(token_data, session)
    match response.get("error"):
        case "Invalid token.":
            res.status_code = 401
            return response
        case "Unauthorized User.":
            res.status_code = 403
            return response
        case _:
            res.status_code = 200
            return response


@router.get("/me/chat_history")
async def user_chat_history(
    token_data: Annotated[str, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    res: Response,
):
    """
    Get the chat history of the authenticated user.

    Args:
        user (Annotated[User, Depends(get_current_user)]): The authenticated user object.
        res (Response): The response object used to send the HTTP response.

    Returns:
        dict: The chat history of the authenticated user. If an error occur, a dictionary with an 'error' key is returned.

    Raises:
        None.

    """
    response = get_auth_user_chat_history(token_data, session)
    match response.get("error"):
        case "Invalid token.":
            res.status_code = 401
            return response
        case "Unauthorized User.":
            res.status_code = 403
            return response
        case _:
            res.status_code = 200
            return response


@router.put("/me/profile")
async def update_user_profile(
    update_user: UpdateUser,
    token_data: Annotated[str, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    res: Response,
):
    """
    Updates the user profile with the provided data.

    Args:
        update_user (UpdateUser): The data to update the user profile.
        token_data (Annotated[str, Depends(get_current_user)]): The token data for user authentication.
        session (Annotated[Session, Depends(get_session)]): The current database session.
        res (Response): The response object to send the HTTP response.

    Returns:
        The result of the profile update operation as a dictionary.
        If successful, the dictionary will have a "message" key.
        If there is an error, the dictionary will have an "error" key with the error message.
    """
    response = modify_user_profile(token_data, update_user, session)
    match response.get("error"):
        case "Invalid token.":
            res.status_code = 401
            return response
        case "Unauthorized user.":
            res.status_code = 403
            return response
        case "Username must be unique":
            res.status_code = 400
            return response 
        case _:
            res.status_code = 200
            return response


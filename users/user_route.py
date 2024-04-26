from .models import Prompt
from fastapi import APIRouter, Response, Depends
from dependencies.db import get_session
from dependencies.user_deps import get_current_user
from auth.dbschema import User
from sqlmodel import Session
from typing import Annotated
from .controller import process_user_prompt, get_auth_user



router = APIRouter(prefix='/users', tags=["Users"])



@router.post('/me/chat')
async def user_prompt(prompt: Prompt, token_data: Annotated[str, Depends(get_current_user)] ,session: Annotated[Session, Depends(get_session)], res: Response):
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



@router.get('/me/profile')
async def user_profile(token_data: Annotated[str, Depends(get_current_user)], session: Annotated[Session, Depends(get_session)], res: Response):
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

from fastapi import APIRouter, Response, Depends, Path
from sqlmodel import Session
from typing import Annotated
from dependencies.db import get_session
from .models import RegisterUser, LoginUser, NewPassword
from .controller import create_new_user, log_user_in, password_recovery, passwd_reset, verify_user_email




router = APIRouter(prefix="/auth" ,tags=["Authentication"])

@router.post('/register')
async def register(user: RegisterUser, session: Annotated[Session, Depends(get_session)], res: Response):
    """
    Registers a new user in the system.

    Parameters:
        - user: An instance of the RegisterUser model representing the user to be registered.
        - session: An instance of the Session class representing the database session.
        - res: An instance of the Response class representing the HTTP response.

    Returns:
        - If the user registration is successful, returns a dictionary with the following keys:
            - message: A string indicating the success message.
            - details: A dictionary containing the details of the newly created user.
        - If there is an error during user registration, returns a dictionary with the following keys:
            - error: A string indicating the error message.

    Raises:
        - None.
    """
    response = create_new_user(user, session)
    if "error" in response:
        res.status_code = 400
        return response
    res.status_code = 201
    return {"message": "User created successfully"}



@router.post('/login')
async def login(user: LoginUser, session: Annotated[Session, Depends(get_session)], res: Response):
    """
    Logs in a user by calling the log_user_in function with the provided user and session.
    
    Parameters:
        - user: An instance of the LoginUser model representing the user to log in.
        - session: An instance of the Session class representing the database session.
        - res: An instance of the Response class representing the HTTP response.

    Returns:
        - If the user login is successful, returns a dictionary with the response.
        - If there is an error during user login, returns a dictionary with an 'error' key.
    """
    response = log_user_in(user, session)
    match response.get("error"):
        case "User does not exist.":
            res.status_code = 404
            return response
        case "Password is incorrect.":
            res.status_code = 400
            return response
    res.status_code = 200
    return {"message": "User logged in successfully", "Access_token": response}







@router.post('/password-recovery/{email}')
async def recover_password(email: str, session: Annotated[Session, Depends(get_session)], res: Response):
    """
    Initiates the password recovery process for the provided email.

    Parameters:
        - email (str): The email address for which the password recovery is requested.
        - session (Session): The database session to execute the password recovery operation.
        - res (Response): The HTTP response object to handle the status codes.

    Returns:
        - If the password recovery is successful, returns a dictionary with the response.
        - If there is an error during password recovery, returns a dictionary with an 'error' key.
    """
    response = password_recovery(email, session)
    if "error" in response:
        res.status_code = 404
        return response
    res.status_code = 200
    return response
    



@router.post('/reset-password/{token}')
async def reset_password(new_password: NewPassword, session: Annotated[Session, Depends(get_session)], res: Response, token: str = Path(title="Password reset token")):
    """
    Initiates the password reset process for the provided token.

    Parameters:
        - new_password (NewPassword): The new password to be set.
        - session (Session): The database session to execute the password reset operation.
        - res (Response): The HTTP response object to handle the status codes.
        - token (str): The token used for password reset.

    Returns:
        - If the password reset is successful, returns a dictionary with the response.
        - If there is an error during password reset, returns a dictionary with an 'error' key.
    """
    response = passwd_reset(new_password, session, token)
    match response.get("error"):
        case "User does not exist.":
            res.status_code = 404
            return response
        case "Invalid token.":
            res.status_code = 400
            return response
        case "User is not active.":
            res.status_code = 401
            return response
        case _:
            res.status_code = 200
            return response




@router.post("/verify-email/{token}")
async def verify_email(session: Annotated[Session, Depends(get_session)], res: Response, token: str = Path(title="Verification token")):
    response = verify_user_email(session, token)
    pass
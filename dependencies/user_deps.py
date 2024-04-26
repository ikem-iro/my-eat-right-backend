from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from dependencies.db import get_session
from utils.config_utils import settings
from crud.crud import get_blacklisted_token
from fastapi import Depends
from typing import Annotated
from utils.token_utils import verify_access_token




# The line `oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.}/auth/login")` is creating an
# instance of the `OAuth2PasswordBearer` class from the `fastapi.security` module. This instance is
# used for handling OAuth2 authentication with a password bearer token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[Session, Depends(get_session)]):
    """
    Retrieves the current user based on the provided token after verifying access.
    
    Args:
        token (Annotated[str, Depends(oauth2_scheme)]): The token used for user verification.
    
    Returns:
        The current user if the token is valid.
    """
    is_token_blacklisted = get_blacklisted_token(token, session)
    if is_token_blacklisted is not None:
        return None
    data = verify_access_token(token)
    return data
    
    
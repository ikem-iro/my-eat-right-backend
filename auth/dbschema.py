from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    """
    SQL Model representing a user.
    """

    # UUID primary key
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    # User's first name
    first_name: str

    # User's last name
    last_name: str

    # User's email
    email: str = Field(unique=True, index=True)

    # User's hashed password
    password: str

    # User's phone number
    phone_number: str | None = None

    # Flag indicating if the user is active
    is_active: bool = Field(default=False)

    # Flag indicating if the user is disabled
    is_disabled: bool = Field(default=False)

    # Time when the user was created
    created_at: datetime = Field(default_factory=None, nullable=False)

    # Time when the user was last updated
    updated_at: datetime = Field(default_factory=None, nullable=False)



class BlacklistedTokens(SQLModel, table=True):
    """
    SQL Model representing a blacklisted token.
    """

    # UUID primary key
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)

    # Token
    token: str

    # Time when the token was blacklisted
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
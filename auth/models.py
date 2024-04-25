import re
from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber


class RegisterUser(BaseModel):
    """
    Pydantic model representing a user registration.
    """

    # User's first name
    first_name: str = Field(
        title="First name",
        description="User first name",
        min_length=3,
        max_length=50,
        examples=["John"],
        pattern="^[a-zA-Z]+$",  # Only allows alphabetic characters
    )

    # User's last name
    last_name: str = Field(
        title="Last name",
        description="User last name",
        min_length=3,
        max_length=50,
        examples=["Doe"],
        pattern="^[a-zA-Z]+$",  # Only allows alphabetic characters
    )

    # User's email
    email: EmailStr = Field(
        title="E-mail", description="User e-mail", examples=["nG9uE@example.com"]
    )

    # User's password
    password: str = Field(
        title="Password",
        description="User password. Must contain at least one capital letter, one small letter, one digit and one special character. Must be at least 8 characters long",
        min_length=8,
        max_length=64,
        examples=["Password123$"],
    )

    @field_validator("password")
    def validate_password(cls, v):
        """
        Validates the password field.

        Args:
            cls: The class itself.
            v: The value to be validated.

        Raises:
            ValueError: If the password does not meet the requirements.
        """
        password_pattern = (
            r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,64}$"
        )
        if not re.match(password_pattern, v):
            raise ValueError("Invalid password format.")
        return v


class LoginUser(BaseModel):
    """
    Pydantic model representing a user login.
    """

    # User's email
    email: EmailStr = Field(
        title="E-mail", description="User e-mail", examples=["nG9uE@example.com"]
    )
    #: User's email

    # User's password
    password: str = Field(title="Password", description="User password")


class EmailData(BaseModel):
    """
    Pydantic model representing the data of an email.
    """

    #: The HTML content of the email.
    html_content: str = Field(
        title="HTML content", description="The HTML content of the email."
    )

    #: The subject of the email.
    subject: str = Field(title="Subject", description="The subject of the email.")


class NewPassword(BaseModel):
    """
    Pydantic model representing a new password for a user.

    Attributes:
        new_password (str): The new password for the user. Must contain at least one capital letter, one small letter, one digit and one special character. Must be at least 8 characters long.
    """

    #: The new password for the user. Must contain at least one capital letter, one small letter, one digit and one special character. Must be at least 8 characters long.
    new_password: str = Field(
        title="Password",
        description="User password. Must contain at least one capital letter, one small letter, one digit and one special character. Must be at least 8 characters long",
        min_length=8,  # Must be at least 8 characters long
        max_length=64,  # Must be at most 64 characters long
        examples=["Password123$"],  # An example of a valid password
    )

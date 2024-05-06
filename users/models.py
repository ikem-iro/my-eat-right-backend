from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber






# Pydantic model representing a user prompt for a model
class Prompt(BaseModel):
    """
    Pydantic model representing a user prompt for a model.

    Attributes:
        query (str): The query for the model.
    """
    # The query for the model
    query: str = Field(
        title="Query",  # The title of the field
        description="Query for model",  # The description of the field
    )




class UpdateUser(BaseModel):
    """
    Pydantic model representing a user update.

    Attributes:
        first_name (Optional[str]): User's first name.
        last_name (Optional[str]): User's last name.
        username (Optional[str]): User's username.
        phone_number (Optional[PhoneNumber]): User's phone number.
    """

    # User's first name
    first_name: str | None = Field(
        title="First Name",
        description="User's first name",
        examples=["John"],
        default=None
    )

    # User's last name
    last_name: str | None = Field(
        title="Last Name",
        description="User's last name",
        examples=["Doe"],
        default=None
    )

    # User's username
    username: str | None = Field(
        title="Username",
        description="User's username",
        examples=["JohnDoe"],
        default=None
    )

    # User's phone number
    phone_number: PhoneNumber | None = Field(
        title="Phone Number",
        description="User's phone number",
        examples=["+2348123456789"],
        default=None
    )

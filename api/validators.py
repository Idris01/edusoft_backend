from django.conf import settings
from rest_framework import status
import re


def validate_password(password, confirm_password):
    """Check for password validity"""

    if (password is None) or (confirm_password is None):
        return (
            dict(password=["password and confirm_password field required"]),
            status.HTTP_400_BAD_REQUEST,
        )

    elif password != confirm_password:
        return (dict(password=["password mismatch"]), status.HTTP_400_BAD_REQUEST)
    elif len(password) < settings.MINIMUM_PASSWORD_SIZE:
        return (dict(password=["password too short"]), status.HTTP_400_BAD_REQUEST)
    elif re.search(r"[\s]+", password):
        return (
            dict(password=["password must not include space"]),
            status.HTTP_400_BAD_REQUEST,
        )
    elif not all(
        (
            re.search("[a-z]+", password),
            re.search("[A-Z]+", password),
            re.search("[^a-zA-z0-9]+", password),
            re.search("[0-9]+", password),
        )
    ):
        return (
            dict(
                password=[
                    " ".join(
                        (
                            "password must have lower",
                            "and uppercase, number and special char",
                        )
                    )
                ]
            ),
            status.HTTP_400_BAD_REQUEST,
        )

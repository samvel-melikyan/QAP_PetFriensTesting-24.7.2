import secrets
valid_email = "vasya@mail.com"
invalid_email = "vasya@.com"
valid_password = "12345"
invalid_password = "   "


def invalid_auth_key(length=56):
    """Generate a secure authentication key with the given length."""
    return secrets.token_hex(length // 2)

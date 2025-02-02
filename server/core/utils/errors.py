from fastapi import HTTPException, status

cred_exp = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="could_not_validate_credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
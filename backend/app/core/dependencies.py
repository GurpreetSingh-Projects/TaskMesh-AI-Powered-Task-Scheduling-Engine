from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.features.auth.dependencies import get_auth_service
from app.features.auth.services import AuthService
from app.features.users.enums import UserRoles

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/swagger-login")


def require_roles(allowed_roles: list[UserRoles]):
    async def checker(
        token: str = Depends(oauth2_scheme),
        auth_service: AuthService = Depends(get_auth_service),
    ):
        return await auth_service.require_roles(
            allowed_roles=allowed_roles, token=token
        )

    return checker

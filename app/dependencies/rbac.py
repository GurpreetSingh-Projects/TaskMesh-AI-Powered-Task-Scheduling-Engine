from fastapi import Depends, HTTPException
from ..models.user_roles import UserRoles
from ..dependencies.auth import getCurrentUser

def require_roles(*allowed_roles: UserRoles):
    async def role_checker(current_user= Depends(getCurrentUser)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden Action!!")
        
        return current_user
    
    return role_checker
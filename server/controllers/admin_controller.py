from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..core.utils.auth import authenticate, create_access_token
from ..core.utils.hashing import get_password_hash, verify_password
from ..repositories.admin_repository import *
from ..repositories.user_repository import get_user_by_id, get_active_and_total_users_count, update_user_profile_data_by_id
from ..schemas.admin_schemas.request import *
from ..schemas.admin_schemas.response import *
from ..schemas.base_schemas import TokenData, AdminData

def register(req: AdminRegisterRequestSchema) -> AdminRegisterResponseSchema:
    try:
        if get_admin_by_email(req.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email_already_registered"
            )
        
        hashed_password = get_password_hash(req.password)
        
        create_admin(req.email, hashed_password);
        
        return AdminRegisterResponseSchema(status_code=201)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
   
    
def login(req: OAuth2PasswordRequestForm) -> AdminLoginResponseSchema:
    try:
        admin = authenticate(req.username, req.password, isAdmin=True)
        
        access_token = create_access_token(data={"admin_id": admin.id})
        
        return AdminLoginResponseSchema(status_code=status.HTTP_200_OK, access_token=access_token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  
        
def get_profile_data(token: TokenData) -> AdminGetProfileDataResponseSchema:
    try:
        admin = get_admin_by_id(token.admin_id)
        return AdminGetProfileDataResponseSchema(
            status_code=status.HTTP_200_OK,
            profile_data=AdminData(
                email=admin.email,
                full_name=admin.full_name,
                phone=admin.phone, 
                address=admin.address,
                country=admin.country,
                disabled=admin.disabled
            )
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
def get_dashboard_data(token: TokenData) -> AdminGetDashboardDataResponseSchema:
    try:
        users_data = get_active_and_total_users_count()
        admins_data = get_total_admins_count()
        
        return AdminGetDashboardDataResponseSchema(
            status_code=status.HTTP_200_OK,
            dashboard_data=DashboardData(
                total_users=users_data.total_users,
                active_users=users_data.active_users,
                inactive_users=users_data.total_users - users_data.active_users,
                total_admins=admins_data.total_admins
            )
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

def update_profile_data(req: AdminUpdateProfileDataRequestSchema, token: TokenData) -> AdminUpdateProfileDataResponseSchema:
    try:
        update_data: dict = {k: v for k, v in req.update_data.model_dump().items() if v is not None}
        update_admin_profile_data_by_id(token.admin_id, update_data)
        return AdminUpdateProfileDataResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
     
def update_password(req: AdminUpdatePasswordRequestSchema, token: TokenData) -> AdminUpdatePasswordResponseSchema:
    try:
        admin = get_admin_by_id(token.admin_id)
        if not verify_password(req.curr_password, admin.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password_not_matched")
        
        hashed_password = get_password_hash(req.new_password)
        update_admin_password_by_id(token.admin_id, {'hashed_password': hashed_password})
            
        return AdminUpdatePasswordResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
def enable_or_disable(req: AdminEnableOrDisableRequestSchema, token: TokenData) -> AdminEnableOrDisableResponseSchema:
    try:
        user = get_user_by_id(req.user_id)
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_not_found")
        
        update_user_profile_data_by_id(req.user_id, {'disabled': not user.disabled})
        return AdminEnableOrDisableResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
def delete(token: TokenData) -> AdminDeleteResponseSchema:
    try:
        delete_admin_by_id(token.admin_id)
        return AdminDeleteResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
from fastapi import HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from ...core.utils.auth import authenticate, gen_access_token
from ...core.utils.hashing import get_password_hash, verify_password
from ...repositories.activity_repository import *
from ...repositories.admin_repository import *
from ...repositories.session_repository import *
from ...repositories.user_repository import *
from ...schemas.admin_schemas.request import *
from ...schemas.admin_schemas.response import *
from ...schemas.base_schemas import TokenData, AdminData

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
   
    
def login(req_body: OAuth2PasswordRequestForm, request: Request, response: Response) -> AdminLoginResponseSchema:
    try:
        admin = authenticate(req_body.email, req_body.password, is_admin=True)
        
        # access_token = gen_access_token(data={"admin_id": admin.id})
        
        ip_address = request.client.host
        
        session = create_session(
            admin_id=admin.id,
            is_admin=True,
            ip_address=ip_address,
        )
        
        response.set_cookie(
            key=getenv('SESSION_COOKIE_NAME'),
            value=session.session_id,
            httponly=True,
            secure=False,
            samesite="Lax"
        )
        
        return AdminLoginResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  

def logout(request: Request, response: Response) -> AdminLogoutResponseSchema:
    try:
        session_id = request.cookies.get(getenv('SESSION_COOKIE_NAME'))

        if session_id:
            delete_session_by_session_id(session_id)

        response.delete_cookie(getenv('SESSION_COOKIE_NAME'))

        return AdminLogoutResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))  

        
def get_profile_data(session_id: str) -> AdminGetProfileDataResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        admin = get_admin_by_id(session.admin_id)
        return AdminGetProfileDataResponseSchema(
            status_code=status.HTTP_200_OK,
            profile_data=AdminData(
                id=admin.id,
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
    
    
def get_dashboard_data() -> AdminGetDashboardDataResponseSchema:
    try:
        users_data = get_user_data()
        admins_data = get_admin_data()
        
        return AdminGetDashboardDataResponseSchema(
            status_code=status.HTTP_200_OK,
            dashboard_data=DashboardData(
                total_users=users_data.total_users,
                active_users=users_data.active_users,
                inactive_users=users_data.total_users - users_data.active_users,
                verified_users=users_data.verified_users,
                unverified_users=users_data.total_users - users_data.verified_users,
                total_admins=admins_data.total_admins
            )
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

def update_profile_data(req_body: AdminUpdateProfileDataRequestSchema, session_id: str) -> AdminUpdateProfileDataResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        update_data: dict = {k: v for k, v in req_body.update_data.model_dump().items() if v is not None}
        update_admin_profile_data_by_id(session.admin_id, update_data)
        return AdminUpdateProfileDataResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
     
def update_password(req_body: AdminUpdatePasswordRequestSchema, session_id: str) -> AdminUpdatePasswordResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        admin = get_admin_by_id(session.admin_id)
        if not verify_password(req_body.curr_password, admin.hashed_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password_not_matched")
        
        hashed_password = get_password_hash(req_body.new_password)
        update_admin_password_by_id(session.admin_id, {'hashed_password': hashed_password})
            
        return AdminUpdatePasswordResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
def update_user_password(req_body: AdminUpdateUserPasswordRequestSchema, session_id: str, request: Request) -> AdminUpdateUserPasswordResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        hashed_password = get_password_hash(req_body.new_password)
        update_user_password_by_id(req_body.user_id, {'hashed_password': hashed_password})
        
        ip_address = request.client.host
        create_activity(user_id=req_body.user_id, admin_id=session.admin_id, activity_type=ActivityType.PASSWORD_RESET, ip_address=ip_address)
            
        return AdminUpdateUserPasswordResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
def enable_or_disable(req_body: AdminEnableOrDisableRequestSchema, session_id: str, request: Request) -> AdminEnableOrDisableResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        user = get_user_by_id(req_body.user_id)
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_not_found")
        
        update_user_profile_data_by_id(req_body.user_id, {'disabled': not user.disabled})
        
        ip_address = request.client.host
        create_activity(user_id=user.id, admin_id=session.admin_id, activity_type=ActivityType.ENABLE_OR_DISABLE, ip_address=ip_address)
        
        return AdminEnableOrDisableResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
def delete(session_id: str) -> AdminDeleteResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        delete_admin_by_id(session.admin_id)
        return AdminDeleteResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
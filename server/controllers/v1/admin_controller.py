from fastapi import HTTPException, status, Request, Response
import user_agents
from ...core.utils.auth import *
from ...core.utils.hashing import get_password_hash, verify_password
from ...core.utils.network import get_ip_info
from ...repositories.activity_repository import *
from ...repositories.admin_repository import *
from ...repositories.session_repository import *
from ...repositories.user_repository import *
from ...schemas.admin_schemas.request import *
from ...schemas.admin_schemas.response import *
from ...schemas.base_schemas import *



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
   
    
async def login(req_body: AdminLoginRequestSchema, request: Request, response: Response) -> AdminLoginResponseSchema:
    try:
        await check_login_attempts(req_body.email)
        admin = await authenticate(req_body.email, req_body.password, is_admin=True)
        
        ip_address = request.client.host
        user_agent = user_agents.parse(request.headers.get('user-agent'))
        
        session = create_session(
            admin_id=admin.id,
            is_admin=True,
            ip_address=ip_address,
            device=user_agent.device.family,
            os=user_agent.os.family,
            browser=user_agent.browser.family
        )
        
        response.set_cookie(
            key=getenv('SESSION_COOKIE_NAME'),
            value=session.session_id,
            httponly=True,
            secure=False,
            samesite="Lax"
        )
        
        ip_info = get_ip_info(request)
        create_activity(session_id=session.session_id, activity_type=ActivityType.LOGIN, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))
        
        return AdminLoginResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  

def logout(request: Request, response: Response) -> AdminLogoutResponseSchema:
    try:
        session_id = request.cookies.get(getenv('SESSION_COOKIE_NAME'))

        # if session_id:
        #     delete_session_by_session_id(session_id)

        response.delete_cookie(getenv('SESSION_COOKIE_NAME'))
        
        ip_info = get_ip_info(request)
        create_activity(session_id=session_id, activity_type=ActivityType.LOGOUT, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))

        return AdminLogoutResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))  


def get_users() -> AdminGetUsersResponseSchema:
    try:
        users = get_all_users()
        
        return AdminGetUsersResponseSchema(
            status_code=status.HTTP_200_OK,
            users_data=[
                UserData(
                    id=u.id,
                    email=u.email
                )
                for u in users
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

        
def get_profile_data(session_id: str, user_id: Optional[int] = None) -> AdminGetProfileDataResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        entity = get_admin_by_id(session.admin_id) if not user_id else get_user_by_id(user_id)
        return AdminGetProfileDataResponseSchema(
            status_code=status.HTTP_200_OK,
            profile_data=ProfileData(
                id=entity.id,
                email=entity.email,
                full_name=entity.full_name,
                phone=entity.phone, 
                address=entity.address,
                country=entity.country,
                disabled=entity.disabled
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
    

def get_sessions() -> AdminGetSessionsResponseSchema:
    try:
        sessions = get_all_sessions()
        
        return AdminGetSessionsResponseSchema(
            status_code=status.HTTP_200_OK,
            sessions_data=[
                SessionData(
                    session_id=s.session_id,
                    user_id=s.user_id,
                    admin_id=s.admin_id,
                    is_admin=s.is_admin,
                    ip_address=s.ip_address,
                    device=s.device,
                    os=s.os,
                    browser=s.browser,
                    created_at=s.created_at.strftime("%B %d, %Y at %I:%M %p"),
                    expired_at=s.expired_at.strftime("%B %d, %Y at %I:%M %p")
                )
                for s in sessions
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def get_activities() -> AdminGetActivitiesResponseSchema:
    try:
        activities = get_all_activities()
        
        return AdminGetActivitiesResponseSchema(
            status_code=status.HTTP_200_OK,
            activities_data=[
                ActivityData(
                    id=a.id,
                    session_id=a.session_id,
                    user_id=a.user_id,
                    activity_type=a.activity_type,
                    timestamp=a.timestamp.strftime("%B %d, %Y at %I:%M %p"),
                )
                for a in activities
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def update_profile_data(req_body: AdminUpdateProfileDataRequestSchema, session_id: str, request: Request, user_id: Optional[int] = None) -> AdminUpdateProfileDataResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        update_data: dict = {k: v for k, v in req_body.update_data.model_dump().items() if v is not None}
        update_admin_profile_data_by_id(session.admin_id, update_data) if not user_id else update_user_profile_data_by_id(user_id, update_data)
        
        ip_info = get_ip_info(request)
        create_activity(session_id=session_id, activity_type=ActivityType.UPDATE_PROFILE, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))
        return AdminUpdateProfileDataResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
     
def update_password(req_body: AdminUpdatePasswordRequestSchema, session_id: str, request: Request, user_id: Optional[int] = None) -> AdminUpdatePasswordResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        if not user_id:
            admin = get_admin_by_id(session.admin_id)
            if not verify_password(req_body.curr_password, admin.hashed_password):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password_not_matched")
        
        hashed_password = get_password_hash(req_body.new_password)
        update_admin_password_by_id(session.admin_id, {'hashed_password': hashed_password}) if not user_id else update_user_password_by_id(user_id, {'hashed_password': hashed_password})
        
        ip_info = get_ip_info(request)
        create_activity(session_id=session_id, user_id=user_id, activity_type=ActivityType.PASSWORD_RESET, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))
            
        return AdminUpdatePasswordResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
def enable_or_disable(req_body: AdminEnableOrDisableRequestSchema, session_id: str, request: Request) -> AdminEnableOrDisableResponseSchema:
    try:
        user = get_user_by_id(req_body.user_id)
        
        if user is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user_not_found")
        
        update_user_profile_data_by_id(req_body.user_id, {'disabled': not user.disabled})
        
        ip_info = get_ip_info(request)
        create_activity(session_id=session_id, user_id=user.id, activity_type=ActivityType.ENABLE_OR_DISABLE, public_ip_address=ip_info.get('ip'), city=ip_info.get('city'), region=ip_info.get('region'), country=ip_info.get('country'), isp=ip_info.get('org'))
        
        return AdminEnableOrDisableResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    
def delete(session_id: str, request: Request) -> AdminDeleteResponseSchema:
    try:
        session = get_session_by_session_id(session_id)
        delete_admin_by_id(session.admin_id)
        return AdminDeleteResponseSchema(status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
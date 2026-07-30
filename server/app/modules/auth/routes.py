from fastapi import APIRouter

from app.modules.auth.controller import AuthController
from app.modules.auth.service import AuthService

controller = AuthController(auth_service=AuthService())
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

auth_router.add_api_route("/github/login", controller.github_login, methods=["GET"])

auth_router.add_api_route(
    "/github/callback", controller.github_callback, methods=["GET"]
)

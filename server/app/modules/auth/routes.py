from fastapi import APIRouter, Depends, Request, Response

from app.modules.auth.controller import AuthController
from app.core.dependencies import get_auth_controller

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


async def _github_login(controller: AuthController = Depends(get_auth_controller)):
    return await controller.github_login()


async def _github_callback(
    request: Request,
    code: str,
    state: str,
    controller: AuthController = Depends(get_auth_controller),
):
    return await controller.github_callback(request=request, code=code, state=state)


auth_router.add_api_route("/github/login", _github_login, methods=["GET"])

auth_router.add_api_route("/github/callback", _github_callback, methods=["GET"])

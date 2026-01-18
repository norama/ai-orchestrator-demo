from fastapi import APIRouter, Response

from app.api.response import ResetWorkspaceResponse
from app.api.workflows_dependencies import set_workspace_cookie

workspace_router = APIRouter(prefix="/workspace", tags=["workspace"])


@workspace_router.post("/reset", response_model=ResetWorkspaceResponse)
def reset_workspace(response: Response):
    workspace_name = set_workspace_cookie(response)
    return ResetWorkspaceResponse(
        workspace_name=workspace_name,
        status="ok",
    )

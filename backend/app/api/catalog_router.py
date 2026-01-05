from fastapi import APIRouter, Depends

from app.api.workflows_dependencies import get_workflow_repository, get_workflow_service_for_creation
from app.application.exceptions import CatalogItemNotFound
from app.domain.catalog import DEMO_CATALOG, WorkflowStateCreateFromCatalog
from app.domain.catalog_response import CatalogItemResponse, CatalogResponse
from app.domain.response import WorkflowDetailResponse
from app.domain.workflow import WorkflowCreate
from app.infrastructure.persistence.workflow_repository import WorkflowRepository

catalog_router = APIRouter(prefix="/catalog", tags=["workflows", "catalog"])


@catalog_router.get("", response_model=CatalogResponse)
def list_catalog_items():
    items = [CatalogItemResponse(**item.model_dump(exclude={"source_dump"})) for item in DEMO_CATALOG]
    return CatalogResponse(
        items=items,
        status="ok",
    )


@catalog_router.post("/workflows", response_model=WorkflowDetailResponse)
def create_workflow_from_catalog(
    req: WorkflowStateCreateFromCatalog,
    repo: WorkflowRepository = Depends(get_workflow_repository),
):
    catalog_item = next(
        (item for item in DEMO_CATALOG if item.id == req.item_id),
        None,
    )
    if not catalog_item:
        raise CatalogItemNotFound(f"Catalog item {req.item_id} not found")

    create_req = WorkflowCreate(
        ticket=catalog_item.to_ticket(),
        domain_type=catalog_item.domain_type,
        name=req.name,
        description=req.description,
        max_steps=req.max_steps,
    )
    service = get_workflow_service_for_creation(create_req, repo=repo)

    workflow = service.create(create_req)

    return WorkflowDetailResponse(
        workflow_id=workflow.id,
        status="created",
        workflow=workflow,
        waiting_reason=service.get_waiting_reason(workflow),
        workflow_confidence=service.get_workflow_confidence(workflow),
    )

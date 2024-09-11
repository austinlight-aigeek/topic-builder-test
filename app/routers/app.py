from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.core.utils import UserDep
from app.database.exports import SessionDep
from app.core.utils import get_edit_view_rulesets
from app.templates import html_templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def root(request: Request, user: UserDep, db: SessionDep):
    edit_rulesets, view_rulesets = await get_edit_view_rulesets(user, db)

    return html_templates.landingpage_response(
        request, user, edit_rulesets, view_rulesets
    )

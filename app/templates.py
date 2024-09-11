from fastapi import Request
from fastapi.templating import Jinja2Templates
from typing import Any
from collections.abc import Mapping
from starlette.background import BackgroundTask
from functools import wraps
from app.database.exports import Ruleset, User
from app.expr.exports import default_expression, filters, operators
from app.expr.nodes import Group


class TopicBuilderTemplates(Jinja2Templates):

    @wraps(Jinja2Templates.TemplateResponse)
    def template_response(self, *args, **kwargs):
        return self.TemplateResponse(*args, **kwargs)

    def body_response(
        self,
        request: Request,
        name: str,
        title: str,
        context: dict[str, Any] | None = None,
        status_code: int = 200,
        headers: Mapping[str, str] | None = None,
        media_type: str | None = None,
        background: BackgroundTask | None = None,
    ):
        if context is None:
            context = {}
        if headers is None:
            headers = {}

        return self.template_response(
            request,
            "base.html",
            context | {"body": name, "title": title},
            status_code,
            headers | {"HX-Push-Url": "false"},
            media_type,
            background,
        )

    def modal_response(self, request: Request, title: str, content: str):
        context = {"title": title, "content": content}

        return self.template_response(
            request, "modal.html", context, headers={"HX-Retarget": "#modal"}
        )

    def landingpage_response(
        self,
        request: Request,
        user: User,
        edit_rulesets: list[Ruleset],
        view_rulesets: list[Ruleset],
    ):
        return self.createruleset_response(request, user, edit_rulesets, view_rulesets)

    def createruleset_response(
        self,
        request: Request,
        user: User,
        edit_rulesets: list[Ruleset],
        view_rulesets: list[Ruleset],
    ):
        context = {
            "edit_rulesets": edit_rulesets,
            "view_rulesets": view_rulesets,
            "filters": filters,
            "expression": default_expression,
            "operators": operators,
            "username": user.username,
            "owner": user.username,
        }

        return self.body_response(request, "querybuilder.html", "Create Topic", context)

    def editruleset_response(
        self,
        request: Request,
        user: User,
        ruleset: Ruleset,
        owner: User,
        edit_rulesets: list[Ruleset],
        view_rulesets: list[Ruleset],
    ):
        expression = Group.model_validate(ruleset.expression).model_dump(
            mode="json", by_alias=True
        )
        context = {
            "edit_rulesets": edit_rulesets,
            "view_rulesets": view_rulesets,
            "fitlers": filters,
            "expression": expression,
            "operators": operators,
            "username": user.username,
            "owner": owner.username,
            "ruleset": ruleset,
        }

        return self.body_response(
            request, "querybuilder.html", f"Edit Topic - {ruleset.name}", context
        )

    def viewruleset_response(
        self,
        request: Request,
        user: User,
        ruleset: Ruleset,
        owner: User,
        edit_rulesets: list[Ruleset],
        view_rulesets: list[Ruleset],
    ):
        expression = Group.model_validate(ruleset.expression).model_dump(
            mode="json", by_alias=True
        )
        context = {
            "edit_rulesets": edit_rulesets,
            "view_rulesets": view_rulesets,
            "filters": filters,
            "expression": expression,
            "operators": operators,
            "username": user.username,
            "owner": owner.username,
            "ruleset": ruleset,
        }

        return self.body_response(
            request, "querybuilder.html", f"View Topic - {ruleset.name}", context
        )


html_templates = TopicBuilderTemplates(directory=["templates/html"])

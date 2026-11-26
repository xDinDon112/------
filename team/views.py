import json

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_safe

DATA_DIR = settings.BASE_DIR / "data"


def read_json(filename):
    with (DATA_DIR / filename).open(encoding="utf-8") as source:
        return json.load(source)


@require_safe
def index(request):
    team = read_json("team.json")
    projects = read_json("projects.json")

    skills = team["skills"]
    selected = request.GET.get("skill", "all")
    if selected not in skills:
        selected = "all"

    visible_members = []
    for member in team["members"]:
        if selected != "all" and selected not in member["skills"]:
            continue
        skill_labels = [skills[key] for key in member["skills"] if key in skills]
        visible_members.append({**member, "skill_labels": skill_labels})

    return render(
        request,
        "index.html",
        {
            "team": team,
            "projects": projects,
            "members": visible_members,
            "selected": selected,
            "selected_label": skills.get(selected),
        },
    )

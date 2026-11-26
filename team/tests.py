import json

from django.conf import settings
from django.contrib.staticfiles import finders
from django.test import SimpleTestCase
from django.urls import reverse
from django.utils.html import escape


class SiteTests(SimpleTestCase):
    def setUp(self):
        data = settings.BASE_DIR / "data"
        self.team = json.loads((data / "team.json").read_text(encoding="utf-8"))
        self.projects = json.loads((data / "projects.json").read_text(encoding="utf-8"))
        self.home = reverse("home")

    def test_home_shows_all_members_and_projects(self):
        response = self.client.get(self.home)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [member["name"] for member in response.context["members"]],
            [member["name"] for member in self.team["members"]],
        )
        self.assertContains(response, 'class="card member-card"', count=len(self.team["members"]))
        for project in self.projects:
            self.assertContains(response, escape(project["title"]))

    def test_skill_filter(self):
        for skill in self.team["skills"]:
            with self.subTest(skill=skill):
                response = self.client.get(self.home, {"skill": skill})
                expected = [
                    member["name"]
                    for member in self.team["members"]
                    if skill in member["skills"]
                ]
                self.assertEqual(response.context["selected"], skill)
                self.assertEqual(
                    [member["name"] for member in response.context["members"]],
                    expected,
                )

    def test_unknown_filter_shows_all_members(self):
        response = self.client.get(self.home, {"skill": "unknown-skill"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["selected"], "all")
        self.assertEqual(len(response.context["members"]), len(self.team["members"]))

    def test_project_assets_are_available(self):
        for asset in ("style.css", "images/hero-desktop.svg", "images/hero-mobile.svg", "images/favicon.svg"):
            with self.subTest(asset=asset):
                self.assertIsNotNone(finders.find(asset))

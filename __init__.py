"""SearXNG plugin — search tool and bundled internet-search skill."""
from pathlib import Path

from . import schemas, tools


def _register_bundled_skills(ctx) -> None:
    skills_dir = Path(__file__).parent / "skills"
    if not skills_dir.is_dir():
        return
    for child in sorted(skills_dir.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)


def register(ctx):
    ctx.register_tool(
        name="searxng",
        schema=schemas.SEARXNG,
        handler=tools.searxng_handler,
        toolset="searxng",
    )
    _register_bundled_skills(ctx)

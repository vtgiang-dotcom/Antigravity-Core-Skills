"""Tests for .github/scripts/boundary_audit.py — harness/project boundary.

The audit's job is to catch PROJECT code that leaked into a harness directory.
Its failure mode is therefore two-sided: missing a real leak, or crying wolf
until people ignore it. The mcp-builder skill ships an XML data asset its
scripts read, which the extension allowlist flagged on every run — chasing
that noise with a global ".xml" entry would have blinded the audit everywhere.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / ".github" / "scripts" / "boundary_audit.py"


def _load_audit():
    spec = importlib.util.spec_from_file_location("boundary_audit_module", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def audit():
    return _load_audit()


SKILL_MIRRORS = [
    ".kilo/skill",
    ".claude/skills",
    ".copilot/skill",
    ".gemini/antigravity/skills",
]


def test_skill_data_asset_is_not_reported(audit, tmp_path):
    """An .xml under a skill directory is skill content, not project code."""
    f = tmp_path / ".kilo" / "skill" / "mcp-builder" / "scripts" / "example_evaluation.xml"
    f.parent.mkdir(parents=True)
    f.write_text("<evaluation><qa_pair/></evaluation>\n", encoding="utf-8")

    report, reason = audit.should_report(f, tmp_path)

    assert report is False
    assert "skill data asset" in reason


@pytest.mark.parametrize("mirror", SKILL_MIRRORS)
def test_every_skill_mirror_is_allowed(audit, tmp_path, mirror):
    """The allowance is by path shape, so it holds for every engine mirror."""
    f = tmp_path / mirror / "mcp-builder" / "scripts" / "example_evaluation.xml"
    f.parent.mkdir(parents=True)
    f.write_text("<evaluation/>\n", encoding="utf-8")

    report, _ = audit.should_report(f, tmp_path)

    assert report is False


def test_stray_xml_outside_skill_is_still_reported(audit, tmp_path):
    """Regression: the exception must not become a global .xml allowance.

    A project XML file dropped straight into a harness dir is exactly the
    leak this audit exists to catch.
    """
    f = tmp_path / ".kilo" / "leaked_schema.xml"
    f.parent.mkdir(parents=True)
    f.write_text("<schema/>\n", encoding="utf-8")

    report, reason = audit.should_report(f, tmp_path)

    assert report is True
    assert "non-harness extension" in reason


def test_real_mcp_builder_asset_is_clean(audit):
    """End-to-end: the shipped asset must not appear as an audit finding."""
    real = (
        ROOT / ".kilo" / "skill" / "mcp-builder" / "scripts"
        / "example_evaluation.xml"
    )
    assert real.is_file(), "expected the mcp-builder example asset to exist"

    report, reason = audit.should_report(real, ROOT)

    assert report is False, reason


def test_real_repo_audit_has_no_xml_findings(audit):
    """The repo's own audit must not flag any .xml file."""
    warnings, _errors, _info = audit.audit(ROOT)

    offenders = [w for w in warnings if ".xml" in w]

    assert not offenders, f"audit still flags skill assets: {offenders}"

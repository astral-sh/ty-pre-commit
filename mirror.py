# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "packaging==23.1",
#   "urllib3==2.0.5",
# ]
# ///
"""Update ty-pre-commit to the latest version of ty."""

import os
import re
import subprocess
import typing
from datetime import datetime
from pathlib import Path

import urllib3
from packaging.version import Version


def main():
    current_ty_version = get_current_ty_version()
    dispatched_version = os.environ.get("TY_VERSION")
    if dispatched_version:
        ty_releases = None
        target_versions = [Version(dispatched_version)]
    else:
        ty_releases = get_releases(package="ty")
        target_versions = list(ty_releases)

    target_versions = sorted(v for v in target_versions if v > current_ty_version)
    if not target_versions:
        return

    uv_releases = get_releases(package="uv")

    for ty_version in target_versions:
        if ty_releases is None:
            uv_version = max(uv_releases)
        else:
            uv_version = get_latest_version(
                releases=uv_releases, released_at=ty_releases[ty_version]
            )
        paths = process_version(ty_version=ty_version, uv_version=uv_version)
        if subprocess.check_output(["git", "status", "-s"]).strip():
            subprocess.run(["git", "add", *paths], check=True)
            subprocess.run(["git", "commit", "-m", f"Mirror: {ty_version}"], check=True)
            subprocess.run(["git", "tag", f"v{ty_version}"], check=True)
        else:
            print(f"No change v{ty_version}")


def get_releases(package: str) -> dict[Version, datetime]:
    response = urllib3.request("GET", f"https://pypi.org/pypi/{package}/json")
    if response.status != 200:
        raise RuntimeError(f"Failed to fetch {package} versions from PyPI")

    releases = {}
    for version, files in response.json()["releases"].items():
        if files:
            releases[Version(version)] = min(
                datetime.fromisoformat(file["upload_time_iso_8601"]) for file in files
            )
    return releases


def get_latest_version(
    releases: dict[Version, datetime], released_at: datetime
) -> Version:
    return max(
        version
        for version, release_time in releases.items()
        if release_time <= released_at
    )


def get_current_ty_version() -> Version:
    content = (Path(__file__).parent / ".pre-commit-hooks.yaml").read_text()
    versions = set(re.findall(r"--ty-version=(\S+)", content))
    assert len(versions) == 1, ".pre-commit-hooks.yaml does not have one ty version"
    return Version(versions.pop())


def process_version(ty_version: Version, uv_version: Version) -> typing.Sequence[str]:
    def replace_pyproject_toml(content: str) -> str:
        return re.sub(r'"uv==.*"', f'"uv=={uv_version}"', content)

    def replace_pre_commit_hooks_yaml(content: str) -> str:
        return re.sub(r"--ty-version=\S+", f"--ty-version={ty_version}", content)

    def replace_readme_md(content: str) -> str:
        content = re.sub(r"rev: v\d+\.\d+\.\d+", f"rev: v{ty_version}", content)
        content = re.sub(r'rev = "v\d+\.\d+\.\d+"', f'rev = "v{ty_version}"', content)
        return re.sub(r"/ty/\d+\.\d+\.\d+\.svg", f"/ty/{ty_version}.svg", content)

    paths = {
        "pyproject.toml": replace_pyproject_toml,
        ".pre-commit-hooks.yaml": replace_pre_commit_hooks_yaml,
        "README.md": replace_readme_md,
    }

    for path, replacer in paths.items():
        with open(path) as f:
            content = replacer(f.read())
        with open(path, mode="w") as f:
            f.write(content)

    return tuple(paths.keys())


if __name__ == "__main__":
    main()

# ty-pre-commit

[![image](https://img.shields.io/pypi/v/ty/0.0.46.svg)](https://pypi.python.org/pypi/ty)
[![image](https://img.shields.io/pypi/l/ty/0.0.46.svg)](https://pypi.python.org/pypi/ty)
[![image](https://img.shields.io/pypi/pyversions/ty/0.0.46.svg)](https://pypi.python.org/pypi/ty)
[![Actions status](https://github.com/astral-sh/ty-pre-commit/workflows/main/badge.svg)](https://github.com/astral-sh/ty-pre-commit/actions)

A [pre-commit](https://pre-commit.com/) hook for running [ty](https://github.com/astral-sh/ty)
quickly over your whole Python project.

The hook uses the dependencies declared in your project's `pyproject.toml`, so your project
configuration remains the single source of truth: you do not need to duplicate type-checking
dependencies in the hook's `additional_dependencies` setting. By default, uv installs the project's [`dev`
dependency group](https://docs.astral.sh/uv/concepts/projects/dependencies/#default-groups); use
`tool.uv.default-groups` to customize which groups are installed.
Any dependencies listed in the hook's `additional_dependencies` setting will be ignored by ty.

Under the hood, the hook runs [uv](https://github.com/astral-sh/uv)'s preview
[`uv check`](https://docs.astral.sh/uv/reference/cli/#uv-check) command. Each hook revision pins both
the corresponding ty version and the latest uv version that was available when that ty version was
released. New ty releases trigger ty-pre-commit releases; new uv releases do not trigger releases
on their own. The full uv command invoked by the hook can be found in
[`.pre-commit-hooks.yaml`](.pre-commit-hooks.yaml).

### Using ty with pre-commit

To run ty via pre-commit, add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
- repo: https://github.com/astral-sh/ty-pre-commit
  # ty version.
  rev: v0.0.46
  hooks:
    - id: ty
```

Configure ty in your project's `pyproject.toml` or `ty.toml`; see
[ty's configuration reference](https://docs.astral.sh/ty/reference/configuration/).

The `ty` hook uses uv's normal project behavior. It may create or update `uv.lock`, create a local
virtual environment if one does not exist, and sync the local virtual environment before checking
the project.

The `ty` hook accepts additional [`uv check`](https://docs.astral.sh/uv/reference/cli/#uv-check)
arguments. If you do not want the hook to create or update your project's lockfile or local virtual
environment, use uv's isolated mode:

```yaml
hooks:
  - id: ty
    args: [--isolated]
```

`--isolated` resolves and installs the project's declared requirements into a temporary virtual
environment. It leaves the project's existing virtual environment and lockfile unchanged, and does
not create either one if it is missing. It may still populate uv's cache or download a compatible
Python interpreter.

Other synchronization options include:

- `--locked` still syncs the virtual environment, but fails if `uv.lock` is missing or out of date.
- `--frozen` still syncs the virtual environment using `uv.lock` without checking or updating it.
- `--no-sync` skips synchronization entirely. Use it only if another step keeps the virtual
  environment up to date.

The hook always runs and does not pass filenames to ty. ty checks the full project according to your
ty configuration, including for deletion-only commits where no Python filename remains for
pre-commit or prek to match.

You can customize which files ty emits diagnostics for using the [`src.include` and `src.exclude` settings](https://docs.astral.sh/ty/exclusions/) in your ty configuration.

Do not set `pass_filenames: true`. `uv check` does not accept positional arguments, so the hook
errors when pre-commit or prek appends filenames to the command.

### Using ty with prek

If you prefer using [prek](https://github.com/j178/prek) instead of
pre-commit, you can define a `prek.toml` file with your hooks:

```toml
[[repos]]
repo = "https://github.com/astral-sh/ty-pre-commit"
rev = "v0.0.46" # ty version.
hooks = [
  { id = "ty" },
]
```

## License

ty-pre-commit is licensed under either of

- Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

Unless you explicitly state otherwise, any contribution intentionally submitted
for inclusion in ty-pre-commit by you, as defined in the Apache-2.0 license, shall be
dually licensed as above, without any additional terms or conditions.

<div align="center">
  <a target="_blank" href="https://astral.sh" style="background:none">
    <img src="https://raw.githubusercontent.com/astral-sh/ty/main/assets/svg/Astral.svg">
  </a>
</div>

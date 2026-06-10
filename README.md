# ty-pre-commit

[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![PyPI version](https://img.shields.io/pypi/v/ty/0.0.46.svg)](https://pypi.python.org/pypi/ty)
[![License](https://img.shields.io/pypi/l/ty/0.0.46.svg)](https://pypi.python.org/pypi/ty)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/ty/0.0.46.svg)](https://pypi.python.org/pypi/ty)
[![Actions status](https://github.com/astral-sh/ty-pre-commit/workflows/main/badge.svg)](https://github.com/astral-sh/ty-pre-commit/actions)

A [pre-commit](https://pre-commit.com/) hook for running [ty](https://github.com/astral-sh/ty) quickly over your whole Python project.

When ty is invoked by this hook, dependencies declared in your project's `pyproject.toml` will automatically be resolvable by ty. This means your project configuration remains the single source of truth: you do not need to duplicate type-checking dependencies in the hook's `additional_dependencies` setting. Any additional dependencies listed in the hook's `additional_dependencies` setting **will not be resolvable** by ty.

Under the hood, the hook runs [uv](https://github.com/astral-sh/uv)'s preview [`uv check`](https://docs.astral.sh/uv/reference/cli/#uv-check) command. Each hook revision pins both the corresponding ty version and the latest uv version that was available when that ty version was released. New ty releases trigger ty-pre-commit releases; new uv releases do not trigger releases on their own. The full uv command invoked by the hook can be found in [`.pre-commit-hooks.yaml`](.pre-commit-hooks.yaml).

Configure ty in your project's `pyproject.toml` or `ty.toml`: see [ty's configuration reference](https://docs.astral.sh/ty/reference/configuration/).

## Using ty with pre-commit

To run ty via pre-commit, add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
- repo: https://github.com/astral-sh/ty-pre-commit
  # ty version.
  rev: v0.0.46
  hooks:
    - id: ty
```

## Using ty with prek

If you prefer using [prek](https://github.com/j178/prek) instead of pre-commit, you can define a `prek.toml` file with your hooks:

```toml
[[repos]]
repo = "https://github.com/astral-sh/ty-pre-commit"
rev = "v0.0.46" # ty version.
hooks = [
  { id = "ty" },
]
```

## Customizing side effects of the hook

By default, the `ty` hook uses uv's normal behavior with regards to locking and synchronizing projects. The hook's default behavior may therefore create or update a `uv.lock` file, create a local virtual environment if one does not exist, and/or install or update dependencies into a local virtual environment.

However, the `ty` hook accepts all additional arguments accepted by [`uv check`](https://docs.astral.sh/uv/reference/cli/#uv-check). If you do not want the hook to create or update your project's uv lockfile or local virtual environment, use uv's isolated mode:

```yaml
hooks:
  - id: ty
    args: [--isolated]
```

Other options can also be used to further increase the idempotency of the hook, if desired:

```yaml
hooks:
  - id: ty
    args: [--isolated, --no-python-downloads, --no-cache]
```

See the [`uv check` reference documentation](https://docs.astral.sh/uv/reference/cli/#uv-check) for an exhaustive list of options available.

## Customizing files checked by ty

Many pre-commit hooks pass a list of all files modified in that commit to the underlying tool. This can be an effective optimization in many cases, as it can allow a hook to only perform checks on the files that changed in that commit.

Unfortunately, this is not a good model for a pre-commit hook that invokes a type checker. The reason is that a commit that only changes `a.py` can easily cause new diagnostics to appear in `b.py`, even if the commit made no edits to `b.py` (`b.py` might import `a.py`!). As such, this hook does not pass filenames to ty; instead, ty checks the full project according to your ty configuration. You can customize which files ty emits diagnostics for using the [`src.include` and `src.exclude` settings](https://docs.astral.sh/ty/exclusions/) in your ty configuration.

Do not try to override this behavior by setting `pass_filenames: true` in your pre-commit configuration for this hook. `uv check` does not accept positional arguments, so **the hook will error** if pre-commit or prek attempts to pass filenames to the hook.

## Customizing when the hook runs

By default, the hook runs on every commit. This ensures that the hook will run even on commits that only delete Python files. However, it also has the drawback that the hook will run even on commits that do not add, modify or delete any Python files. (pre-commit and prek do not provide ways of distinguishing between commits that delete Python files and commits that only delete non-Python files.)

This behavior can be overridden in your pre-commit configuration by setting `always_run: false`:

```yaml
hooks:
  - id: ty
    always_run: false
```

## Customizing dependencies installed by the hook

As well as your project's base dependencies, uv will also install any dependencies listed in your project's default [dependency groups](https://packaging.python.org/en/latest/specifications/dependency-groups/) (which includes the `dev` group). The [`tool.uv.default-groups`](https://docs.astral.sh/uv/concepts/projects/dependencies/#default-groups) `pyproject.toml` setting can be used to customize your project's default groups.

The hook also accepts uv's standard CLI arguments, which can all be passed as `args` to further customize uv's behavior here. For example:

```yaml
hooks:
  - id: ty
    # to avoid uv installing the `dev` group,
    # but ensure that dependencies in the `typechecking` group are installed:
    args: [--no-default-groups, --group=typechecking]
```

See [the `uv check` reference documentation](https://docs.astral.sh/uv/reference/cli/#uv-check) for a full list of supported flags.

## License

ty-pre-commit is licensed under either of

- Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or <https://www.apache.org/licenses/LICENSE-2.0>)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or <https://opensource.org/licenses/MIT>)

at your option.

Unless you explicitly state otherwise, any contribution intentionally submitted for inclusion in ty-pre-commit by you, as defined in the Apache-2.0 license, shall be dually licensed as above, without any additional terms or conditions.

<div align="center">
  <a target="_blank" href="https://astral.sh" style="background:none">
    <img alt="Astral" src="https://raw.githubusercontent.com/astral-sh/ruff/main/assets/svg/Astral.svg">
  </a>
</div>

# ty-pre-commit

[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v2.json)](https://github.com/astral-sh/ty)
[![image](https://img.shields.io/pypi/v/ty/0.0.30.svg)](https://pypi.python.org/pypi/ty)
[![image](https://img.shields.io/pypi/l/ty/0.0.30.svg)](https://pypi.python.org/pypi/ty)
[![image](https://img.shields.io/pypi/pyversions/ty/0.0.30.svg)](https://pypi.python.org/pypi/ty)
[![Actions status](https://github.com/astral-sh/ty-pre-commit/workflows/main/badge.svg)](https://github.com/astral-sh/ty-pre-commit/actions)

A [pre-commit](https://pre-commit.com/) hook for [ty](https://github.com/astral-sh/ty).

Distributed as a standalone repository to enable installing ty via prebuilt wheels from
[PyPI](https://pypi.org/project/ty/).

### Using ty with pre-commit

To run ty's [type checker](https://docs.astral.sh/ty) via pre-commit, add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
- repo: https://github.com/astral-sh/ty-pre-commit
  # ty version.
  rev: v0.0.30
  hooks:
    # Run the type checker.
    - id: ty
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

# Release instructions

## Release the PyPI package

```
# Bump the version number in pyproject.toml
poetry version [major|minor|patch]

# Commit change

# Release to PyPI
poetry publish
```

## Release the GitHub Action
Create a release in GitHub that corresponds to the current package version. This should trigger the CI workflow which creates the new GitHub Action version.
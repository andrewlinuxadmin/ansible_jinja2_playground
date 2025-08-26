# Version Update Summary - v2.2.0

## Files Updated for Version 2.2.0

### ✅ Core Version Files
- **pyproject.toml**: `version = "2.2.0"`
- **Containerfile**: `version="2.2.0"` in LABEL
- **README.md**: Badge updated to `version-2.2-blue.svg`

### ✅ Example/Demo Files
- **minimal.yml**: `app_version: "2.2.0"`
- **README_URI.md**: `app_version: "2.2.0"` (both examples)

### ✅ New Documentation
- **RELEASE_NOTES_v2.2.md**: Complete v2.2.0 release notes created

## Version References Summary

| File | Previous | Updated | Status |
|------|----------|---------|---------|
| pyproject.toml | 2.1.0 | 2.2.0 | ✅ |
| Containerfile | 1.0.0 | 2.2.0 | ✅ |
| README.md | 2.1 | 2.2 | ✅ |
| minimal.yml | 1.0.0 | 2.2.0 | ✅ |
| README_URI.md | 1.0.0 | 2.2.0 | ✅ |

## Verification Commands

```bash
# Check all version references
grep -r "version.*2\.2" .
grep -r "app_version.*2\.2" .

# Verify container label
podman build -t test . && podman inspect test | jq '.[0].Config.Labels.version'

# Check pyproject.toml
grep "version = " pyproject.toml
```

## Release Checklist

- [x] Update pyproject.toml version
- [x] Update Containerfile LABEL version
- [x] Update README.md badge
- [x] Update example files (minimal.yml, README_URI.md)
- [x] Create RELEASE_NOTES_v2.2.md
- [ ] Test container build with new version
- [ ] Commit changes with version tag
- [ ] Create GitHub release

## Next Steps

1. Test the updated version
2. Build and verify container
3. Commit changes: `git commit -m "Release v2.2.0"`
4. Create tag: `git tag v2.2.0`
5. Push to repository: `git push origin main --tags`

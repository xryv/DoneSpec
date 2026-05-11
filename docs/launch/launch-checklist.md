# v1.0 launch checklist draft

This checklist is for a future DoneSpec v1.0 launch. It does not publish, tag, or release anything by itself.

## Local validation

- [ ] Working tree is clean.
- [ ] `python -m ruff check .` passes.
- [ ] `python -m ruff format --check .` passes.
- [ ] `python -m pytest -q` passes.
- [ ] `donespec validate done.json` passes.

## Strict validation

- [ ] `donespec validate done.json --strict` passes.
- [ ] No DoneSpec checks were weakened to pass validation.

## CI verification

- [ ] CI / self-validation workflow is green.
- [ ] Cross-platform workflow is green on Windows, Linux, and macOS.
- [ ] Package verification workflow is green.

## Package verification

- [ ] Package build gate passes.
- [ ] `twine check dist/*` passes.
- [ ] Local wheel smoke test passes.
- [ ] PyPI smoke test passes after publish.

## Release assets

- [ ] README verification badges render.
- [ ] README positioning remains conservative.
- [ ] CHANGELOG.md is current.
- [ ] GitHub Release copy is reviewed.
- [ ] PyPI copy is reviewed.
- [ ] Repository metadata is reviewed.

## Release publication

- [ ] Release tag is created only after all gates pass.
- [ ] PyPI upload is completed.
- [ ] GitHub Release is published.
- [ ] Published install path is verified.

## Post-launch monitoring

- [ ] Watch GitHub Actions after release.
- [ ] Watch package install reports.
- [ ] Watch issues for packaging, Windows output, schema, and docs problems.
- [ ] Fix defects with normal patch releases. Do not expand scope during launch.

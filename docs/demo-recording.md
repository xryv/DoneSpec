# Demo recording guide

Use this guide to record the forbidden-file demo as a terminal GIF, short video, or README preview asset.

DoneSpec does not require video assets to work. Recordings are only communication material for release notes, README polish, and social previews.

Keep the recording local-first:

- run the demo locally
- avoid cloud recording services
- do not require SaaS tools
- do not add generated binary assets unless the release process explicitly calls for them

## Storyboard

Aim for 15 to 20 seconds:

```text
0-3s   create temporary demo project
3-6s   show baseline done.json contract
6-9s   simulate forbidden README change
9-13s  run DoneSpec and show validation failed
13-16s restore README
16-20s run DoneSpec and show validation passed
```

Suggested title:

```text
AI said done. DoneSpec said no.
```

## Terminal GIF

One practical local workflow is `asciinema` plus `agg`:

```bash
asciinema rec docs/assets/demo.cast
./scripts/demo-forbidden-file.sh
exit
agg docs/assets/demo.cast docs/assets/demo.gif
```

Keep the GIF short and readable:

- 80 to 100 columns
- large terminal font
- no noisy prompt theme
- one clean run
- crop idle time

Do not commit `.cast` or `.gif` files unless the release checklist explicitly asks for generated assets.

## Short video

OBS or any local screen recorder works well:

1. Open a terminal at the repository root.
2. Use a readable font size.
3. Record only the terminal window.
4. Run the PowerShell or Unix demo script.
5. Trim dead time before the first command and after `Demo complete.`

Export as WebM or MP4 for release planning. Keep the source local.

## README preview asset

For a README preview, prefer a compact terminal GIF or a static SVG/PNG if the animation is too large.

GitHub-friendly guidance:

- keep animated GIFs small
- prefer WebM for release pages when supported
- keep text readable at README width
- avoid audio-only context
- preserve the exact failure/pass flow

The preview should communicate one idea:

```text
AI agents can claim completion. DoneSpec verifies the contract.
```

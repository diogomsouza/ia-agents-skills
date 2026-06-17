---
name: gpt-image-2
description: Generate or edit raster images through the OpenAI Images API using the gpt-image-2 model. Use when Codex should create image files with explicit API/model control, save outputs to local paths, generate website or product assets, create concept art, produce mockups, or edit existing bitmap images with gpt-image-2 rather than the built-in image_gen tool. Requires OPENAI_API_KEY for live generation.
---

# GPT Image 2

Generate and edit project-ready bitmap images using the OpenAI Images API with `gpt-image-2`.

## Core Rules

- Use `scripts/gpt_image_2.py`; do not call the built-in `image_gen` tool for this skill's primary workflow.
- Keep `gpt-image-2` as the model. Do not downgrade to another model unless the user explicitly asks.
- Require `OPENAI_API_KEY` for live API calls. Never ask the user to paste the key in chat; ask them to set it in their shell or environment.
- Save final assets under the current project when the image is meant to be consumed by code, docs, slides, or a website.
- Do not overwrite existing assets unless the user explicitly requested replacement. Choose a new descriptive filename.
- Use `--dry-run` first when checking command shape, size, prompt, or output paths.

## Workflow

1. Decide whether the task is `generate` or `edit`.
2. Convert the user's request into a concise production prompt. Preserve exact text the user wants rendered.
3. Pick output settings:
   - draft: `--quality low --size 1024x1024`
   - normal final: `--quality medium --size auto`
   - polished final or text-heavy image: `--quality high`
   - 4K landscape: `--size 3840x2160`
   - 4K portrait: `--size 2160x3840`
4. Run a dry-run command to confirm payload and destination.
5. Run the live command only when `OPENAI_API_KEY` is available.
6. Inspect the output when possible. Check subject, composition, text accuracy, and request constraints.
7. Iterate with one targeted prompt change if the result misses a key requirement.
8. Report the saved path and the final prompt/settings.

## CLI

Generate:

```bash
python "$CODEX_HOME/skills/gpt-image-2/scripts/gpt_image_2.py" generate \
  --prompt "A clean product photo of a matte black ceramic mug on a stone surface, soft studio lighting, no text, no watermark" \
  --quality high \
  --size 1536x1024 \
  --out output/imagegen/mug.png
```

Edit:

```bash
python "$CODEX_HOME/skills/gpt-image-2/scripts/gpt_image_2.py" edit \
  --image input/product.png \
  --prompt "Change only the background to a warm neutral studio backdrop. Keep the product unchanged." \
  --quality high \
  --out output/imagegen/product-edit.png
```

Dry-run:

```bash
python "$CODEX_HOME/skills/gpt-image-2/scripts/gpt_image_2.py" generate \
  --prompt "Test image" \
  --out output/imagegen/test.png \
  --dry-run
```

## Prompt Shape

Use only the fields that help:

```text
Asset type: <website hero, product mockup, icon, concept art, slide visual>
Primary request: <main subject/action>
Input images: <for edits, list image role by path or index>
Style/medium: <photo, illustration, 3D render, UI mockup>
Composition/framing: <close-up, wide, centered, negative space>
Lighting/mood: <lighting and mood>
Text: "<exact text, if any>"
Constraints: <must keep, must avoid>
Avoid: no watermark, no unintended logos, no extra text
```

For edits, repeat invariants clearly: "change only X; keep Y unchanged."

## gpt-image-2 Notes

- `quality`: `low`, `medium`, `high`, or `auto`.
- `size`: `auto` or `WIDTHxHEIGHT`.
- Size constraints for explicit dimensions:
  - max edge `<= 3840px`
  - both edges multiples of `16px`
  - long-to-short ratio `<= 3:1`
  - total pixels between `655360` and `8294400`
- `gpt-image-2` image inputs are high fidelity by default; do not set `input_fidelity`.
- `gpt-image-2` does not support `background=transparent`. For transparent assets, prompt for a flat chroma-key background and remove it locally, or ask the user before switching to a different model.

## Dependencies

Install the Python package in the active environment if needed:

```bash
uv pip install openai
```

If `OPENAI_API_KEY` is missing, tell the user to create a key at `https://platform.openai.com/api-keys` and set it as an environment variable.

## References

- `references/api.md`: parameter and troubleshooting quick reference.
- `scripts/gpt_image_2.py`: generation and edit CLI.

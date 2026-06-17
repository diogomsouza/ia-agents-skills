# gpt-image-2 API Quick Reference

Use this reference only for the `gpt-image-2` skill's API/CLI workflow.

## Endpoints

- Generate: `client.images.generate(...)`
- Edit: `client.images.edit(...)`

## Required Parameters

- `model`: always `gpt-image-2`
- `prompt`: final image instruction
- `size`: `auto` or a valid `WIDTHxHEIGHT`
- `quality`: `low`, `medium`, `high`, or `auto`
- `output_format`: `png`, `jpeg`, or `webp`

## Size Guidance

Popular sizes:

- `1024x1024`: fast square draft
- `1536x1024`: standard landscape
- `1024x1536`: standard portrait
- `2048x1152`: 2K landscape
- `3840x2160`: 4K landscape
- `2160x3840`: 4K portrait
- `auto`: let the API choose

Explicit dimensions must:

- have max edge no larger than `3840`
- be multiples of `16`
- have a long-to-short ratio no greater than `3:1`
- contain between `655360` and `8294400` pixels

## Transparent Backgrounds

`gpt-image-2` does not support native `background=transparent`. Keep this skill on `gpt-image-2`. For simple cutouts, generate on a flat chroma-key background and remove it locally. If the user needs native transparency, ask before using a different model.

## Failure Handling

- Missing API key: ask the user to set `OPENAI_API_KEY`; do not ask them to paste it.
- Missing package: install `openai` in the active environment.
- Unsupported size: choose `auto` or a popular valid size.
- Bad text rendering: retry with shorter exact text, quoted verbatim, and simpler composition.

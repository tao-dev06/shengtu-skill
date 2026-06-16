---
name: jojocode-imagegen
description: Generate images with JOJO Code through an OpenAI-compatible image API. Use when the user asks to create or generate an image with a text prompt, size, and output filename, especially for gpt-5.5 image-generation scenarios that must save the result to a local file and report the saved path.
---

# JOJO Code Image Generation

## Overview

Use this skill to generate a local image file with JOJO Code. The helper script calls the OpenAI-compatible endpoint at `https://api2.jojocode.com/v1` and saves the generated image to disk.

## Inputs

Collect these values from the user or infer safe defaults:

- Image description: required. Pass it as `--prompt`.
- Size: optional. Use `1024x1024` when the user does not specify one.
- Output filename: required. Pass it as `--output`; relative paths are resolved from the current working directory.
- Model: optional. Use `gpt-image-2` unless the user explicitly asks for another image model.

## Secret Handling

Never place the real API key in `SKILL.md`, examples, screenshots, public docs, or files that may be committed. The script reads `JOJO_API_KEY` from the environment, or from a local `.env.local` file beside this skill. Keep `.env.local` private and ignored by git.

## Generate An Image

Run the bundled script:

```powershell
python scripts/generate_image.py --prompt "赛博朋克城市夜景" --size 1024x1024 --output outputs/city.png
```

If the current shell is not inside the skill directory, use the absolute path to the script:

```powershell
python C:\Users\Tao\.codex\skills\jojocode-imagegen\scripts\generate_image.py --prompt "赛博朋克城市夜景" --size 1024x1024 --output outputs/city.png
```

After the command succeeds, tell the user the saved absolute path printed by the script.

## Failure Handling

- If `JOJO_API_KEY` is missing, tell the user to set it in the environment or private `.env.local`.
- If the API returns an error, show the status code and error message without exposing the key.
- If the output path is invalid, ask for a different filename or path.

# Narration WAV Workflow

This repo includes a project-specific batch workflow for turning `script.md` into `.wav` narration files.

The generator only speaks `Body:` content. `Title:` lines are metadata and are not synthesized.

## Quick Start

### PowerShell on Windows

```powershell
.\scripts\generate_body_wavs.ps1
```

### WSL

```bash
scripts/generate_body_wavs.sh ./script.md ./generated/body_wavs
```

Both commands:

- read `script.md`
- extract only `Body:` sections
- generate one `.wav` file per step
- write `manifest.json`

Default output:

```text
generated/body_wavs/
```

## Input Format

The parser expects blocks shaped like this:

```text
Step 01.2
Title: Optional title here
Body: Spoken narration starts here.

Additional narration can continue here.
Blank lines create paragraph pauses in the generated audio.
```

Rules:

- `Step` IDs drive the output filenames
- only `Body:` content is spoken
- blank lines inside a body become short pauses

## Output Files

Each run creates:

- one `.wav` file per step body
- `manifest.json`

The manifest includes:

- `step_id`
- `title`
- original `body`
- normalized `spoken_text`
- output `file`
- `sample_rate`
- `duration_seconds`

## Direct To Unity

You can point the output directly at a Unity project.

### PowerShell

```powershell
.\scripts\generate_body_wavs.ps1 -OutputDir ..\YourUnityProject\Assets\Audio\Narration
```

### WSL

```bash
scripts/generate_body_wavs.sh ./script.md /mnt/c/path/to/YourUnityProject/Assets/Audio/Narration
```

## Default Narration Settings

Current narration settings:

- voice: `af_sarah`
- language: `en-us`
- speed: `0.96`

The generator also does small text cleanups for speech quality, including:

- `OK` -> `okay`
- `#1` -> `number one`
- `12 o'clock` -> `twelve o'clock`

## GPU Check

When the generator starts, it prints the ONNX provider. For GPU-backed generation, look for:

```text
Using ONNX provider: CUDAExecutionProvider
```

If it prints `CPUExecutionProvider`, generation still works, but it will be slower.

## Files To Know

- `script.md`
- `scripts/generate_body_wavs.py`
- `scripts/generate_body_wavs.ps1`
- `scripts/generate_body_wavs.sh`
- `generated/body_wavs/`

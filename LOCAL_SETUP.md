# Local Kokoro-TTS Setup

This checkout is configured for direct `.wav` generation so you can drop output files into a Unity project.

For the step-by-step narration workflow, use `NARRATION_WAV_WORKFLOW.md`.

Default runtime behavior:

- Voice: `af_sarah`
- Accent target: clear neutral American female narration
- Language: `en-us`
- Speed: `0.96`
- ONNX provider: auto-selects `CUDAExecutionProvider` when available, preloads ONNX Runtime CUDA/cuDNN libraries, otherwise falls back to CPU

## What is installed

- Local virtual environment: `.venv`
- Editable package install of this repo
- Model assets:
  - `models/kokoro-v1.0.onnx`
  - `models/voices-v1.0.bin`

## Basic usage

Create a plain text file, then run:

```bash
scripts/generate_wav.sh /path/to/input.txt /path/to/output.wav
```

Example:

```bash
scripts/generate_wav.sh ./example.txt ./example.wav --voice af_sarah --speed 0.96
```

## Output directly into Unity

You can write straight into your Unity project if you want:

```bash
scripts/generate_wav.sh \
  ./line.txt \
  /path/to/YourUnityProject/Assets/Audio/Voice/line_001.wav \
  --voice af_sarah
```

Unity will import the `.wav` after the file appears in `Assets/`.

## Generate only `Body` lines from `script.md`

From your own WSL terminal, run:

```bash
scripts/generate_body_wavs.sh ./script.md ./generated/body_wavs
```

That script:

- extracts only `Body:` content from each step
- writes one `.wav` per step
- writes `manifest.json` with the step IDs, titles, bodies, and output filenames
- reuses one Kokoro session for the whole batch
- slows narration slightly and inserts short pauses between body paragraphs for smoother cadence

From PowerShell on Windows, run:

```powershell
.\scripts\generate_body_wavs.ps1
```

Or:

```powershell
.\scripts\generate_body_wavs.cmd
```
 
## Narration preset

Use this narration preset for project audio generation:

- `--voice af_sarah`
- `--lang en-us`
- `--speed 0.96`

To force a specific provider manually:

```bash
ONNX_PROVIDER=CUDAExecutionProvider scripts/generate_wav.sh ./line.txt ./line.wav
```

To list voices:

```bash
.venv/bin/python -m kokoro_tts --help-voices --model ./models/kokoro-v1.0.onnx --voices ./models/voices-v1.0.bin
```

## Notes for Unity

- `.wav` is the safest export format for import quality.
- Generate final assets outside the Unity editor if you want cleaner source control diffs and easier batch regeneration.
- This model typically writes mono speech audio at the model's sample rate; Unity can resample on import if your project audio settings differ.

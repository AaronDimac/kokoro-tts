#!/usr/bin/env python3
import argparse
import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import onnxruntime as rt
import soundfile as sf
from kokoro_onnx import Kokoro

from kokoro_tts import chunk_text, process_chunk_sequential, validate_language, validate_voice


@dataclass
class ScriptStep:
    step_id: str
    title: str
    body: str


SMALL_NUMBER_WORDS = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
    20: "twenty",
    30: "thirty",
    40: "forty",
    50: "fifty",
    60: "sixty",
}


def number_to_words(value: int) -> str:
    if value in SMALL_NUMBER_WORDS:
        return SMALL_NUMBER_WORDS[value]
    if 21 <= value < 60:
        tens = (value // 10) * 10
        ones = value % 10
        if ones == 0:
            return SMALL_NUMBER_WORDS[tens]
        return f"{SMALL_NUMBER_WORDS[tens]} {SMALL_NUMBER_WORDS[ones]}"
    return str(value)


def choose_provider() -> str:
    requested = os.environ.get("ONNX_PROVIDER")
    if requested:
        return requested

    available = rt.get_available_providers()
    for provider in ("CUDAExecutionProvider", "DmlExecutionProvider", "CPUExecutionProvider"):
        if provider in available:
            os.environ["ONNX_PROVIDER"] = provider
            return provider

    fallback = "CPUExecutionProvider"
    os.environ["ONNX_PROVIDER"] = fallback
    return fallback


def parse_script_steps(path: Path) -> list[ScriptStep]:
    steps: list[ScriptStep] = []
    current_step_id: str | None = None
    current_title = ""
    current_body_lines: list[str] | None = None

    def flush_current() -> None:
        nonlocal current_body_lines
        if current_step_id is None or current_body_lines is None:
            return
        body = "\n".join(current_body_lines).strip()
        if body:
            steps.append(ScriptStep(step_id=current_step_id, title=current_title.strip(), body=body))
        current_body_lines = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()

        if line.startswith("Step "):
            flush_current()
            current_step_id = line.removeprefix("Step ").strip()
            current_title = ""
            current_body_lines = None
            continue

        if line.startswith("Title:"):
            current_title = line.partition(":")[2].strip()
            continue

        if line.startswith("Body:"):
            current_body_lines = [line.partition(":")[2].strip()]
            continue

        if current_body_lines is not None:
            current_body_lines.append(line)

    flush_current()
    return steps


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return cleaned.strip("_")


def output_name(step: ScriptStep) -> str:
    step_part = step.step_id.replace(".", "_").replace(" ", "_")
    title_part = slugify(step.title)
    if title_part:
        return f"step_{step_part}_{title_part}.wav"
    return f"step_{step_part}.wav"


def normalize_narration_text(text: str) -> str:
    normalized = text.strip()
    normalized = normalized.replace("’", "'")
    normalized = normalized.replace("–", "-")
    normalized = normalized.replace("OK", "okay")
    normalized = normalized.replace("GE MX", "G E M X")
    normalized = normalized.replace("balance-critical", "balance critical")
    normalized = normalized.replace("counter-clockwise", "counterclockwise")

    normalized = re.sub(
        r"#(\d+)",
        lambda match: f"number {number_to_words(int(match.group(1)))}",
        normalized,
    )
    normalized = re.sub(
        r"\b(\d+)\s+to\s+(\d+)\b",
        lambda match: f"{number_to_words(int(match.group(1)))} to {number_to_words(int(match.group(2)))}",
        normalized,
        flags=re.IGNORECASE,
    )
    normalized = re.sub(
        r"\b(\d+)\s+o'clock\b",
        lambda match: f"{number_to_words(int(match.group(1)))} o'clock",
        normalized,
        flags=re.IGNORECASE,
    )
    normalized = normalized.replace("at the top which is", "at the top, which is")
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def split_body_paragraphs(body: str) -> list[str]:
    paragraphs = [
        normalize_narration_text(paragraph)
        for paragraph in re.split(r"\n\s*\n+", body.strip())
        if paragraph.strip()
    ]
    return paragraphs


def synthesize_step(
    kokoro: Kokoro,
    step: ScriptStep,
    output_path: Path,
    voice: str | np.ndarray,
    speed: float,
    lang: str,
    pause_ms: int,
) -> tuple[int, float, str]:
    paragraphs = split_body_paragraphs(step.body)
    all_samples: list[float] = []
    sample_rate: int | None = None
    spoken_text_parts: list[str] = []

    for paragraph_index, paragraph in enumerate(paragraphs):
        spoken_text_parts.append(paragraph)
        chunks = chunk_text(paragraph, initial_chunk_size=1000)
        for chunk in chunks:
            samples, sr = process_chunk_sequential(chunk, kokoro, voice, speed, lang)
            if samples is None or sr is None:
                raise RuntimeError(f"Failed to synthesize step {step.step_id}")
            if sample_rate is None:
                sample_rate = sr
            all_samples.extend(samples)

        if paragraph_index < len(paragraphs) - 1 and sample_rate is not None:
            pause_samples = np.zeros(int(sample_rate * (pause_ms / 1000.0)), dtype=np.float32)
            all_samples.extend(pause_samples.tolist())

    if sample_rate is None:
        raise RuntimeError(f"No audio generated for step {step.step_id}")

    audio = np.array(all_samples)
    sf.write(output_path, audio, sample_rate)
    return sample_rate, len(audio) / sample_rate, "\n\n".join(spoken_text_parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate one WAV per Body section from script.md")
    parser.add_argument("input", nargs="?", default="script.md", help="Path to script markdown file")
    parser.add_argument("output_dir", nargs="?", default="generated/body_wavs", help="Directory for WAV outputs")
    parser.add_argument("--voice", default="af_sarah", help="Kokoro voice name or blend")
    parser.add_argument("--lang", default="en-us", help="Language code")
    parser.add_argument("--speed", type=float, default=0.96, help="Speech speed")
    parser.add_argument("--pause-ms", type=int, default=320, help="Silence inserted between body paragraphs")
    parser.add_argument("--model", default="models/kokoro-v1.0.onnx", help="Path to ONNX model")
    parser.add_argument("--voices", default="models/voices-v1.0.bin", help="Path to voices file")
    args = parser.parse_args()

    provider = choose_provider()
    try:
        rt.preload_dlls()
    except Exception:
        pass

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    steps = parse_script_steps(input_path)
    if not steps:
        raise SystemExit(f"No Body sections found in {input_path}")

    print(f"Using ONNX provider: {provider}")
    print(f"Extracted {len(steps)} Body sections from {input_path}")

    kokoro = Kokoro(args.model, args.voices)
    lang = validate_language(args.lang, kokoro)
    voice = validate_voice(args.voice, kokoro)

    manifest: list[dict[str, object]] = []
    for index, step in enumerate(steps, start=1):
        output_path = output_dir / output_name(step)
        print(f"[{index}/{len(steps)}] {step.step_id} -> {output_path.name}")
        sample_rate, duration, spoken_text = synthesize_step(
            kokoro,
            step,
            output_path,
            voice,
            args.speed,
            lang,
            args.pause_ms,
        )
        manifest.append(
            {
                **asdict(step),
                "spoken_text": spoken_text,
                "file": output_path.name,
                "sample_rate": sample_rate,
                "duration_seconds": round(duration, 2),
            }
        )

    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Created {len(steps)} wav files in {output_dir}")
    print(f"Wrote manifest: {manifest_path}")


if __name__ == "__main__":
    main()

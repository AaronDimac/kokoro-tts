#!/usr/bin/env python3
import os
import sys

import onnxruntime as rt


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


def main() -> None:
    provider = choose_provider()

    try:
        rt.preload_dlls()
    except Exception:
        pass

    print(f"Using ONNX provider: {provider}")

    from kokoro_tts import main as kokoro_main

    sys.argv[0] = "kokoro-tts"
    kokoro_main()


if __name__ == "__main__":
    main()

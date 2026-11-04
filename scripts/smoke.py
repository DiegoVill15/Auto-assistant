"""Prueba de humo: una llamada mínima por proveedor. No corre en CI."""

import os
import subprocess
import sys

from auto_assistant.models.client import OPENCODE_GO_ENV, complete

PROMPT = "Responde solo: ok"


def local() -> str:
    return complete("ollama/qwen3.5:9b", PROMPT)


def opencode_go() -> str:
    if not os.environ.get(OPENCODE_GO_ENV):
        raise RuntimeError(f"falta la variable de entorno {OPENCODE_GO_ENV}")
    return complete("opencode_go/glm-5.3-flash", PROMPT)


def claude_pro() -> str:
    # Sin ANTHROPIC_API_KEY para que use el plan Pro y no la API de pago.
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    r = subprocess.run(
        ["claude", "-p", "--model", "claude-opus-5-5", PROMPT],
        capture_output=True, text=True, env=env, timeout=120,
    )  # fmt: skip
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or r.stdout.strip() or f"código {r.returncode}")
    return r.stdout


def main() -> int:
    fallas = 0
    for nombre, fn in [("ollama", local), ("opencode_go", opencode_go), ("claude -p", claude_pro)]:
        try:
            fn()
            print(f"OK    {nombre}")
        except Exception as e:  # un fallo no detiene a los demás
            fallas += 1
            print(f"FALLA {nombre}: {str(e).strip().splitlines()[-1][:200]}")
    return 1 if fallas else 0


if __name__ == "__main__":
    sys.exit(main())

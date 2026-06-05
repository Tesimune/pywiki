# Pywiki — AI Personal Assistant v2.0

A professional Streamlit-based AI assistant managed with [uv](https://docs.astral.sh/uv/).

---

## Prerequisites

Install **uv** (Astral's fast Python package manager):

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

---

## Quick Start

```bash
# 1. Enter the project folder
cd pywiki

# 2. Create virtual environment + install all dependencies
uv sync

# 3. Run via Streamlit directly
uv run streamlit run main.py
```

---

## Project Structure

```
pywiki/
├── main.py          # Streamlit app + uv script entry point
├── pyproject.toml   # uv / project metadata & dependencies
├── uv.lock          # Auto-generated lockfile (commit this)
└── README.md
```

---

## Common uv Commands

| Task | Command |
|---|---|
| Install all deps | `uv sync` |
| Add a package | `uv add <package>` |
| Remove a package | `uv remove <package>` |
| Upgrade all packages | `uv sync --upgrade` |
| Run any command in venv | `uv run <command>` |
| Show installed packages | `uv pip list` |
| Install dev extras | `uv sync --extra dev` |
| Lint code | `uv run ruff check main.py` |
| Format code | `uv run ruff format main.py` |

---

## Optional: PyAudio (microphone support)

PyAudio requires PortAudio system libraries before `uv sync` will succeed.

```bash
# Ubuntu / Debian
sudo apt-get install portaudio19-dev python3-dev

# macOS
brew install portaudio

# Windows — wheel is handled automatically by uv
```

If you don't need mic input, remove `pyaudio` and `SpeechRecognition` from
`pyproject.toml` then run `uv sync` again — the app degrades gracefully.

---

## API Keys

Enter at runtime in the sidebar — never hard-code secrets:

| Key | Where to get it |
|---|---|
| OpenWeatherMap | [openweathermap.org/api](https://openweathermap.org/api) — free tier |
| Wolfram Alpha App ID | [developer.wolframalpha.com](https://developer.wolframalpha.com/) — free tier |

# Spoken English Audio

A Codex skill that rewrites English drafts into natural spoken English, annotates stress, pauses, and intonation, and generates two US English male neural-voice MP3s:

- a natural-speed version for delivery practice;
- a slower version for shadowing.

## Outputs

For an input such as `update.txt`, the skill produces:

- `update_spoken.txt` — clean speech-ready text used for audio generation;
- `update_marked.md` — practice text annotated with stress and intonation;
- `update_spoken_normal.mp3` — natural-speed audio;
- `update_spoken_slow.mp3` — slow shadowing audio.

The marked script uses:

- `/` for a short pause;
- `//` for a longer pause;
- `UPPERCASE` for primary stress;
- `↗` for a slight rise;
- `↘` for a falling, completed thought.

## Use as a Codex skill

Clone the repository into the Codex skills directory, or create a symbolic link from that directory to your checkout:

```bash
ln -s /path/to/spoken-english-audio ~/.codex/skills/spoken-english-audio
```

Then invoke it in Codex:

```text
Use $spoken-english-audio to make this script conversational and generate the marked script plus normal and slow practice MP3s:

<your English draft>
```

## Run the audio generator directly

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/generate_mp3.py path/to/script_spoken.txt
```

By default, the generator uses `en-US-BrianMultilingualNeural`, a `-4%` rate for the natural version, and a `-15%` rate for the slow version. Run the script with `--help` to see the available options.

## Privacy

Audio generation uses the `edge-tts` package and sends the clean speech text to Microsoft's online neural speech service. Do not submit secrets, credentials, or sensitive personal information without appropriate approval.

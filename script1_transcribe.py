"""
SCRIPT 1 — Transcribe Voiceover
---------------------------------
1. Runs Whisper on your voiceover file
2. Outputs a clean transcript with timestamps
3. You paste that into your Claude project
4. Claude identifies scene breaks + writes image prompts

Usage:
    python script1_transcribe.py your_voiceover.mp3

Requirements:
    pip install openai-whisper
    ffmpeg installed on your system
"""

import sys
import json
import whisper
from pathlib import Path


# ── CONFIG ────────────────────────────────────────────────────────────────────
WHISPER_MODEL = "base"   # tiny | base | small | medium | large
                          # base = fast, good enough for most voiceovers
                          # small or medium = more accurate, slower
# ──────────────────────────────────────────────────────────────────────────────


def transcribe(audio_path: str) -> dict:
    print(f"\n[1/2] Loading Whisper model ({WHISPER_MODEL})...")
    model = whisper.load_model(WHISPER_MODEL)
    print(f"[1/2] Transcribing: {audio_path}")
    result = model.transcribe(audio_path, word_timestamps=True)
    print(f"      ✓ Done — {len(result['segments'])} segments found")
    return result


def build_timestamped_transcript(result: dict) -> str:
    """One line per sentence with start and end timestamps."""
    lines = []
    for seg in result["segments"]:
        start = round(seg["start"], 2)
        end   = round(seg["end"], 2)
        text  = seg["text"].strip()
        lines.append(f"[{start}s - {end}s] {text}")
    return "\n".join(lines)


def save_outputs(audio_path: str, transcript: str, result: dict):
    print("\n[2/2] Saving outputs...")
    base = Path(audio_path).stem

    # --- transcript.txt (paste this into Claude) ---
    transcript_path = Path(f"{base}_transcript.txt")
    with open(transcript_path, "w") as f:
        f.write("=== VOICEOVER TRANSCRIPT WITH TIMESTAMPS ===\n")
        f.write("(paste this into your Claude project)\n\n")
        f.write(transcript)

    print(f"      ✓ Transcript saved → {transcript_path}")

    # --- segments.json (raw Whisper output, for reference) ---
    segments_path = Path(f"{base}_segments.json")
    segments = [
        {
            "start": round(seg["start"], 2),
            "end":   round(seg["end"], 2),
            "text":  seg["text"].strip()
        }
        for seg in result["segments"]
    ]
    with open(segments_path, "w") as f:
        json.dump(segments, f, indent=2)

    print(f"      ✓ Segments saved   → {segments_path}")

    return transcript_path, segments_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python script1_transcribe.py your_voiceover.mp3")
        sys.exit(1)

    audio_path = sys.argv[1]

    if not Path(audio_path).exists():
        print(f"✗ File not found: {audio_path}")
        sys.exit(1)

    result     = transcribe(audio_path)
    transcript = build_timestamped_transcript(result)
    transcript_path, segments_path = save_outputs(audio_path, transcript, result)

    base = Path(audio_path).stem

    print("\n" + "="*55)
    print("  DONE. Here is what to do next:\n")
    print(f"  1. Open  →  {transcript_path}")
    print("  2. Paste the full contents into your Claude project")
    print("  3. Claude will identify scene breaks + give you image prompts")
    print("  4. Generate images IN ORDER (scene 1 first, scene 2 next...)")
    print("  5. Drop all images into a folder called  images/")
    print("  6. Run script 2:")
    print(f"     python script2_assemble.py {segments_path} images/ {base}_final.mp4 {audio_path}")
    print("="*55 + "\n")


if __name__ == "__main__":
    main()
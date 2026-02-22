<<<<<<< HEAD
# Image Syncer

Turn a voiceover audio file into a narrated slideshow video — automatically synced to speech.

## How It Works

1. **Transcribe** your voiceover with Whisper (Script 1)
2. **Paste** the transcript into your Claude project — Claude identifies scene breaks and writes image prompts
3. **Generate** images for each scene (in order) using any image tool
4. **Assemble** the final video with images synced to the audio (Script 2)

---

## Requirements

**Python packages:**
```bash
pip install openai-whisper
```

**System dependencies:**
- [ffmpeg](https://ffmpeg.org/download.html) — must be installed and available on your PATH

---

## Usage

### Step 1 — Transcribe your voiceover

```bash
python script1_transcribe.py your_voiceover.mp3
```

This produces two files:
- `your_voiceover_transcript.txt` — timestamped transcript to paste into Claude
- `your_voiceover_segments.json` — raw Whisper output used by Script 2

**Whisper model:** The default model is `base` (fast, good quality). To use a more accurate model, edit the `WHISPER_MODEL` variable at the top of `script1_transcribe.py`:

| Model  | Speed  | Accuracy |
|--------|--------|----------|
| tiny   | Fastest | Lowest  |
| base   | Fast    | Good    |
| small  | Medium  | Better  |
| medium | Slow    | Best    |
| large  | Slowest | Highest |

---

### Step 2 — Get image prompts from Claude

1. Open `your_voiceover_transcript.txt`
2. Paste the full contents into your Claude project
3. Claude will identify scene breaks and produce image prompts for each scene

---

### Step 3 — Generate images

Generate one image per scene **in order** (scene 1 first, scene 2 next, etc.) using any image generation tool (Midjourney, DALL·E, Stable Diffusion, etc.).

Place all generated images into a folder called `images/`.

---

### Step 4 — Assemble the final video

```bash
python script2_assemble.py your_voiceover_segments.json images/ your_voiceover_final.mp4 your_voiceover.mp3
```

Replace `your_voiceover` with your actual filename stem throughout.

---

## Example

```bash
# Transcribe
python script1_transcribe.py narration.mp3

# (paste narration_transcript.txt into Claude, generate images into images/)

# Assemble
python script2_assemble.py narration_segments.json images/ narration_final.mp4 narration.mp3
```

---

## Supported Audio Formats

Any format supported by ffmpeg: `.mp3`, `.mp4`, `.wav`, `.m4a`, `.ogg`, `.flac`, etc.
=======
# Voiceover-Timestamper
Gives you timestamp of voiceover
>>>>>>> f66faec0599ebac0a70b49845225585fbae67401

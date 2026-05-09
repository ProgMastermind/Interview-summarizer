# Interview Summarizer

A command-line script that takes an interview transcript as input and produces a structured hiring summary: topics covered, candidate profile with justification, and a concise candidate summary.

---

## How to Run

### 1. Install dependencies

```bash
pip install openai python-dotenv
```

### 2. Set up your API key

```bash
cp .env.example .env
# Open .env and replace "your_api_key_here" with your actual OpenAI API key
```

### 3. Run the script

```bash
# Print summary to stdout
python summarizer.py transcripts/sample_transcript_1.txt

# Write summary to a file
python summarizer.py transcripts/sample_transcript_2.txt output.md
```

---

## LLM Provider and Model

**Provider:** OpenAI  
**Model:** `gpt-5.5`

OpenAI's `gpt-5.5` was chosen because it follows structured output instructions reliably and handles both technical and non-technical interview styles well without special configuration. It provides a good balance of output quality and speed for this task.

---

## Reflection

**What surprised me**

Honestly the biggest thing was how much one small prompt change mattered. The two transcripts are very different — one's a technical interview where the real signal is whether theory holds up when the candidate has to actually write code, the other is ops/stakeholder stuff where the interviewer's feedback at the end is more useful than anything the candidate said. My first prompt was implicitly built for a tech interview, so Transcript 2 came out flat and generic. Adding one line — telling the model to treat non-technical interviews differently and list behavioral topics — fixed it. Didn't expect that to be enough, but it was.

**What I'd improve with another day**

- Pass the job description in alongside the transcript. The model infers the role from scratch right now, which mostly works but gets imprecise when the role is broad or hybrid — Transcript 2 is a good example of that.
- Add a separate red-flags field to the output with rough severity, so a reviewer can scan for concerns quickly without reading the full summary.
- A second prompt pass that generates follow-up questions for the next interview round would make this genuinely useful end-to-end rather than just a summarizer.

**Limitations of the final prompt**

- Both sample transcripts start mid-interview, so there's no background section to extract from — the model is inferring it from how the candidate answers questions. The "note any gaps" instruction helps but it's not the same as having the full transcript.
- The model has no sense of how hard a question was relative to the role. Not knowing Zustand reads the same as not knowing how React renders — without the JD as context, it can't weigh gaps accurately.
- Tone and confidence are invisible in text. The interviewer flagged the Hindi jargon issue directly in Transcript 2, but without that comment the model would have had no way to detect it.

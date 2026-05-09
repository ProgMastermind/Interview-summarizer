import openai
import os
import sys
from dotenv import load_dotenv

load_dotenv()

PROMPT = """You are an experienced technical recruiter analyzing an interview transcript. \
Your job is to produce a concise, structured hiring summary for the reviewing team.

Produce exactly three sections using the format below. \
Use only information present in the transcript — do not invent details. \
If the transcript is partial or brief, work with what is available and note any gaps.

---

## 1. Topics Covered
List 4–8 bullet points of the main themes discussed. \
Be specific (e.g., "Angular lazy loading and modular architecture" not just "Angular"). \
For non-technical interviews, list behavioral or domain topics (e.g., "Stakeholder conflict resolution", "Data accuracy under pressure").

## 2. Profile
**Role fit:** [Job function] — [seniority level]
**Justification:** 2–3 sentences citing specific evidence from the transcript: what the candidate demonstrated well, how they answered under pressure, and what they struggled with or avoided.

## 3. Candidate Summary
A single paragraph of 3–6 sentences covering: professional background (inferred from answers), key strengths shown in the interview, any notable gaps or concerns, and your overall hiring impression.

---

<transcript>
{transcript}
</transcript>"""


def summarize(transcript_text: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set. "
            "Copy .env.example to .env and add your key."
        )

    client = openai.OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-5.5",
        max_completion_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": PROMPT.format(transcript=transcript_text),
            }
        ],
    )

    return response.choices[0].message.content


def main():
    if len(sys.argv) < 2:
        print("Usage: python summarizer.py <transcript_file> [output_file]")
        print()
        print("  transcript_file   Path to a .txt interview transcript")
        print("  output_file       Optional path to write the summary (default: stdout)")
        sys.exit(1)

    transcript_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        with open(transcript_file, "r", encoding="utf-8") as f:
            transcript_text = f.read().strip()
    except FileNotFoundError:
        print(f"Error: file not found — {transcript_file}")
        sys.exit(1)

    if not transcript_text:
        print("Error: transcript file is empty.")
        sys.exit(1)

    print(f"Summarizing: {transcript_file} ...\n")

    try:
        summary = summarize(transcript_text)
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(summary)
        print(f"Summary written to: {output_file}")
    else:
        print("=" * 60)
        print(summary)


if __name__ == "__main__":
    main()

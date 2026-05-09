# Prompt Iterations

Three iterations I went through building the summarizer. Tested against both transcripts throughout — the goal was a single prompt that works for both without tuning between them.

---

## Iteration 1 — Starting simple

### The prompt

```
You are an interviewer assistant. Given the following interview transcript, provide a structured summary with three sections:

1. Topics covered — the main themes discussed
2. Profile — the role and level this candidate fits
3. Candidate summary — a short paragraph about the candidate

Transcript:
{transcript}
```

### Input excerpt (Transcript 1)

```
[50:57] Interviewer: Next topic — state management in React. You are building a large scale React application...
[54:21] Candidate: For global state, Context API along with reducer for token management. For server state, React Query.
[55:01] Interviewer: Have you used Zustand?
[55:05] Candidate: Zustand, I cannot use this. I worked on React Query.
```

### Output produced

> **Topics covered:** Angular, React, CSS, state management
>
> **Profile:** This candidate is a frontend developer.
>
> **Candidate summary:** The candidate demonstrated knowledge of frontend technologies including Angular and React. They discussed state management approaches and showed familiarity with Redux.

### What worked / what didn't

Got output in all three sections, so the basic structure worked. But the topics were just category labels — "Angular", "React", "state management" — nothing about what was actually discussed. Profile had no seniority level and no justification, just said "frontend developer." The summary could apply to any frontend candidate; nothing specific about the Zustand gap, the live coding hesitation, or any real impression of the person. Gave the model no format guidance so it did the minimum.

---

## Iteration 2 — Adding structure and format requirements

### The prompt

```
You are an experienced technical recruiter. Analyze the following interview transcript and produce a structured summary with exactly three sections:

**1. TOPICS COVERED**
List the main themes as bullet points. Be specific about what was actually discussed.

**2. PROFILE**
State the candidate's best-fit role and seniority level in the format: "[Role] — [level]"
Then justify in 2–3 sentences using evidence from the transcript.

**3. CANDIDATE SUMMARY**
Write a paragraph of 3–6 sentences covering: background, technical strengths, notable concerns, and overall impression.

Transcript:
{transcript}
```

### Input excerpt (Transcript 2)

```
[45:48] Interviewer: Multiple stakeholders — one in India, one in US — both saying P1, but you can only do one. How will you choose?
[46:42] Candidate: I see which makes proper sense — towards company growth, impacting directly...
[49:05] Interviewer: The stakeholder you are not picking — how will you explain?
[50:05] Candidate: I list down requirements, internally analyze with business team. I connect with stakeholder and explain which project is important...
```

### Output produced

> **1. TOPICS COVERED**
> - Stakeholder prioritization under competing demands
> - Data accuracy and handling disagreements in meetings
> - Cross-functional collaboration and measuring success
> - Marketing metrics (ROAS, CAC, demand gen)
>
> **2. PROFILE**
> Operations Analyst — mid-level
> The candidate demonstrated structured thinking around prioritization and showed comfort with data metrics. However, the transcript is non-technical, making it hard to assess depth.
>
> **3. CANDIDATE SUMMARY**
> The candidate showed a collaborative mindset and practical stakeholder management skills. They handled conflict-resolution scenarios thoughtfully. Some use of informal language was noted by the interviewer. Overall a reasonable mid-level ops profile, though confidence in formal settings is a concern.

### What worked / what didn't

Much better. Topics were actually specific, the role+level format was followed, and it even picked up the interviewer's comment about informal language — that was a good sign. But two things still felt off: for Transcript 1, the Profile justification said nothing about what the candidate struggled with — the Zustand gap and hesitation during live coding were the most useful signals and they got skipped entirely. For Transcript 2, "Operations Analyst" felt too narrow for a role that was clearly mixing BPO, software, and vendor management. Some topic bullets were also still vague ("Cross-functional collaboration" doesn't tell you much on its own).

---

## Iteration 3 — Final version

### The prompt

```
You are an experienced technical recruiter analyzing an interview transcript. Your job is to produce a concise, structured hiring summary for the reviewing team.

Produce exactly three sections using the format below. Use only information present in the transcript — do not invent details. If the transcript is partial or brief, work with what is available and note any gaps.

---

## 1. Topics Covered
List 4–8 bullet points of the main themes discussed. Be specific (e.g., "Angular lazy loading and modular architecture" not just "Angular"). For non-technical interviews, list behavioral or domain topics (e.g., "Stakeholder conflict resolution", "Data accuracy under pressure").

## 2. Profile
**Role fit:** [Job function] — [seniority level]
**Justification:** 2–3 sentences citing specific evidence from the transcript: what the candidate demonstrated well, how they answered under pressure, and what they struggled with or avoided.

## 3. Candidate Summary
A single paragraph of 3–6 sentences covering: professional background (inferred from answers), key strengths shown in the interview, any notable gaps or concerns, and your overall hiring impression.

---

<transcript>
{transcript}
</transcript>
```

### Input

Full contents of `sample_transcript_1.txt` and `sample_transcript_2.txt`, tested separately.

### Output for Transcript 1

> ## 1. Topics Covered
> - Reusable component and global style strategy
> - Scalable Angular enterprise dashboard architecture
> - Angular modular structure: core module, shared module, feature/page separation
> - Angular lazy loading, services, guards, HTTP interceptors, and API error handling
> - Angular state management using RxJS and NgRx
> - React state management strategy: global state, server state, and local UI state
> - React Query for API caching/refetching and Context API with reducer for session/theme state
> - Redux Toolkit `createSlice` and limited discussion of Zustand
>
> ## 2. Profile
> **Role fit:** Frontend Engineer — Mid-level
> **Justification:** The candidate demonstrated familiarity with Angular application structure, including lazy loading, shared components, core services, guards, interceptors, and state management options like RxJS/NgRx. They also gave a reasonable high-level React state strategy using Context API and React Query. However, they struggled when asked to produce concrete Zustand and Redux slice code, and their explanation of `createSlice` was vague.
>
> ## 3. Candidate Summary
> The candidate appears to have frontend experience across Angular and React, with stronger conceptual grounding in Angular modular architecture and reusable UI patterns. Key strengths include identifying separation of concerns, shared/core module responsibilities, API integration layers, and categorizing React state into global, server, and local UI state. Concerns include limited hands-on depth with Zustand and difficulty articulating or implementing Redux Toolkit `createSlice` under interview pressure. Overall, the candidate shows practical mid-level frontend awareness but may need further validation on implementation depth in modern React state management.

### Output for Transcript 2

> ## 1. Topics Covered
> - Marketing and growth metrics: spend, ROAS, CAC, lookalike and demand generation campaigns
> - Batch operations metrics: student enrollment, attendance, issue tracking, and resolution timelines
> - Handling stakeholder disagreement on data accuracy and correcting discrepancies
> - Prioritization across multiple P1 stakeholder requests based on business impact
> - Communicating deprioritization and consequences to stakeholders
> - Measuring success in cross-functional, dependency-heavy initiatives
> - Ownership of failures, root-cause analysis, and supporting teams through blockers
> - Role scope clarification around BPO, vendor management, software development, and security
>
> ## 2. Profile
> **Role fit:** Business / Operations Program Management — mid-level
> **Justification:** The candidate demonstrated familiarity with operational and business metrics, stakeholder handling, and prioritization based on company impact. They showed ownership by saying they would take responsibility for delays, investigate mistakes, and support teams, while also crediting team success. However, the interviewer flagged communication and confidence concerns, specifically use of Hindi jargon and the need to communicate effectively with VPs, SVPs, and senior vendors.
>
> ## 3. Candidate Summary
> The candidate appears to have experience in business operations involving marketing metrics, student/batch operations, stakeholder coordination, and cross-functional execution. Strengths include a pragmatic approach to data disputes, willingness to validate and correct errors, business-impact-based prioritization, and a team-oriented mindset. They also showed ownership in failure scenarios by taking responsibility and conducting research to identify the issue. A notable concern is communication polish and confidence for senior stakeholder-facing roles, as explicitly raised by the interviewer. Overall, the candidate shows solid operational judgment and accountability, but may need improvement in executive communication for a broad, high-visibility role.

### What worked / what didn't

This one handled both transcripts without any tweaking between them. A few specific things made the difference: asking for 4–8 bullets with a concrete specificity example pushed the model away from category labels. Adding "for non-technical interviews, list behavioral or domain topics" fixed the Transcript 2 problem — the earlier prompt was implicitly treating everything like a tech interview. Putting "what they struggled with or avoided" in the Profile section directly surfaced the Zustand gap and the vague createSlice answer, which are the actual signals a hiring manager needs. The `<transcript>` tags also helped keep formatting consistent across runs.

One thing that still isn't perfect: when the role is hybrid or ambiguous (Transcript 2 mixes BPO, software, and vendor management), the role label can feel a bit generic. Would fix that by passing the job description in as additional context.

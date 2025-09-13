# PyCon25 Hackathon — Intelligent Support Ticket Assignment System

A compact, explainable solution for routing support tickets to the most suitable agents while balancing load and considering availability and experience.

This repository contains a minimal, extensible implementation that reads `dataset.json` (agents + tickets) and produces `output_result.json` with ticket assignments and a short rationale for each assignment.

---

## Quick Start

Requirements
- Python 3.8+

Run the assignment script from the project root (PowerShell shown):

```powershell
python .\solution.py
```

This will create or overwrite `output_result.json` with the assignment results in the same folder.

---

## Files in this repository

- `dataset.json` — input data with `agents` and `tickets`.
- `solution.py` — assignment algorithm (heuristic, explainable).
- `output_result.json` — generated assignment results.
- `README.md` — this file.

---

## What the solution does

- Parses tickets and agents from `dataset.json`.
- Extracts normalized tokens from ticket titles/descriptions.
- Builds an agent scoring function that combines:
  - skill match (agent skill levels),
  - current load (penalty),
  - experience (bonus), and
  - availability (agents marked "Available" are considered).
- Assigns each ticket to the best scoring available agent and increments their simulated load to distribute work.
- Writes assignments with fields: `ticket_id`, `assigned_agent_id`, and `rationale`.

The implementation is intentionally simple and deterministic — easy to inspect and extend.

---

## Design notes / scoring

- Tokenization: ticket text is split into alphanumeric tokens, lowercased, and normalized (non-alphanumerics -> underscore). Agent skill names are normalized the same way.
- Skill match: a direct token match with an agent skill adds skill-level-based points.
- Load balancing: agents with higher `current_load` are penalized so subsequent assignments favor less-busy agents.
- Experience: agents with higher `experience_level` receive a small bonus.
- Availability: only agents with `availability_status: "Available"` are eligible.

This scoring is a heuristic designed for clarity — swap in a trained model or more complex business rules as needed.

---

## Example output (snippet)

```json
{
  "assignments": [
    {
      "ticket_id": "TKT-2025-001",
      "assigned_agent_id": "agent_008",
      "rationale": "Matched skills: None; Agent experience: 9; Current load after assignment: 3"
    },
    {
      "ticket_id": "TKT-2025-002",
      "assigned_agent_id": "agent_008",
      "rationale": "Matched skills: None; Agent experience: 9; Current load after assignment: 4"
    }
  ]
}
```

---

## Edge cases handled

- No available agents: ticket will be assigned `assigned_agent_id: null` with a rationale message.
- Skill token mismatches: skill names and ticket tokens are normalized to reduce false negatives. Further synonym mapping can be added.
- Tie-breakers: the scoring and load update strategy favors lower-load and higher-experience agents when scores are similar.
- Large inputs: current heuristic is O(#tickets * #agents). For larger datasets, use inverted indices or candidate prefiltering.

---

## Next steps (recommended enhancements)

- Add ticket priority or SLA-aware weighting so critical incidents are prioritized.
- Incorporate historical resolution success per (agent, topic) to predict probability of resolution.
- Add unit tests for tokenization, scoring, and assignment (pytest).
- Expose CLI flags to control behavior (e.g., produce minimal output with only required fields).
- Replace heuristics with a learn-to-rank model if labeled historic data is available.

---

If you want, I can add unit tests and a short CLI wrapper next — tell me which improvement you want and I'll implement it.

import json
import re
from collections import defaultdict


def normalize_token(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def extract_ticket_tags(ticket):
    # Heuristic: extract words from title and description, normalize
    text = (ticket.get("title", "") + " " + ticket.get("description", ""))
    words = re.findall(r"[A-Za-z0-9]+", text)
    tokens = set(normalize_token(w) for w in words if len(w) > 2)
    return tokens


def agent_available(agent):
    return agent.get("availability_status", "").lower() == "available"


def ticket_priority(ticket):
    return ticket.get("creation_timestamp", 0)


def match_score(agent, ticket_tags):
    score = 0
    matched = []
    # Ensure agent skills are normalized
    skills = {normalize_token(k): v for k, v in agent.get("skills", {}).items()}
    for tag in ticket_tags:
        if tag in skills:
            score += skills[tag] * 3
            matched.append(tag)
    score += agent.get("experience_level", 0)
    score -= agent.get("current_load", 0) * 2
    return score, matched


def assign_tickets(agents, tickets):
    result = []
    agent_load = {a["agent_id"]: a.get("current_load", 0) for a in agents}
    for ticket in sorted(tickets, key=lambda t: ticket_priority(t)):
        tags = extract_ticket_tags(ticket)
        best_score = float("-inf")
        best_agent = None
        best_matched = []
        for agent in agents:
            if not agent_available(agent):
                continue
            score, matched = match_score(agent, tags)
            score -= agent_load[agent["agent_id"]] * 0.5
            if score > best_score:
                best_score = score
                best_agent = agent
                best_matched = matched
        if best_agent:
            agent_load[best_agent["agent_id"]] += 1
            rationale = (
                f"Matched skills: {', '.join(best_matched) if best_matched else 'None'}; "
                f"Agent experience: {best_agent.get('experience_level',0)}; "
                f"Current load after assignment: {agent_load[best_agent['agent_id']]}"
            )
            result.append({
                "ticket_id": ticket["ticket_id"],
                "assigned_agent_id": best_agent["agent_id"],
                "rationale": rationale
            })
        else:
            result.append({
                "ticket_id": ticket["ticket_id"],
                "assigned_agent_id": None,
                "rationale": "No available agent"
            })
    return result


if __name__ == "__main__":
    with open("dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    agents = data.get("agents", [])
    tickets = data.get("tickets", [])
    output = assign_tickets(agents, tickets)
    with open("output_result.json", "w", encoding="utf-8") as f:
        json.dump({"assignments": output}, f, indent=2)
    print(f"Assigned {len(output)} tickets. Results in output_result.json.")
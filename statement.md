# PyCon25 Hackathon: Intelligent Support Ticket Assignment System

Welcome to the PyCon25 Hackathon project! 🚀

Once you are done with the hackathon, share your github link here: https://forms.gle/gnR62EoZUfeA8zqJ9

## 📋 Project Overview

### Problem Statement

In a helpdesk system, when customers raise support issues about different topics, we should ideally route tickets to agents who have knowledge and experience in solving that particular set of problems. However:

- **Volume Imbalance**: Not all topics have equal request volumes
- **Skill Gaps**: Not all agents have expertise in all areas
- **Fair Distribution**: Workload needs to be distributed equitably
- **Effective Resolution**: Tickets should go to the most capable agents

### Challenge

Build an optimal routing system that assigns support tickets to the best possible agent while ensuring:
- ✅ Maximum likelihood of successful resolution
- ✅ Fair distribution of workload across agents
- ✅ Effective prioritization of issues
- ✅ Cost-effective and scalable approach

## 📊 Data Structure

### Input: `dataset.json`
Contains two main sections:
- **Agents**: Support staff with skills, availability, and experience levels
- **Tickets**: Support requests with descriptions and timestamps

### Output: `output_result.json`
Your solution should generate ticket assignments with the following fields:

- **Mandatory:**
   - Ticket ID
   - Assigned Agent ID
- **Optional:**
   - Rationale/Justification for the assignment


## 🎯 Evaluation Criteria

Your solution will be judged on:

1. **Assignment Effectiveness** 
   - How well tickets are matched to agent skills
   - Likelihood of successful resolution

2. **Prioritization Strategy**
   - Creative use of ticket and agent attributes
   - Intelligent priority scoring

3. **Load Balancing**
   - Fair distribution of workload
   - Agent availability management

4. **Performance & Scalability**
   - Cost efficiency of the approach
   - Ability to handle large datasets

## 🏗️ Project Structure

```
pycon25-hackathon/
├── dataset.json           # Input data (agents and tickets)
├── output_result.json     # Expected output
├── README.md             # This file
└── [your solution files] # Your implementation
```

## 📈 Success Metrics

Your solution should optimize for:
- **Resolution Rate**: Tickets assigned to skilled agents
- **Response Time**: Efficient agent utilization
- **Workload Distribution**: Balanced assignment across team
- **Scalability**: Performance with increasing data size

## 🤝 Contributing

This is a hackathon project - unleash your creativity and build an innovative solution!

---

**Happy Hacking!** 🎉


---

## How to run

Make sure you have Python 3.8+ installed. From the project root run:

```powershell
python .\solution.py
```

This will read `dataset.json` and write `output_result.json` with assignments and rationales.

## Approach (summary)

- Keyword-based tokenization of ticket title + description.
- Build a skill index from agent skills (normalize tokens like `Linux_Administration` -> `linux_administration`).
- Score each agent for a ticket using: matched skill levels, agent availability, current load (penalty), and an experience bonus.
- Assign each ticket to the highest-scoring available agent and increment that agent's load to help balance subsequent assignments.

This approach is intentionally simple, deterministic, and easy to extend (replace scoring with ML model or incorporate historical resolution rates).

## Edge cases considered

- No available agents: ticket is left unassigned with an explanatory rationale.
- Multiple agents tie: tie-breaker favors lower current load then higher experience.
- Skill-name/token mismatches: skill index includes splitting skill names by underscores to increase matching chance.
- Large volumes: algorithm is O(#tickets * #agents) and can be optimized by pre-filtering agents or using inverted indices.

## Next steps / Improvements

- Add ticket priority weighting (e.g., critical incidents get higher weight) and SLA-aware assignment.
- Incorporate historical resolution success rates per agent-topic to predict resolution probability.
- Replace heuristic scoring with a lightweight ML ranking model trained on past tickets.
- Add unit tests to validate tokenization, scoring, and assignment behaviors.






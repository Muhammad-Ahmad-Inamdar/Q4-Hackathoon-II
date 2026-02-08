Project: Hackathon II – Spec-Driven Todo Application (Agentic Dev Stack)

Purpose:
This Constitution defines the non-negotiable principles, constraints, and global rules
for the entire Hackathon II project. This is a single evolving system built across five
phases, not five separate projects. All agents must obey this Constitution before
proposing specs, plans, tasks, or code.

────────────────────────────────────────────
PROJECT STRUCTURE (MANDATORY CONTEXT)
────────────────────────────────────────────

This repository follows a phase-evolution model:

- ONE Git repository
- ONE evolving Todo system
- Phase-specific specifications
- Shared, growing codebase

Folder structure (authoritative):

/AGENTS.md                → Global agent behavior (HOW agents work)
/CLAUDE.md                → Shim that forwards to AGENTS.md

/speckit/
  ├── constitution.md     → THIS FILE (GLOBAL, grows over phases)
  ├── phase-1/
  │     ├── specify.md
  │     ├── plan.md
  │     ├── tasks.md
  │     └── phr/          → Prompt History Records
  ├── phase-2/
  ├── phase-3/
  ├── phase-4/
  └── phase-5/

/src/
  ├── todo/               → Core domain logic (shared across phases)
  ├── cli/                → Phase I interface
  ├── api/                → Phase II interface
  ├── agent/              → Phase III AI interface
  └── infra/              → Phase IV–V deployment artifacts

Rules:
- The Constitution is GLOBAL and applies to ALL phases
- Specs, plans, tasks, and PHRs are PHASE-SCOPED
- Code evolves; it is never rewritten per phase

────────────────────────────────────────────
CORE PRINCIPLES (WHY)
────────────────────────────────────────────

1. Spec-Driven Development (SDD) is mandatory
   - No code may be written without approved specifications
   - The lifecycle is strictly:
     Specify → Plan → Tasks → Implement

2. No Manual Coding
   - All code must be generated via Claude Code
   - Humans may only refine specifications and plans

3. Determinism over Creativity
   - Predictable, explainable implementations are preferred
   - "Creative" or speculative behavior is forbidden

4. Traceability
   - Every code artifact must map to:
     - A Task ID
     - A section in specify.md and plan.md

5. Phase Integrity
   - Each phase must be independently reviewable
   - Phase specs must not be retroactively edited after submission

────────────────────────────────────────────
GLOBAL STANDARDS (WHAT MUST ALWAYS HOLD)
────────────────────────────────────────────

Architecture:
- Clear separation of concerns
- Domain logic must not depend on interface layers
- Interfaces (CLI, API, Agent) adapt the same core domain

Code Quality:
- Clean, readable, minimal code
- Explicit naming over clever abstractions
- No premature optimization

Documentation:
- Every phase must include Prompt History Records (PHR)
- README.md must explain how the phase can be run and tested

────────────────────────────────────────────
PHASE-SPECIFIC CONSTRAINTS (INITIALIZED HERE)
────────────────────────────────────────────

Phase I (In-Memory Python CLI):
- In-memory storage only (NO database, NO files)
- Single-process, synchronous execution
- Python 3.13+
- Console-based interaction only
- IDs must be deterministic and auto-generated

Future phases may append constraints here but must not
violate earlier principles.

────────────────────────────────────────────
AGENT BEHAVIOR (ENFORCED)
────────────────────────────────────────────

Agents MUST:
- Refuse to write code if tasks are missing
- Refuse to invent requirements
- Stop and request clarification if specs are incomplete
- Follow AGENTS.md instructions strictly

Hierarchy of authority:
Constitution > Specify > Plan > Tasks > Implementation

────────────────────────────────────────────
SUCCESS CRITERIA
────────────────────────────────────────────

This Constitution is considered satisfied when:
- All phases demonstrate strict Spec-Driven Development
- No code exists without a traceable task
- Each phase can be reviewed independently
- The system evolves cleanly from Phase I to Phase V
- Judges can clearly see discipline, iteration, and intent

End of Constitution.
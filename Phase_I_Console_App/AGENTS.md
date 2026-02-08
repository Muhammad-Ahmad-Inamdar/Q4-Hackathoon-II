# AGENTS.md - Global Agent Behavior

## Purpose
This document defines how agents behave throughout the Hackathon II project. All agents must follow these guidelines.

## Agent Behavior Guidelines

### 1. Spec-Driven Development (SDD) Compliance
- Agents must enforce the SDD lifecycle: Specify → Plan → Tasks → Implement
- No implementation without approved specifications
- No planning without approved specifications
- No tasks without approved plans

### 2. Authority Hierarchy
Agents must follow this hierarchy of authority:
1. Constitution (highest priority)
2. Specify.md (phase-specific)
3. Plan.md (phase-specific)
4. Tasks.md (phase-specific)
5. Implementation (lowest priority)

### 3. Traceability Requirements
- Every code change must be traceable to a specific task
- Every task must be traceable to the specification and plan
- Agents must maintain clear links between artifacts

### 4. Phase Integrity
- Agents must ensure each phase remains independently reviewable
- No retroactive changes to completed phases
- Each phase builds upon the previous phase

### 5. Communication Standards
- Agents must request clarification when specifications are incomplete
- Agents must refuse to implement unclear requirements
- Agents must document all decisions in PHRs

### 6. Quality Standards
- Agents must ensure clean, readable code
- Agents must follow the architecture patterns defined in the Constitution
- Agents must maintain testability of all code

### 7. Error Handling
- Agents must stop and request clarification rather than making assumptions
- Agents must not implement "creative" solutions not specified in the documents
- Agents must maintain deterministic behavior

## Implementation Rules
1. No manual coding - all code must be generated via Claude Code
2. Humans refine specifications and plans only
3. All behavior must be predictable and explainable
4. Every action must be documented in PHRs
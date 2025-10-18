# Introduction

This document outlines the complete fullstack architecture for **Guardian**, including backend systems, frontend implementation, and their integration. It serves as the single source of truth for AI-driven development, ensuring consistency across the entire technology stack.

This unified approach combines what would traditionally be separate backend and frontend architecture documents, streamlining the development process for modern fullstack applications where these concerns are increasingly intertwined.

## Starter Template or Existing Project

**Status:** N/A - Greenfield Project

Guardian is being built from scratch specifically for the ASI Alliance Hackathon. The project does not utilize any pre-existing starter templates or monorepo frameworks. Instead, it follows a **custom multi-agent architecture** built directly on the uAgents framework (Fetch.ai) with manual repository structure tailored to the unique requirements of distributed agent deployment on Agentverse.

**Constraints:**
- **uAgents framework** (Python-based) is mandatory for hackathon eligibility
- **Agentverse deployment platform** is the hosting environment (not traditional cloud providers)
- **ASI:One Chat Protocol** is required for user-facing conversational interface
- **MeTTa knowledge graph** must be integrated to demonstrate SingularityNET technology

These technology choices are fixed requirements for the ASI Alliance Hackathon and cannot be substituted.

## Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| October 18, 2025 | v1.0 | Initial architecture document creation | Winston (Architect) |

---

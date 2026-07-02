# HelpOS — Master Project Plan (v1)

> A privacy-first, offline AI utility engine built for scientific computation, tutoring, and local productivity.

---

# 1. Product Brief

## Project

HelpOS is a local-first AI utility engine that combines deterministic computation, intelligent tutoring, and productivity tools into a single offline application.

Unlike cloud AI assistants, HelpOS performs exact scientific calculations through Python while using a locally hosted LLM (Ollama) for reasoning, tutoring, and natural language interaction.

The entire application is designed to run without internet access while remaining modular, extensible, and highly maintainable.

---

## Audience

- Students
- Peer Tutors
- Teachers
- STEM learners
- Anyone wanting an offline AI assistant

---

## Primary User Actions

Users should be able to:

- Ask chemistry questions
- Solve math and science problems
- Generate explanations
- Convert natural language into exact calculations
- Use offline utility tools
- Study with an intelligent tutor

---

## Core Value

HelpOS combines:

- 100% local execution
- Exact deterministic calculations
- AI reasoning
- Modern interface
- Expandable utility ecosystem

---

## What Should Feel Impressive

The application should feel:

- Instant
- Intelligent
- Extremely reliable
- Professional
- Privacy-first
- More like a desktop operating system than a chatbot

The user should immediately notice:

- Fast responses
- Beautiful interface
- Exact calculations
- Smooth workflow
- High polish

---

## Avoid

Avoid:

- Cloud dependencies
- Generic chatbot interfaces
- Slow workflows
- AI hallucinations for math
- Feature bloat
- Poor organization
- Inconsistent UI

---

# 2. Design & Style Brief

## Design References

Inspired by:

- Apple
- Linear
- Raycast
- Anthropic
- Arc Browser

---

## Visual Tone

- Minimal
- Premium
- Modern
- Calm
- Highly readable
- Desktop-focused

---

## Motion

Animations should be:

- Smooth
- Subtle
- Purposeful
- Fast

Avoid flashy animations.

---

## Layout Philosophy

Large spacing

Strong hierarchy

Minimal distractions

Focused workspace

Dark-first interface

---

## Color Philosophy

Primary:

- Deep purple
- Blue
- Cyan accents

Neutrals:

- Dark backgrounds
- Soft grays
- High contrast text

---

# 3. Project Scope

## Version 1 Includes

### AI

- Local Ollama integration
- Dual AI modes
- Natural language routing

---

### Chemistry Engine

- Formula parser
- Molar mass
- Grams ↔ Moles
- STP conversions
- Avogadro calculations

---

### Math Engine

Expandable deterministic solver framework.

---

### Study Tools

- Flashcards
- Markdown notes
- Pomodoro
- AI tutoring

---

### Utility Tools

- JSON formatter
- Base64 encoder/decoder
- Regex tester
- Unix timestamp converter

---

### Document Tools

- Local PDF summarization
- Text summarization

---

### Interface

Single dashboard containing:

- Chat
- Tool panels
- Calculation outputs
- Documentation viewer

---

## Not Included (v1)

- Authentication
- Accounts
- Cloud sync
- Online APIs
- Databases
- User profiles
- Multi-user support
- Payments
- Plugins
- Mobile app

---

# 4. Technical Constraints

## Core Requirements

Everything must work offline.

No cloud AI.

No remote APIs.

No internet dependency.

No telemetry.

---

## AI

Use Ollama only.

Reasoning is performed by the LLM.

Calculations are always performed by Python.

Never allow the LLM to perform arithmetic directly.

---

## Architecture

Frontend

- HTML
- Tailwind CSS
- Vanilla JavaScript

Backend

- Python
- FastAPI

Inference

- Ollama

Communication

REST API

---

## Development Philosophy

Every component should be:

- Modular
- Replaceable
- Testable
- Expandable

---

# 5. Optimization Priorities

Highest priorities:

1. Reliability
2. Exact calculations
3. Fast interface
4. Clean architecture

Secondary priorities:

- Beautiful UI
- Easy maintenance
- Future scalability

---

# 6. System Architecture

```
Frontend
        │
        ▼
 FastAPI Coordinator
        │
 ├──────────────┐
 ▼              ▼
Python Engine   Ollama
 │              │
 ▼              ▼
Exact Math      Reasoning
```

---

## Frontend

Responsibilities:

- Dashboard
- Chat interface
- Tool pages
- Rendering
- User interaction

---

## Backend

Responsibilities:

- Route requests
- Execute deterministic calculations
- Manage tools
- Call Ollama

---

## Ollama

Responsibilities:

- Conversation
- Tutoring
- Planning
- Query understanding

Never performs arithmetic.

---

## Deterministic Engine

Responsible for:

- Chemistry
- Math
- Unit conversions
- Scientific constants
- Formula parsing

---

# 7. Core Systems

## Chemistry Engine

Capabilities

- Formula parser
- Atomic mass lookup
- Molar mass
- Mole conversions
- Gas laws
- Stoichiometry foundation

Future expansion:

- Equilibrium
- Thermodynamics
- Kinetics

---

## Dual AI Assistant

### Mode A

Reasoning

Examples:

- Explain concepts
- Teach chemistry
- Quiz students
- Generate study guides

---

### Mode B

Deterministic Routing

Workflow

User

↓

Ollama understands request

↓

Produces structured command

↓

Python executes calculation

↓

Returns exact result

This guarantees mathematical accuracy.

---

## Utility Engine

Planned modules:

- JSON tools
- Base64
- Regex
- Time conversion
- Unit conversion

Future modules can be added independently.

---

## Study Engine

Features:

- Flashcards
- AI tutoring
- Markdown notes
- Study timer

---

## Document Engine

Local processing only.

Supports:

- PDFs
- Plain text

Future:

- OCR
- Office documents

---

# 8. Development Plan

## Phase 0 — Planning

Complete architecture.

Finalize specifications.

Identify risks.

---

## Phase 1 — Foundation

Build:

- FastAPI server
- Ollama connection
- Project structure

No UI polish yet.

---

## Phase 2 — Deterministic Engine

Implement:

- Formula parser
- Chemistry engine
- Math engine

Unit test thoroughly.

---

## Phase 3 — AI Integration

Implement:

- Dual-mode routing
- Prompt templates
- JSON command parser

---

## Phase 4 — Interface

Create:

- Dashboard
- Chat
- Tool panels
- Navigation

Focus only on structure.

---

## Phase 5 — Styling

Improve:

- Typography
- Spacing
- Colors
- Icons
- Cards

---

## Phase 6 — Motion

Add:

- Page transitions
- Hover states
- Loading animations
- Microinteractions

Remain subtle.

---

## Phase 7 — Tool Expansion

Implement:

- Study tools
- Utility tools
- PDF tools

---

## Phase 8 — Polish

Improve:

- Responsiveness
- Accessibility
- Error handling
- Performance
- Code cleanup

---

# 9. Critique Checklist

After every major phase, review:

- Does anything feel generic?
- Is architecture becoming too coupled?
- Can modules be separated further?
- Is the interface still minimal?
- Is every animation necessary?
- Are calculations still deterministic?
- Is the project easier to extend?

---

# 10. Quality Rules

Every implementation should follow these principles.

- Local-first
- Privacy-first
- Deterministic calculations
- Premium UI
- Clean architecture
- Modular code
- Strong documentation
- High readability
- Easy future expansion
- Production-quality organization

Never sacrifice long-term maintainability for short-term convenience.

---

# Long-Term Vision

HelpOS should evolve into a modular local AI operating environment rather than a single-purpose chemistry application.

The architecture should allow additional engines (physics, mathematics, programming, writing, productivity, and future AI capabilities) to be added without redesigning the core system.

Every feature should reinforce three guiding principles:

1. **Offline by default**
2. **Exact where correctness matters**
3. **Intelligent where reasoning adds value**

The goal is to build a platform that remains useful, extensible, and maintainable as AI capabilities continue to improve, allowing HelpOS to leverage stronger local models over time without requiring fundamental architectural changes.

# Scientific Data Standards

All scientific constants, reference values, atomic masses, molar masses, periodic table data, and chemistry calculations must use the official values published by the California Department of Education (CDE) whenever applicable.

## Periodic Table

The application shall use the official California Department of Education (CDE) Periodic Table of the Elements as the single authoritative source for:

- Atomic masses (molar masses)
- Element symbols
- Element names
- Atomic numbers
- Parenthesized isotope values where provided

No third-party periodic tables or alternate atomic mass values shall be used unless explicitly enabled in a future version.

This ensures all chemistry calculations exactly match:

- California Science Test (CAST)
- California educational standards
- High school chemistry coursework
- Classroom worksheets and assessments

## Deterministic Chemistry

Every chemistry calculation must reference the CDE dataset internally.

Examples include:

- Molar mass calculations
- Stoichiometry
- Mole conversions
- Percent composition
- Empirical formulas
- Molecular formulas
- Limiting reactants
- Gas law calculations
- Solution chemistry

The chemistry engine must never substitute alternative atomic mass values from external databases or the language model.

## Scientific Constants

Where applicable, standard scientific constants (e.g., Avogadro's number, the gas constant, STP definitions) should also be stored as deterministic constants within the application rather than generated by the AI.

All constants should be centralized in a single reference module to ensure consistency throughout the project.
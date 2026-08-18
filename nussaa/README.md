# Nussaa — support ticket analysis

The working folder for the workshop.

Nussaa (نص ساعة, "half an hour") is a fictional food delivery app. It does
not exist, and neither do its customers — everything here was written for a
workshop.

## What's here

```
tickets-q1/    200 support tickets, one per file
tickets-q2/    120 more, from the following quarter
context/       the product changelog and last quarter's report
AGENTS.md      conventions, and the report format to match
CLAUDE.md      the same file, under the name Claude Code reads
```

## Start

```bash
cd nussaa
agy          # Antigravity CLI — reads AGENTS.md
claude       # Claude Code    — reads CLAUDE.md
```

Start whichever agent your workshop uses. Then ask for what you want.

Read the rules file first if you want to know what the agent already knows
before you type anything. `AGENTS.md` and `CLAUDE.md` are the same file under
two names, because the two tools each read only their own.

## A note on the tickets

They are messy on purpose. Some are one useless line. Some are duplicates.
They arrive in Arabic, English, and both at once, because that is what a
Riyadh support queue looks like. Handling that is the point.

A few customers noticed the company is called "half an hour" and their food
took two. Those tickets are real complaints and also jokes; both things at
once, which is also what a real queue looks like.

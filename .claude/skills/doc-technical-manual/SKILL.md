---
name: doc-technical-manual
description: MODE A (existing code). Write the Technical Manual (installation, configuration, deployment, administration, security, monitoring, backup/recovery, troubleshooting) for a fed-in project. It is for sysadmins, DevOps, and IT support. Use when the user asks for a technical manual, operations manual, admin guide, installation guide, deployment guide, or runbook.
argument-hint: <project-slug or path> [target environment, e.g. Windows Server / Azure / Docker]
---

# Technical Manual

> **Mode A — Existing project.** Use this skill only when source code exists. For an idea with no code yet, use the Mode B `new-*` skills.

Input: `$ARGUMENTS` (slug or path, plus an optional target environment).

## Preconditions
1. Resolve `<slug>`. Run the `doc-intake` procedure if the profile is missing.
2. Read the profile, `mode-a-existing-project/templates/04-technical-manual.md`, and `mode-a-existing-project/rules/40-document-specific.md` §4.

## Procedure
1. **Architecture:** build the component table and a Mermaid diagram from docker-compose
   services, server entry points, DB connections, queues, caches, and external APIs.
   List every port found in code or config.
2. **Requirements:** take runtime versions from manifests (`engines`, `python_requires`,
   `TargetFramework`, base images). Hardware sizing is `[TBD]` unless it is defined
   (e.g. container resource limits).
3. **Installation:** reconstruct exact steps from Dockerfile / Makefile / scripts / CI /
   README. Provide them for the target environment the user named. Otherwise provide
   them for what the project supports (e.g. Docker + bare-metal Linux). Put each command
   in its own code block with the shell named. Unverified commands get `[VERIFY]`.
4. **Configuration reference (critical):** Grep every env/config read in the code. Merge
   with `.env.example` and the config files. For each key, record whether it is required
   (does the code fail or throw without it?), its default (the code fallback), its type,
   its purpose, and the `path:line` where it is read (in a comment or appendix). Flag
   keys that the code reads but are missing from `.env.example`, and the reverse.
5. **Deployment:** describe it from CI/CD workflows and infra-as-code. If there is none,
   write a manual deployment procedure marked `[ASSUMPTION]`, and recommend automation.
6. **Administration:** cover user/role management (seed scripts, admin screens, CLI
   commands), scheduled jobs, and maintenance tasks (migrations, cache clear, log rotation).
7. **Security:** cover the auth mechanism, password hashing, CORS, CSRF, HTTPS, secret
   storage, and a hardening checklist based on actual gaps found.
8. **Monitoring and logging:** cover the logger config, log destinations, health endpoints,
   and metrics libraries. If there is none, state that and recommend some.
9. **Backup and recovery:** use the database type to give standard backup and restore
   commands (e.g. `pg_dump`, `mysqldump`, `sqlcmd BACKUP DATABASE`). Mark RTO/RPO `[TBD]`.
10. **Troubleshooting:** derive entries from startup failure paths, connection errors,
    and missing-config errors in the code.

## Output
`output/mode-a/<slug>/04-technical-manual.md`

Run the review checklist. Report the file path, the number of config keys documented,
the config mismatches found, and the Open Items.

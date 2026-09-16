# Security Policy

## Supported versions

Security fixes are developed for the latest supported MonitorGlow release line.

## Reporting a vulnerability

Please do not open a public issue for an unpatched vulnerability. Use GitHub's private vulnerability reporting feature when it is enabled for this repository. If private reporting is unavailable, contact the project maintainer through the support channel documented in the README and avoid including exploit details in public discussions.

Include the affected version, operating system, reproduction steps, impact, and any suggested mitigation. Reports will be triaged before disclosure.

## Security design principles

MonitorGlow is offline-first. Display control does not require telemetry or a cloud account. Application builds should not embed credentials that are expected to remain secret on an end-user machine. Dependencies and release workflows are continuously audited through the repository quality gates.

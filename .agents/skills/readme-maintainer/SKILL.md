---
name: readme-maintainer
description: Create or reorganize a repository README. Use when making the README concise, maintaining English/Japanese pairs, or moving detailed procedures to dedicated documentation.
---

# README Maintainer

Read the [technical documentation policy](../../../docs/ai/documentation-policy.md) and repository instructions. Inventory the existing README and links before editing it.

## Default structure

1. Overview
2. Installation
3. Usage
4. Advanced Usage
5. Documentation

For a policy-only repository, replace Installation with Adoption or Integration; do not invent installation steps.

## Procedure

1. Keep the purpose, supported use, important prerequisites, and material limitations near the top.
2. Retain concise, verified quick-start commands only when the README's audience needs them.
3. Move detailed implementation history, experiment evidence, recovery procedures, and internal specifications to suitable documents. Add direct links and a source-to-destination map before dropping substantial material.
4. Check every retained command, path, feature, and status against the target revision. Preserve uncertainty and experimental labels.
5. Keep `README.md` in English and create or update `README_jp.md` as a semantic translation. Preserve code and identifiers exactly.
6. Check internal links, heading structure, and whether a new reader can find the detailed material.

## Report

Compare the original and revised README by concrete changes in length, structure, navigation, claims, and migrated content. Name any missing, unverified, or stale destination and keep it visible as follow-up work.

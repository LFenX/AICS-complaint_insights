# Norm Packet: T-INSIGHTS-MCP-REPAIR-20261030-05 / S6

- Objective: 修复工具限频、窄屏提示和当前交接并完成原需求复验
- Rule set: `VC-PPG-TAIL-001` / `d7abae34423493620a86aa8f1533a977dbe4b3e612f773fadea4ec83fc6d6eee`
- Normative sources digest: `43c0990e110fec3ae97a99bd2fc7b43a31c5786e21f9ce7b8876811c87efb3ac`
- Resolver digest: `add9aff766c9b5ddb3eed0cdf5da8f7e464707648f5ea4870c98a462002ae153`
- TaskContract Schema digest: `ad3db51c243bee235546c3093cba400fdb2227e7fc7e97dc2a4fc2d055672045`
- Task Profile digest: `f397a0909d74d0e7002c0c397c3f3554f40296c1e8e0f584b57da0d33f042750`
- Control strength: enhanced
- Independent review: True
- Explicit human gate: False
- Applicable standards: C01, C02, C03, C04, C05, C06, C07, C08, C09, C10, C11, C12, E01, E02, E03, E05
- Stage context: C03, C04, C05, C06, C09, C10, C11, C12, E01, E02, E03, E05
- Pending standards: None

## Blocking reasons

- None

## Complete normative coverage

- `norm-source-pack.md` contains the complete contents and SHA-256 of every selected governance, index, applicable, and pending source.
- The control cards and section locators below are non-exhaustive navigation aids; they are never the complete normative obligation set.
- Before a material action, search the Source Pack and read the passages governing that action. If relevance cannot be narrowed safely, read the complete selected source.

## Non-trimmable control cards (navigation summary)

### C03 — PRD and Feature

- Owned Profiles in full index: 7
- Source sections: §3, §7, §8, §10, §12, §15, §17, §18
- MUST: observable behavior
- MUST: requirement-to-acceptance link
- MUST: state and edge conditions
- MUST: supersession trace

### C04 — Atomic Requirement and Evolution

- Owned Profiles in full index: 7
- Source sections: §3, §7, §8, §10, §12, §15, §17, §18
- MUST: atomic requirement identity
- MUST: revision and supersession trace
- MUST: defect-to-requirement reference
- MUST: migration and retirement boundary

### C05 — Acceptance, Verification and Validation

- Owned Profiles in full index: 8
- Source sections: §3, §7, §8, §10, §12, §15, §17, §18
- MUST: acceptance criteria
- MUST: verification evidence
- MUST: validation conclusion
- MUST: failed and blocked checks remain visible

### C06 — UX and Technical Design

- Owned Profiles in full index: 10
- Source sections: §3, §7, §8, §10, §12, §15, §17, §18
- MUST: surface-specific design decision
- MUST: interface and data contract
- MUST: failure and rollback design
- MUST: design-to-requirement trace

### C09 — Agent Execution and Evidence

- Owned Profiles in full index: 9
- Source sections: §3, §7, §8, §10, §12, §15, §17, §18
- MUST: TaskContract before execution
- MUST: ordered material RunLedger events
- MUST: TaskOutcome terminal facts
- MUST: side effect and evidence trace

### C10 — Decision Traceability and Lineage

- Owned Profiles in full index: 8
- Source sections: §3, §7, §8, §10, §12, §15, §17, §18
- MUST: source-to-change trace
- MUST: decision authority
- MUST: cross-task lineage
- MUST: derived view cannot own authority

### C11 — Configuration, Version, Baseline and Change

- Owned Profiles in full index: 10
- Source sections: §3, §7, §8, §10, §12, §15, §17, §18
- MUST: source snapshot
- MUST: revision and amendment
- MUST: change identity
- MUST: baseline, supersession and rollback trace

### C12 — Review, Quality Gate and Product Health

- Owned Profiles in full index: 8
- Source sections: §3, §7, §8, §10, §12, §15, §17, §18
- MUST: entry and exit gate
- MUST: independent review when required
- MUST: human acceptance remains human
- MUST: residual risk and health conclusion

### E01 — Architecture Governance

- Owned Profiles in full index: 8
- Source sections: §3, §7, §8, §10, §13, §15, §17, §18
- MUST: architecture boundary
- MUST: decision and dependency
- MUST: cross-repository impact
- MUST: architecture risk and verification

### E02 — Security, Privacy and Compliance

- Owned Profiles in full index: 9
- Source sections: §3, §7, §8, §10, §13, §15, §17, §18
- MUST: identity and access boundary
- MUST: threat and vulnerability
- MUST: privacy and compliance obligation
- MUST: security evidence and residual risk

### E03 — Data and AI Data Governance

- Owned Profiles in full index: 9
- Source sections: §3, §7, §8, §10, §13, §15, §17, §18
- MUST: data source and lineage
- MUST: schema and quality
- MUST: license and permitted use
- MUST: retention and deletion

### E05 — Product Operations and Service Management

- Owned Profiles in full index: 10
- Source sections: §3, §7, §8, §10, §13, §15, §17, §18
- MUST: release and rollback
- MUST: service objective and observability
- MUST: incident and problem trace
- MUST: operational feedback closure

## Profile instantiation rules

- profile owner standard must first be applicable
- stable valid baseline uses Reference instead of duplicate creation
- event profiles use On Event only when the named event occurred
- review or presentation views use Generate on demand and never become authority
- N/A requires rule reference, fact basis, scope, owner, and re-evaluation trigger
- a profile may share a physical carrier but keeps independent identity, state, trace, and history

## Resolution rules

- 1. law, policy, approved baseline, and explicit accountable-human authority within scope
- 2. Critical over High over Medium over Low control strength
- 3. active extension and explicit applicability fact over generic route
- 4. change surface and all development types are unioned; primary type is display-only
- 5. delivery scenario, baseline inheritance, mode, and stage add controls but do not subtract
- 6. specific owner-standard profile rule over generic profile rule
- 7. when equal-rank rules conflict, keep both, mark conflict, and stop the affected action

## Source locators

| Source | Sections | Embedded path |
|---|---|---|
| VC-PPG-COM-001 | §2, §10, §12 | `references/01_治理基线/Vibe_Coding_公共术语与规范性用语基线_V6.3.md` |
| VC-PPG-COM-002 | §2, §3, §4, §22, §23 | `references/01_治理基线/Vibe_Coding_受控产物目录与状态模型_V6.3.md` |
| VC-PPG-DEC-001 | §9, §10, §11, §12, §13, §14, §15, §16, §17 | `references/01_治理基线/Vibe_Coding_P2裁剪与扩展规范适用性决议_V6.3.md` |
| VC-PPG-PRO-001 | §10, §14, §15, §16, §17 | `references/01_治理基线/Vibe_Coding_任务类型裁剪与统一执行流程规范_V6.3.md` |
| VC-PPG-IDX-001 | §2, §3, §4, §9 | `references/05_记录与登记册/V6.3_跨规范产物归属索引.md` |
| C01 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C01_Product_Discovery_Evidence_and_Intent_Standard.md` |
| C02 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C02_Initiative_and_Scope_Standard.md` |
| C03 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C03_PRD_and_Feature_Standard.md` |
| C04 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C04_Atomic_Requirement_and_Evolution_Standard.md` |
| C05 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C05_Acceptance_Verification_and_Validation_Standard.md` |
| C06 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C06_UX_and_Technical_Design_Standard.md` |
| C07 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C07_Human_Agent_Collaboration_Standard.md` |
| C08 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C08_Agent_Context_Governance_Standard.md` |
| C09 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C09_Agent_Execution_and_Evidence_Standard.md` |
| C10 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C10_Decision_Traceability_and_Lineage_Standard.md` |
| C11 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C11_Configuration_Version_Baseline_and_Change_Standard.md` |
| C12 | §3, §7, §8, §10, §12, §15, §17, §18 | `references/02_核心规范/C12_Review_Quality_Gate_and_Product_Health_Standard.md` |
| E01 | §3, §7, §8, §10, §13, §15, §17, §18 | `references/03_扩展规范/E01_Architecture_Governance_Extension_Standard.md` |
| E02 | §3, §7, §8, §10, §13, §15, §17, §18 | `references/03_扩展规范/E02_Security_Privacy_and_Compliance_Extension_Standard.md` |
| E03 | §3, §7, §8, §10, §13, §15, §17, §18 | `references/03_扩展规范/E03_Data_and_AI_Data_Governance_Extension_Standard.md` |
| E05 | §3, §7, §8, §10, §13, §15, §17, §18 | `references/03_扩展规范/E05_Product_Operations_and_Service_Management_Extension_Standard.md` |

## Compiler boundary

This packet is a DerivedView. Normative authority remains in the cited sources and VC-PPG-TAIL-001. A hash or source change makes this packet stale.

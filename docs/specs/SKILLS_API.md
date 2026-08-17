# SPEC: the skill API — one definition, five artifacts

Status: presented for acceptance. Direction ratified: typed Rust skills publishing
over MCP (tools + `skill://` per SEP-2640); compiled built-ins; Guardian-validated
schema-first TS/Python declarations executing in-pod; small per-agent surfaces.
References: `SKILLS.md` (architecture), `PROTOCOL.md` §6 (hecate-wire), `REGISTRY.md`
(Skill kind, staging).

## 1. The Rust surface

```rust
#[derive(Skill)]                       // the single interpreter of the definition
#[skill(name = "workspace", domain = Domain::Implementation)]
pub struct WorkspaceSkill { /* handles into owning stores — no Arc, per doctrine */ }

impl SkillImpl for WorkspaceSkill {
    type Action = WorkspaceAction;     // #[derive(Wire)] closed enum — the façade
    type Output = WorkspaceOutput;     // #[derive(Wire)]
    const INSTRUCTIONS: &'static str = include_str!("workspace.skill.md");
    const CONTRACT: Contract = Contract {
        produces: &[ArtifactKind::FileChange],
        consumes: &[ArtifactKind::WriteBasis],
    };
    const CAPABILITIES: Capabilities = Capabilities::WORKSPACE_RW; // Guardian-visible
    async fn invoke(&mut self, cx: &mut SkillCx, a: Self::Action)
        -> Result<Self::Output, SkillError>;
}
```

The derive emits, from this one definition: (1) the hecate-wire codecs and schema
hashes; (2) the MCP tool projection (JSON Schema generated from the same reflection
— no serde, no schemars, no second interpreter); (3) the `skill://` instructional
resource (INSTRUCTIONS + supporting files, content-digested); (4) the registry
`Skill` document (name, domain, contract, **declared capabilities**); (5) dispatch
glue with input/output validation at the boundary.

- **Façade-first**: one skill, one closed `Action` enum — never sibling verb
  families. Append-only evolution checked against the committed schema snapshot.
- `SkillCx` carries the claims façade, the store handles, and the emitters — skills
  reach the world through it, never ambiently.

## 2. TS/Python declarations

- Declared against **generated SDKs** (from the same JSON-Schema reflection): the
  declaration — schemas, contract, metadata, declared capabilities — is a static
  artifact the **Guardian validates at staging, before any code loads**
  (inventory-from-declaration; `REGISTRY.md` §2).
- Handlers execute **in-pod**, in the role image's runtime, behind the identical
  typed contract: inputs validated in, outputs validated out, capabilities bounded
  by the bundle. A skill can declare nothing its bundle doesn't grant — checked at
  staging, enforced by the warden at effect boundaries regardless.

## 3. Surface discipline

- An agent's default surface = the shared fabric façades + its role façades — a
  derived handful (counted, tested), with progressive disclosure (`search` +
  activation) behind it. Activation state can shrink.
- **Omission is absence**: a capability a role must never hold is not registered in
  its bundle — invoking it is *unknown tool*, not *denied tool*.

## 4. Tests and acceptance

| # | Test | Catches |
|---|---|---|
| S1 | Schema fidelity: Rust type → JSON Schema → TS/Py SDK round-trip against the committed vector corpus | drift between wire, MCP, and SDKs |
| S2 | Omission semantics: unregistered skill ⇒ unknown (not denied); registered-but-inactive ⇒ discoverable via search | gating theater; hidden-but-present leaks |
| S3 | Contract enforcement: produces/consumes checked at dispatch; violations typed | protocol artifacts drifting from declarations |
| S4 | Capability ⊆ bundle: staging refuses any declaration exceeding its bundle's grants; warden enforcement holds even if staging were bypassed | privilege via declaration |
| S5 | Evolution trybuild: field/variant removal or reorder in any skill type is a compile error against the snapshot | silent wire breaks in tool schemas |
| S6 | Surface count: each role's default-visible surface within its derived budget (CI-counted; the Sylk 31-tool turn is the named regression) | tool-surface sprawl returning |

Acceptance: one derive produces all five artifacts (no second interpreter exists);
Guardian static validation precedes every TS/Py load, structurally; S1/S5/S6
permanent; `SkillCx` is the only capability path (no ambient reaches — lint).

# PRD: [Your Project Name]

## 1. Product overview

### 1.1 Document title and version
- PRD: [Your Project Name]
- Version: 1.0

### 1.2 Product summary
[2-3 paragraph summary of what this project does, who it's for, and why it matters. Include the key value proposition and how it solves user problems.]

## 2. Goals

### 2.1 Business goals
- [Business goal 1]
- [Business goal 2]
- [Business goal 3]

### 2.2 User goals
- [User goal 1]
- [User goal 2]
- [User goal 3]

### 2.3 Non-goals
- [What this project explicitly will NOT do]
- [Feature/scope exclusion 1]
- [Feature/scope exclusion 2]

## 3. User personas

### 3.1 Key user types
- [User type 1]
- [User type 2]
- [User type 3]

### 3.2 Basic persona details
- **[Persona name 1]**: [Brief description and needs]
- **[Persona name 2]**: [Brief description and needs]
- **[Persona name 3]**: [Brief description and needs]

### 3.3 Role-based access
- **[Role 1]**: [Access level and permissions]
- **[Role 2]**: [Access level and permissions]
- **[Role 3]**: [Access level and permissions]

## 4. Phases

### 4.1 Phase Overview

Project work is organized into phases, each with a reserved task ID range:

- **Phase 0: Setup & Infrastructure** (Task IDs: 1-99)
  - [Setup objectives and deliverables]
  - Status: [ ] Pending | [🔄] In Progress | [✅] Complete

- **Phase 1: Foundation** (Task IDs: 100-199)
  - [Foundation objectives and deliverables]
  - Status: [ ] Pending

- **Phase 2: Core Development** (Task IDs: 200-299)
  - [Core development objectives and deliverables]
  - Status: [ ] Pending

### 4.2 Phase References
- Phase documents: `.trent/phases/`
- Phase template: `.trent/templates/phase_template.md`

### 4.3 Adding New Phases
- Use `@trent-phase-add` in Cursor
- Phases can be added at any time
- Gaps in numbering allowed for pivots

## 5. User experience

### 5.1 Entry points & first-time user flow
**For [User Type 1]:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**For [User Type 2]:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

### 5.2 Core experience
**[Core User Flow 1]:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**[Core User Flow 2]:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

### 5.3 Advanced features & edge cases
- [Advanced scenario 1]
- [Edge case handling 1]
- [Error recovery flow]

### 5.4 UI/UX highlights
- [UI principle 1]
- [UX consideration 1]
- [Interaction pattern 1]

## 6. Narrative
[Write a compelling narrative that tells the story of a user successfully using your product. Make it concrete with specific examples. This should bring the PRD to life and help readers visualize the product in action.]

## 7. Success metrics

### 7.1 User-centric metrics
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]
- [Metric 3]: [Target value]

### 7.2 Business metrics
- [Metric 1]
- [Metric 2]
- [Metric 3]

### 7.3 Technical metrics
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]
- [Metric 3]: [Target value]

## 8. Technical considerations

### 8.1 Affected subsystems
- **Primary subsystems** (directly modified/extended):
  - [Subsystem 1]: [How it's affected]
  - [Subsystem 2]: [How it's affected]

- **Secondary subsystems** (indirectly affected):
  - [Subsystem 1]: [How it's affected]
  - [Subsystem 2]: [How it's affected]

### 8.2 Integration points
- [Integration 1]
- [Integration 2]
- [Integration 3]

### 8.3 Data storage & privacy
- [Storage approach]
- [Privacy consideration 1]
- [Privacy consideration 2]
- [Compliance requirement]

### 8.4 Scalability & performance
- [Scalability consideration 1]
- [Performance target 1]
- [Performance target 2]

### 8.5 Potential challenges
- [Challenge 1 and mitigation]
- [Challenge 2 and mitigation]
- [Challenge 3 and mitigation]

## 9. Milestones & sequencing

### 9.1 Project estimate
- **[Size: Small/Medium/Large]**: [Time estimate]

### 9.2 Team size & composition
- [Team size]: [Role 1], [Role 2], [Role 3]

### 9.3 Suggested phases

- **Phase 1: [Phase Name]** ([Duration])
  - Key deliverables:
    - [Deliverable 1]
    - [Deliverable 2]
    - [Deliverable 3]

- **Phase 2: [Phase Name]** ([Duration])
  - Key deliverables:
    - [Deliverable 1]
    - [Deliverable 2]
    - [Deliverable 3]

- **Phase 3: [Phase Name]** ([Duration])
  - Key deliverables:
    - [Deliverable 1]
    - [Deliverable 2]
    - [Deliverable 3]

## 10. User stories

### 10.1 [User Story Title 1]
- **ID**: US-001
- **Description**: As a [user type], I want to [action], so that [benefit].
- **Acceptance Criteria**:
  - [Criterion 1]
  - [Criterion 2]
  - [Criterion 3]

### 10.2 [User Story Title 2]
- **ID**: US-002
- **Description**: As a [user type], I want to [action], so that [benefit].
- **Acceptance Criteria**:
  - [Criterion 1]
  - [Criterion 2]
  - [Criterion 3]

### 10.3 [User Story Title 3]
- **ID**: US-003
- **Description**: As a [user type], I want to [action], so that [benefit].
- **Acceptance Criteria**:
  - [Criterion 1]
  - [Criterion 2]
  - [Criterion 3]

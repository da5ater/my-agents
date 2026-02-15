# ANKIFY Executable Enforcement Schema (v4)

This file contains the machine-checkable rules for Ankify.
Doctrine is the source of truth for what cards to create and how they should read.
If any rule here conflicts with doctrine, follow doctrine and treat the schema rule as stale.
Execute scopes in order: PRE_DISCOVERY -> POST_DISCOVERY -> PRE_CARD -> PER_CARD -> POST_CARD -> POST_NOTE -> SERIALIZATION -> GLOBAL.

Computed field conventions used by rules:
- overlap_ratio(a, b): common_token_count(a, b) / max(1, token_count(a))
- front.word_count: count of whitespace-delimited tokens in front
- front.jargon_terms_count: count of tokens in front with length >= 12 or containing 2+ uppercase letters
- read_complete: true if the input read operation finished
- file_text_length: length of full_document_text
- parse_success: true if parsing completed without fatal errors
- partial_read: true if parsing failed but text length > 0
- chat_output_contains_tsv: true if the assistant output includes TSV rows
- relational_operator_present: true if front contains relational operator words
- references_two_distinct_concepts: true if front references two distinct H2 concepts
- validate_tsv_passed: true if scripts/validate_tsv.sh reports zero failures
- front_label_length: number of characters inside the leading <strong>...</strong>
- run_stats_present: true if run-level stats are available
- require_run_stats: true if run-level stats are required
- max_cards_per_note: clamp(10 + code_blocks*2, 12, 18)

```yaml
# PRE_DISCOVERY - before any file is read

R-PD-001:  # SilentExecution
  Scope: PRE_DISCOVERY
  ActivationCondition: agent_invoked == true
  RequiredArtifact: none
  ValidationMethod: chat_output_contains_tsv == false
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-PD-002:  # AutoFileCreation
  Scope: PRE_DISCOVERY
  ActivationCondition: agent_invoked == true
  RequiredArtifact: output_path
  ValidationMethod: output_path_set == true
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-PD-003:  # ManifestBuild
  Scope: PRE_DISCOVERY
  ActivationCondition: input_mode in [folder, cwd]
  RequiredArtifact: file_manifest
  ValidationMethod: manifest.length > 0 AND all_entries_have_status_field
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: [R-PD-004]
  ConflictsWith: []

R-PD-004:  # RecursiveScan
  Scope: PRE_DISCOVERY
  ActivationCondition: input_mode in [folder, cwd]
  RequiredArtifact: directory_tree
  ValidationMethod: scan_includes_subdirectories == true
  FailureBehavior: reject
  PrecedenceWeight: 90
  Dependencies: []
  ConflictsWith: []

R-PD-005:  # DefaultExclusions
  Scope: PRE_DISCOVERY
  ActivationCondition: input_mode in [folder, cwd]
  RequiredArtifact: exclusion_list
  ValidationMethod: excluded_dirs.contains_all([node_modules, .git, .obsidian])
  FailureBehavior: warn
  PrecedenceWeight: 50
  Dependencies: []
  ConflictsWith: []

R-PD-006:  # ZeroSkipPolicy
  Scope: PRE_DISCOVERY
  ActivationCondition: input_mode in [folder, cwd]
  RequiredArtifact: file_manifest
  ValidationMethod: for_all(f in manifest): f.status in [PROCESSED, SKIPPED_WITH_REASON, PARTIAL_READ]
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: [R-PD-003]
  ConflictsWith: []

# POST_DISCOVERY - after file read, before card gen

R-POD-001:  # CompleteInputRead
  Scope: POST_DISCOVERY
  ActivationCondition: file_loaded == true
  RequiredArtifact: full_document_text
  ValidationMethod: file_text_length > 0 AND full_document_text != null
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-POD-002:  # KnowledgeElementExtraction
  Scope: POST_DISCOVERY
  ActivationCondition: R-POD-001.passed
  RequiredArtifact: element_inventory
  ValidationMethod: >
    element_types.is_superset_of(
      [definitions, distinctions, procedures, code_examples,
       failure_modes, mental_models].intersect(present_in_input))
  FailureBehavior: reject
  PrecedenceWeight: 90
  Dependencies: [R-POD-001]
  ConflictsWith: []

R-POD-003:  # ContextDependencyMapping
  Scope: POST_DISCOVERY
  ActivationCondition: categorized_elements.any(type == code_example)
  RequiredArtifact: context_map
  ValidationMethod: >
    for_all(ce in code_elements):
      ce.has_fields([imports, variables, state_shapes, external_deps])
  FailureBehavior: reject
  PrecedenceWeight: 85
  Dependencies: [R-POD-002]
  ConflictsWith: []

R-POD-004:  # PrincipleMapping
  Scope: POST_DISCOVERY
  ActivationCondition: R-POD-002.passed
  RequiredArtifact: principle_map
  ValidationMethod: for_all(elem): elem.mapped_principles.length >= 1
  FailureBehavior: warn
  PrecedenceWeight: 70
  Dependencies: [R-POD-002]
  ConflictsWith: []

R-POD-005:  # Tier1RuleEvaluation
  Scope: POST_DISCOVERY
  ActivationCondition: R-POD-002.passed
  RequiredArtifact: rule_verdicts
  ValidationMethod: >
    for_all(r in tier1_rules): r.verdict in [APPLICABLE, NOT_APPLICABLE]
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: [R-POD-002]
  ConflictsWith: []

R-POD-006:  # RuleApplicationPlanBuild
  Scope: POST_DISCOVERY
  ActivationCondition: R-POD-005.passed
  RequiredArtifact: rule_application_plan
  ValidationMethod: >
    for_all(r in tier1_rules where r.verdict == APPLICABLE):
      r.plan.has_fields([target_content, card_type, estimated_count])
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: [R-POD-005]
  ConflictsWith: []

R-POD-007:  # InputClassification
  Scope: POST_DISCOVERY
  ActivationCondition: R-POD-001.passed
  RequiredArtifact: classification
  ValidationMethod: input_classification.type in [PURE_THEORY, PURE_CODE, MIXED]
  FailureBehavior: reject
  PrecedenceWeight: 90
  Dependencies: [R-POD-001]
  ConflictsWith: []

R-POD-008:  # InternalizationReport
  Scope: POST_DISCOVERY
  ActivationCondition: R-POD-001.passed
  RequiredArtifact: internalization_report
  ValidationMethod: >
    internalization_report.has_fields([summary, boundaries, misconceptions, links]) AND
    internalization_report.summary.sentences_count >= 3 AND
    internalization_report.boundaries.count >= 1 AND
    internalization_report.misconceptions.count >= 1 AND
    internalization_report.links.count >= 1
  FailureBehavior: reject
  PrecedenceWeight: 90
  Dependencies: [R-POD-007]
  ConflictsWith: []

R-POD-009:  # PartialReadAllowed
  Scope: POST_DISCOVERY
  ActivationCondition: parse_success == false AND file_text_length > 0
  RequiredArtifact: file_status
  ValidationMethod: file_status == PARTIAL_READ
  FailureBehavior: warn
  PrecedenceWeight: 60
  Dependencies: [R-POD-001]
  ConflictsWith: []

R-POD-010:  # CardBudgetPlan
  Scope: POST_DISCOVERY
  ActivationCondition: R-POD-001.passed
  RequiredArtifact: card_budget_plan
  ValidationMethod: >
    card_budget_plan.has_fields([
      target_total_cards_min,
      target_total_cards_max,
      target_synthesis,
      target_cross_h2_synthesis,
      target_model,
      target_failure_mode,
      target_negation,
      target_counter_evidence,
      target_constructive_min,
      target_constructive_max,
      target_theory_max,
      target_definition_max,
      target_procedure_max
    ])
  FailureBehavior: reject
  PrecedenceWeight: 85
  Dependencies: [R-POD-008]
  ConflictsWith: []

# PRE_CARD - before generating each card

R-PC-001:  # TenMinuteValueHeuristic
  Scope: PRE_CARD
  ActivationCondition: candidate_element_identified
  RequiredArtifact: value_assessment
  ValidationMethod: value_assessment in [YES, UNSURE] OR (NO AND card_not_created)
  FailureBehavior: reject
  PrecedenceWeight: 80
  Dependencies: []
  ConflictsWith: []

R-PC-002:  # BasicsFirstOrdering
  Scope: PRE_CARD
  ActivationCondition: input_classification.type in [PURE_CODE, MIXED]
  RequiredArtifact: card_sequence
  ValidationMethod: for_all(theory, code where same_concept): theory.index < code.index
  FailureBehavior: warn
  PrecedenceWeight: 60
  Dependencies: [R-POD-007]
  ConflictsWith: []

R-PC-003:  # StructuralDensityIndex (SDI)
  Scope: PRE_CARD
  ActivationCondition: processing_note == true
  RequiredArtifact: structural_element_count
  ValidationMethod: >
    card_count >= structural_elements_count AND
    SDI (cards / structural_elements) <= 2.5
  FailureBehavior: reject_if_below_1.0, warn_if_above_2.5
  PrecedenceWeight: 85
  Dependencies: [R-POD-002]
  ConflictsWith: []

R-PC-004:  # MinDensityPerH2
  Scope: PRE_CARD
  ActivationCondition: h2_section_identified
  RequiredArtifact: h2_element_count
  ValidationMethod: h2_cards >= structural_elements_in_h2
  FailureBehavior: regenerate
  PrecedenceWeight: 80
  Dependencies: [R-POD-002]
  ConflictsWith: [R-POC-006]

R-PC-005:  # NoCodeBlockSkip
  Scope: PRE_CARD
  ActivationCondition: code_block_present
  RequiredArtifact: code_block_inventory
  ValidationMethod: for_all(cb in code_blocks): cb.constructive_card_count >= 1
  FailureBehavior: regenerate
  PrecedenceWeight: 90
  Dependencies: []
  ConflictsWith: []

R-PC-006:  # UnderstandingPrerequisite
  Scope: PRE_CARD
  ActivationCondition: candidate_element_identified
  RequiredArtifact: comprehension_check
  ValidationMethod: understanding_confirmed == true
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: []
  ConflictsWith: []

# PER_CARD - validated on every generated card

R-C-001:  # GenerationEffect_NoPassiveCopy
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: overlap_ratio(card.back, source_text) <= 0.35
  FailureBehavior: regenerate
  PrecedenceWeight: 90
  Dependencies: []
  ConflictsWith: []

R-C-002:  # Atomicity_OneIdea
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: card.concept_count == 1 AND (type != CONSTRUCTIVE OR back.line_count <= 6)
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: []
  ConflictsWith: [R-C-009]

R-C-003:  # FeynmanTest_PlainLanguage
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: front.word_count <= 35 AND front.jargon_terms_count <= 2
  FailureBehavior: regenerate
  PrecedenceWeight: 85
  Dependencies: []
  ConflictsWith: []

R-C-004:  # ContextDocking
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: front.contains_context_label OR front.contains_anchoring_phrase
  FailureBehavior: regenerate
  PrecedenceWeight: 80
  Dependencies: []
  ConflictsWith: []

R-C-005:  # Connectivity_NoBroaderIsolation
  Scope: PER_CARD
  ActivationCondition: card.is_connectivity_card == true
  RequiredArtifact: card_set
  ValidationMethod: card.related_cards_in_same_note >= 1
  FailureBehavior: regenerate
  PrecedenceWeight: 60
  Dependencies: []
  ConflictsWith: []

R-C-006:  # SignalToNoise
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: front.word_count <= 50 AND front.ends_with("?") AND NOT front.contains(".")
  FailureBehavior: regenerate
  PrecedenceWeight: 75
  Dependencies: []
  ConflictsWith: [R-C-007]

R-C-007:  # ContextMandate_Constructive
  Scope: PER_CARD
  ActivationCondition: card.type == CONSTRUCTIVE
  RequiredArtifact: card
  ValidationMethod: >
    front.provides_variables AND front.provides_imports AND
    front.provides_scope AND front.provides_expected_behavior
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: [R-POD-003]
  ConflictsWith: [R-C-006]

R-C-008:  # WhiteboardRule_DemandCreation
  Scope: PER_CARD
  ActivationCondition: card.type == CONSTRUCTIVE
  RequiredArtifact: card
  ValidationMethod: front.verb in [Write, Implement, Create, Build, Add]
  FailureBehavior: regenerate
  PrecedenceWeight: 85
  Dependencies: []
  ConflictsWith: []

R-C-009:  # CodeDecomposition_AntiMonolith
  Scope: PER_CARD
  ActivationCondition: source_code_block.line_count > 5
  RequiredArtifact: decomposed_cards
  ValidationMethod: decomposed_cards.length >= 2 AND all sub-cards.back <= 6 lines
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: []
  ConflictsWith: [R-C-002]

R-C-010:  # CodeAnswerMaxLines
  Scope: PER_CARD
  ActivationCondition: card.type == CONSTRUCTIVE
  RequiredArtifact: card
  ValidationMethod: card.back.line_count <= 6
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: []
  ConflictsWith: []

R-C-011:  # CodeFrontScope
  Scope: PER_CARD
  ActivationCondition: card.type == CONSTRUCTIVE
  RequiredArtifact: card
  ValidationMethod: scope_specificity != WHOLE_SYSTEM AND targets_single_concept
  FailureBehavior: regenerate
  PrecedenceWeight: 85
  Dependencies: []
  ConflictsWith: []

R-C-012:  # MereExposure_ActiveRecall
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: front.verb in [Write, Explain, Describe, Implement, Build, Create, Add, Define]
  FailureBehavior: regenerate
  PrecedenceWeight: 80
  Dependencies: []
  ConflictsWith: []

R-C-013:  # YesNoProhibition
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: front.expected_answer_type != BOOLEAN
  FailureBehavior: regenerate
  PrecedenceWeight: 85
  Dependencies: []
  ConflictsWith: []

R-C-014:  # SetAvoidance
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: NOT front.matches("list * things") AND NOT front.matches("name all")
  FailureBehavior: reject
  PrecedenceWeight: 85
  Dependencies: []
  ConflictsWith: []

R-C-015:  # InterferencePrevention
  Scope: PER_CARD
  ActivationCondition: card.type != CONSTRUCTIVE
  RequiredArtifact: card
  ValidationMethod: >
    NOT front.contains(" or ") AND NOT back.contains(" or ") AND
    NOT front.contains(" / ") AND NOT back.contains(" / ")
  FailureBehavior: regenerate
  PrecedenceWeight: 80
  Dependencies: []
  ConflictsWith: []

R-C-016:  # WordChoiceOptimization
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: front.trailing_messages == 0 AND back.trailing_messages == 0
  FailureBehavior: regenerate
  PrecedenceWeight: 70
  Dependencies: []
  ConflictsWith: []

R-C-017:  # SemanticAnchoring
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: front.contains_context_label OR front.contains(":")
  FailureBehavior: warn
  PrecedenceWeight: 50
  Dependencies: []
  ConflictsWith: []

R-C-018:  # DomainContextCues
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: >
    front.starts_with("<strong>") AND
    front.contains("</strong><br>") AND
    front_label_length > 0
  FailureBehavior: regenerate
  PrecedenceWeight: 75
  Dependencies: []
  ConflictsWith: []

R-C-019:  # SourceTraceability
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: card.obsidian_url != null AND != ""
  FailureBehavior: reject
  PrecedenceWeight: 90
  Dependencies: []
  ConflictsWith: []

R-C-020:  # EmotionalSalience
  Scope: PER_CARD
  ActivationCondition: source has failure_mode OR emotional_example
  RequiredArtifact: card
  ValidationMethod: card.uses_emotional_hook OR consequence_framing
  FailureBehavior: warn
  PrecedenceWeight: 40
  Dependencies: []
  ConflictsWith: []

R-C-021:  # CardContentPurity
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: >
    NOT front.contains("Rule:") AND NOT front.contains("Evidence:") AND
    NOT back.contains("Rule:") AND NOT back.contains("Evidence:") AND
    NOT contains("[Source:")
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: [R-S-009]

R-C-023:  # NegationFormat
  Scope: PER_CARD
  ActivationCondition: card.type == NEGATION
  RequiredArtifact: card
  ValidationMethod: front.contains("NOT") OR front.contains("differs from")
  FailureBehavior: regenerate
  PrecedenceWeight: 80
  Dependencies: []
  ConflictsWith: []

R-C-024:  # CounterEvidenceFormat
  Scope: PER_CARD
  ActivationCondition: card.type == COUNTER_EVIDENCE
  RequiredArtifact: card
  ValidationMethod: front.contains("What contradicts") OR front.contains("NOT apply")
  FailureBehavior: regenerate
  PrecedenceWeight: 80
  Dependencies: []
  ConflictsWith: []

R-C-025:  # ModelCardFormat
  Scope: PER_CARD
  ActivationCondition: card.type == MODEL
  RequiredArtifact: card
  ValidationMethod: >
    front.contains("Explain/visualize how") OR
    front.contains("What are the stages")
  FailureBehavior: regenerate
  PrecedenceWeight: 80
  Dependencies: []
  ConflictsWith: []

R-C-026:  # RedundancyCheck
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card_set
  ValidationMethod: >
    NOT any(c in card_set where c != card AND 
            overlap_ratio(c.front, card.front) > 0.8) AND
    NOT any(c in card_set where c != card AND
            c.type == CONSTRUCTIVE and card.type == CONSTRUCTIVE AND
            c.back == card.back)
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-C-027:  # ContentPurity_Callouts
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: >
    NOT back.matches("\[!.*\]")
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: []
  ConflictsWith: []

# POST_CARD - per-section coverage checks

R-POC-001:  # NegationCardPerDistinction
  Scope: POST_CARD
  ActivationCondition: section contains distinctions
  RequiredArtifact: section_cards
  ValidationMethod: for_all(d in distinctions): negation_cards.any(source == d)
  FailureBehavior: regenerate
  PrecedenceWeight: 85
  Dependencies: []
  ConflictsWith: []

R-POC-002:  # CounterEvidencePerContradiction
  Scope: POST_CARD
  ActivationCondition: section contains contradictions
  RequiredArtifact: section_cards
  ValidationMethod: for_all(ce): counter_cards.any(source == ce)
  FailureBehavior: regenerate
  PrecedenceWeight: 90
  Dependencies: []
  ConflictsWith: []

R-POC-003:  # ConstructiveCardPerCodeBlock
  Scope: POST_CARD
  ActivationCondition: section contains code blocks
  RequiredArtifact: section_cards
  ValidationMethod: for_all(cb): constructive_cards.any(source_block == cb)
  FailureBehavior: regenerate
  PrecedenceWeight: 95
  Dependencies: []
  ConflictsWith: []

R-POC-004:  # TheoryCardPerBoldedRule
  Scope: POST_CARD
  ActivationCondition: section contains bolded rules
  RequiredArtifact: section_cards
  ValidationMethod: for_all(br): theory_cards.any(source == br)
  FailureBehavior: regenerate
  PrecedenceWeight: 80
  Dependencies: []
  ConflictsWith: []

R-POC-005:  # QuestionCalloutTranslation
  Scope: POST_CARD
  ActivationCondition: document contains > [!question] callouts
  RequiredArtifact: section_cards
  ValidationMethod: for_all(q): cards.any(derived_from == q)
  FailureBehavior: regenerate
  PrecedenceWeight: 70
  Dependencies: []
  ConflictsWith: []

R-POC-006:  # MinOneCardPerH2
  Scope: POST_CARD
  ActivationCondition: h2_section_processed
  RequiredArtifact: section_cards
  ValidationMethod: h2_card_count >= 1
  FailureBehavior: regenerate
  PrecedenceWeight: 85
  Dependencies: []
  ConflictsWith: [R-PC-004]

# POST_NOTE - after all cards for a note

R-PN-001:  # StructuralTypeEnforcement
  Scope: POST_NOTE
  ActivationCondition: note_processing_complete
  RequiredArtifact: card_type_counts
  ValidationMethod: >
    constructive_cards >= code_blocks AND
    (distinctions_present == false OR negation_cards >= 1) AND
    (contradictions_present == false OR counter_evidence_cards >= 1) AND
    (failure_mode_triggers_present == false OR failure_mode_cards >= 1)
  FailureBehavior: regenerate
  PrecedenceWeight: 90
  Dependencies: []
  ConflictsWith: []

R-PN-002:  # Tier1RuleCoverageAudit
  Scope: POST_NOTE
  ActivationCondition: note_processing_complete
  RequiredArtifact: rule_application_plan
  ValidationMethod: for_all(r where APPLICABLE): r.cards_generated >= 1
  FailureBehavior: regenerate
  PrecedenceWeight: 95
  Dependencies: [R-POD-006]
  ConflictsWith: []

R-PN-003:  # ContentCoverageVerification
  Scope: POST_NOTE
  ActivationCondition: note_processing_complete
  RequiredArtifact: coverage_report
  ValidationMethod: >
    every_h2_has_cards AND every_code_block_has_card AND
    every_distinction_has_card AND no_section_silently_skipped
  FailureBehavior: regenerate
  PrecedenceWeight: 90
  Dependencies: []
  ConflictsWith: []

R-PN-004:  # SDI_PostCheck
  Scope: POST_NOTE
  ActivationCondition: note_processing_complete
  RequiredArtifact: card_count, structural_element_count
  ValidationMethod: >
    card_count >= structural_elements_count AND
    SDI <= 2.5
  FailureBehavior: reject_if_SDI_below_1.0, warn_if_above_2.5
  PrecedenceWeight: 85
  Dependencies: [R-PC-003]
  ConflictsWith: []

R-PN-005:  # NoSilentSectionSkip
  Scope: POST_NOTE
  ActivationCondition: note_processing_complete
  RequiredArtifact: section_status_list
  ValidationMethod: for_all(section): status in [PROCESSED, SKIPPED_WITH_REASON]
  FailureBehavior: reject
  PrecedenceWeight: 90
  Dependencies: []
  ConflictsWith: []

R-PN-007:  # CrossH2SynthesisRequired
  Scope: POST_NOTE
  ActivationCondition: h2_count >= 2
  RequiredArtifact: cross_h2_synthesis_cards
  ValidationMethod: cross_h2_synthesis_cards >= 1
  FailureBehavior: regenerate
  PrecedenceWeight: 90
  Dependencies: [R-PN-002]
  ConflictsWith: []

R-PN-008:  # ConnectivityMinimum
  Scope: POST_NOTE
  ActivationCondition: concept_count >= 3
  RequiredArtifact: connectivity_cards
  ValidationMethod: connectivity_cards >= max(2, floor(total_cards * 0.15))
  FailureBehavior: regenerate
  PrecedenceWeight: 85
  Dependencies: [R-PN-002]
  ConflictsWith: []

R-PN-009:  # DistributionCaps
  Scope: POST_NOTE
  ActivationCondition: note_processing_complete
  RequiredArtifact: card_type_counts
  ValidationMethod: >
    definition_cards <= floor(total_cards * 0.35) AND
    procedure_cards <= floor(total_cards * 0.50)
  FailureBehavior: regenerate
  PrecedenceWeight: 80
  Dependencies: [R-PN-002]
  ConflictsWith: []

R-PN-010:  # InternalizationLinkage
  Scope: POST_NOTE
  ActivationCondition: internalization_report_present == true
  RequiredArtifact: internalization_linkage_counts
  ValidationMethod: >
    boundary_cards >= 1 AND
    misconception_cards >= 1 AND
    link_cards >= 1
  FailureBehavior: regenerate
  PrecedenceWeight: 85
  Dependencies: [R-POD-008]
  ConflictsWith: []

R-PN-011:  # FailureModeTriggeredMinimum
  Scope: POST_NOTE
  ActivationCondition: failure_mode_triggers_present == true
  RequiredArtifact: failure_mode_cards
  ValidationMethod: failure_mode_cards >= 1
  FailureBehavior: regenerate
  PrecedenceWeight: 85
  Dependencies: [R-PN-002]
  ConflictsWith: []

R-PN-012:  # CardBudgetAdherence
  Scope: POST_NOTE
  ActivationCondition: card_budget_plan_present == true
  RequiredArtifact: card_type_counts
  ValidationMethod: >
    total_cards >= card_budget_plan.target_total_cards_min AND
    total_cards <= card_budget_plan.target_total_cards_max AND
    # ... other targets ...
    constructive_cards >= min(total_cards, card_budget_plan.target_constructive_min) AND
    constructive_cards <= card_budget_plan.target_constructive_max
  FailureBehavior: regenerate
  PrecedenceWeight: 85
  Dependencies: [R-POD-010]
  ConflictsWith: []

R-PN-013:  # MaxCardsPerNote
  Scope: POST_NOTE
  ActivationCondition: note_processing_complete
  RequiredArtifact: card_type_counts
  ValidationMethod: total_cards <= max_cards_per_note
  FailureBehavior: regenerate
  PrecedenceWeight: 80
  Dependencies: [R-PN-002]
  ConflictsWith: []

R-PN-006:  # DoctrineComplianceGate
  Scope: POST_NOTE
  ActivationCondition: note_processing_complete
  RequiredArtifact: doctrine_compliance_report
  ValidationMethod: >
    doctrine_compliance_report.has_fields([
      all_checks_passed,
      internalization_ok,
      internalization_linkage_ok,
      mapping_ok,
      elements_ok,
      coverage_ok,
      tier1_ok,
      minimums_ok,
      connectivity_ok,
      caps_ok,
      global_failure_mode_ok,
      budget_ok,
      conversion_quota_ok,
      quality_ok,
      output_purity_ok,
      failures
    ]) AND
    doctrine_compliance_report.internalization_ok == true AND
    doctrine_compliance_report.internalization_linkage_ok == true AND
    doctrine_compliance_report.mapping_ok == true AND
    doctrine_compliance_report.elements_ok == true AND
    doctrine_compliance_report.coverage_ok == true AND
    doctrine_compliance_report.tier1_ok == true AND
    doctrine_compliance_report.minimums_ok == true AND
    doctrine_compliance_report.connectivity_ok == true AND
    doctrine_compliance_report.caps_ok == true AND
    doctrine_compliance_report.global_failure_mode_ok == true AND
    doctrine_compliance_report.budget_ok == true AND
    doctrine_compliance_report.conversion_quota_ok == true AND
    doctrine_compliance_report.quality_ok == true AND
    doctrine_compliance_report.output_purity_ok == true AND
    doctrine_compliance_report.all_checks_passed == true AND
    doctrine_compliance_report.failures.length == 0
  FailureBehavior: regenerate
  PrecedenceWeight: 95
  Dependencies: [R-PN-002, R-PN-003]
  ConflictsWith: []

# SERIALIZATION - TSV formatting rules

R-S-001:  # TSVThreeColumns
  Scope: SERIALIZATION
  ActivationCondition: always
  RequiredArtifact: tsv_line
  ValidationMethod: tsv_line.tab_count == 2
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-S-002:  # NoPhysicalNewlines
  Scope: SERIALIZATION
  ActivationCondition: always
  RequiredArtifact: tsv_line
  ValidationMethod: tsv_line.contains_literal_newline == false
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-S-003:  # NoTabsInContent
  Scope: SERIALIZATION
  ActivationCondition: always
  RequiredArtifact: tsv_line
  ValidationMethod: column(0) and column(1) contain no literal tabs
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-S-004:  # CodeBlockSerialization
  Scope: SERIALIZATION
  ActivationCondition: card.type == CONSTRUCTIVE
  RequiredArtifact: tsv_line
  ValidationMethod: "newlines-><br>, spaces->&nbsp;, tabs->&nbsp;&nbsp;&nbsp;&nbsp;"
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-S-005:  # PreCodeWrapper
  Scope: SERIALIZATION
  ActivationCondition: card.type == CONSTRUCTIVE
  RequiredArtifact: tsv_line
  ValidationMethod: >
    back.starts_with("<pre style='text-align:left; font-family:monospace;'><code>") AND
    back.ends_with("</code></pre>")
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: [R-S-004]
  ConflictsWith: []

R-S-006:  # ObsidianURLFormat
  Scope: SERIALIZATION
  ActivationCondition: always
  RequiredArtifact: tsv_line
  ValidationMethod: url.starts_with("obsidian://open?vault=mohamed&file=")
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-S-007:  # URLEncoding
  Scope: SERIALIZATION
  ActivationCondition: always
  RequiredArtifact: tsv_line
  ValidationMethod: file_path uses %2F not /, spaces encoded, no .md suffix
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: [R-S-006]
  ConflictsWith: []

R-S-008:  # VaultConstant
  Scope: SERIALIZATION
  ActivationCondition: always
  RequiredArtifact: tsv_line
  ValidationMethod: url.vault_name == "mohamed"
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-S-009:  # NoSourceMetadataInCards
  Scope: SERIALIZATION
  ActivationCondition: always
  RequiredArtifact: tsv_line
  ValidationMethod: NOT column(0..1).contains("[Source:")
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: [R-C-021]

R-S-010:  # FrontColumnFormat
  Scope: SERIALIZATION
  ActivationCondition: always
  RequiredArtifact: tsv_line
  ValidationMethod: front.matches_pattern("<strong>[*]</strong><br>*?")
  FailureBehavior: regenerate
  PrecedenceWeight: 75
  Dependencies: []
  ConflictsWith: []

R-S-011:  # BackColumnFormat
  Scope: SERIALIZATION
  ActivationCondition: always
  RequiredArtifact: tsv_line
  ValidationMethod: column(1).length > 0 AND (type != CONSTRUCTIVE OR R-S-005.passed)
  FailureBehavior: reject
  PrecedenceWeight: 90
  Dependencies: [R-S-005]
  ConflictsWith: []

R-S-012:  # PostGenValidationScript
  Scope: SERIALIZATION
  ActivationCondition: tsv_file_written
  RequiredArtifact: tsv_file
  ValidationMethod: validate_tsv_passed == true
  FailureBehavior: regenerate
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-S-013:  # FailureProtocol_StopAndFix
  Scope: SERIALIZATION
  ActivationCondition: R-S-012.passed == false
  RequiredArtifact: failure_report
  ValidationMethod: failing_lines_fixed AND revalidation_passed
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: [R-S-012]
  ConflictsWith: []

R-S-014:  # OutputFileCreated
  Scope: SERIALIZATION
  ActivationCondition: tsv_file_written
  RequiredArtifact: output_path
  ValidationMethod: file_exists(output_path) == true
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: [R-S-012]
  ConflictsWith: []

# GLOBAL - run-level checks

R-G-001:  # ManifestCompletionCheck
  Scope: GLOBAL_RUN
  ActivationCondition: input_mode in [folder, cwd]
  RequiredArtifact: file_manifest
  ValidationMethod: for_all(f in manifest): f.status in [PROCESSED, SKIPPED_WITH_REASON, PARTIAL_READ]
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: [R-PD-006]
  ConflictsWith: [R-PD-006]

R-G-002:  # UnifiedTSVOutput
  Scope: GLOBAL_RUN
  ActivationCondition: input_mode in [folder, cwd]
  RequiredArtifact: output_files
  ValidationMethod: output_files.count == 1 AND all_cards_in_single_file
  FailureBehavior: reject
  PrecedenceWeight: 90
  Dependencies: []
  ConflictsWith: []

R-G-003:  # FilenameRule
  Scope: GLOBAL_RUN
  ActivationCondition: always
  RequiredArtifact: output_file
  ValidationMethod: filename matches input convention OR user_override
  FailureBehavior: warn
  PrecedenceWeight: 50
  Dependencies: []
  ConflictsWith: []

R-G-004:  # ExecutionReport
  Scope: GLOBAL_RUN
  ActivationCondition: all_files_processed
  RequiredArtifact: report
  ValidationMethod: report.contains_manifest_status AND total_cards AND total_files AND report.contains_partial_reads
  FailureBehavior: warn
  PrecedenceWeight: 60
  Dependencies: [R-G-001]
  ConflictsWith: []

R-G-005:  # MaxRegenerationAttempts
  Scope: GLOBAL_RUN
  ActivationCondition: regeneration_tracking_enabled == true
  RequiredArtifact: regeneration_attempts
  ValidationMethod: regeneration_attempts <= 3
  FailureBehavior: reject
  PrecedenceWeight: 90
  Dependencies: []
  ConflictsWith: []

R-G-006:  # GlobalFailureModeMinimum
  Scope: GLOBAL_RUN
  ActivationCondition: input_mode in [folder, cwd] AND run_stats_present == true
  RequiredArtifact: global_failure_mode_cards
  ValidationMethod: >
    total_cards > 0 IMPLIES
    global_failure_mode_cards >= ceil(total_cards / 25)
  FailureBehavior: regenerate
  PrecedenceWeight: 85
  Dependencies: [R-G-002]
  ConflictsWith: []

R-G-007:  # RunStatsMissing
  Scope: GLOBAL_RUN
  ActivationCondition: input_mode in [folder, cwd] AND require_run_stats == true AND run_stats_present == false
  RequiredArtifact: report
  ValidationMethod: report.contains("run_stats_missing")
  FailureBehavior: reject
  PrecedenceWeight: 80
  Dependencies: []
  ConflictsWith: []
```

## Schema Execution Order

```
1_Discovery:    R-PD-001 || R-PD-002 -> R-PD-004 -> R-PD-005 -> R-PD-003 -> R-PD-006
2_Analysis:     R-POD-001 -> R-POD-007 -> R-POD-008 -> R-POD-010 || R-POD-002 -> R-POD-003 -> R-POD-004 -> R-POD-005 -> R-POD-006 -> R-POD-009
3_PreCard:      R-PC-006 || R-PC-003 || R-PC-001 -> R-PC-002 -> R-PC-004 || R-PC-005
4_PerCard:      [R-C-007 || R-C-008 || R-C-011] -> [R-C-001 || R-C-002 || R-C-009 || R-C-010] ->
               [R-C-003..R-C-015] -> [R-C-016..R-C-020] -> [R-C-019 || R-C-021]
5_PostCard:     R-POC-003 -> R-POC-002 -> R-POC-001 || R-POC-006 -> R-POC-004 -> R-POC-005
6_PostNote:     R-PN-002 -> R-PN-003 || R-PN-005 -> R-PN-007 -> R-PN-008 -> R-PN-009 -> R-PN-010 -> R-PN-011 -> R-PN-012 -> R-PN-013 -> R-PN-006 -> R-PN-001 -> R-PN-004
7_Serialization: [R-S-001..R-S-003] -> R-S-004 -> R-S-005 -> R-S-006..R-S-008 -> R-S-009..R-S-011 -> R-S-012 -> R-S-013 -> R-S-014
8_Global:       R-G-002 -> R-G-003 -> R-G-001 -> R-G-004 -> R-G-005 -> R-G-006 -> R-G-007
```

## Conflict Resolutions

| Collision | Resolution |
|-----------|-----------|
| R-C-002 vs R-C-009 | Sequential: R-C-009 decomposes, then R-C-002 validates each sub-card |
| R-C-006 vs R-C-007 | R-C-007 (P:100) overrides R-C-006 (P:75) for CONSTRUCTIVE cards only |
| R-PC-004 vs R-POC-006 | R-PC-004 (per structural element) subsumes R-POC-006 (>=1 safety net) |
| R-S-009 vs R-C-021 | Both apply: defense in depth at different scopes |
| R-PD-006 vs R-G-001 | Both apply: pre-check and post-check reinforcement |

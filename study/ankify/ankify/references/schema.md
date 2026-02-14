# ANKIFY Executable Enforcement Schema (v4)

This file contains the machine-checkable rules for Ankify.
Doctrine is the source of truth for what cards to create and how they should read.
If any rule here conflicts with doctrine, follow doctrine and treat the schema rule as stale.
Execute scopes in order: PRE_DISCOVERY -> POST_DISCOVERY -> PRE_CARD -> PER_CARD -> POST_CARD -> POST_NOTE -> SERIALIZATION -> GLOBAL.

```yaml
# PRE_DISCOVERY - before any file is read

R-PD-001:  # SilentExecution
  Scope: PRE_DISCOVERY
  ActivationCondition: agent_invoked == true
  RequiredArtifact: none
  ValidationMethod: zero_chat_messages_before_file_write
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-PD-002:  # AutoFileCreation
  Scope: PRE_DISCOVERY
  ActivationCondition: agent_invoked == true
  RequiredArtifact: output_path
  ValidationMethod: file_exists(output_path) AND chat_output_count == 0
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
  ValidationMethod: for_all(f in manifest): f.status in [PROCESSED, SKIPPED_WITH_REASON]
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: [R-PD-003]
  ConflictsWith: []

# POST_DISCOVERY - after file read, before card gen

R-POD-001:  # CompleteInputRead
  Scope: POST_DISCOVERY
  ActivationCondition: file_loaded == true
  RequiredArtifact: full_document_text
  ValidationMethod: read_position == EOF
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
  ValidationMethod: levenshtein_similarity(card.back, source_text) < 0.85
  FailureBehavior: regenerate
  PrecedenceWeight: 90
  Dependencies: []
  ConflictsWith: []

R-C-002:  # Atomicity_OneIdea
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: card.concept_count == 1 AND (type != CODE OR back.line_count <= 6)
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: []
  ConflictsWith: [R-C-009]

R-C-003:  # FeynmanTest_PlainLanguage
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: readability_score(front) <= GRADE_10 AND jargon_without_context == 0
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
  ActivationCondition: always
  RequiredArtifact: card_set
  ValidationMethod: card.related_cards_in_same_note >= 1
  FailureBehavior: warn
  PrecedenceWeight: 60
  Dependencies: []
  ConflictsWith: []

R-C-006:  # SignalToNoise
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: front.word_count <= 50 AND front.contains_only_question
  FailureBehavior: regenerate
  PrecedenceWeight: 75
  Dependencies: []
  ConflictsWith: [R-C-007]

R-C-007:  # ContextMandate_CodeCards
  Scope: PER_CARD
  ActivationCondition: card.type == CODE
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
  ActivationCondition: card.type == CODE
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
  ActivationCondition: card.type == CODE
  RequiredArtifact: card
  ValidationMethod: card.back.line_count <= 6
  FailureBehavior: reject
  PrecedenceWeight: 95
  Dependencies: []
  ConflictsWith: []

R-C-011:  # CodeFrontScope
  Scope: PER_CARD
  ActivationCondition: card.type == CODE
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
  ValidationMethod: front.requires_active_recall AND NOT answerable_by_recognition_only
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
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: answer_is_unambiguous AND possible_correct_answers == 1
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
  ValidationMethod: front.uses_familiar_anchor_words
  FailureBehavior: warn
  PrecedenceWeight: 50
  Dependencies: []
  ConflictsWith: []

R-C-018:  # DomainContextCues
  Scope: PER_CARD
  ActivationCondition: always
  RequiredArtifact: card
  ValidationMethod: front.starts_with("<strong>[Domain]</strong>")
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
    constructive_cards >= code_blocks_count AND
    negation_cards >= distinctions_count AND
    counter_cards >= contradictions_count AND
    predictive_cards >= failure_modes_count
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

R-PN-006:  # DoctrineComplianceGate
  Scope: POST_NOTE
  ActivationCondition: note_processing_complete
  RequiredArtifact: doctrine_compliance_report
  ValidationMethod: >
    doctrine_compliance_report.has_fields([
      all_checks_passed,
      mapping_ok,
      elements_ok,
      coverage_ok,
      tier1_ok,
      quality_ok,
      output_purity_ok,
      failures
    ]) AND
    doctrine_compliance_report.mapping_ok == true AND
    doctrine_compliance_report.elements_ok == true AND
    doctrine_compliance_report.coverage_ok == true AND
    doctrine_compliance_report.tier1_ok == true AND
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
  ActivationCondition: card.type == CODE
  RequiredArtifact: tsv_line
  ValidationMethod: "newlines-><br>, spaces->&nbsp;, tabs->&nbsp;&nbsp;&nbsp;&nbsp;"
  FailureBehavior: reject
  PrecedenceWeight: 100
  Dependencies: []
  ConflictsWith: []

R-S-005:  # PreCodeWrapper
  Scope: SERIALIZATION
  ActivationCondition: card.type == CODE
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
  ValidationMethod: column(1).length > 0 AND (type != CODE OR R-S-005.passed)
  FailureBehavior: reject
  PrecedenceWeight: 90
  Dependencies: [R-S-005]
  ConflictsWith: []

R-S-012:  # PostGenValidationScript
  Scope: SERIALIZATION
  ActivationCondition: tsv_file_written
  RequiredArtifact: tsv_file
  ValidationMethod: awk_validation.failure_count == 0
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

# GLOBAL - run-level checks

R-G-001:  # ManifestCompletionCheck
  Scope: GLOBAL_RUN
  ActivationCondition: input_mode in [folder, cwd]
  RequiredArtifact: file_manifest
  ValidationMethod: for_all(f in manifest): f.status in [PROCESSED, SKIPPED_WITH_REASON]
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
  ValidationMethod: report.contains_manifest_status AND total_cards AND total_files
  FailureBehavior: warn
  PrecedenceWeight: 60
  Dependencies: [R-G-001]
  ConflictsWith: []
```

## Schema Execution Order

```
1_Discovery:    R-PD-001 || R-PD-002 -> R-PD-004 -> R-PD-005 -> R-PD-003 -> R-PD-006
2_Analysis:     R-POD-001 -> R-POD-007 || R-POD-002 -> R-POD-003 -> R-POD-004 -> R-POD-005 -> R-POD-006
3_PreCard:      R-PC-006 || R-PC-003 || R-PC-001 -> R-PC-002 -> R-PC-004 || R-PC-005
4_PerCard:      [R-C-007 || R-C-008 || R-C-011] -> [R-C-001 || R-C-002 || R-C-009 || R-C-010] ->
               [R-C-003..R-C-015] -> [R-C-016..R-C-020] -> [R-C-019 || R-C-021]
5_PostCard:     R-POC-003 -> R-POC-002 -> R-POC-001 || R-POC-006 -> R-POC-004 -> R-POC-005
6_PostNote:     R-PN-002 -> R-PN-003 || R-PN-005 -> R-PN-006 -> R-PN-001 -> R-PN-004
7_Serialization: [R-S-001..R-S-003] -> R-S-004 -> R-S-005 -> R-S-006..R-S-008 -> R-S-009..R-S-011 -> R-S-012 -> R-S-013
8_Global:       R-G-002 -> R-G-003 -> R-G-001 -> R-G-004
```

## Conflict Resolutions

| Collision | Resolution |
|-----------|-----------|
| R-C-002 vs R-C-009 | Sequential: R-C-009 decomposes, then R-C-002 validates each sub-card |
| R-C-006 vs R-C-007 | R-C-007 (P:100) overrides R-C-006 (P:75) for CODE cards only |
| R-PC-004 vs R-POC-006 | R-PC-004 (per structural element) subsumes R-POC-006 (>=1 safety net) |
| R-S-009 vs R-C-021 | Both apply: defense in depth at different scopes |
| R-PD-006 vs R-G-001 | Both apply: pre-check and post-check reinforcement |

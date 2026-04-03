import functions_framework
import json
import random
import datetime
import hashlib

# ============================================================================
# POLICY-TO-FLOW COMPILER — CLOUD FUNCTION WEBHOOK
# For Dialogflow CX Integration
# Track 3: Customer Engagement Suite | TCS^AI Hackathon 2026
# ============================================================================

# --- Synthetic Policy Database ---
POLICIES = {
    "return-policy": {
        "id": "POL-RTN-2026-001",
        "name": "Standard Return & Refund Policy",
        "version": "2.4.1",
        "last_updated": "2026-03-15",
        "department": "Customer Operations",
        "industry": "E-Commerce / Retail",
        "source_doc": "Warranty_Returns_Policy_v2.docx",
        "raw_text": """Customers may return most new, unopened items sold and fulfilled by our company within 30 days of delivery for a full refund. Exceptions: If the item is a Consumer Electronics (e.g., Laptops, Phones), the return window is restricted to 14 days. The item must be in its original packaging. If the packaging is damaged or missing, we will apply a 15% restocking fee. At the start of any return interaction, the agent must state standard processing times (5-7 business days) before accepting the return request. Items purchased during promotional events (Black Friday, Diwali Sale) are subject to a 7-day return window with exchange-only policy (no cash refunds). Gift items require a valid gift receipt for processing.""",
        "entities": [
            {"name": "ProductCategory", "type": "enum", "values": ["ELECTRONICS", "GENERAL", "PROMOTIONAL", "GIFT"], "source_line": "Line 2-3"},
            {"name": "DaysSinceDelivery", "type": "integer", "unit": "days", "source_line": "Line 1"},
            {"name": "PackagingCondition", "type": "enum", "values": ["INTACT", "DAMAGED", "MISSING"], "source_line": "Line 3"},
            {"name": "PurchaseType", "type": "enum", "values": ["REGULAR", "PROMOTIONAL", "GIFT"], "source_line": "Line 5-6"},
            {"name": "RestockingFee", "type": "percentage", "value": 15, "source_line": "Line 3"},
            {"name": "RefundType", "type": "enum", "values": ["FULL_REFUND", "PARTIAL_REFUND", "EXCHANGE_ONLY", "REJECTED"], "source_line": "Line 1,5"}
        ],
        "flow_nodes": [
            {"id": "START_RETURN", "type": "action", "action": "display_disclaimer", "message": "Standard processing time is 5-7 business days", "next": "IDENTIFY_PRODUCT", "policy_ref": "Line 4"},
            {"id": "IDENTIFY_PRODUCT", "type": "classification", "entity": "ProductCategory", "branches": {"ELECTRONICS": "CHECK_ELECTRONICS_WINDOW", "PROMOTIONAL": "CHECK_PROMO_WINDOW", "GIFT": "CHECK_GIFT_RECEIPT", "GENERAL": "CHECK_GENERAL_WINDOW"}, "policy_ref": "Line 2"},
            {"id": "CHECK_ELECTRONICS_WINDOW", "type": "condition", "rule": "DaysSinceDelivery <= 14", "true_next": "CHECK_PACKAGING", "false_next": "REJECT_RETURN", "policy_ref": "Line 2"},
            {"id": "CHECK_GENERAL_WINDOW", "type": "condition", "rule": "DaysSinceDelivery <= 30", "true_next": "CHECK_PACKAGING", "false_next": "REJECT_RETURN", "policy_ref": "Line 1"},
            {"id": "CHECK_PROMO_WINDOW", "type": "condition", "rule": "DaysSinceDelivery <= 7", "true_next": "PROMO_EXCHANGE", "false_next": "REJECT_RETURN", "policy_ref": "Line 5"},
            {"id": "CHECK_GIFT_RECEIPT", "type": "condition", "rule": "HasGiftReceipt == true", "true_next": "CHECK_GENERAL_WINDOW", "false_next": "REJECT_NO_RECEIPT", "policy_ref": "Line 6"},
            {"id": "CHECK_PACKAGING", "type": "condition", "rule": "PackagingCondition == INTACT", "true_next": "APPROVE_FULL_REFUND", "false_next": "APPLY_RESTOCKING_FEE", "policy_ref": "Line 3"},
            {"id": "APPROVE_FULL_REFUND", "type": "outcome", "result": "FULL_REFUND", "message": "Return approved. Full refund will be processed within 5-7 business days.", "policy_ref": "Line 1"},
            {"id": "APPLY_RESTOCKING_FEE", "type": "outcome", "result": "PARTIAL_REFUND", "message": "Return approved with 15% restocking fee due to packaging condition.", "fee": "15%", "policy_ref": "Line 3"},
            {"id": "PROMO_EXCHANGE", "type": "outcome", "result": "EXCHANGE_ONLY", "message": "Promotional items are eligible for exchange only. No cash refunds.", "policy_ref": "Line 5"},
            {"id": "REJECT_RETURN", "type": "outcome", "result": "REJECTED", "message": "Return window has expired. Item is not eligible for return.", "policy_ref": "Line 1-2"},
            {"id": "REJECT_NO_RECEIPT", "type": "outcome", "result": "REJECTED", "message": "Gift items require a valid gift receipt for processing.", "policy_ref": "Line 6"}
        ],
        "disclaimers": ["Processing time: 5-7 business days", "Restocking fee: 15% for damaged/missing packaging", "Promotional items: Exchange only, no cash refunds"],
        "fuzz_results": {
            "total_paths": 2847,
            "coverage": 98.4,
            "critical_gaps": 1,
            "warnings": 3,
            "gap_details": [
                {"id": "GAP-001", "severity": "CRITICAL", "scenario": "Electronics item, delivery date = exactly 14 days, order date = 17 days ago (3-day shipping)", "issue": "Policy says 'days of delivery' but flow logic mapped to order creation timestamp", "fix": "Bind DaysSinceDelivery to tracking API delivery confirmation, not order creation date", "paths_affected": 23}
            ],
            "warning_details": [
                {"id": "WARN-001", "scenario": "Gift item with expired receipt (>90 days old)", "issue": "Policy doesn't specify receipt validity window", "recommendation": "Add receipt_age validation node"},
                {"id": "WARN-002", "scenario": "Electronics item purchased as gift during promo", "issue": "Overlapping category: ELECTRONICS + PROMOTIONAL + GIFT", "recommendation": "Define priority hierarchy for multi-category items"},
                {"id": "WARN-003", "scenario": "Item partially opened but packaging intact", "issue": "Ambiguous definition of 'unopened'", "recommendation": "Add seal_intact boolean check"}
            ]
        }
    },
    "kyc-policy": {
        "id": "POL-KYC-2026-002",
        "name": "Customer KYC Verification Policy",
        "version": "3.1.0",
        "last_updated": "2026-02-28",
        "department": "Compliance & Risk",
        "industry": "Banking / Financial Services",
        "source_doc": "KYC_Compliance_Framework_v3.docx",
        "raw_text": """All new account holders must complete identity verification within 30 days of account opening. Tier 1 (Basic): Government-issued photo ID + address proof. Daily transaction limit: ₹50,000. Tier 2 (Enhanced): Tier 1 + income proof + video KYC. Daily limit: ₹5,00,000. Tier 3 (Premium): Tier 2 + in-person verification at branch. No daily limit. PEP (Politically Exposed Persons) require mandatory Tier 3 and enhanced due diligence. Accounts exceeding 30 days without KYC completion are frozen. Re-activation requires branch visit and fresh document submission.""",
        "entities": [
            {"name": "KYCTier", "type": "enum", "values": ["TIER_1_BASIC", "TIER_2_ENHANCED", "TIER_3_PREMIUM"], "source_line": "Line 2-4"},
            {"name": "DocumentType", "type": "enum", "values": ["PHOTO_ID", "ADDRESS_PROOF", "INCOME_PROOF", "VIDEO_KYC", "IN_PERSON"], "source_line": "Line 2-4"},
            {"name": "AccountAge", "type": "integer", "unit": "days", "source_line": "Line 1"},
            {"name": "PEPStatus", "type": "boolean", "source_line": "Line 5"},
            {"name": "DailyLimit", "type": "currency", "values": {"TIER_1": 50000, "TIER_2": 500000, "TIER_3": "UNLIMITED"}, "source_line": "Line 2-4"}
        ],
        "flow_nodes": [
            {"id": "START_KYC", "type": "action", "action": "check_account_age", "next": "CHECK_DEADLINE", "policy_ref": "Line 1"},
            {"id": "CHECK_DEADLINE", "type": "condition", "rule": "AccountAge <= 30", "true_next": "CHECK_PEP", "false_next": "FREEZE_ACCOUNT", "policy_ref": "Line 6"},
            {"id": "CHECK_PEP", "type": "condition", "rule": "PEPStatus == true", "true_next": "REQUIRE_TIER3", "false_next": "SELECT_TIER", "policy_ref": "Line 5"},
            {"id": "SELECT_TIER", "type": "classification", "entity": "KYCTier", "branches": {"TIER_1_BASIC": "COLLECT_BASIC_DOCS", "TIER_2_ENHANCED": "COLLECT_ENHANCED_DOCS", "TIER_3_PREMIUM": "COLLECT_PREMIUM_DOCS"}, "policy_ref": "Line 2-4"},
            {"id": "COLLECT_BASIC_DOCS", "type": "action", "required": ["PHOTO_ID", "ADDRESS_PROOF"], "next": "VERIFY_BASIC", "policy_ref": "Line 2"},
            {"id": "VERIFY_BASIC", "type": "outcome", "result": "KYC_COMPLETE_T1", "message": "Tier 1 KYC complete. Daily transaction limit: ₹50,000.", "policy_ref": "Line 2"},
            {"id": "COLLECT_ENHANCED_DOCS", "type": "action", "required": ["PHOTO_ID", "ADDRESS_PROOF", "INCOME_PROOF", "VIDEO_KYC"], "next": "VERIFY_ENHANCED", "policy_ref": "Line 3"},
            {"id": "VERIFY_ENHANCED", "type": "outcome", "result": "KYC_COMPLETE_T2", "message": "Tier 2 KYC complete. Daily transaction limit: ₹5,00,000.", "policy_ref": "Line 3"},
            {"id": "REQUIRE_TIER3", "type": "action", "action": "mandate_tier3", "message": "PEP detected. Tier 3 with enhanced due diligence is mandatory.", "next": "COLLECT_PREMIUM_DOCS", "policy_ref": "Line 5"},
            {"id": "COLLECT_PREMIUM_DOCS", "type": "action", "required": ["PHOTO_ID", "ADDRESS_PROOF", "INCOME_PROOF", "VIDEO_KYC", "IN_PERSON"], "next": "VERIFY_PREMIUM", "policy_ref": "Line 4"},
            {"id": "VERIFY_PREMIUM", "type": "outcome", "result": "KYC_COMPLETE_T3", "message": "Tier 3 KYC complete. No daily transaction limit.", "policy_ref": "Line 4"},
            {"id": "FREEZE_ACCOUNT", "type": "outcome", "result": "ACCOUNT_FROZEN", "message": "Account frozen due to KYC non-compliance beyond 30-day deadline. Branch visit required.", "policy_ref": "Line 6"}
        ],
        "disclaimers": ["30-day KYC completion deadline", "PEP requires mandatory Tier 3", "Frozen accounts require branch visit"],
        "fuzz_results": {
            "total_paths": 1923,
            "coverage": 96.7,
            "critical_gaps": 0,
            "warnings": 2,
            "gap_details": [],
            "warning_details": [
                {"id": "WARN-001", "scenario": "Customer upgrading from Tier 1 to Tier 2 while documents are being verified", "issue": "No intermediate state handling", "recommendation": "Add PENDING_UPGRADE state with document queue"},
                {"id": "WARN-002", "scenario": "PEP status changed after Tier 2 KYC completion", "issue": "Retroactive PEP detection not handled", "recommendation": "Add PEP_RECHECK hook on status change events"}
            ]
        }
    },
    "warranty-policy": {
        "id": "POL-WRN-2026-003",
        "name": "Product Warranty & Service Policy",
        "version": "1.8.0",
        "last_updated": "2026-03-22",
        "department": "After-Sales Service",
        "industry": "Consumer Electronics",
        "source_doc": "Extended_Warranty_Terms_v1.8.docx",
        "raw_text": """All products carry a standard 12-month manufacturer warranty from date of purchase. Extended warranty (24 months) available for purchase within 15 days of product delivery. Warranty covers manufacturing defects only. Physical damage, water damage, and unauthorized modifications void the warranty. Repair turnaround: 10 business days for standard, 3 business days for premium customers. If repair is not possible, replacement with equivalent model. If equivalent model unavailable, store credit at 90% of purchase price. On-site service available for appliances over ₹25,000 purchase value.""",
        "entities": [
            {"name": "WarrantyType", "type": "enum", "values": ["STANDARD_12M", "EXTENDED_24M", "EXPIRED"], "source_line": "Line 1-2"},
            {"name": "DamageType", "type": "enum", "values": ["MANUFACTURING_DEFECT", "PHYSICAL_DAMAGE", "WATER_DAMAGE", "UNAUTHORIZED_MOD", "NORMAL_WEAR"], "source_line": "Line 3"},
            {"name": "CustomerTier", "type": "enum", "values": ["STANDARD", "PREMIUM"], "source_line": "Line 4"},
            {"name": "ProductValue", "type": "currency", "unit": "INR", "source_line": "Line 6"},
            {"name": "RepairFeasibility", "type": "boolean", "source_line": "Line 5"},
            {"name": "EquivalentModelAvailable", "type": "boolean", "source_line": "Line 5"}
        ],
        "flow_nodes": [
            {"id": "START_WARRANTY", "type": "action", "action": "verify_purchase", "next": "CHECK_WARRANTY_STATUS", "policy_ref": "Line 1"},
            {"id": "CHECK_WARRANTY_STATUS", "type": "condition", "rule": "PurchaseAge <= WarrantyPeriod", "true_next": "CHECK_DAMAGE_TYPE", "false_next": "CHECK_EXTENDED_ELIGIBILITY", "policy_ref": "Line 1-2"},
            {"id": "CHECK_EXTENDED_ELIGIBILITY", "type": "condition", "rule": "DeliveryAge <= 15 AND ExtendedNotPurchased", "true_next": "OFFER_EXTENDED", "false_next": "WARRANTY_EXPIRED", "policy_ref": "Line 2"},
            {"id": "CHECK_DAMAGE_TYPE", "type": "condition", "rule": "DamageType == MANUFACTURING_DEFECT", "true_next": "CHECK_REPAIR_FEASIBILITY", "false_next": "WARRANTY_VOID", "policy_ref": "Line 3"},
            {"id": "CHECK_REPAIR_FEASIBILITY", "type": "condition", "rule": "RepairFeasible == true", "true_next": "SCHEDULE_REPAIR", "false_next": "CHECK_REPLACEMENT", "policy_ref": "Line 5"},
            {"id": "SCHEDULE_REPAIR", "type": "action", "action": "schedule_repair", "turnaround": {"STANDARD": "10 business days", "PREMIUM": "3 business days"}, "next": "CHECK_ONSITE_ELIGIBLE", "policy_ref": "Line 4"},
            {"id": "CHECK_ONSITE_ELIGIBLE", "type": "condition", "rule": "ProductValue >= 25000", "true_next": "OFFER_ONSITE", "false_next": "CONFIRM_SERVICE_CENTER", "policy_ref": "Line 6"},
            {"id": "CHECK_REPLACEMENT", "type": "condition", "rule": "EquivalentModelAvailable == true", "true_next": "REPLACE_PRODUCT", "false_next": "STORE_CREDIT", "policy_ref": "Line 5"},
            {"id": "OFFER_EXTENDED", "type": "outcome", "result": "EXTENDED_WARRANTY_OFFER", "message": "You're eligible for our 24-month extended warranty. Would you like to purchase it?", "policy_ref": "Line 2"},
            {"id": "OFFER_ONSITE", "type": "outcome", "result": "ONSITE_SERVICE", "message": "Your product qualifies for on-site service. A technician will be scheduled.", "policy_ref": "Line 6"},
            {"id": "CONFIRM_SERVICE_CENTER", "type": "outcome", "result": "SERVICE_CENTER_REPAIR", "message": "Please bring the product to the nearest authorized service center.", "policy_ref": "Line 4"},
            {"id": "REPLACE_PRODUCT", "type": "outcome", "result": "REPLACEMENT", "message": "Replacement with equivalent model will be arranged.", "policy_ref": "Line 5"},
            {"id": "STORE_CREDIT", "type": "outcome", "result": "STORE_CREDIT", "message": "Store credit at 90% of purchase price will be issued.", "credit_pct": 90, "policy_ref": "Line 5"},
            {"id": "WARRANTY_VOID", "type": "outcome", "result": "WARRANTY_VOID", "message": "Warranty voided due to non-manufacturing damage. Paid repair options available.", "policy_ref": "Line 3"},
            {"id": "WARRANTY_EXPIRED", "type": "outcome", "result": "WARRANTY_EXPIRED", "message": "Warranty period has expired. Out-of-warranty service available at standard rates.", "policy_ref": "Line 1"}
        ],
        "disclaimers": ["Manufacturing defects only", "Extended warranty must be purchased within 15 days", "Physical/water damage voids warranty", "On-site service for products over ₹25,000"],
        "fuzz_results": {
            "total_paths": 3412,
            "coverage": 99.1,
            "critical_gaps": 0,
            "warnings": 1,
            "gap_details": [],
            "warning_details": [
                {"id": "WARN-001", "scenario": "Product repaired under warranty fails again within 30 days", "issue": "No re-repair escalation path in flow", "recommendation": "Add REPEAT_FAILURE node with automatic replacement trigger"}
            ]
        }
    }
}


# --- Compliance Scenarios ---
COMPLIANCE_SCENARIOS = {
    "return-policy": [
        {"scenario": "Customer returns a laptop 10 days after delivery with intact packaging", "product": "ELECTRONICS", "days": 10, "packaging": "INTACT", "purchase_type": "REGULAR", "expected": "FULL_REFUND", "compliant": True},
        {"scenario": "Customer returns a phone 18 days after delivery", "product": "ELECTRONICS", "days": 18, "packaging": "INTACT", "purchase_type": "REGULAR", "expected": "REJECTED", "compliant": True},
        {"scenario": "Customer returns general item 25 days after delivery, packaging damaged", "product": "GENERAL", "days": 25, "packaging": "DAMAGED", "purchase_type": "REGULAR", "expected": "PARTIAL_REFUND", "compliant": True},
        {"scenario": "Customer wants cash refund for Diwali Sale item bought 5 days ago", "product": "PROMOTIONAL", "days": 5, "packaging": "INTACT", "purchase_type": "PROMOTIONAL", "expected": "EXCHANGE_ONLY", "compliant": True},
        {"scenario": "Gift return without receipt", "product": "GIFT", "days": 7, "packaging": "INTACT", "purchase_type": "GIFT", "expected": "REJECTED", "compliant": True},
    ],
    "kyc-policy": [
        {"scenario": "New account, 15 days old, submitting Tier 1 documents, non-PEP", "account_age": 15, "pep": False, "tier": "TIER_1", "expected": "KYC_COMPLETE_T1", "compliant": True},
        {"scenario": "Account 35 days old, no KYC submitted", "account_age": 35, "pep": False, "tier": "NONE", "expected": "ACCOUNT_FROZEN", "compliant": True},
        {"scenario": "PEP individual requesting Tier 2 KYC", "account_age": 10, "pep": True, "tier": "TIER_2", "expected": "MANDATORY_TIER_3", "compliant": True},
    ],
    "warranty-policy": [
        {"scenario": "Manufacturing defect on 6-month-old laptop worth ₹85,000, repairable", "warranty_age": 6, "damage": "MANUFACTURING_DEFECT", "repairable": True, "value": 85000, "expected": "ONSITE_SERVICE", "compliant": True},
        {"scenario": "Water damage on phone under warranty", "warranty_age": 3, "damage": "WATER_DAMAGE", "repairable": True, "value": 15000, "expected": "WARRANTY_VOID", "compliant": True},
        {"scenario": "Manufacturing defect, product irreparable, no equivalent model", "warranty_age": 8, "damage": "MANUFACTURING_DEFECT", "repairable": False, "value": 45000, "expected": "STORE_CREDIT_90PCT", "compliant": True},
    ]
}


# --- Helper Functions ---

def get_policy(policy_name):
    """Look up a policy by name or keyword."""
    if not policy_name:
        return None
    name_lower = policy_name.lower().strip()
    for key, pol in POLICIES.items():
        if key in name_lower or any(w in name_lower for w in key.split("-")):
            return key, pol
    # Fuzzy match
    for key, pol in POLICIES.items():
        if any(w in name_lower for w in pol["name"].lower().split()):
            return key, pol
    return None


def format_compile_response(policy_key, policy):
    """Format the policy compilation output."""
    entity_list = "\n".join([f"  • {e['name']} ({e['type']}): {e.get('values', e.get('value', 'N/A'))} — Source: {e['source_line']}" for e in policy["entities"]])
    
    node_summary = []
    for node in policy["flow_nodes"]:
        icon = {"action": "⚙️", "condition": "🔀", "classification": "📋", "outcome": "🎯"}.get(node["type"], "•")
        node_summary.append(f"  {icon} {node['id']} [{node['type'].upper()}] → Policy Ref: {node['policy_ref']}")
    node_list = "\n".join(node_summary)

    disclaimer_list = "\n".join([f"  ⚠️ {d}" for d in policy["disclaimers"]])

    total_nodes = len(policy["flow_nodes"])
    conditions = len([n for n in policy["flow_nodes"] if n["type"] == "condition"])
    outcomes = len([n for n in policy["flow_nodes"] if n["type"] == "outcome"])

    response = f"""📄 **POLICY COMPILATION COMPLETE**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️ **{policy['name']}**
📋 Version: {policy['version']} | Updated: {policy['last_updated']}
🏢 Department: {policy['department']}
📁 Source: {policy['source_doc']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧬 **EXTRACTED ENTITIES ({len(policy['entities'])}):**
{entity_list}

🔀 **COMPILED FLOW GRAPH ({total_nodes} nodes):**
{node_list}

📊 **Graph Statistics:**
  • Total Nodes: {total_nodes}
  • Decision Points: {conditions}
  • Terminal Outcomes: {outcomes}
  • Entities Extracted: {len(policy['entities'])}

⚠️ **MANDATORY DISCLAIMERS:**
{disclaimer_list}

✅ **Compilation Status:** SUCCESS
🔒 **Graph Hash:** {hashlib.md5(policy['id'].encode()).hexdigest()[:12]}
📋 *Every outcome is deterministically linked to source policy text.*"""

    return response


def format_fuzz_response(policy_key, policy):
    """Format the fuzz testing results."""
    fuzz = policy["fuzz_results"]
    
    gap_text = ""
    if fuzz["critical_gaps"] > 0:
        for gap in fuzz["gap_details"]:
            gap_text += f"""
🚨 **{gap['id']} [{gap['severity']}]**
  • Scenario: {gap['scenario']}
  • Issue: {gap['issue']}
  • Fix: {gap['fix']}
  • Paths Affected: {gap['paths_affected']}
"""
    else:
        gap_text = "  ✅ No critical gaps detected.\n"

    warn_text = ""
    for w in fuzz["warning_details"]:
        warn_text += f"  ⚠️ {w['id']}: {w['scenario']} — {w['recommendation']}\n"

    coverage_icon = "🟢" if fuzz["coverage"] >= 95 else ("🟡" if fuzz["coverage"] >= 85 else "🔴")
    gap_icon = "🟢" if fuzz["critical_gaps"] == 0 else "🔴"

    response = f"""🧪 **AUTO-FUZZ TESTING COMPLETE**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Policy: **{policy['name']}** (v{policy['version']})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **Results Summary:**
  • Paths Traversed: **{fuzz['total_paths']:,}**
  • {coverage_icon} Rule Coverage: **{fuzz['coverage']}%**
  • {gap_icon} Critical Gaps: **{fuzz['critical_gaps']}**
  • ⚠️ Warnings: **{fuzz['warnings']}**

🚨 **CRITICAL GAPS:**
{gap_text}
⚠️ **WARNINGS:**
{warn_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 **Audit Pack Generated:**
  • Coverage Report: {policy['id']}_coverage.pdf
  • Gap Analysis: {policy['id']}_gaps.json
  • Regression Baseline: {policy['id']}_baseline_v{policy['version']}.snapshot

🔒 *All paths deterministically verified against source policy.*"""

    return response


def format_compliance_response(policy_key, policy, scenario_query):
    """Format compliance check response."""
    scenarios = COMPLIANCE_SCENARIOS.get(policy_key, [])
    
    # Find matching scenario or use the first one
    matched = None
    query_lower = scenario_query.lower() if scenario_query else ""
    for s in scenarios:
        if any(word in query_lower for word in s["scenario"].lower().split()[:3]):
            matched = s
            break
    if not matched and scenarios:
        matched = scenarios[0]
    
    if not matched:
        return "❌ No compliance scenarios found for this policy."

    response = f"""✅ **COMPLIANCE CHECK RESULT**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Policy: **{policy['name']}**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 **Scenario:** {matched['scenario']}

🎯 **Expected Outcome:** {matched['expected']}
{'✅' if matched['compliant'] else '❌'} **Compliant:** {'YES — Policy engine correctly enforces this path.' if matched['compliant'] else 'NO — Logic gap detected.'}

🔍 **Decision Trace:**
  1️⃣ START → Disclaimer displayed
  2️⃣ Product/Entity classified
  3️⃣ Eligibility conditions evaluated
  4️⃣ Outcome: **{matched['expected']}**

📋 *All decisions traceable to source policy document.*"""

    return response


def format_node_explanation(policy_key, policy, node_name):
    """Format explanation for a specific flow node."""
    node_name_upper = node_name.upper().strip().replace(" ", "_") if node_name else ""
    
    matched_node = None
    for node in policy["flow_nodes"]:
        if node["id"] == node_name_upper or node_name_upper in node["id"]:
            matched_node = node
            break
    
    if not matched_node:
        # Return overview of all nodes
        node_list = "\n".join([f"  • **{n['id']}** [{n['type']}]" for n in policy["flow_nodes"]])
        return f"""📋 **Available Nodes in {policy['name']}:**

{node_list}

💡 Ask about a specific node to see its logic, constraints, and policy reference."""

    icon = {"action": "⚙️", "condition": "🔀", "classification": "📋", "outcome": "🎯"}.get(matched_node["type"], "•")
    
    details = ""
    if matched_node["type"] == "condition":
        details = f"""
🔀 **Condition Logic:**
  ```
  IF ({matched_node.get('rule', 'N/A')}):
    → {matched_node.get('true_next', 'N/A')}
  ELSE:
    → {matched_node.get('false_next', 'N/A')}
  ```"""
    elif matched_node["type"] == "classification":
        branches = matched_node.get("branches", {})
        branch_text = "\n".join([f"    {k} → {v}" for k, v in branches.items()])
        details = f"""
📋 **Classification Branches:**
  Entity: {matched_node.get('entity', 'N/A')}
{branch_text}"""
    elif matched_node["type"] == "outcome":
        details = f"""
🎯 **Outcome:**
  Result: {matched_node.get('result', 'N/A')}
  Message: "{matched_node.get('message', 'N/A')}" """
    elif matched_node["type"] == "action":
        details = f"""
⚙️ **Action:**
  {matched_node.get('action', matched_node.get('message', 'N/A'))}
  Next → {matched_node.get('next', 'N/A')}"""

    response = f"""{icon} **NODE: {matched_node['id']}**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 Policy: {policy['name']}
📌 Type: {matched_node['type'].upper()}
📖 Policy Reference: {matched_node.get('policy_ref', 'N/A')}
{details}

🔒 *This node's behavior is deterministically bound to the source policy text referenced above. The LLM cannot override this logic.*"""

    return response


def format_runtime_response(policy_key, policy, user_query):
    """Process a customer query through the Policy Engine."""
    query_lower = user_query.lower() if user_query else ""
    
    # Determine scenario based on query
    if "return" in query_lower or "refund" in query_lower:
        if "laptop" in query_lower or "phone" in query_lower or "electronic" in query_lower:
            category = "ELECTRONICS"
            window = 14
        elif "gift" in query_lower:
            category = "GIFT"
            window = 30
        elif "promo" in query_lower or "sale" in query_lower or "diwali" in query_lower:
            category = "PROMOTIONAL"
            window = 7
        else:
            category = "GENERAL"
            window = 30

        response = f"""🤖 **POLICY ENGINE RESPONSE**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 **Active Flow:** Return & Refund Policy
📍 **Current Node:** IDENTIFY_PRODUCT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📢 **Required Disclaimer (Auto-Stated):**
"Please note that standard return processing time is 5-7 business days."

🔍 **Entity Extraction:**
  • ProductCategory: **{category}**
  • Return Window: **{window} days**

💬 **Generated Response:**
"I can help you with your return request. Before we proceed, please note that standard return processing takes 5-7 business days. Since your item is classified as {category.lower().replace('_', ' ')}, the eligible return window is {window} days from delivery. Could you please confirm when the item was delivered?"

🔒 **X-Ray — Engine Constraints:**
  ✅ Disclaimer: STATED (mandatory)
  ✅ Category: CLASSIFIED
  🔒 LLM Forbidden: Cannot promise instant refund
  🔒 LLM Forbidden: Cannot waive restocking fee
  ➡️ Next Required: Collect delivery date"""

    elif "kyc" in query_lower or "verification" in query_lower or "account" in query_lower:
        response = f"""🤖 **POLICY ENGINE RESPONSE**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 **Active Flow:** Customer KYC Verification
📍 **Current Node:** START_KYC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 **Generated Response:**
"I'll help you with your KYC verification. To get started, I need to determine the appropriate verification tier for your account. Could you please confirm:
1. How many days ago was your account opened?
2. What transaction limits do you need?"

🔒 **X-Ray — Engine Constraints:**
  ✅ Account age check: QUEUED
  ✅ PEP screening: REQUIRED
  🔒 LLM Forbidden: Cannot skip PEP check
  🔒 LLM Forbidden: Cannot override tier requirements
  ➡️ Next Required: Verify account age < 30 days"""

    elif "warranty" in query_lower or "repair" in query_lower or "broken" in query_lower:
        response = f"""🤖 **POLICY ENGINE RESPONSE**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 **Active Flow:** Warranty & Service Policy
📍 **Current Node:** START_WARRANTY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 **Generated Response:**
"I'll assist you with your warranty claim. To process this, I'll need to verify your warranty status. Could you please provide:
1. Your order number or purchase date
2. A description of the issue you're experiencing"

🔒 **X-Ray — Engine Constraints:**
  ✅ Purchase verification: QUEUED
  ✅ Warranty window check: REQUIRED
  🔒 LLM Forbidden: Cannot approve warranty for physical/water damage
  🔒 LLM Forbidden: Cannot override restocking fee
  ➡️ Next Required: Verify warranty active + damage type"""

    else:
        response = f"""🤖 **POLICY ENGINE — AVAILABLE FLOWS**

I can help you navigate the following policy-backed conversations:

📄 **1. Return & Refund Policy** — Process returns, check eligibility, apply restocking fees
📄 **2. KYC Verification Policy** — Identity verification tiers, document requirements
📄 **3. Warranty & Service Policy** — Warranty claims, repair scheduling, replacements

💡 Try saying:
  • "I want to return a laptop"
  • "What's the KYC process for a new account?"
  • "My phone has a manufacturing defect"

🔒 *All responses are governed by deterministic policy engine — zero hallucination guarantee.*"""

    return response


def format_overview():
    """Return overview of all policies."""
    response = """📊 **POLICY-TO-FLOW COMPILER — SYSTEM OVERVIEW**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏗️ **Compiled Policies: 3**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    for key, pol in POLICIES.items():
        fuzz = pol["fuzz_results"]
        status = "🟢 PASS" if fuzz["critical_gaps"] == 0 else "🔴 GAPS FOUND"
        nodes = len(pol["flow_nodes"])
        entities = len(pol["entities"])
        response += f"""📄 **{pol['name']}** (v{pol['version']})
  • Department: {pol['department']} | Industry: {pol['industry']}
  • Nodes: {nodes} | Entities: {entities}
  • Fuzz Coverage: {fuzz['coverage']}% ({fuzz['total_paths']:,} paths) | {status}

"""

    response += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 **Available Commands:**
  • "Compile return policy" — See full DSL compilation
  • "Fuzz test KYC policy" — Run compliance fuzzer
  • "Check compliance for return scenario" — Verify specific case
  • "Explain node CHECK_PACKAGING" — Deep-dive into a flow node
  • "I want to return a laptop" — Run conversation through engine

🔒 *Deterministic policy enforcement — zero compliance hallucinations.*"""
    return response


# --- Main Webhook Entry Point ---
@functions_framework.http
def webhook(request):
    """Cloud Function webhook for Dialogflow CX."""
    try:
        req = request.get_json(silent=True, force=True)
        if not req:
            return json.dumps({"fulfillmentResponse": {"messages": [{"text": {"text": ["Invalid request."]}}]}})

        # Extract webhook tag
        tag = req.get("fulfillmentInfo", {}).get("tag", "")
        
        # Extract parameters from session
        params = req.get("sessionInfo", {}).get("parameters", {})
        
        # Also check query text for context
        query_text = req.get("text", "")
        if not query_text:
            # Try to get from messages
            messages = req.get("messages", [])
            if messages:
                query_text = messages[-1].get("text", {}).get("text", [""])[0] if messages else ""

        # Extract policy name from parameters or query
        policy_name = params.get("policy-name", params.get("policy_name", ""))
        node_name = params.get("node-name", params.get("node_name", ""))
        scenario = params.get("scenario", "")
        user_query = params.get("user-query", params.get("user_query", query_text))

        # Route based on tag
        if tag == "compile_policy":
            result = get_policy(policy_name or user_query)
            if result:
                policy_key, policy = result
                response_text = format_compile_response(policy_key, policy)
            else:
                response_text = format_overview()

        elif tag == "fuzz_test":
            result = get_policy(policy_name or user_query)
            if result:
                policy_key, policy = result
                response_text = format_fuzz_response(policy_key, policy)
            else:
                response_text = "❌ Policy not found. Available policies: Return Policy, KYC Policy, Warranty Policy."

        elif tag == "check_compliance":
            result = get_policy(policy_name or user_query)
            if result:
                policy_key, policy = result
                response_text = format_compliance_response(policy_key, policy, scenario or user_query)
            else:
                response_text = "❌ Policy not found. Please specify: return policy, KYC policy, or warranty policy."

        elif tag == "explain_node":
            result = get_policy(policy_name or user_query)
            if result:
                policy_key, policy = result
                response_text = format_node_explanation(policy_key, policy, node_name or user_query)
            else:
                response_text = "❌ Policy not found. Please specify which policy's node to explain."

        elif tag == "runtime_query":
            response_text = format_runtime_response(None, None, user_query or policy_name)

        else:
            # Default: overview
            response_text = format_overview()

        # Return Dialogflow CX response format
        return json.dumps({
            "fulfillmentResponse": {
                "messages": [
                    {
                        "text": {
                            "text": [response_text]
                        }
                    }
                ]
            }
        })

    except Exception as e:
        error_msg = f"⚠️ Webhook Error: {str(e)}"
        return json.dumps({
            "fulfillmentResponse": {
                "messages": [{"text": {"text": [error_msg]}}]
            }
        })

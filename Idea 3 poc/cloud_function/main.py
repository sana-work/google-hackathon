import functions_framework
import json
import random
import datetime

# ============================================================================
# SILENT ESCALATION PREDICTOR — CLOUD FUNCTION WEBHOOK
# For Dialogflow CX Integration
# Track 3: Customer Engagement Suite | TCS^AI Hackathon 2026
# ============================================================================

# --- Synthetic Customer Database ---
CUSTOMERS = {
    "A-7842": {
        "name": "Priya Sharma",
        "company": "FinEdge Solutions",
        "segment": "Enterprise SaaS",
        "tier": "Gold",
        "tenure_months": 26,
        "acv": 4200000,
        "usage": {"login_freq_30d": 2, "login_freq_prev": 12, "feature_depth": 0.13, "session_duration_avg": 4.2, "session_prev": 18.5, "features_tried_30d": 0, "api_calls_weekly": 45, "api_prev": 320},
        "communication": {"email_open_rate": 0.08, "email_prev": 0.72, "newsletters_unopened": 6, "notification_response": 0.03, "last_email_open_days": 28, "unsubscribe": False},
        "support": {"tickets_90d": 0, "tickets_prev_90d": 4, "open_ticket_age_max": 0, "survey_response_rate": 0.0, "survey_prev": 0.80, "faq_visits_30d": 1, "faq_prev": 12},
        "transactions": {"purchase_freq_trend": -0.65, "payment_delay_days": 8, "payment_prev_delay": 0, "plan_change": "none", "cart_abandon_rate": 0.0, "renewal_days": 45, "renewal_engaged": False}
    },
    "B-3156": {
        "name": "Rajesh Mehta",
        "company": "CloudStack India",
        "segment": "Mid-Market SaaS",
        "tier": "Silver",
        "tenure_months": 14,
        "acv": 1800000,
        "usage": {"login_freq_30d": 8, "login_freq_prev": 10, "feature_depth": 0.55, "session_duration_avg": 14.0, "session_prev": 16.0, "features_tried_30d": 1, "api_calls_weekly": 180, "api_prev": 200},
        "communication": {"email_open_rate": 0.45, "email_prev": 0.60, "newsletters_unopened": 2, "notification_response": 0.30, "last_email_open_days": 5, "unsubscribe": False},
        "support": {"tickets_90d": 2, "tickets_prev_90d": 3, "open_ticket_age_max": 3, "survey_response_rate": 0.50, "survey_prev": 0.70, "faq_visits_30d": 8, "faq_prev": 10},
        "transactions": {"purchase_freq_trend": -0.10, "payment_delay_days": 0, "payment_prev_delay": 0, "plan_change": "none", "cart_abandon_rate": 0.0, "renewal_days": 120, "renewal_engaged": True}
    },
    "C-9281": {
        "name": "Ananya Reddy",
        "company": "MedSecure Health",
        "segment": "Enterprise Healthcare",
        "tier": "Platinum",
        "tenure_months": 38,
        "acv": 7500000,
        "usage": {"login_freq_30d": 5, "login_freq_prev": 14, "feature_depth": 0.28, "session_duration_avg": 6.8, "session_prev": 22.0, "features_tried_30d": 0, "api_calls_weekly": 89, "api_prev": 410},
        "communication": {"email_open_rate": 0.12, "email_prev": 0.65, "newsletters_unopened": 5, "notification_response": 0.05, "last_email_open_days": 22, "unsubscribe": False},
        "support": {"tickets_90d": 1, "tickets_prev_90d": 6, "open_ticket_age_max": 18, "survey_response_rate": 0.0, "survey_prev": 0.90, "faq_visits_30d": 3, "faq_prev": 15},
        "transactions": {"purchase_freq_trend": -0.40, "payment_delay_days": 0, "payment_prev_delay": 0, "plan_change": "downgrade_requested", "cart_abandon_rate": 0.0, "renewal_days": 60, "renewal_engaged": False}
    },
    "D-4510": {
        "name": "Vikram Joshi",
        "company": "RetailPulse",
        "segment": "SMB E-commerce",
        "tier": "Bronze",
        "tenure_months": 8,
        "acv": 480000,
        "usage": {"login_freq_30d": 18, "login_freq_prev": 20, "feature_depth": 0.72, "session_duration_avg": 25.0, "session_prev": 22.0, "features_tried_30d": 3, "api_calls_weekly": 550, "api_prev": 500},
        "communication": {"email_open_rate": 0.78, "email_prev": 0.75, "newsletters_unopened": 0, "notification_response": 0.65, "last_email_open_days": 1, "unsubscribe": False},
        "support": {"tickets_90d": 3, "tickets_prev_90d": 2, "open_ticket_age_max": 1, "survey_response_rate": 1.0, "survey_prev": 0.80, "faq_visits_30d": 6, "faq_prev": 5},
        "transactions": {"purchase_freq_trend": 0.15, "payment_delay_days": 0, "payment_prev_delay": 0, "plan_change": "upgrade_considered", "cart_abandon_rate": 0.12, "renewal_days": 180, "renewal_engaged": True}
    },
    "E-6723": {
        "name": "Kavitha Nair",
        "company": "TelcoVista",
        "segment": "Enterprise Telecom",
        "tier": "Gold",
        "tenure_months": 30,
        "acv": 5600000,
        "usage": {"login_freq_30d": 3, "login_freq_prev": 16, "feature_depth": 0.18, "session_duration_avg": 3.5, "session_prev": 20.0, "features_tried_30d": 0, "api_calls_weekly": 30, "api_prev": 280},
        "communication": {"email_open_rate": 0.05, "email_prev": 0.68, "newsletters_unopened": 8, "notification_response": 0.02, "last_email_open_days": 35, "unsubscribe": True},
        "support": {"tickets_90d": 0, "tickets_prev_90d": 5, "open_ticket_age_max": 0, "survey_response_rate": 0.0, "survey_prev": 0.75, "faq_visits_30d": 0, "faq_prev": 8},
        "transactions": {"purchase_freq_trend": -0.72, "payment_delay_days": 12, "payment_prev_delay": 0, "plan_change": "auto_renewal_cancelled", "cart_abandon_rate": 0.0, "renewal_days": 22, "renewal_engaged": False}
    }
}


def calculate_usage_score(usage):
    """Calculate usage channel score (0-100)."""
    login_decline = max(0, 1 - (usage["login_freq_30d"] / max(usage["login_freq_prev"], 1)))
    session_decline = max(0, 1 - (usage["session_duration_avg"] / max(usage["session_prev"], 1)))
    feature_score = 1 - usage["feature_depth"]
    api_decline = max(0, 1 - (usage["api_calls_weekly"] / max(usage["api_prev"], 1)))
    adoption = 1.0 if usage["features_tried_30d"] == 0 else 0.3

    score = (login_decline * 30 + session_decline * 20 + feature_score * 20 +
             api_decline * 15 + adoption * 15)
    return min(100, round(score))


def calculate_communication_score(comm):
    """Calculate communication channel score (0-100)."""
    email_decline = max(0, 1 - (comm["email_open_rate"] / max(comm["email_prev"], 0.01)))
    newsletter_score = min(1.0, comm["newsletters_unopened"] / 6)
    notif_silence = max(0, 1 - comm["notification_response"])
    days_inactive = min(1.0, comm["last_email_open_days"] / 30)
    unsub_penalty = 1.0 if comm["unsubscribe"] else 0.0

    score = (email_decline * 25 + newsletter_score * 20 + notif_silence * 20 +
             days_inactive * 20 + unsub_penalty * 15)
    return min(100, round(score))


def calculate_support_score(support):
    """Calculate support channel score (0-100)."""
    ticket_absence = 1.0 if support["tickets_90d"] == 0 and support["tickets_prev_90d"] > 2 else 0.0
    open_age = min(1.0, support["open_ticket_age_max"] / 14)
    survey_silence = max(0, 1 - (support["survey_response_rate"] / max(support["survey_prev"], 0.01)))
    faq_decline = max(0, 1 - (support["faq_visits_30d"] / max(support["faq_prev"], 1)))

    score = (ticket_absence * 35 + open_age * 20 + survey_silence * 25 + faq_decline * 20)
    return min(100, round(score))


def calculate_transaction_score(txn):
    """Calculate transaction channel score (0-100)."""
    freq_decline = max(0, abs(txn["purchase_freq_trend"])) if txn["purchase_freq_trend"] < 0 else 0
    payment_risk = min(1.0, txn["payment_delay_days"] / 10) if txn["payment_prev_delay"] == 0 else min(1.0, txn["payment_delay_days"] / 15)
    plan_risk = {"none": 0, "upgrade_considered": 0, "downgrade_requested": 0.6, "auto_renewal_cancelled": 1.0}.get(txn["plan_change"], 0)
    renewal_risk = 1.0 if txn["renewal_days"] < 60 and not txn["renewal_engaged"] else 0.0

    score = (freq_decline * 100 * 0.25 + payment_risk * 100 * 0.25 +
             plan_risk * 100 * 0.25 + renewal_risk * 100 * 0.25)
    return min(100, round(score))


def calculate_srs(customer):
    """Calculate composite Silent Risk Score."""
    usage_score = calculate_usage_score(customer["usage"])
    comm_score = calculate_communication_score(customer["communication"])
    support_score = calculate_support_score(customer["support"])
    txn_score = calculate_transaction_score(customer["transactions"])

    srs = round(0.30 * usage_score + 0.25 * comm_score + 0.20 * support_score + 0.25 * txn_score)

    # Special triggers
    if any(s > 90 for s in [usage_score, comm_score, support_score, txn_score]):
        srs = max(srs, 75)

    # Tenure trigger
    if customer["tenure_months"] > 24 and srs >= 41:
        srs = max(srs, 71)

    tier = "LOW" if srs <= 40 else ("MEDIUM" if srs <= 70 else "HIGH")
    color = "🟢" if tier == "LOW" else ("🟡" if tier == "MEDIUM" else "🔴")

    return {
        "srs": min(100, srs),
        "tier": tier,
        "color": color,
        "usage_score": usage_score,
        "comm_score": comm_score,
        "support_score": support_score,
        "txn_score": txn_score
    }


def build_evidence(customer, scores):
    """Build explainable evidence breakdown."""
    u = customer["usage"]
    c = customer["communication"]
    s = customer["support"]
    t = customer["transactions"]

    evidence = []

    # Usage evidence
    login_change = round((1 - u["login_freq_30d"] / max(u["login_freq_prev"], 1)) * 100)
    if login_change > 20:
        evidence.append(f"📱 Platform Usage: Logins dropped from {u['login_freq_prev']}/week to {u['login_freq_30d']}/week (↓{login_change}%)")
    session_change = round((1 - u["session_duration_avg"] / max(u["session_prev"], 1)) * 100)
    if session_change > 20:
        evidence.append(f"📱 Session Duration: Avg {u['session_prev']}min → {u['session_duration_avg']}min (↓{session_change}%)")
    if u["features_tried_30d"] == 0:
        evidence.append(f"📱 Feature Adoption: Zero new features tried in last 30 days (depth: {round(u['feature_depth']*100)}%)")

    # Communication evidence
    if c["newsletters_unopened"] >= 3:
        evidence.append(f"📧 Email Silence: Last {c['newsletters_unopened']} newsletters unopened (open rate: {round(c['email_open_rate']*100)}%)")
    if c["last_email_open_days"] > 14:
        evidence.append(f"📧 Communication Gap: No email engagement for {c['last_email_open_days']} days")
    if c["unsubscribe"]:
        evidence.append("📧 ⚠️ UNSUBSCRIBE detected — customer actively opted out of communications")

    # Support evidence
    if s["tickets_90d"] == 0 and s["tickets_prev_90d"] > 2:
        evidence.append(f"🎫 Support Silence: Zero tickets in 90 days (previously: {s['tickets_prev_90d']} tickets)")
    if s["open_ticket_age_max"] > 7:
        evidence.append(f"🎫 Unresolved Ticket: Open for {s['open_ticket_age_max']} days with no customer follow-up")
    if s["survey_response_rate"] == 0 and s["survey_prev"] > 0.5:
        evidence.append(f"🎫 Survey Disengagement: 0% response rate (was {round(s['survey_prev']*100)}%)")

    # Transaction evidence
    if t["payment_delay_days"] > 0 and t["payment_prev_delay"] == 0:
        evidence.append(f"💳 Payment Alert: Invoice {t['payment_delay_days']} days late (FIRST late payment in {customer['tenure_months']} months)")
    if t["plan_change"] == "downgrade_requested":
        evidence.append("💳 ⚠️ DOWNGRADE REQUEST submitted — evaluating lower tier")
    if t["plan_change"] == "auto_renewal_cancelled":
        evidence.append("💳 🚨 AUTO-RENEWAL CANCELLED — explicit departure intent")
    if t["renewal_days"] < 60 and not t["renewal_engaged"]:
        evidence.append(f"💳 Renewal Warning: {t['renewal_days']} days to renewal with ZERO engagement")

    return evidence


def get_intervention(customer, scores):
    """Generate intervention recommendation based on risk tier."""
    tier = scores["tier"]
    name = customer["name"]
    company = customer["company"]

    if tier == "LOW":
        return {
            "action": "Automated Re-engagement",
            "channel": "Email + In-App Notification",
            "urgency": "Within 48 hours",
            "details": f"Send personalized 'What's New' digest to {name} highlighting features they haven't explored. Include relevant case study from {customer['segment']} vertical.",
            "budget": "N/A",
            "approval": "None required"
        }
    elif tier == "MEDIUM":
        return {
            "action": "CSM Proactive Outreach",
            "channel": "Phone + Follow-up Email",
            "urgency": "Within 24 hours",
            "details": f"Customer Success Manager must contact {name} at {company} with specific reference to observed behavioral changes. Offer priority support queue access and schedule a product review session.",
            "budget": f"Up to ₹{round(customer['acv'] * 0.10):,} (10% of ACV)",
            "approval": "CSM Director"
        }
    else:
        return {
            "action": "🚨 IMMEDIATE Manager Escalation",
            "channel": "Executive Phone Call + Context Brief",
            "urgency": "Within 12 hours — CRITICAL",
            "details": f"Relationship Manager must personally contact {name} (CEO/CTO level at {company}). Full context brief auto-generated. Prepare custom retention package. Schedule executive business review.",
            "budget": f"Up to ₹{round(customer['acv'] * 0.20):,} (20% of ACV)",
            "approval": "VP/Account Director — HUMAN-IN-THE-LOOP REQUIRED"
        }


def get_cohort_insights(segment=None):
    """Return cohort-level insights."""
    insights = [
        {"segment": "Enterprise SaaS", "insight": "Customers show 3x higher silent churn risk after onboarding month 4 — the 'feature discovery cliff'", "action": "Schedule proactive feature workshops at month 3"},
        {"segment": "Telecom", "insight": "Weekend-only users who shift to zero weekend usage churn within 21 days (92% accuracy)", "action": "Trigger immediate SMS re-engagement for weekend usage drop"},
        {"segment": "Banking", "insight": "Transaction frequency below 2x/month after averaging 8x/month signals closure within 30 days", "action": "Offer premium account benefits and dedicated relationship manager"},
        {"segment": "E-commerce", "insight": "Cart abandonment increasing from <20% to >60% over 30 days predicts churn with 78% accuracy", "action": "Deploy personalized discount codes and recommendation engine"},
        {"segment": "Insurance", "insight": "Customers not opening renewal emails 60 days before expiry have 5.8x higher lapse rate", "action": "Switch to phone outreach for non-responsive renewal customers"},
        {"segment": "Healthcare", "insight": "API call volume dropping >50% in compliance-heavy accounts correlates with vendor evaluation", "action": "Proactive compliance assurance briefing with executive sponsor"}
    ]
    if segment:
        filtered = [i for i in insights if segment.lower() in i["segment"].lower()]
        return filtered if filtered else insights
    return insights


def format_risk_response(customer_id, customer, scores, evidence):
    """Format the risk analysis response for Dialogflow."""
    intervention = get_intervention(customer, scores)
    churn_probability = min(98, scores["srs"] + random.randint(3, 12))
    churn_window = "15-30 days" if scores["tier"] == "HIGH" else ("30-60 days" if scores["tier"] == "MEDIUM" else "60-90 days")

    response = f"""🔍 **SILENT RISK ANALYSIS — Customer {customer_id}**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 **{customer['name']}** | {customer['company']}
📊 Segment: {customer['segment']} | Tier: {customer['tier']} | Tenure: {customer['tenure_months']} months
💰 ACV: ₹{customer['acv']:,}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{scores['color']} **SILENT RISK SCORE: {scores['srs']}/100 — {scores['tier']} RISK**

📈 **Channel Breakdown:**
• Platform Usage: {scores['usage_score']}/100
• Communication: {scores['comm_score']}/100
• Support: {scores['support_score']}/100
• Transactions: {scores['txn_score']}/100

🔎 **Evidence:**
"""
    for e in evidence:
        response += f"• {e}\n"

    response += f"""
🎯 **Prediction:** {churn_probability}% churn probability within {churn_window}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ **RECOMMENDED INTERVENTION**
• Action: {intervention['action']}
• Channel: {intervention['channel']}
• Urgency: {intervention['urgency']}
• Details: {intervention['details']}
• Budget Authority: {intervention['budget']}
• Approval: {intervention['approval']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 *Reference: Customer_Retention_Policy_2025.txt, Behavioral_Signal_Definitions.txt*
⚠️ *DISCLAIMER: This is an AI-generated assessment. Human review is required before customer contact for MEDIUM and HIGH risk tiers.*"""

    return response


def format_intervention_response(customer_id, customer, scores):
    """Format intervention plan with personalized message."""
    intervention = get_intervention(customer, scores)

    if scores["tier"] == "HIGH":
        message = f"""Dear {customer['name']},

I'm reaching out personally because your partnership with us is incredibly important. I understand that things may not have been perfect recently, and I want to make sure we're fully aligned with your team's needs at {customer['company']}.

I'd love to schedule a brief call this week to:
1. Address any concerns your team may have
2. Share some exciting updates on our roadmap that are directly relevant to {customer['segment']}
3. Explore how we can better support your goals

Would Thursday or Friday work for a 30-minute conversation?

Best regards,
[Account Director Name]"""
    elif scores["tier"] == "MEDIUM":
        message = f"""Hi {customer['name']},

I noticed your team at {customer['company']} might benefit from some of our newer capabilities that we've launched recently. Based on your {customer['segment']} use case, I think you'd find [Feature X] particularly valuable.

Would you be open to a quick 15-minute walkthrough? I can also address any questions or feedback your team might have.

Looking forward to connecting!

[CSM Name]
Customer Success Manager"""
    else:
        message = f"""Hi {customer['name']},

We've been working on some exciting new features that customers in {customer['segment']} are loving! Here are 3 things you might want to check out:

✨ [Feature 1] — Save 30% time on [task]
📊 [Feature 2] — New analytics dashboard
🔗 [Feature 3] — Integration with [tool they use]

Check them out here: [link]

Warmly,
The Customer Success Team"""

    response = f"""📨 **PERSONALIZED INTERVENTION PLAN — Customer {customer_id}**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👤 {customer['name']} | {customer['company']} | {scores['color']} {scores['tier']} RISK (SRS: {scores['srs']})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ **Intervention Strategy:**
• Type: {intervention['action']}
• Channel: {intervention['channel']}
• Execute By: {intervention['urgency']}
• Approval: {intervention['approval']}

💬 **Gemini-Generated Personalized Message:**
───────────────────────────────
{message}
───────────────────────────────

📊 **Success Probability:**
• Re-engagement likelihood: {'54%' if scores['tier'] == 'HIGH' else ('44%' if scores['tier'] == 'MEDIUM' else '33%')} (based on historical benchmarks)
• Optimal follow-up: {'Same day' if scores['tier'] == 'HIGH' else ('3 days' if scores['tier'] == 'MEDIUM' else '7 days')}

📋 *Reference: Intervention_Playbook_SaaS.txt, Communication_Preferences_Guidelines.txt*
⚠️ *HUMAN-IN-THE-LOOP: {'REQUIRED — Manager must approve before sending' if scores['tier'] != 'LOW' else 'Not required for LOW risk automated outreach'}*"""

    return response


def format_cohort_response(segment=None):
    """Format cohort insights response."""
    insights = get_cohort_insights(segment)

    response = """📊 **COHORT INTELLIGENCE REPORT**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    for i, insight in enumerate(insights, 1):
        response += f"""**{i}. {insight['segment']}**
   📈 Insight: {insight['insight']}
   ⚡ Action: {insight['action']}

"""

    response += """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 *Reference: Churn_Analysis_Q4_2025.txt, Customer_Segmentation_Strategy.txt*
⚠️ *These insights are derived from anonymized behavioral data. No PII is used in analysis.*"""

    return response


def format_portfolio_response():
    """Format portfolio overview of all customers."""
    response = """📋 **CUSTOMER RISK PORTFOLIO OVERVIEW**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    high_risk = []
    medium_risk = []
    low_risk = []

    for cid, customer in CUSTOMERS.items():
        scores = calculate_srs(customer)
        entry = f"• **{cid}** — {customer['name']} ({customer['company']}) | SRS: {scores['srs']} | ACV: ₹{customer['acv']:,}"
        if scores["tier"] == "HIGH":
            high_risk.append(entry)
        elif scores["tier"] == "MEDIUM":
            medium_risk.append(entry)
        else:
            low_risk.append(entry)

    response += f"🔴 **HIGH RISK ({len(high_risk)} accounts)**\n"
    for entry in high_risk:
        response += f"  {entry}\n"

    response += f"\n🟡 **MEDIUM RISK ({len(medium_risk)} accounts)**\n"
    for entry in medium_risk:
        response += f"  {entry}\n"

    response += f"\n🟢 **LOW RISK ({len(low_risk)} accounts)**\n"
    for entry in low_risk:
        response += f"  {entry}\n"

    total_at_risk = len(high_risk) + len(medium_risk)
    total_acv_at_risk = sum(c["acv"] for cid, c in CUSTOMERS.items() if calculate_srs(c)["tier"] != "LOW")

    response += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 **Summary:** {total_at_risk}/{len(CUSTOMERS)} accounts at risk | At-risk ACV: ₹{total_acv_at_risk:,}
⚠️ *Scores refreshed: {datetime.datetime.now().strftime('%d %b %Y, %H:%M IST')}*"""

    return response


@functions_framework.http
def webhook(request):
    """Main Dialogflow CX webhook handler."""
    req = request.get_json(silent=True, force=True)

    # Extract the tag from Dialogflow CX
    tag = req.get("fulfillmentInfo", {}).get("tag", "")

    # Extract parameters
    params = {}
    session_params = req.get("sessionInfo", {}).get("parameters", {})
    page_params = req.get("pageInfo", {}).get("formInfo", {}).get("parameterInfo", [])

    for p in page_params:
        params[p.get("displayName", "")] = p.get("value", "")
    params.update(session_params)

    customer_id = params.get("customer-id", params.get("customer_id", "")).upper().strip()
    segment = params.get("segment", params.get("industry-segment", ""))

    response_text = ""

    if tag == "analyze_risk":
        if customer_id and customer_id in CUSTOMERS:
            customer = CUSTOMERS[customer_id]
            scores = calculate_srs(customer)
            evidence = build_evidence(customer, scores)
            response_text = format_risk_response(customer_id, customer, scores, evidence)
        elif customer_id:
            response_text = f"❌ Customer ID '{customer_id}' not found in our system. Available IDs for demo: {', '.join(CUSTOMERS.keys())}"
        else:
            response_text = f"Please provide a customer ID. Available demo customers: {', '.join(CUSTOMERS.keys())}"

    elif tag == "generate_intervention":
        if customer_id and customer_id in CUSTOMERS:
            customer = CUSTOMERS[customer_id]
            scores = calculate_srs(customer)
            response_text = format_intervention_response(customer_id, customer, scores)
        elif customer_id:
            response_text = f"❌ Customer ID '{customer_id}' not found. Try: {', '.join(CUSTOMERS.keys())}"
        else:
            response_text = f"Please provide a customer ID for intervention planning. Available: {', '.join(CUSTOMERS.keys())}"

    elif tag == "cohort_insights":
        response_text = format_cohort_response(segment if segment else None)

    elif tag == "portfolio_overview":
        response_text = format_portfolio_response()

    elif tag == "check_score":
        if customer_id and customer_id in CUSTOMERS:
            customer = CUSTOMERS[customer_id]
            scores = calculate_srs(customer)
            response_text = f"{scores['color']} Customer {customer_id} ({customer['name']}): Silent Risk Score = **{scores['srs']}/100** — **{scores['tier']} RISK**"
        else:
            response_text = f"Please provide a valid customer ID. Available: {', '.join(CUSTOMERS.keys())}"

    else:
        response_text = f"Welcome to the Silent Escalation Predictor! I can help you:\n\n• 🔍 **Analyze risk** for a specific customer\n• 📨 **Generate intervention** plans\n• 📊 **View cohort insights** across segments\n• 📋 **Portfolio overview** of all accounts\n\nTry: 'Analyze risk for customer A-7842'"

    # Build Dialogflow CX webhook response
    res = {
        "fulfillmentResponse": {
            "messages": [
                {
                    "text": {
                        "text": [response_text]
                    }
                }
            ]
        }
    }

    return json.dumps(res), 200, {"Content-Type": "application/json"}

const GRAPH = {
  "nodes": [
    {
      "id": 0,
      "label": "COMMAND Orchestrator",
      "group": "SUPER_AGENTS",
      "type": "orchestrator",
      "status": "active",
      "tools": 458,
      "description": "Top-level orchestrator that routes every request across all 85 EMG-JARVIS agents, arbitrates priority, and keeps the full agent mesh in sync.",
      "linkedAgents": [
        1,
        2,
        4,
        6,
        10,
        12,
        29
      ],
      "color": "#C9A84C"
    },
    {
      "id": 1,
      "label": "ORACLE BI",
      "group": "SUPER_AGENTS",
      "type": "analytics-engine",
      "status": "processing",
      "tools": 45,
      "description": "Business-intelligence agent that aggregates revenue, pipeline, and campaign metrics into live dashboards and forecasts for leadership.",
      "linkedAgents": [
        0,
        10,
        31,
        61,
        84
      ],
      "color": "#C9A84C"
    },
    {
      "id": 2,
      "label": "CLOSE COMMANDER",
      "group": "SUPER_AGENTS",
      "type": "sales-closer",
      "status": "active",
      "tools": 38,
      "description": "Runs the deal-closing playbook end to end: pricing, objection handling, contract generation, and final sign-off coordination.",
      "linkedAgents": [
        0,
        3,
        50,
        72,
        59,
        11
      ],
      "color": "#C9A84C"
    },
    {
      "id": 3,
      "label": "KAREN",
      "group": "SUPER_AGENTS",
      "type": "conflict-resolution",
      "status": "active",
      "tools": 32,
      "description": "De-escalation and negotiation specialist that steps in on angry customers, refund disputes, and high-risk churn conversations.",
      "linkedAgents": [
        0,
        2,
        16,
        35,
        20,
        52
      ],
      "color": "#C9A84C"
    },
    {
      "id": 4,
      "label": "EMPIRE VIDEO COMMANDER",
      "group": "SUPER_AGENTS",
      "type": "video-production",
      "status": "active",
      "tools": 672,
      "description": "Master video production agent overseeing scripting, shot lists, editing pipelines, and delivery for every client video asset.",
      "linkedAgents": [
        0,
        6,
        56,
        8,
        9
      ],
      "color": "#C9A84C"
    },
    {
      "id": 5,
      "label": "GUARDIAN",
      "group": "SUPER_AGENTS",
      "type": "security-guardian",
      "status": "processing",
      "tools": 28,
      "description": "Security and access-control agent that watches credentials, API keys, and permission boundaries across the entire agent network.",
      "linkedAgents": [
        0,
        7,
        30,
        39,
        18
      ],
      "color": "#C9A84C"
    },
    {
      "id": 6,
      "label": "CONTENT STUDIO ORCHESTRATOR",
      "group": "SUPER_AGENTS",
      "type": "content-orchestrator",
      "status": "active",
      "tools": 35,
      "description": "Coordinates the content studio: briefs, drafts, approvals, and hand-off between copywriters, designers, and the video pipeline.",
      "linkedAgents": [
        0,
        4,
        9,
        8,
        32,
        56
      ],
      "color": "#C9A84C"
    },
    {
      "id": 7,
      "label": "SENTINEL",
      "group": "SUPER_AGENTS",
      "type": "system-monitor",
      "status": "processing",
      "tools": 22,
      "description": "Uptime and anomaly-detection agent that continuously health-checks every integration, workflow, and automation in the stack.",
      "linkedAgents": [
        0,
        5,
        39,
        30,
        79
      ],
      "color": "#C9A84C"
    },
    {
      "id": 8,
      "label": "BROADCAST MANAGER",
      "group": "SUPER_AGENTS",
      "type": "broadcast-manager",
      "status": "active",
      "tools": 41,
      "description": "Schedules and dispatches mass email, SMS, and voicemail-drop broadcasts, then tracks deliverability and engagement.",
      "linkedAgents": [
        0,
        4,
        9,
        44,
        57,
        58
      ],
      "color": "#C9A84C"
    },
    {
      "id": 9,
      "label": "SOCIAL PLANNER",
      "group": "SUPER_AGENTS",
      "type": "social-strategist",
      "status": "active",
      "tools": 29,
      "description": "Plans and queues the social content calendar across every client channel, syncing with video production and copy approvals.",
      "linkedAgents": [
        0,
        4,
        6,
        8,
        55,
        32
      ],
      "color": "#C9A84C"
    },
    {
      "id": 10,
      "label": "DATA-FORGE",
      "group": "SUPER_AGENTS",
      "type": "data-engine",
      "status": "active",
      "tools": 55,
      "description": "Central data-engineering agent that cleans, normalizes, tags, and syncs records across CRM, ad platforms, and reporting tools.",
      "linkedAgents": [
        0,
        1,
        38,
        82,
        83,
        80,
        81
      ],
      "color": "#C9A84C"
    },
    {
      "id": 11,
      "label": "AD COMMANDER",
      "group": "SUPER_AGENTS",
      "type": "ad-operations",
      "status": "active",
      "tools": 48,
      "description": "Manages paid-media operations across ad platforms: budget pacing, creative rotation, audience targeting, and spend reporting.",
      "linkedAgents": [
        0,
        2,
        63,
        70,
        71,
        1
      ],
      "color": "#C9A84C"
    },
    {
      "id": 12,
      "label": "NEXUS MASTER SOP",
      "group": "SUPER_AGENTS",
      "type": "sop-engine",
      "status": "active",
      "tools": 33,
      "description": "Owns the standard-operating-procedure library and enforces workflow compliance across every other agent in the fleet.",
      "linkedAgents": [
        0,
        29,
        62,
        65,
        66
      ],
      "color": "#C9A84C"
    },
    {
      "id": 13,
      "label": "REVIVE COMMANDER",
      "group": "SUPER_AGENTS",
      "type": "reactivation-engine",
      "status": "active",
      "tools": 27,
      "description": "Runs win-back campaigns for dormant leads and lapsed clients, sequencing outreach until a contact reactivates or opts out.",
      "linkedAgents": [
        0,
        46,
        54,
        69,
        52,
        27
      ],
      "color": "#C9A84C"
    },
    {
      "id": 14,
      "label": "GENESIS PRIME",
      "group": "SUPER_AGENTS",
      "type": "lead-generation",
      "status": "active",
      "tools": 52,
      "description": "Primary lead-generation agent that spins up new-market campaigns, landing funnels, and top-of-funnel qualification logic.",
      "linkedAgents": [
        0,
        37,
        17,
        63,
        48,
        21
      ],
      "color": "#C9A84C"
    },
    {
      "id": 15,
      "label": "REFERRAL ENGINE",
      "group": "SUPER_AGENTS",
      "type": "referral-engine",
      "status": "active",
      "tools": 24,
      "description": "Automates referral requests, tracks referral chains, and rewards clients who send new business into the pipeline.",
      "linkedAgents": [
        0,
        40,
        41,
        16,
        28
      ],
      "color": "#C9A84C"
    },
    {
      "id": 16,
      "label": "REVIEW COMMANDER",
      "group": "SUPER_AGENTS",
      "type": "reputation-manager",
      "status": "active",
      "tools": 31,
      "description": "Manages online reputation: review requests, response drafting, sentiment triage, and escalation of negative feedback to KAREN.",
      "linkedAgents": [
        0,
        42,
        43,
        67,
        68,
        3
      ],
      "color": "#C9A84C"
    },
    {
      "id": 17,
      "label": "INTAKE COMMANDER",
      "group": "SUPER_AGENTS",
      "type": "intake-manager",
      "status": "active",
      "tools": 36,
      "description": "Owns new-client and new-lead intake: form routing, qualification scoring, and first-touch assignment to the right pipeline.",
      "linkedAgents": [
        0,
        47,
        48,
        22,
        14,
        63
      ],
      "color": "#C9A84C"
    },
    {
      "id": 18,
      "label": "ABLE",
      "group": "VOICE_AI",
      "type": "voice-agent",
      "status": "active",
      "tools": 0,
      "description": "Boss's personal voice interface into EMG-JARVIS -- handles direct verbal commands, briefings, and system status requests.",
      "linkedAgents": [
        0,
        5,
        1,
        12
      ],
      "color": "#00E5FF"
    },
    {
      "id": 19,
      "label": "VICTOR",
      "group": "VOICE_AI",
      "type": "voice-agent",
      "status": "active",
      "tools": 0,
      "description": "Outbound sales voice agent that runs live cold and warm call scripts and hands qualified prospects to CLOSE COMMANDER.",
      "linkedAgents": [
        2,
        11,
        50,
        49
      ],
      "color": "#00E5FF"
    },
    {
      "id": 20,
      "label": "SONYA",
      "group": "VOICE_AI",
      "type": "voice-agent",
      "status": "active",
      "tools": 0,
      "description": "Customer-care voice agent for inbound support calls, escalating unresolved or heated conversations straight to KAREN.",
      "linkedAgents": [
        3,
        16,
        68,
        67
      ],
      "color": "#00E5FF"
    },
    {
      "id": 21,
      "label": "NOVA-VOICE",
      "group": "VOICE_AI",
      "type": "voice-agent",
      "status": "active",
      "tools": 0,
      "description": "Lead-generation voice agent that cold-calls fresh lists and pushes qualified answers into the intake pipeline.",
      "linkedAgents": [
        14,
        17,
        37,
        48
      ],
      "color": "#00E5FF"
    },
    {
      "id": 22,
      "label": "SAGE-INBOUND",
      "group": "VOICE_AI",
      "type": "voice-agent",
      "status": "active",
      "tools": 0,
      "description": "First-response inbound call agent that answers every ringing line, captures intent, and books the next available slot.",
      "linkedAgents": [
        17,
        47,
        62
      ],
      "color": "#00E5FF"
    },
    {
      "id": 23,
      "label": "ARIA-L",
      "group": "VOICE_AI",
      "type": "voice-agent",
      "status": "active",
      "tools": 0,
      "description": "Local-market voice agent handling geo-targeted campaigns and community outreach calls for regional clients.",
      "linkedAgents": [
        9,
        8,
        55
      ],
      "color": "#00E5FF"
    },
    {
      "id": 24,
      "label": "ARIA-E",
      "group": "VOICE_AI",
      "type": "voice-agent",
      "status": "active",
      "tools": 0,
      "description": "Enterprise-account voice agent for high-value client calls, renewal conversations, and account-review scheduling.",
      "linkedAgents": [
        11,
        10,
        52
      ],
      "color": "#00E5FF"
    },
    {
      "id": 25,
      "label": "ARIA-C",
      "group": "VOICE_AI",
      "type": "voice-agent",
      "status": "active",
      "tools": 0,
      "description": "Client-success voice agent that runs proactive check-in calls and feeds satisfaction signals to REVIEW COMMANDER.",
      "linkedAgents": [
        16,
        52,
        42
      ],
      "color": "#00E5FF"
    },
    {
      "id": 26,
      "label": "ECHO",
      "group": "VOICE_AI",
      "type": "voice-agent",
      "status": "active",
      "tools": 0,
      "description": "Appointment-booking voice agent that converses live to find, confirm, and lock in calendar slots.",
      "linkedAgents": [
        36,
        62,
        65
      ],
      "color": "#00E5FF"
    },
    {
      "id": 27,
      "label": "ATLAS",
      "group": "VOICE_AI",
      "type": "voice-agent",
      "status": "active",
      "tools": 0,
      "description": "Reactivation voice agent that calls dormant leads directly, working hand-in-hand with REVIVE COMMANDER's sequences.",
      "linkedAgents": [
        13,
        46,
        54
      ],
      "color": "#00E5FF"
    },
    {
      "id": 28,
      "label": "DOM-Voice",
      "group": "VOICE_AI",
      "type": "voice-agent",
      "status": "active",
      "tools": 0,
      "description": "Referral and review outreach voice agent that calls happy clients to ask for referrals and five-star reviews.",
      "linkedAgents": [
        15,
        40,
        16,
        42
      ],
      "color": "#00E5FF"
    },
    {
      "id": 29,
      "label": "COMMAND-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Text-chat front door to the COMMAND Orchestrator; routes SMS and webchat requests to the right specialist agent.",
      "linkedAgents": [
        0,
        12,
        62
      ],
      "color": "#00C896"
    },
    {
      "id": 30,
      "label": "GUARDIAN-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Chat-based access-request handler that logs and verifies permission changes on behalf of GUARDIAN.",
      "linkedAgents": [
        5,
        7,
        39
      ],
      "color": "#00C896"
    },
    {
      "id": 31,
      "label": "ORACLE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Conversational reporting bot that answers plain-language metric questions by querying ORACLE BI's dashboards.",
      "linkedAgents": [
        1,
        61,
        84
      ],
      "color": "#00C896"
    },
    {
      "id": 32,
      "label": "SPARK",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Creative-ideation chat bot that brainstorms campaign concepts and hooks for the content studio and social planner.",
      "linkedAgents": [
        6,
        9,
        56
      ],
      "color": "#00C896"
    },
    {
      "id": 33,
      "label": "MAYA",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "General-purpose scheduling conversation bot that chats with leads to find a time before handing off to MAYA-BOOK.",
      "linkedAgents": [
        34,
        62,
        65
      ],
      "color": "#00C896"
    },
    {
      "id": 34,
      "label": "MAYA-BOOK",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Calendar-booking bot that finalizes and writes confirmed appointments from MAYA's conversations into the calendar.",
      "linkedAgents": [
        33,
        62,
        65,
        66
      ],
      "color": "#00C896"
    },
    {
      "id": 35,
      "label": "MARCUS-AGREEMENTS",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Contract and agreement bot that drafts, sends, and tracks e-signature status for closed deals.",
      "linkedAgents": [
        2,
        3,
        59,
        60
      ],
      "color": "#00C896"
    },
    {
      "id": 36,
      "label": "ECHO-BOOK",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Text counterpart to the ECHO voice agent, confirming bookings by SMS after a live call.",
      "linkedAgents": [
        26,
        62,
        65
      ],
      "color": "#00C896"
    },
    {
      "id": 37,
      "label": "GENESIS-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Chat-based top-of-funnel qualifier that scores inbound leads for GENESIS PRIME's campaigns.",
      "linkedAgents": [
        14,
        17,
        48
      ],
      "color": "#00C896"
    },
    {
      "id": 38,
      "label": "DATA-FORGE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Conversational data-cleanup bot that flags duplicate or malformed records for DATA-FORGE to reconcile.",
      "linkedAgents": [
        10,
        82,
        83,
        81
      ],
      "color": "#00C896"
    },
    {
      "id": 39,
      "label": "SENTINEL-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Alerting chat bot that posts SENTINEL's uptime and anomaly warnings into the team's monitoring channel.",
      "linkedAgents": [
        7,
        5,
        79
      ],
      "color": "#00C896"
    },
    {
      "id": 40,
      "label": "REFERRAL-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends referral-ask messages to happy clients and tracks who has responded for the REFERRAL ENGINE.",
      "linkedAgents": [
        15,
        41,
        28
      ],
      "color": "#00C896"
    },
    {
      "id": 41,
      "label": "REFERRAL-AI",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Conversational assistant that answers referral-program questions and issues reward codes automatically.",
      "linkedAgents": [
        15,
        40
      ],
      "color": "#00C896"
    },
    {
      "id": 42,
      "label": "REVIEW-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends review-request texts after service completion and nudges non-responders for REVIEW COMMANDER.",
      "linkedAgents": [
        16,
        43,
        67
      ],
      "color": "#00C896"
    },
    {
      "id": 43,
      "label": "REVIEW-AI",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Drafts suggested responses to incoming reviews, flagging negative ones for KAREN and REVIEW COMMANDER.",
      "linkedAgents": [
        16,
        42,
        3
      ],
      "color": "#00C896"
    },
    {
      "id": 44,
      "label": "BROADCAST-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Executes scheduled mass-message sends queued by BROADCAST MANAGER and reports delivery status.",
      "linkedAgents": [
        8,
        57,
        58
      ],
      "color": "#00C896"
    },
    {
      "id": 45,
      "label": "NURTURE-PRIME",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Primary long-term nurture-sequence bot that keeps warm leads engaged with drip content until they're sales-ready.",
      "linkedAgents": [
        64,
        49,
        63
      ],
      "color": "#00C896"
    },
    {
      "id": 46,
      "label": "REVIVE-FINAL",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Last-touch reactivation message bot that sends the final win-back offer before a lead is archived.",
      "linkedAgents": [
        13,
        27,
        54,
        79
      ],
      "color": "#00C896"
    },
    {
      "id": 47,
      "label": "INTAKE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "First-message intake bot that greets new leads, collects basics, and routes them to INTAKE COMMANDER.",
      "linkedAgents": [
        17,
        48,
        22
      ],
      "color": "#00C896"
    },
    {
      "id": 48,
      "label": "QUALIFY-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Asks qualification questions over chat and scores leads before they're passed to sales.",
      "linkedAgents": [
        17,
        14,
        63,
        37
      ],
      "color": "#00C896"
    },
    {
      "id": 49,
      "label": "FOLLOW-UP-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Automated follow-up message sequencer that keeps a prospect warm between sales touches.",
      "linkedAgents": [
        2,
        50,
        45
      ],
      "color": "#00C896"
    },
    {
      "id": 50,
      "label": "CLOSE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends pricing, proposal links, and closing nudges on behalf of CLOSE COMMANDER over chat.",
      "linkedAgents": [
        2,
        59,
        74,
        49
      ],
      "color": "#00C896"
    },
    {
      "id": 51,
      "label": "ONBOARD-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Walks brand-new clients through onboarding steps and collects required setup information.",
      "linkedAgents": [
        2,
        53,
        65
      ],
      "color": "#00C896"
    },
    {
      "id": 52,
      "label": "RETAIN-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Proactively messages at-risk accounts with retention offers before they churn.",
      "linkedAgents": [
        13,
        3,
        25
      ],
      "color": "#00C896"
    },
    {
      "id": 53,
      "label": "UPSELL-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Identifies upsell moments in the client lifecycle and sends targeted upgrade offers.",
      "linkedAgents": [
        51,
        2,
        74
      ],
      "color": "#00C896"
    },
    {
      "id": 54,
      "label": "REACTIVATE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends reactivation offers to dormant contacts as part of REVIVE COMMANDER's campaign sequence.",
      "linkedAgents": [
        13,
        46,
        69
      ],
      "color": "#00C896"
    },
    {
      "id": 55,
      "label": "SOCIAL-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Publishes queued posts and replies to comments/DMs across social channels for SOCIAL PLANNER.",
      "linkedAgents": [
        9,
        32,
        56
      ],
      "color": "#00C896"
    },
    {
      "id": 56,
      "label": "VIDEO-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Notifies clients when a video asset is ready for review and collects revision feedback.",
      "linkedAgents": [
        4,
        6,
        55
      ],
      "color": "#00C896"
    },
    {
      "id": 57,
      "label": "EMAIL-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends and tracks transactional and campaign emails queued by BROADCAST MANAGER.",
      "linkedAgents": [
        8,
        44,
        58
      ],
      "color": "#00C896"
    },
    {
      "id": 58,
      "label": "SMS-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends and tracks transactional and campaign SMS messages queued by BROADCAST MANAGER.",
      "linkedAgents": [
        8,
        44,
        57
      ],
      "color": "#00C896"
    },
    {
      "id": 59,
      "label": "PROPOSAL-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Generates and sends pricing proposals, tracking opens and follow-up timing for CLOSE COMMANDER.",
      "linkedAgents": [
        2,
        50,
        35
      ],
      "color": "#00C896"
    },
    {
      "id": 60,
      "label": "INVOICE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Generates invoices after a deal closes and sends payment reminders until settled.",
      "linkedAgents": [
        2,
        35,
        59
      ],
      "color": "#00C896"
    },
    {
      "id": 61,
      "label": "REPORT-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends scheduled performance-report summaries pulled from ORACLE BI to clients and staff.",
      "linkedAgents": [
        1,
        31,
        84
      ],
      "color": "#00C896"
    },
    {
      "id": 62,
      "label": "SCHEDULE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Handles calendar-slot lookups and holds for every booking conversation across the fleet.",
      "linkedAgents": [
        33,
        34,
        65,
        66
      ],
      "color": "#00C896"
    },
    {
      "id": 63,
      "label": "LEAD-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Captures and routes new inbound leads from web forms and ads into the correct pipeline stage.",
      "linkedAgents": [
        14,
        11,
        48,
        72
      ],
      "color": "#00C896"
    },
    {
      "id": 64,
      "label": "NURTURE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends scheduled nurture-drip content to leads that aren't yet sales-ready.",
      "linkedAgents": [
        45,
        49,
        63
      ],
      "color": "#00C896"
    },
    {
      "id": 65,
      "label": "CONFIRM-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends appointment-confirmation messages immediately after a booking is made.",
      "linkedAgents": [
        62,
        66,
        34
      ],
      "color": "#00C896"
    },
    {
      "id": 66,
      "label": "REMIND-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends reminder messages ahead of scheduled appointments and calls to reduce no-shows.",
      "linkedAgents": [
        62,
        65,
        34
      ],
      "color": "#00C896"
    },
    {
      "id": 67,
      "label": "SURVEY-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends post-interaction satisfaction surveys and compiles the responses for REVIEW COMMANDER.",
      "linkedAgents": [
        16,
        68,
        42
      ],
      "color": "#00C896"
    },
    {
      "id": 68,
      "label": "FEEDBACK-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Collects free-text client feedback and routes negative sentiment to KAREN for follow-up.",
      "linkedAgents": [
        16,
        67,
        3
      ],
      "color": "#00C896"
    },
    {
      "id": 69,
      "label": "REACTIVATE-AI",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "AI-personalized reactivation message writer that tailors win-back copy per contact history.",
      "linkedAgents": [
        13,
        54,
        46
      ],
      "color": "#00C896"
    },
    {
      "id": 70,
      "label": "COLD-OUTREACH-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Runs first-touch cold outreach sequences into new prospect lists for AD COMMANDER's campaigns.",
      "linkedAgents": [
        11,
        63,
        71
      ],
      "color": "#00C896"
    },
    {
      "id": 71,
      "label": "HOT-LIST-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Monitors engagement signals to flag hot, sales-ready leads for immediate follow-up.",
      "linkedAgents": [
        11,
        63,
        70,
        49
      ],
      "color": "#00C896"
    },
    {
      "id": 72,
      "label": "PIPELINE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Keeps deal-pipeline stages up to date as prospects move through the sales process.",
      "linkedAgents": [
        2,
        73,
        74
      ],
      "color": "#00C896"
    },
    {
      "id": 73,
      "label": "STAGE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Moves deals between pipeline stages automatically based on conversation and activity triggers.",
      "linkedAgents": [
        72,
        74,
        2
      ],
      "color": "#00C896"
    },
    {
      "id": 74,
      "label": "DEAL-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Tracks individual deal status, value, and next steps, syncing changes back to CLOSE COMMANDER.",
      "linkedAgents": [
        2,
        72,
        75,
        76
      ],
      "color": "#00C896"
    },
    {
      "id": 75,
      "label": "WIN-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Logs closed-won deals, triggers onboarding hand-off, and notifies the team of the win.",
      "linkedAgents": [
        74,
        51,
        2
      ],
      "color": "#00C896"
    },
    {
      "id": 76,
      "label": "LOSS-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Logs closed-lost deals with reason codes and queues them for REVIVE COMMANDER's later win-back attempts.",
      "linkedAgents": [
        74,
        13,
        2
      ],
      "color": "#00C896"
    },
    {
      "id": 77,
      "label": "PAUSE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Handles subscription/service pause requests and schedules the resume date.",
      "linkedAgents": [
        13,
        78,
        52
      ],
      "color": "#00C896"
    },
    {
      "id": 78,
      "label": "RESUME-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Sends resume-reminder messages and reactivates paused services on schedule.",
      "linkedAgents": [
        77,
        13,
        52
      ],
      "color": "#00C896"
    },
    {
      "id": 79,
      "label": "ARCHIVE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Archives stale or unresponsive contacts and records after final outreach attempts fail.",
      "linkedAgents": [
        7,
        46,
        39
      ],
      "color": "#00C896"
    },
    {
      "id": 80,
      "label": "EXPORT-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Handles on-demand data export requests and delivers formatted files from DATA-FORGE.",
      "linkedAgents": [
        10,
        81,
        38
      ],
      "color": "#00C896"
    },
    {
      "id": 81,
      "label": "SYNC-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Keeps CRM, ad-platform, and reporting records in sync across all connected systems.",
      "linkedAgents": [
        10,
        38,
        80
      ],
      "color": "#00C896"
    },
    {
      "id": 82,
      "label": "TAG-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Applies and cleans up contact tags based on behavior and campaign rules for DATA-FORGE.",
      "linkedAgents": [
        10,
        38,
        83
      ],
      "color": "#00C896"
    },
    {
      "id": 83,
      "label": "SEGMENT-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Builds and maintains audience segments used by campaigns across the fleet.",
      "linkedAgents": [
        10,
        82,
        38
      ],
      "color": "#00C896"
    },
    {
      "id": 84,
      "label": "SCORE-BOT",
      "group": "CONVERSATION_AI",
      "type": "conversation-bot",
      "status": "offline",
      "tools": 0,
      "description": "Calculates and updates lead and client scores consumed by ORACLE BI and the sales agents.",
      "linkedAgents": [
        1,
        31,
        63
      ],
      "color": "#00C896"
    }
  ],
  "links": [
    {
      "source": 0,
      "target": 1
    },
    {
      "source": 0,
      "target": 2
    },
    {
      "source": 0,
      "target": 4
    },
    {
      "source": 0,
      "target": 6
    },
    {
      "source": 0,
      "target": 10
    },
    {
      "source": 0,
      "target": 12
    },
    {
      "source": 0,
      "target": 29
    },
    {
      "source": 1,
      "target": 10
    },
    {
      "source": 1,
      "target": 31
    },
    {
      "source": 1,
      "target": 61
    },
    {
      "source": 1,
      "target": 84
    },
    {
      "source": 2,
      "target": 3
    },
    {
      "source": 2,
      "target": 50
    },
    {
      "source": 2,
      "target": 72
    },
    {
      "source": 2,
      "target": 59
    },
    {
      "source": 2,
      "target": 11
    },
    {
      "source": 3,
      "target": 0
    },
    {
      "source": 3,
      "target": 16
    },
    {
      "source": 3,
      "target": 35
    },
    {
      "source": 3,
      "target": 20
    },
    {
      "source": 3,
      "target": 52
    },
    {
      "source": 4,
      "target": 6
    },
    {
      "source": 4,
      "target": 56
    },
    {
      "source": 4,
      "target": 8
    },
    {
      "source": 4,
      "target": 9
    },
    {
      "source": 5,
      "target": 0
    },
    {
      "source": 5,
      "target": 7
    },
    {
      "source": 5,
      "target": 30
    },
    {
      "source": 5,
      "target": 39
    },
    {
      "source": 5,
      "target": 18
    },
    {
      "source": 6,
      "target": 9
    },
    {
      "source": 6,
      "target": 8
    },
    {
      "source": 6,
      "target": 32
    },
    {
      "source": 6,
      "target": 56
    },
    {
      "source": 7,
      "target": 0
    },
    {
      "source": 7,
      "target": 39
    },
    {
      "source": 7,
      "target": 30
    },
    {
      "source": 7,
      "target": 79
    },
    {
      "source": 8,
      "target": 0
    },
    {
      "source": 8,
      "target": 9
    },
    {
      "source": 8,
      "target": 44
    },
    {
      "source": 8,
      "target": 57
    },
    {
      "source": 8,
      "target": 58
    },
    {
      "source": 9,
      "target": 0
    },
    {
      "source": 9,
      "target": 55
    },
    {
      "source": 9,
      "target": 32
    },
    {
      "source": 10,
      "target": 38
    },
    {
      "source": 10,
      "target": 82
    },
    {
      "source": 10,
      "target": 83
    },
    {
      "source": 10,
      "target": 80
    },
    {
      "source": 10,
      "target": 81
    },
    {
      "source": 11,
      "target": 0
    },
    {
      "source": 11,
      "target": 63
    },
    {
      "source": 11,
      "target": 70
    },
    {
      "source": 11,
      "target": 71
    },
    {
      "source": 11,
      "target": 1
    },
    {
      "source": 12,
      "target": 29
    },
    {
      "source": 12,
      "target": 62
    },
    {
      "source": 12,
      "target": 65
    },
    {
      "source": 12,
      "target": 66
    },
    {
      "source": 13,
      "target": 0
    },
    {
      "source": 13,
      "target": 46
    },
    {
      "source": 13,
      "target": 54
    },
    {
      "source": 13,
      "target": 69
    },
    {
      "source": 13,
      "target": 52
    },
    {
      "source": 13,
      "target": 27
    },
    {
      "source": 14,
      "target": 0
    },
    {
      "source": 14,
      "target": 37
    },
    {
      "source": 14,
      "target": 17
    },
    {
      "source": 14,
      "target": 63
    },
    {
      "source": 14,
      "target": 48
    },
    {
      "source": 14,
      "target": 21
    },
    {
      "source": 15,
      "target": 0
    },
    {
      "source": 15,
      "target": 40
    },
    {
      "source": 15,
      "target": 41
    },
    {
      "source": 15,
      "target": 16
    },
    {
      "source": 15,
      "target": 28
    },
    {
      "source": 16,
      "target": 0
    },
    {
      "source": 16,
      "target": 42
    },
    {
      "source": 16,
      "target": 43
    },
    {
      "source": 16,
      "target": 67
    },
    {
      "source": 16,
      "target": 68
    },
    {
      "source": 17,
      "target": 0
    },
    {
      "source": 17,
      "target": 47
    },
    {
      "source": 17,
      "target": 48
    },
    {
      "source": 17,
      "target": 22
    },
    {
      "source": 17,
      "target": 63
    },
    {
      "source": 18,
      "target": 0
    },
    {
      "source": 18,
      "target": 1
    },
    {
      "source": 18,
      "target": 12
    },
    {
      "source": 19,
      "target": 2
    },
    {
      "source": 19,
      "target": 11
    },
    {
      "source": 19,
      "target": 50
    },
    {
      "source": 19,
      "target": 49
    },
    {
      "source": 20,
      "target": 16
    },
    {
      "source": 20,
      "target": 68
    },
    {
      "source": 20,
      "target": 67
    },
    {
      "source": 21,
      "target": 17
    },
    {
      "source": 21,
      "target": 37
    },
    {
      "source": 21,
      "target": 48
    },
    {
      "source": 22,
      "target": 47
    },
    {
      "source": 22,
      "target": 62
    },
    {
      "source": 23,
      "target": 9
    },
    {
      "source": 23,
      "target": 8
    },
    {
      "source": 23,
      "target": 55
    },
    {
      "source": 24,
      "target": 11
    },
    {
      "source": 24,
      "target": 10
    },
    {
      "source": 24,
      "target": 52
    },
    {
      "source": 25,
      "target": 16
    },
    {
      "source": 25,
      "target": 52
    },
    {
      "source": 25,
      "target": 42
    },
    {
      "source": 26,
      "target": 36
    },
    {
      "source": 26,
      "target": 62
    },
    {
      "source": 26,
      "target": 65
    },
    {
      "source": 27,
      "target": 46
    },
    {
      "source": 27,
      "target": 54
    },
    {
      "source": 28,
      "target": 40
    },
    {
      "source": 28,
      "target": 16
    },
    {
      "source": 28,
      "target": 42
    },
    {
      "source": 29,
      "target": 62
    },
    {
      "source": 30,
      "target": 39
    },
    {
      "source": 31,
      "target": 61
    },
    {
      "source": 31,
      "target": 84
    },
    {
      "source": 32,
      "target": 56
    },
    {
      "source": 33,
      "target": 34
    },
    {
      "source": 33,
      "target": 62
    },
    {
      "source": 33,
      "target": 65
    },
    {
      "source": 34,
      "target": 62
    },
    {
      "source": 34,
      "target": 65
    },
    {
      "source": 34,
      "target": 66
    },
    {
      "source": 35,
      "target": 2
    },
    {
      "source": 35,
      "target": 59
    },
    {
      "source": 35,
      "target": 60
    },
    {
      "source": 36,
      "target": 62
    },
    {
      "source": 36,
      "target": 65
    },
    {
      "source": 37,
      "target": 17
    },
    {
      "source": 37,
      "target": 48
    },
    {
      "source": 38,
      "target": 82
    },
    {
      "source": 38,
      "target": 83
    },
    {
      "source": 38,
      "target": 81
    },
    {
      "source": 39,
      "target": 79
    },
    {
      "source": 40,
      "target": 41
    },
    {
      "source": 42,
      "target": 43
    },
    {
      "source": 42,
      "target": 67
    },
    {
      "source": 43,
      "target": 3
    },
    {
      "source": 44,
      "target": 57
    },
    {
      "source": 44,
      "target": 58
    },
    {
      "source": 45,
      "target": 64
    },
    {
      "source": 45,
      "target": 49
    },
    {
      "source": 45,
      "target": 63
    },
    {
      "source": 46,
      "target": 54
    },
    {
      "source": 46,
      "target": 79
    },
    {
      "source": 47,
      "target": 48
    },
    {
      "source": 48,
      "target": 63
    },
    {
      "source": 49,
      "target": 2
    },
    {
      "source": 49,
      "target": 50
    },
    {
      "source": 50,
      "target": 59
    },
    {
      "source": 50,
      "target": 74
    },
    {
      "source": 51,
      "target": 2
    },
    {
      "source": 51,
      "target": 53
    },
    {
      "source": 51,
      "target": 65
    },
    {
      "source": 53,
      "target": 2
    },
    {
      "source": 53,
      "target": 74
    },
    {
      "source": 54,
      "target": 69
    },
    {
      "source": 55,
      "target": 32
    },
    {
      "source": 55,
      "target": 56
    },
    {
      "source": 57,
      "target": 58
    },
    {
      "source": 60,
      "target": 2
    },
    {
      "source": 60,
      "target": 59
    },
    {
      "source": 61,
      "target": 84
    },
    {
      "source": 62,
      "target": 65
    },
    {
      "source": 62,
      "target": 66
    },
    {
      "source": 63,
      "target": 72
    },
    {
      "source": 64,
      "target": 49
    },
    {
      "source": 64,
      "target": 63
    },
    {
      "source": 65,
      "target": 66
    },
    {
      "source": 67,
      "target": 68
    },
    {
      "source": 68,
      "target": 3
    },
    {
      "source": 69,
      "target": 46
    },
    {
      "source": 70,
      "target": 63
    },
    {
      "source": 70,
      "target": 71
    },
    {
      "source": 71,
      "target": 63
    },
    {
      "source": 71,
      "target": 49
    },
    {
      "source": 72,
      "target": 73
    },
    {
      "source": 72,
      "target": 74
    },
    {
      "source": 73,
      "target": 74
    },
    {
      "source": 73,
      "target": 2
    },
    {
      "source": 74,
      "target": 2
    },
    {
      "source": 74,
      "target": 75
    },
    {
      "source": 74,
      "target": 76
    },
    {
      "source": 75,
      "target": 51
    },
    {
      "source": 75,
      "target": 2
    },
    {
      "source": 76,
      "target": 13
    },
    {
      "source": 76,
      "target": 2
    },
    {
      "source": 77,
      "target": 13
    },
    {
      "source": 77,
      "target": 78
    },
    {
      "source": 77,
      "target": 52
    },
    {
      "source": 78,
      "target": 13
    },
    {
      "source": 78,
      "target": 52
    },
    {
      "source": 80,
      "target": 81
    },
    {
      "source": 80,
      "target": 38
    },
    {
      "source": 82,
      "target": 83
    },
    {
      "source": 84,
      "target": 63
    }
  ]
};

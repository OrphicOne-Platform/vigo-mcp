# VIGO — The First MCP Server for Financial Regulatory Intelligence

> **Regulatory Intelligence Expert · Bilingual AI Agent for Hong Kong SFC Regulations**
> 
> *By [OrphicOne](https://orphicone.com) · English & 繁體中文 · Continuously Updated Knowledge Base*

---

## What is VIGO?

**VIGO** (遠見 · 洞察 · 治理 · 優化) is a specialized financial regulatory intelligence AI agent — and the industry's first MCP server dedicated to financial regulatory intelligence in any jurisdiction.

At its core, VIGO is a **regulatory intelligence expert**: deeply versed in Hong Kong SFC regulations, enforcement history, licensing requirements, and AML/CFT rules. But VIGO is more than a compliance encyclopedia. It is a **business-aware compliance navigator** — an AI that understands how compliance intersects with business strategy, capital structures, and market reality.

> *Compliance is the floor. Business is the ceiling.*
> *VIGO helps you build both.*

### V.I.G.O. — The Four Dimensions

| | Dimension | 中文 | Capability |
|---|---|---|---|
| **V** | **Visionary** | 遠見 | Capital path planning — IPO structures (18A/18C, SPAC), market positioning |
| **I** | **Insight** | 洞察 | Architecture design — Red-chip, VIE, LPF, OFC, SPC structures |
| **G** | **Governance** | 治理 | Regulatory mastery — SFC licensing (Type 1-13), FRR, AML/CTF |
| **O** | **Optimization** | 優化 | Cost-effective solutions — market pricing, talent policy, ROI |

### Why VIGO instead of asking Claude/ChatGPT directly?

| | General AI | VIGO |
|---|---|---|
| **Data** | Frozen at training cutoff | Continuously updated — daily SFC sync + weekly HKMA/HKEX + monthly industry scan |
| **Accuracy** | Approximate, details often wrong | Precise — based on original regulatory documents with three-tier verification |
| **Sources** | None | Every answer includes official SFC document links with authority scores |
| **Depth** | Overview-level | Exam papers, exemptions, capital rules, enforcement details, fee benchmarks |
| **Enforcement** | Almost none | Searchable fines, bans, suspensions — 28 structured enforcement records |
| **Perspective** | Generic | Connects compliance requirements to business value (Iceberg Strategy) |
| **Quality** | No quality signals | Three-tier verification: GOLD (65%) / SILVER (35%) — World-Class metrics |
| **Chinese** | Generic translation | Professional regulatory terminology (繁體中文) |
| **Intelligence** | Static | Dual-model routing, 9-type query classification, self-correction engine |

> *Asking ChatGPT about SFC regulations is like asking a smart friend — they roughly know. Asking VIGO is like consulting a senior compliance partner who knows every circular, every enforcement action, every licensing nuance, and always connects compliance back to your business objectives.*

---

## Quick Start

### Claude (Web, Desktop, Mobile)

**Settings → Connectors → Add custom connector** → paste:

```
https://lsoatzzwpltpydwyfqqv.supabase.co/functions/v1/vigo-mcp
```

Claude will automatically invoke VIGO when you ask SFC compliance questions.

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "vigo": {
      "type": "streamableHttp",
      "url": "https://lsoatzzwpltpydwyfqqv.supabase.co/functions/v1/vigo-mcp"
    }
  }
}
```

### VS Code

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "vigo": {
      "type": "streamableHttp",
      "url": "https://lsoatzzwpltpydwyfqqv.supabase.co/functions/v1/vigo-mcp"
    }
  }
}
```

### Claude Code

```bash
claude mcp add --transport http vigo https://lsoatzzwpltpydwyfqqv.supabase.co/functions/v1/vigo-mcp
```

### ChatGPT Desktop

```json
{
  "mcpServers": {
    "vigo": {
      "url": "https://lsoatzzwpltpydwyfqqv.supabase.co/functions/v1/vigo-mcp"
    }
  }
}
```

---

## Tools

VIGO provides 6 tools (4 read-only query tools + 2 analytical tools):

### `query_regulation`

Ask any question about SFC regulations. Covers all license types, VATP/ASPIRe framework, AML/CFT, exams, CPD/CPT, and more. Bilingual — responds in whatever language you ask.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `question` | Yes | Your regulatory question |
| `language` | No | `"en"`, `"zh"`, or `"auto"` (default) |
| `license_type` | No | Filter: `"Type 1"` through `"Type 13"` |

### `search_enforcement`

Search SFC enforcement actions — fines, suspensions, bans, and prosecutions.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | Yes | Company name, person, or violation type |
| `year` | No | Filter by year (e.g. `2025`) |

### `get_license_guide`

Comprehensive guide for any SFC license type: exams, capital, fit-and-proper, CPD.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `license_type` | Yes | `"Type 1"` through `"Type 13"` |
| `aspect` | No | `"overview"`, `"exam"`, `"capital"`, `"fit_and_proper"` |

### `latest_updates`

Latest SFC regulatory updates: circulars, enforcement, VATP developments, consultations.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `category` | No | `"circular"`, `"enforcement"`, `"vatp"`, `"consultation"`, `"all"` |
| `count` | No | Number of results, 1–10 (default: 5) |

### `compliance_check`

Perform a compliance health check for a licensed corporation. Input company profile, get a multi-dimensional compliance risk assessment.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `license_types` | Yes | License types held, e.g. `["Type 1", "Type 9"]` |
| `num_ros` | No | Number of Responsible Officers |
| `num_staff` | No | Total number of staff |
| `aum` | No | Assets under management, e.g. `"500M HKD"` |
| `business_areas` | No | Business areas, e.g. `["securities dealing", "asset management"]` |
| `has_vatp` | No | Whether the firm deals with virtual assets |

### `risk_assessment`

Assess compliance risk of a planned business activity. Returns Red/Yellow/Green risk rating with regulatory basis and recommended actions.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `description` | Yes | Description of the planned business activity |
| `license_types` | No | Relevant license types |
| `urgency` | No | `"immediate"`, `"planned"`, `"exploratory"` |

---

## Example Queries

**Licensing & Exams**
```
What exams do I need for an SFC Type 9 (Asset Management) license?
→ Complete exam structure, pass marks, exemption conditions, official links
```

**Enforcement Intelligence**
```
Search for SFC enforcement actions related to AML in 2025
→ Matching cases with companies, penalties, regulatory basis, official notices
```

**Bilingual Regulatory Updates**
```
SFC最新的通函和監管動態是什麼？
→ 最新通函列表，含參考編號、日期、主題、官方文件鏈接（繁體中文）
```

**Compliance Health Check**
```
Run a compliance check for a Type 1 + Type 9 firm with 3 ROs, 25 staff, 2B HKD AUM
→ FRR capital assessment, RO configuration review, regulatory focus areas
```

**Risk Assessment**
```
We want to launch a tokenized fund product for retail investors in Hong Kong
→ Red/Yellow/Green rating, regulatory basis, recommended actions, timeline
```

**Fee & Market Intelligence**
```
What are the current RO retainer fees and shell company prices?
→ Structured fee benchmarks from vigo_fee_benchmarks with latest market data
```

---

## Knowledge Base

VIGO's intelligence is powered by a structured, continuously updated knowledge base with **6,381 verified knowledge chunks** covering 26 years of SFC regulatory history:

### Data Sources

**Official Sources (6 endpoints + HKMA)**
- SFC Circulars, Enforcement News, Consultation Papers
- VATP/Virtual Asset regulatory updates
- Press Releases and policy announcements
- HKMA Joint Circulars (auto-filtered for SFC-relevant content)

**Foundational Documents (35 + 5 Thematic Reports)**
- 12 Codes + 16 Guidelines + 3 Laws (SFO, SFF, AMLO) + 2 Handbooks + 2 HKEX Listing Rules
- 5 SFC Thematic Inspection Reports (Cybersecurity, Sponsor Business, Prime Services, Securities Margin Financing, Alternative Liquidity Pools)

**Industry Intelligence (17 sources)**
- International Law Firms (6): Charltons, Deacons, KWM, Sidley Austin, Linklaters, Clifford Chance
- Local Law Firms (3): ONC Lawyers, Stevenson Wong, Paradox Management
- Big 4 (4): Deloitte HK, PwC HK, EY HK, KPMG HK
- Compliance Consultants (2): CompliancePlus, Waystone
- Compliance Tech (2): Heinbro, BBCIncorp

### v7.0 Structured Data (76 records)

| Table | Records | Content |
|-------|---------|---------|
| `vigo_enforcement` | 28 | Structured enforcement records (entity, violations, penalties, bans) |
| `vigo_regulations` | 21 | Structured regulation documents (categories, effective dates, requirements) |
| `vigo_fee_benchmarks` | 25 | Fee benchmarks (RO retainers, SFC fees, application costs) |
| `vigo_license_market` | 2 | License market pricing (shell prices, transaction data) |

### Coverage

- All SFC license types (Type 1–13) and VATP licensing
- AML/CFT guidelines and enforcement case history
- Exam requirements, CPD/CPT rules, fit-and-proper criteria
- FRR capital requirements and operational compliance
- HKEX Main Board and GEM Listing Rules
- Cross-border: Stock Connect, MRF Fund Mutual Recognition, WMC

### Quality Assurance

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Duplication rate | ≤ 2% | 1.0% | ✅ World-Class |
| GOLD verification rate | ≥ 60% | 64.8% (4,155 records) | ✅ World-Class |
| Freshness score | ≥ 0.95 | 0.987 | ✅ World-Class |
| Authority score | ≥ 80 | 85.6 | ✅ World-Class |
| Recall@5 | ≥ 70% | 80% | ✅ World-Class |
| MRR | ≥ 0.700 | 0.800 | ✅ World-Class |

**Verification Grading**
- 🥇 **GOLD** (authority ≥ 90): 4,155 records (65%) — SFC official, HKMA, HKEX
- 🥈 **SILVER** (authority ≥ 65): 2,226 records (35%) — Law firms, Big 4, consultants
- 🥉 **BRONZE** (authority < 65): 0 records

**Quality Framework**
- Three-layer deduplication: L1 ref_id exact match → L2 SHA-256 content hash → L3 semantic similarity > 0.92
- Six-point content validation on every chunk before upload
- Five-tier authority scoring: Primary legislation (100) → Senior speeches/Big 4 (80-90) → Specialist firms (68-75) → Brokers/media (50-55) → Social/AI (5-25)
- Bilingual: every entry exists in English and Traditional Chinese

---

## v7.0 Intelligent Engine

### Six-Layer Retrieval Pipeline

```
Query → [Layer 1] Query Router (9 route types)
      → [Layer 2] Hybrid Retrieval (Dense cosine@0.25 top20 + BM25 sparse top15)
      → [Layer 3] RRF Fusion (K=60, structured results get 1.5× boost)
      → [Layer 4] Score Fusion (rerank×0.50 + verification×0.20 + freshness + authority)
      → [Layer 5] Diversity Filter (min 3 sources, max 2 per source, cross-contamination penalty)
      → [Layer 6] Dynamic TopK (6-8 results based on query complexity)
      → Answer with citations
```

### Dual-Model Routing

| Model | Use Case | Trigger |
|-------|----------|---------|
| GPT-4o-mini | Fast lookups, simple facts | capital_requirement / fee_benchmark / enforcement_lookup / license_market |
| DeepSeek Chat | Deep analysis, regulatory interpretation | comparison / how_to / general / latest_update |

Built-in fallback: if GPT-4o-mini fails → auto-switch to DeepSeek.

### 9 Query Route Types

Each route type has optimised search weights (freshness, authority) and strategy (structured_lookup / semantic / multi_query / hybrid):

`capital_requirement` · `license_market` · `enforcement_lookup` · `fee_benchmark` · `latest_update` · `comparison` · `how_to` · `general` · `unknown`

### Six-Layer Anti-Hallucination

1. **LICENSE_TYPE_MAP hardcoded** — all SFC exam subjects verified against HKSI website 2026
2. **System Prompt strict instructions** — never supplement specific numbers from training data
3. **Reranking filter** — demote non-matching license type documents
4. **Verification grade weighting** — GOLD > SILVER > BRONZE
5. **Cross-contamination penalty** — -0.05 for mismatched license documents
6. **Diversity filter** — force minimum 3 different sources

### Iceberg Strategy (Response Philosophy)

| Layer | Description | Role |
|-------|-------------|------|
| Step 1: Direct Answer | Clear numbers, legal provisions, processes | Compliance Officer |
| Step 2: Market Calibration | Reference latest market data and fee benchmarks | Analyst |
| Step 3: Strategic Extension | "From an Optimization perspective, also consider..." | Architect |

---

## Autonomous Operations

v7.0 achieves fully autonomous operations with zero manual intervention:

### pg_cron Scheduled Tasks (4)

| Task | Schedule | Function |
|------|----------|----------|
| Daily freshness update | `0 3 * * *` | Recalculate freshness_score |
| Weekly duplicate detection | `0 4 * * 0` | Flag is_duplicate |
| Monthly statistics | `0 5 1 * *` | Update vigo_stats |
| Quarterly cleanup | `0 6 1 1,4,7,10 *` | Clean expired memory |

### GitHub Actions Three-Tier Scheduling

| Workflow | Schedule | Tasks | Duration |
|----------|----------|-------|----------|
| `vigo-daily.yml` | Sun-Thu 23:00 UTC | Mode 1 daily sync + Mode 14a conflict detection | ~16 min |
| `vigo-weekly.yml` | Sun 00:00 UTC | Mode 13e data quality + Mode 14e full inspection | ~45 min |
| `vigo-monthly.yml` | 15th 00:00 UTC | Mode 6+9+13e+12e+11a comprehensive maintenance | ~60 min |

Monthly GitHub Actions usage: ~350 minutes (well within free tier of 2,000 minutes).

### Collection Pipeline

`auto_collect_upload.py` v7.0.3 (6,292 lines) supports 14+ modes:

| Mode | Function | Frequency |
|------|----------|-----------|
| Mode 1 | SFC latest updates (6 official endpoints + HKMA) | Daily (auto) |
| Mode 2 | Historical deep scan (1m/3m/6m/1y) | Quarterly |
| Mode 3 | Local PDF import | On-demand |
| Mode 4 | Practical experience import (16 templates) | Ongoing |
| Mode 5 | Foundational documents import + health check | Monthly |
| Mode 6 | Industry intelligence scan (17 sources) | Monthly (auto) |
| Mode 7 | Universal file importer (PDF/DOCX/XLSX/TXT/MD) | On-demand |
| Mode 8 | Database management | Monthly |
| Mode 9 | Knowledge base update | Monthly (auto) |
| Mode 11 | Evaluation benchmark (50 questions) | Monthly (auto) |
| Mode 12 | Structured data extraction → 4 tables | Monthly (auto) |
| Mode 13 | Data quality engine — full scan + repair | Weekly (auto) |
| Mode 14 | Self-correction engine — conflict detection + inspection | Daily/Weekly (auto) |

---

## Architecture

```
┌─────────────────────────────────────────────┐
│  MCP Clients                                │
│  Claude · ChatGPT · Cursor · VS Code       │
│  Claude Code · Any MCP Client               │
└──────────────────┬──────────────────────────┘
                   │ MCP Protocol (Streamable HTTP)
                   ▼
┌─────────────────────────────────────────────┐
│  VIGO MCP Server v2.1 (6 tools, 582 lines) │
│  Supabase Edge Function (Deno TypeScript)   │
└──────────────────┬──────────────────────────┘
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
 OpenAI        Supabase       DeepSeek + GPT-4o-mini
 Embeddings    PostgreSQL     Dual-Model Routing
 (1536-dim)    pgvector       (with auto-fallback)
               + BM25 FTS

┌─────────────────────────────────────────────┐
│  vigo-chat v5.2 (1,032 lines)               │
│  Query Router (9 types) → Hybrid Retrieval  │
│  → RRF Fusion → Score Fusion → Diversity    │
│  → Dual-Model → Engram Memory → Response    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  vigo-ingest v6.1.2 (458 lines)             │
│  Auto-classify → Semantic chunk → Verify    │
│  → Grade (GOLD/SILVER/BRONZE) → Store       │
│  → Auto-generate quick questions             │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│  Autonomous Operations                      │
│  pg_cron (4 tasks) + GitHub Actions (3)     │
│  auto_collect_upload.py v7.0.3 (6,292 lines)│
│  14+ modes · Fully autonomous · Zero manual │
└─────────────────────────────────────────────┘
```

### Edge Functions

| Function | Version | Lines | Purpose |
|----------|---------|-------|---------|
| `vigo-chat` | v5.2 | 1,032 | Main API: query → embedding → hybrid retrieval → dual-model routing → answer |
| `vigo-mcp` | v2.1 | 582 | MCP server: 6 tools, Streamable HTTP, authority-weighted post-processing |
| `vigo-ingest` | v6.1.2 | 458 | Intelligent ingest: filter → classify → deduplicate → verify → extract |
| `vigo-quick-questions` | v1.0 | 143 | Personalised follow-up question recommendations via Engram |

### Database

| Table | Purpose |
|-------|---------|
| `vigo_knowledge` | 6,381 knowledge chunks with embeddings (vector 1536), authority scores, verification grades |
| `vigo_enforcement` | 28 structured enforcement records |
| `vigo_regulations` | 21 structured regulation documents |
| `vigo_fee_benchmarks` | 25 fee benchmark records |
| `vigo_license_market` | 2 license market pricing records |
| `vigo_conversation_memory` | Engram: conversation history with semantic vectors |
| `vigo_user_preferences` | Engram: user language and interest preferences |
| `vigo_learning_progress` | Engram: topic understanding levels |

**Transport**: Streamable HTTP (MCP standard)  
**Authentication**: None required  
**Runtime**: Supabase Edge Functions (Deno TypeScript)  

> **Note**: The MCP server is the open, stateless interface for any AI client. On the OrphicOne platform, VIGO also integrates **Engram** — a long-term memory system that stores conversation history, tracks user preferences, and adapts responses based on learning progress. Engram uses semantic retrieval (vector similarity) over past dialogues to deliver increasingly personalised compliance guidance over time.

---

## Distribution

| Channel | Status | Notes |
|---------|--------|-------|
| MCP Official Registry | ✅ Active | Core channel, auto-synced by downstream platforms |
| Smithery | ✅ Published | All 6 tools recognised |
| Glama | ✅ Listed | Connector verification passed |
| Anthropic Connectors | ✅ Live | Highest traffic channel |
| PulseMCP | ⏳ Auto-syncing | Pulls from Registry |
| `.well-known` | ✅ Configured | Supports auto-discovery |

---

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| **v7.0** | 2026-02-24 | Sprint 1-4 (structured extraction + quality engine + self-correction + evaluation benchmarks), autonomous ops (pg_cron + GitHub Actions), dual-model routing, 6,292 lines |
| v6.0 | 2026-02-23 | Six-layer intelligent retrieval, three-tier verification, hybrid search, vigo-ingest, reference engine, 4,547 lines |
| v5.1 | 2026-02-21 | AI RO reasoning framework, compliance_check, risk_assessment, MCP tools 4→6 |
| v5.0 | 2026-02-20 | Quality assurance framework, three-layer dedup, six-point validation, 35 foundational docs |
| v3.2 | 2026-02-03 | Architecture upgrade: DeepSeek/OpenAI direct connection, 50%+ latency reduction |
| v3.0 | 2026-02-03 | Anti-hallucination System Prompt + reranking filter |
| v2.0 | 2026-01-31 | Engram memory system full integration |
| v1.0 | 2026-01-29 | Initial release: basic RAG functionality |

---

## About

**[OrphicOne](https://orphicone.com)** is a Hong Kong-based regulatory intelligence platform for financial services.

**VIGO** is OrphicOne's AI-powered regulatory intelligence agent — the industry's first and currently only MCP server dedicated to financial regulatory intelligence in any jurisdiction.

### Positioning

Among 16,000+ MCP servers globally, VIGO occupies a unique position:

```
Global MCP Ecosystem (16,000+ servers)
├── Developer Tools        ████████████████  thousands
├── Productivity           ██████████        hundreds
├── Data & Analytics       ████████          hundreds
├── Financial Reg Intelligence █                 VIGO (only one)
└── HK SFC Reg Intelligence    █                 VIGO (industry first)
```

### Data Moat

- **26 years** of SFC regulatory history (2000–2026)
- **6,381 verified knowledge chunks** with three-tier quality grading
- **76 structured records** across 4 specialised tables (enforcement, regulations, fees, market)
- **35 foundational documents** + 5 thematic inspection reports
- **17 industry sources** crawled monthly with sub-page extraction
- **HKMA joint circulars** + **HKEX listing rules** cross-referenced
- **Three-layer deduplication** + six-point content validation
- **v7.0 intelligent engine** with dual-model routing, self-correction, and autonomous operations
- **World-Class benchmarks**: Recall@5 80%, MRR 0.800, duplication 1.0%, GOLD rate 64.8%
- Knowledge that took years of domain expertise to curate — not easily replicated

### Philosophy

VIGO is built on the belief that **compliance is not a cost — it is a competitive advantage**. Great compliance doesn't slow business down; it provides the foundation for sustainable growth, client trust, and market credibility.

> *Compliance is the floor (The Floor), ensuring safety.*
> *Business is the ceiling (The Ceiling), achieving breakthroughs.*
> *Grounded in compliance, fluent in capital. Compliance as shield, business as spear.*

---

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | SFC compliance — all license types, enforcement, VATP, v7 engine, 35 foundational docs, 5 thematic reports, 17 industry sources, QA framework, autonomous ops, dual-model routing, structured data extraction | ✅ Live (v7.0) |
| **Phase 2** | Full HK regulatory coverage (HKMA, IA, MPFA) | Planned (2026) |
| **Phase 3** | Cross-border Asia-Pacific (Singapore MAS, Dubai VARA) | Future (2027) |
| **Phase 4** | Global digital asset regulatory intelligence | Vision (2028+) |

---

## Privacy

VIGO is a read-only regulatory intelligence service. We do not collect personal information, store conversation data, or require authentication. All query tools are marked `readOnlyHint: true`. See our [Privacy Policy](https://orphicone.com/privacy).

> VIGO provides regulatory information query services only and does not constitute legal or financial advice. Users should treat VIGO's answers as reference and consult professional compliance advisors or lawyers when necessary.

## Support

- Email: contact@orphicone.com
- Issues: [GitHub Issues](https://github.com/OrphicOne-Platform/vigo-mcp/issues)
- Website: [orphicone.com](https://orphicone.com)

## License

MIT

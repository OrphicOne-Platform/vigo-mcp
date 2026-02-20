# VIGO — The First MCP Server for Financial Regulatory Intelligence

> **Regulatory Intelligence Expert · Bilingual AI Agent for Hong Kong SFC Regulations**
> 
> *By [OrphicOne](https://orphicone.com) · English & 繁體中文 · Continuously Updated Knowledge Base*

---

## What is VIGO?

**VIGO** (Visionary · Insight · Governance · Optimization) is a specialized financial regulatory intelligence AI agent — and the industry's first MCP server dedicated to financial regulatory intelligence in any jurisdiction.

At its core, VIGO is a **regulatory intelligence expert**: deeply versed in Hong Kong SFC regulations, enforcement history, licensing requirements, and AML/CFT rules. But VIGO is more than a compliance encyclopedia. It is a **business-aware compliance navigator** — an AI that understands how compliance intersects with business strategy, capital structures, and market reality.

> *Compliance is the floor. Business is the ceiling.*
> *VIGO helps you build both.*

### V.I.G.O. — The Four Dimensions

| | Dimension | Capability |
|---|---|---|
| **V** | **Visionary** (遠見) | Capital path planning — IPO structures, SPAC, market positioning |
| **I** | **Insight** (洞察) | Architecture design — Red-chip, VIE, LPF, OFC, SPC structures |
| **G** | **Governance** (治理) | Regulatory mastery — SFC licensing (Type 1-13), FRR, AML/CTF |
| **O** | **Optimization** (優化) | Cost-effective solutions — market pricing, talent policy, ROI |

### Why VIGO instead of asking Claude/ChatGPT directly?

| | General AI | VIGO |
|---|---|---|
| **Data** | Frozen at training cutoff | Continuously updated — weekly SFC/HKMA/HKEX sync + monthly industry scan |
| **Accuracy** | Approximate, details often wrong | Precise — based on original regulatory documents |
| **Sources** | None | Every answer includes official SFC document links |
| **Depth** | Overview-level | Exam papers, exemptions, capital rules, enforcement details |
| **Enforcement** | Almost none | Searchable fines, bans, suspensions by company/person/year |
| **Perspective** | Generic | Connects compliance requirements to business value |
| **Chinese** | Generic translation | Professional regulatory terminology (繁體中文) |

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

VIGO provides 4 read-only tools (all annotated with `readOnlyHint: true`):

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

**Complete License Guide**
```
Give me a complete guide for Type 1 (Dealing in Securities) license
→ Exam requirements, capital rules, fit-and-proper criteria, CPD obligations
```

**Capital Structure Advisory**
```
What are the compliance considerations for setting up an OFC in Hong Kong?
→ Regulatory requirements, SFC approval process, tax benefits, practical timeline
```

---

## Knowledge Base

VIGO's intelligence is powered by a structured, continuously updated knowledge base covering 26 years of SFC regulatory history:

**Official Sources (6 endpoints)**
- SFC Circulars, Enforcement News, Consultation Papers
- VATP/Virtual Asset regulatory updates
- Press Releases and policy announcements
- HKMA Joint Circulars (auto-filtered for SFC-relevant content)

**Foundational Documents (35 + 5 Thematic Reports)**
- 12 Codes + 16 Guidelines + 3 Laws + 2 Handbooks + 2 HKEX Listing Rules
- 5 SFC Thematic Inspection Reports (Cybersecurity, Sponsor Business, Prime Services, Securities Margin Financing, Alternative Liquidity Pools)

**Industry Intelligence (17 sources)**
- International Law Firms (6): Charltons, Deacons, KWM, Sidley Austin, Linklaters, Clifford Chance
- Local Law Firms (3): ONC Lawyers, Stevenson Wong, Paradox Management
- Big 4 (4): Deloitte HK, PwC HK, EY HK, KPMG HK
- Compliance Consultants (2): CompliancePlus, Waystone
- Compliance Tech (2): Heinbro, BBCIncorp

**Coverage**
- All SFC license types (Type 1–13) and VATP licensing
- AML/CFT guidelines and enforcement case history
- Exam requirements, CPD/CPT rules, fit-and-proper criteria
- FRR capital requirements and operational compliance
- HKEX Main Board and GEM Listing Rules

**Quality Assurance Framework**
- Three-layer deduplication: L1 ref_id exact match → L2 SHA-256 content hash → L3 semantic similarity
- Six-point content validation on every chunk before upload
- Source authority scoring: SFC official (100) > HKEX/HKMA (95) > Laws (90) > Thematic Reports (85) > Law firms (75) > Big 4 (70)
- Automated health checks with change detection for foundational documents

**Technical**
- Bilingual: every entry exists in English and Traditional Chinese
- Vector search via OpenAI `text-embedding-3-small` embeddings
- Official SFC document links embedded in every response

---

## Architecture

```
┌─────────────────────────────────────────┐
│  MCP Clients                            │
│  Claude · ChatGPT · Cursor · VS Code   │
│  Claude Code · Any MCP Client           │
└──────────────┬──────────────────────────┘
               │ MCP Protocol (Streamable HTTP)
               ▼
┌─────────────────────────────────────────┐
│  VIGO MCP Server                        │
│  Supabase Edge Function (Deno)          │
│  4 read-only tools                      │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
 OpenAI    Supabase    DeepSeek
 Embeddings  Vector DB   Chat API
```

**Transport**: Streamable HTTP (MCP standard)  
**Authentication**: None required  
**Runtime**: Supabase Edge Functions (Deno)  

> **Note**: The MCP server above is the open, stateless interface for any AI client. On the OrphicOne platform itself, VIGO also integrates **Engram** — a long-term memory system that stores conversation history, tracks user preferences, and adapts responses based on learning progress. Engram uses semantic retrieval (vector similarity) over past dialogues to deliver increasingly personalised compliance guidance over time.

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
- **35 foundational documents** + 5 thematic inspection reports
- **17 industry sources** crawled monthly with sub-page extraction
- **HKMA joint circulars** + **HKEX listing rules** cross-referenced
- **Three-layer deduplication** + six-point content validation
- Knowledge that took years of domain expertise to curate — not easily replicated

### Philosophy

VIGO is built on the belief that **compliance is not a cost — it is a competitive advantage**. Great compliance doesn't slow business down; it provides the foundation for sustainable growth, client trust, and market credibility.

---

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | SFC compliance — all license types, enforcement, VATP, 35 foundational docs, 5 thematic reports, HKMA joint circulars, HKEX listing rules, 17 industry sources, QA framework | ✅ Live (v5.0) |
| **Phase 2** | Full HK regulatory coverage (HKMA, IA, MPFA) | Planned |
| **Phase 3** | Cross-border Asia-Pacific (Singapore MAS, Dubai VARA) | Future |
| **Phase 4** | Global financial regulatory intelligence | Vision |

---

## Privacy

VIGO is a read-only regulatory intelligence service. We do not collect personal information, store conversation data, or require authentication. See our [Privacy Policy](https://orphicone.com/privacy).

## Support

- Email: contact@orphicone.com
- Issues: [GitHub Issues](https://github.com/365xbusiness/vigo-mcp/issues)
- Website: [orphicone.com](https://orphicone.com)

## License

MIT

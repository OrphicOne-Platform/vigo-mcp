# VIGO — Hong Kong's First SFC Compliance AI Agent

> **AI-powered Hong Kong Securities & Futures Commission regulatory intelligence, via MCP**
> 
> *By [OrphicOne](https://orphicone.com) · Bilingual (English & 繁體中文) · 1,250+ Structured Knowledge Entries*

---

## What is VIGO?

VIGO is a specialized compliance AI agent that provides instant, accurate answers to Hong Kong SFC regulatory questions — directly inside Claude, ChatGPT, Cursor, VS Code, or any MCP-compatible platform.

Unlike general-purpose AI that gives approximate answers from training data, VIGO draws from a **continuously updated, structured knowledge base** of 1,250+ entries sourced directly from official SFC publications. Every response includes official document links for professional verification.

### Why VIGO instead of asking Claude/ChatGPT directly?

| | General AI (Claude/ChatGPT) | VIGO |
|---|---|---|
| **Data freshness** | Frozen at training cutoff | Continuously updated from SFC sources |
| **Accuracy** | Directionally correct, details may be wrong | Precise, based on original SFC documents |
| **Source links** | None | Every answer includes official SFC links |
| **Depth** | Overview-level | Exam details, exemptions, capital, AML specifics |
| **Enforcement cases** | Almost none | Searchable fines, bans, suspensions |
| **Chinese quality** | Generic translation | Professional regulatory terminology |

> *Think of it this way: asking ChatGPT about SFC regulations is like asking a smart friend — they roughly know. Asking VIGO is like consulting a dedicated SFC compliance advisor who knows every circular, every enforcement action, and gives you the original source.*

---

## Quick Start

### Claude (Web, Desktop, Mobile)

**Settings → Connectors → Add custom connector** → paste the URL:

```
https://lsoatzzwpltpydwyfqqv.supabase.co/functions/v1/vigo-mcp
```

That's it. Claude will automatically invoke VIGO when you ask SFC compliance questions.

### Cursor

Settings → Features → MCP → Add Server, or add to `.cursor/mcp.json`:

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

Add to MCP settings:

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

Ask any question about SFC regulations. Covers all 12 license types, VATP/ASPIRe framework, AML/CFT, exams, CPD/CPT, and more.

**Bilingual**: Responds in whatever language you ask — English or Chinese.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `question` | Yes | Your regulatory question |
| `language` | No | `"en"`, `"zh"`, or `"auto"` (default) |
| `license_type` | No | Filter: `"Type 1"` through `"Type 12"` |

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
| `license_type` | Yes | `"Type 1"` through `"Type 12"` |
| `aspect` | No | `"overview"`, `"exam"`, `"capital"`, `"fit_and_proper"` |

### `latest_updates`

Latest SFC regulatory updates: circulars, enforcement, VATP developments, consultations.

| Parameter | Required | Description |
|-----------|----------|-------------|
| `category` | No | `"circular"`, `"enforcement"`, `"vatp"`, `"consultation"`, `"all"` |
| `count` | No | Number of results, 1-10 (default: 5) |

---

## Examples

### Licensing Exam Requirements

```
User: What exams do I need to pass for an SFC Type 9 (Asset Management) license?

VIGO returns:
- Complete exam structure: Paper 1, 6, 7, 12
- Pass marks, coverage areas, exemption conditions
- Link to SFC official exam requirements page
```

### Enforcement Search

```
User: Search for SFC enforcement actions related to anti-money laundering in 2025

VIGO returns:
- Matching enforcement cases with company names, penalties, dates
- Violation details and regulatory basis
- Links to official SFC enforcement notices
```

### Chinese Language Query

```
User: SFC最新的通函和監管動態是什麼？

VIGO returns:
- 最新通函列表，含參考編號、日期、主題
- 繁體中文專業術語
- 附帶SFC官方文件鏈接
```

### Complete License Guide

```
User: Give me a complete guide for Type 1 (Dealing in Securities) license

VIGO returns:
- Exam requirements and exemptions
- Minimum paid-up capital and liquid capital
- Fit-and-proper criteria for ROs and LRs
- CPD/CPT annual hour obligations
- Links to relevant SFC guidelines
```

---

## Knowledge Base

VIGO's intelligence comes from a structured, continuously updated knowledge base:

- **1,250+ entries** covering SFC regulatory content
- **Bilingual**: Every entry exists in both English and Traditional Chinese
- **6 official data sources**: SFC Circulars, Enforcement News, Consultations, VATP/Virtual Asset updates, Press Releases, and legal analyses
- **Coverage**: All 12 license types, VATP/ASPIRe framework, AML/CFT guidelines, enforcement case history, exam requirements, CPD/CPT rules, consultation papers
- **Official links**: Every response traces back to SFC source documents
- **Vector search**: OpenAI `text-embedding-3-small` embeddings for semantic matching

### Data Pipeline

Knowledge base updates are automated via [`auto_collect_upload.py`](auto_collect_upload.py):
1. Fetches latest content from 5 SFC API endpoints
2. Extracts text from PDF circulars (via `pdfplumber`)
3. Generates bilingual chunks (EN original + ZH translation)
4. Embeds official SFC document links in every entry
5. Uploads to Supabase vector database with embeddings

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
             1,250+
             entries
```

**Transport**: Streamable HTTP (MCP recommended standard)  
**Authentication**: None required (publicly accessible)  
**Runtime**: Supabase Edge Functions (Deno TypeScript)  
**Embedding Model**: OpenAI `text-embedding-3-small`  

---

## About

**[OrphicOne](https://orphicone.com)** is a Hong Kong-based cross-border digital asset regulatory intelligence platform.

**VIGO** (Vigilance · Interpretation · Guidance · Operations) is OrphicOne's AI compliance agent — the world's first and currently only MCP server dedicated to financial regulatory compliance in any jurisdiction.

Among 16,000+ MCP servers globally, VIGO is the only one covering financial regulatory compliance. In the Hong Kong SFC compliance space, it stands alone.

### Competitive Position

```
Global MCP Ecosystem (16,000+ servers)
├── Developer Tools        ████████████████  thousands
├── Productivity           ██████████        hundreds
├── Data & Analytics       ████████          hundreds
├── Financial Compliance   █                 VIGO (only one)
└── HK SFC Compliance      █                 VIGO (the first)
```

---

## Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 1** | SFC compliance — all 12 license types, enforcement, VATP | ✅ Live |
| **Phase 2** | Expand to full HK regulatory (HKMA, IA, MPFA) | Planned |
| **Phase 3** | Cross-border Asia-Pacific (Singapore MAS, Dubai VARA) | Future |
| **Phase 4** | Global digital asset regulatory intelligence | Vision |

---

## Privacy

VIGO is a read-only compliance intelligence service. We do not collect personal information, store conversation data, or require authentication. See our [Privacy Policy](https://orphicone.com/privacy).

## Support

- Email: contact@orphicone.com
- Issues: [GitHub Issues](https://github.com/orphicone/vigo-mcp/issues)
- Website: [orphicone.com](https://orphicone.com)

## License

MIT

# Azure DocumentDB in a Day

This is a full-day, hands-on workshop for Azure DocumentDB.

The scenario is simple: we are building a small mobile shopping assistant. You will load a mobile catalog into Azure DocumentDB, search it with normal queries, try full-text search, generate embeddings, run vector search, and finally place an AI agent on top of the same data.

The goal is to finish the day with a working setup and a clear understanding of where Azure DocumentDB fits in an application.

## If you are attending the workshop

Start with this file:

[WORKSHOP-RUNBOOK.md](WORKSHOP-RUNBOOK.md)

That runbook is written as the main attendee path. It includes the commands to copy, where to run them, and what output to expect.

Use the module README files when you want more explanation or when the instructor asks you to open a specific module.

## What we are building

During the workshop, you will build this flow:

```text
Mobile catalog data
  -> Azure DocumentDB
  -> full-text search and vector search
  -> Python tools
  -> AI agent in DevUI
```

By the end, you should be able to ask questions like:

```text
Recommend a phone under 50000 for camera and battery
```

or:

```text
Where can I buy OnePlus 12?
```

The agent will use Azure DocumentDB behind the scenes to find matching phones and retail offers.

## What you need before starting

You need these installed or available:

- An Azure subscription where you can create resources.
- VS Code.
- Python 3.10 or later.
- Git.
- MongoDB Shell (`mongosh`).
- Access to Azure AI Foundry or Azure OpenAI.

You will create or use:

- An Azure DocumentDB cluster.
- An embedding model deployment, usually `text-embedding-3-small`.
- A chat model deployment, usually `gpt-4.1-mini` or `gpt-4o-mini`.

For the vector search lab, use an Azure DocumentDB cluster tier that supports DiskANN. For this workshop, use **M30 or higher**.

## Full-day workshop agenda

| Time | Session | Focus |
|---|---|---|
| 09:30-10:15 | Slot 1 | Introduction and Azure DocumentDB overview |
| 10:15-11:15 | Hands-on Lab | Cluster setup and connectivity |
| 11:15-13:00 | Slot 2 | Data modeling, data import, querying, query planning, aggregation framework, and indexing |
| 13:00-13:30 | Break | Lunch break |
| 13:30-14:15 | Slot 3 | MongoDB to Azure DocumentDB migration |
| 14:15-15:15 | Hands-on Lab | Migration using VS Code extension and mongodump/mongorestore |
| 15:15-16:00 | Slot 4 | Search capabilities, AI workloads and agents, and RAG patterns |
| 16:00-17:00 | Hands-on Lab | Full-text search, vector search, hybrid search, and RAG patterns |
| 17:00-17:15 | Updates | MCP Server plus GitHub Copilot integration and latest updates |
| 17:15-17:30 | Close | Wrap-up and Q&A |

## Primary workshop modules

| Module | Folder | Purpose |
|---|---|---|
| 1 | [1-Introduction](1-Introduction/README.md) | Slot 1 overview and hands-on cluster setup plus connectivity |
| 2 | [2-NoSQL-Core-Concepts](2-NoSQL-Core-Concepts/README.md) | Slot 2 step-by-step data modeling, import, querying, aggregation, and indexing |
| 3 | [7-Migration](7-Migration/README.md) | Slot 3 migration path using assessment, offline, online, and cutover |
| 4 | [3-AI-Vector-Search](3-AI-Vector-Search/README.md) | Slot 4 search, vector, hybrid, and RAG patterns |
| 5 | [4-AI-Agents](4-AI-Agents/README.md) | Slot 4 AI workloads and agents on top of Azure DocumentDB |

## Extended modules (optional or post-workshop)

| Module | Folder | Purpose |
|---|---|---|
| 6 | [5-Performance-and-Cost-Optimization](5-Performance-and-Cost-Optimization/README.md) | Query tuning and cost optimization deep dive |
| 7 | [6-Security-RBAC](6-Security-RBAC/README.md) | RBAC, network security, and production security checks |

There is also an optional healthcare example under `Industry-solutions`. It is not part of the main 7-hour path.

## Folder guide

```text
.
├── WORKSHOP-RUNBOOK.md
├── 1-Introduction
├── 2-NoSQL-Core-Concepts
├── 7-Migration
├── 3-AI-Vector-Search
│   └── mobile-data
├── 4-AI-Agents
│   └── mobile-agents
├── 5-Performance-and-Cost-Optimization
├── 6-Security-RBAC
└── scripts
```

## Data used in the workshop

The main collections are:

| Collection | What it stores |
|---|---|
| `mobiles` | Mobile catalog, specifications, features, use cases, and embeddings |
| `retail_offers` | Retailer availability, price, and offer notes |

The setup script creates the required indexes for you:

- `mobile_text_index`
- `vector_index`
- `mobile_brand_index`
- `mobile_segment_index`
- `mobile_price_index`
- `offer_title_index`
- `offer_retailer_index`

## A note for first-time Azure users

Do not rush the setup section. Most issues in this workshop come from one of these:

- The DocumentDB cluster is still deploying.
- The current client IP was not added to the firewall.
- The connection string was copied incorrectly.
- The `.env` file was not saved.
- The Azure OpenAI deployment name in `.env` does not match the deployment name in AI Foundry.

If something fails, check those items first.

## Cleanup after the workshop

When you are done:

1. Stop the local Python app.
2. Delete or scale down workshop Azure resources you no longer need.
3. Remove temporary firewall rules.
4. Do not commit `.env`.
5. Rotate any keys that were shared during a live workshop.

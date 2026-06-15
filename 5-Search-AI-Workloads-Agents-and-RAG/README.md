# Module 5: Search Capabilities, AI Workloads, Agents and RAG Patterns

Duration: 15:15-17:30

This module covers Slot 4 topics end-to-end: full-text search, vector search, hybrid search, AI agents, RAG patterns, and MCP + GitHub Copilot integration updates.

## Learning outcomes

By the end of this module, you will be able to:

- Run full-text, vector, and filtered vector queries.
- Compare full-text and hybrid retrieval outcomes.
- Launch and test AI agents backed by Azure DocumentDB.
- Map retrieval flow to RAG patterns.
- Run MCP and GitHub Copilot update discussion tasks.

## Step-by-step hands-on

### Step 1: Validate search data and indexes

```powershell
python .\scripts\validate_workshop_setup.py
mongosh "<your_connection_string>"
```

```javascript
use Workshop_DB
db.mobiles.getIndexes()
db.support_articles.getIndexes()
```

### Step 2: Run full-text search

```javascript
db.mobiles.find(
  { $text: { $search: "camera phone battery 5G" } },
  {
    score: { $meta: "textScore" },
    title: 1,
    brand: 1,
    segment: 1,
    priceInr: 1,
    rating: 1,
    _id: 0
  }
).sort({ score: { $meta: "textScore" } }).limit(5)
```

### Step 3: Run vector search

Open `legacy-modules/3-AI-Vector-Search/mobile-data/query_embeddings.json`, copy one query embedding, then run:

```javascript
const queryVector = [/* paste embedding array here */]

db.mobiles.aggregate([
  {
    $search: {
      cosmosSearch: {
        vector: queryVector,
        path: "contentVector",
        k: 5
      }
    }
  },
  {
    $project: {
      title: 1,
      brand: 1,
      segment: 1,
      priceInr: 1,
      rating: 1,
      score: { $meta: "searchScore" },
      _id: 0
    }
  }
])
```

### Step 4: Run filtered semantic search

```javascript
db.mobiles.aggregate([
  {
    $search: {
      cosmosSearch: {
        vector: queryVector,
        path: "contentVector",
        k: 10,
        filter: { priceInr: { $lte: 50000 } }
      }
    }
  },
  {
    $project: {
      title: 1,
      brand: 1,
      priceInr: 1,
      rating: 1,
      score: { $meta: "searchScore" },
      _id: 0
    }
  }
])
```

### Step 5: Run full-text/vector/hybrid in support app

```powershell
python .\legacy-modules\3-AI-Vector-Search\support-search-app\app.py
```

Open `http://localhost:5050` and run the same query in:

1. Full-text
2. Vector
3. Hybrid

### Step 6: Launch AI agents

```powershell
cd .\legacy-modules\4-AI-Agents\mobile-agents
python app.py
```

Open `http://localhost:8080` and test:

- `Recommend a phone under 50000 for camera and battery`
- `Where can I buy OnePlus 12?`

### Step 7: RAG pattern walkthrough

Use retrieval flow:

```text
User question
  -> Embed query
  -> Retrieve top-k from Azure DocumentDB
  -> Apply filters
  -> Grounded answer generation
```

### Step 8: MCP + GitHub Copilot update segment

1. Review tool boundaries in `legacy-modules/4-AI-Agents/mobile-agents/mobile_tools.py`.
2. Use GitHub Copilot prompts for wrapper/test scaffolding.
3. Capture latest updates and action items.

## Expected result

You complete Slot 4 hands-on activities across search modes, agent workflows, and RAG mapping, then close with MCP + GitHub Copilot updates.

## Workshop close

1. Stop local apps.
2. Remove temporary firewall rules.
3. Keep credentials out of commits.
4. Follow cleanup guidance in `README.md`.

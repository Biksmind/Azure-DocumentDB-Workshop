# Module 4A: Search Capabilities and RAG Patterns

Duration: 15:15-16:00 (concepts) and 16:00-17:00 (hands-on)

Reference used for this module: `Azure-DocumentDB-Search-Vector-RAG-Self-Learning-Runbook.md`.

This module covers the search evolution in Azure DocumentDB:

1. Keyword search
2. Full-text search
3. Vector search
4. Hybrid search and RAG patterns

## Learning objectives

By the end of this module, you will be able to:

- Execute keyword, full-text, vector, and hybrid search patterns.
- Compare retrieval quality across search modes.
- Apply a basic retrieval-augmented generation (RAG) pattern.

## Step 1: Verify data and indexes

From repository root:

```powershell
python .\scripts\validate_workshop_setup.py
```

Then connect:

```powershell
mongosh "<paste DOCUMENTDB_CONNECTION_STRING here>"
```

Inside mongosh:

```javascript
use Workshop_DB
db.mobiles.countDocuments()
db.support_articles.countDocuments()
db.mobiles.getIndexes()
db.support_articles.getIndexes()
```

## Step 2: Keyword search baseline

```javascript
db.support_articles.find(
  {
    $or: [
      { content: /battery/i },
      { content: /update/i }
    ]
  },
  {
    _id: 0,
    articleId: 1,
    title: 1,
    category: 1,
    severity: 1
  }
).limit(5)
```

This search is literal and does not capture semantic similarity.

## Step 3: Full-text search

Mobile catalog full-text:

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

Support full-text:

```javascript
db.support_articles.find(
  { $text: { $search: "battery update" } },
  {
    score: { $meta: "textScore" },
    articleId: 1,
    title: 1,
    category: 1,
    severity: 1,
    _id: 0
  }
).sort({ score: { $meta: "textScore" } }).limit(5)
```

## Step 4: Vector search

Open and copy one embedding from:

- `3-AI-Vector-Search/mobile-data/query_embeddings.json`

Use this prompt embedding:

- `best camera phone for portraits and low light photography`

Then run:

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

## Step 5: Hybrid and filtered semantic search

Filtered vector query (semantic plus business constraint):

```javascript
db.mobiles.aggregate([
  {
    $search: {
      cosmosSearch: {
        vector: queryVector,
        path: "contentVector",
        k: 10,
        filter: {
          priceInr: { $lte: 50000 }
        }
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

Hybrid app demo (text + vector rerank):

```powershell
python .\3-AI-Vector-Search\support-search-app\app.py
```

Open `http://localhost:5050` and run the same query in these modes:

1. Full-text
2. Vector
3. Hybrid

Expected result: each mode returns different relevance characteristics for the same query.

## Step 6: RAG pattern mapping

Use this retrieval flow:

```text
User question
  -> Embed query
  -> Retrieve top-k context from Azure DocumentDB
  -> Apply filters (price, segment, severity)
  -> Send grounded context to LLM
  -> Return answer with product/article evidence
```

Practice RAG-oriented prompts:

1. `Suggest a phone under 50000 for low-light photography and long battery life.`
2. `My phone loses charge very fast after update. What should I check first?`
3. `Find gaming options with fast charging and good thermals.`

## Step 7: Compare search approaches

| Search mode | Best for | Typical limitation |
|---|---|---|
| Keyword | Exact terms and quick filters | Misses synonyms and rephrased intent |
| Full-text | Ranked keyword search | Limited semantic understanding |
| Vector | Meaning and intent match | Requires embedding workflow |
| Hybrid | Best balance of precision and recall | Slightly more complexity |

## Troubleshooting

- If `$text` fails, verify text index creation.
- If vector search fails, verify M30+ tier and vector dimensions.
- If hybrid app fails in vector mode, check Azure OpenAI settings in `.env`.

## Expected outcome

You can explain when to use keyword, full-text, vector, and hybrid retrieval in Azure DocumentDB, and you can implement a simple RAG retrieval flow.

## Next module

Continue to AI workloads and agents:

- [Module 4B: AI Agents](../4-AI-Agents/README.md)

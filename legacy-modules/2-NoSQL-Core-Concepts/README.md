# Module 2: Data Modeling, Import, Querying, Query Planning, Aggregation, and Indexing

Duration: 11:15-13:00

This Slot 2 core lab uses the mobile shopping scenario and prepares data for migration, search, and AI workloads.

## Prerequisites

- Complete [Module 1](../1-Introduction/README.md).
- Ensure `Workshop_DB` exists and network access is configured.
- Ensure Python dependencies are installed.

## Learning outcomes

By the end of this module, you will be able to:

- Model product and offer data as JSON documents.
- Import workshop data into Azure DocumentDB.
- Run filters, projections, sorts, updates, and aggregations.
- Read query plans with `explain("executionStats")`.
- Create indexes and verify index usage.

## Step 1: Verify environment

From the repository root:

```powershell
python .\scripts\validate_workshop_setup.py
```

If validation fails, return to Module 1 and resolve setup issues.

## Step 2: Connect with mongosh

```powershell
mongosh "<paste DOCUMENTDB_CONNECTION_STRING here>"
```

Inside mongosh:

```javascript
use Workshop_DB
db.runCommand({ ping: 1 })
```

## Step 3: Understand the document model

Inspect one mobile and one retail offer:

```javascript
db.mobiles.findOne({}, { _id: 0 })
db.retail_offers.findOne({}, { _id: 0 })
```

Review model choices:

- Mobile specifications are stored in one document for fast reads.
- Offers are in a separate collection to support one-to-many retailer records.
- Arrays like `features` and `useCases` support flexible search patterns.

## Step 4: Data import and validation

If data is not loaded yet, run in a separate PowerShell terminal:

```powershell
python .\scripts\load_workshop_data.py
python .\scripts\validate_workshop_setup.py
```

Then verify counts in mongosh:

```javascript
db.mobiles.countDocuments()
db.support_articles.countDocuments()
db.retail_offers.countDocuments()
```

Expected result: each collection returns a count of `30`.

## Step 5: Querying fundamentals

Run exact filter queries:

```javascript
db.mobiles.find(
	{ brand: "Samsung", priceInr: { $lte: 50000 } },
	{ _id: 0, title: 1, brand: 1, segment: 1, priceInr: 1, rating: 1 }
).sort({ rating: -1 }).limit(5)
```

Run array and range query:

```javascript
db.mobiles.find(
	{
		features: /camera/i,
		batteryMah: { $gte: 5000 }
	},
	{ _id: 0, title: 1, batteryMah: 1, features: 1 }
).limit(5)
```

## Step 6: Projection and update patterns

Projection pattern (return only required fields):

```javascript
db.mobiles.find(
	{ segment: "Premium" },
	{ _id: 0, title: 1, priceInr: 1, rating: 1 }
).limit(10)
```

Update example:

```javascript
db.mobiles.updateOne(
	{ title: "OnePlus 12" },
	{ $set: { workshopTag: "slot2-demo" } }
)

db.mobiles.find(
	{ title: "OnePlus 12" },
	{ _id: 0, title: 1, workshopTag: 1 }
)
```

Cleanup step:

```javascript
db.mobiles.updateOne(
	{ title: "OnePlus 12" },
	{ $unset: { workshopTag: "" } }
)
```

## Step 7: Aggregation framework

Average price by segment:

```javascript
db.mobiles.aggregate([
	{
		$group: {
			_id: "$segment",
			avgPrice: { $avg: "$priceInr" },
			avgRating: { $avg: "$rating" },
			count: { $sum: 1 }
		}
	},
	{ $sort: { avgPrice: 1 } }
])
```

Top brands by document count:

```javascript
db.mobiles.aggregate([
	{ $group: { _id: "$brand", count: { $sum: 1 } } },
	{ $sort: { count: -1, _id: 1 } }
])
```

## Step 8: Query planning with explain

Run explain before tuning:

```javascript
db.mobiles.find(
	{ brand: "Samsung", priceInr: { $lte: 50000 } }
).explain("executionStats")
```

In the output, review these fields:

- `winningPlan`
- `totalDocsExamined`
- `nReturned`
- `executionTimeMillis`

## Step 9: Indexing and re-check plan

Create a compound index for common browse filters:

```javascript
db.mobiles.createIndex(
	{ brand: 1, priceInr: 1 },
	{ name: "mobile_brand_price_idx" }
)
```

Run explain again:

```javascript
db.mobiles.find(
	{ brand: "Samsung", priceInr: { $lte: 50000 } }
).explain("executionStats")
```

Expected result: reduced document scans and index usage.

## Step 10: Practice exercises

1. Find top 5 phones under INR 40000 by rating.
2. Build an aggregation that groups by `segment` and returns max battery.
3. Compare explain output before and after adding an index on `segment`.
4. Query `retail_offers` for one retailer and sort by best discount.

## Module references

- [L100 NoSQL Fundamentals](L100_nosql_fundamentals.md)
- [L200 Schema Design Patterns](L200_schema_design_patterns.md)
- [L300 Data Relationships](L300_data_relationships.md)
- [Module 5 Performance Deep Dive](../5-Performance-and-Cost-Optimization/README.md)

## Next module

Continue to migration:

- [Module 3 (Slot 3): MongoDB to Azure DocumentDB Migration](../7-Migration/README.md)

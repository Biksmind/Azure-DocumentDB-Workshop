# Module 4: Migration to Azure DocumentDB

Duration: 13:30-15:15

This module covers migration using both the VS Code migration extension (DMS-based) and command-line migration with `mongodump` and `mongorestore`.

## Learning outcomes

By the end of this module, you will be able to:

- Run pre-migration assessment.
- Execute offline migration.
- Execute online migration and cutover.
- Validate migrated data.
- Run command-line migration path.

## Step-by-step hands-on

### Step 1: Connect source MongoDB in VS Code

1. Open DocumentDB extension in VS Code.
2. Add source MongoDB connection (provided by workshop team).
3. Confirm source appears in connection list.

### Step 2: Run pre-migration assessment

1. Right-click source cluster.
2. Select **Data Migration**.
3. Select **Pre-Migration Assessment for Azure DocumentDB**.
4. Run validation and review assessment report.

### Step 3: Run offline migration

1. Right-click source cluster and choose **Migrate to Azure DocumentDB**.
2. Select mode `Offline`.
3. Select target subscription, resource group, and Azure DocumentDB cluster.
4. Configure/reuse Azure DMS.
5. Complete firewall/database/collection selection.
6. Start migration and wait for `Succeeded`.

### Step 4: Validate offline migration

Connect to target and run:

```javascript
use <your_database_name>

db.getCollectionNames().forEach(function(c) {
  print(c + ": " + db.getCollection(c).countDocuments());
});
```

### Step 5: Run online migration and cutover

1. Start new migration with mode `Online`.
2. Reuse DMS.
3. Wait for `Ready To Cutover`.
4. Stop source writes/workload.
5. Trigger cutover.
6. Confirm final state `Succeeded`.

### Step 6: Command-line migration path

```powershell
mongodump --uri "<source_mongodb_connection_string>" --out .\dump
mongorestore --uri "<target_azure_documentdb_connection_string>" .\dump
```

Run count validation query again on target.

## Expected result

Migration is complete, data counts match, and target is validated for application use.

## Next module

Continue to:

- `../5-Search-AI-Workloads-Agents-and-RAG/README.md`

# Module 3: MongoDB to Azure DocumentDB Migration

Duration: 13:30-14:15 (concepts) and 14:15-15:15 (hands-on)

Reference used for this module:

- `https://github.com/Biksmind/DocumentDB_Workshop_0906/blob/main/MongoDB-to-Azure-DocumentDB-Migration-Workshop.md`

This module provides an end-to-end migration path by using the VS Code migration experience (DMS-based) and a command-line path with `mongodump` and `mongorestore`.

## Objectives

By the end of this module, you will:

- Run pre-migration assessment.
- Execute offline migration.
- Execute online migration and cutover.
- Validate data consistency.
- Perform a command-line migration using `mongodump` and `mongorestore`.

## Module outcome

After this module, you can execute and validate migration from MongoDB to Azure DocumentDB using both guided and command-line workflows.

## Prerequisites

- Source MongoDB connection details from the workshop facilitator.
- Target Azure DocumentDB cluster deployed and reachable.
- VS Code with DocumentDB extension installed.
- Azure DocumentDB Migration extension (install when prompted).
- `mongodump` and `mongorestore` available in your PATH.

## Track A: VS Code Migration Extension (DMS)

### Step 1: Connect to source MongoDB

1. Open VS Code.
2. Open the DocumentDB extension panel.
3. Add a MongoDB source connection using the workshop-provided source URI.
4. Verify the source cluster appears in the connection pane.

### Step 2: Run pre-migration assessment

1. Right-click the source MongoDB cluster.
2. Select `Data Migration`.
3. Choose `Pre-Migration Assessment for Azure DocumentDB`.
4. Run validation.
5. Enter assessment name and optional report/log paths.
6. Start assessment.
7. Review the report for compatibility findings and recommendations.

### Step 3: Run offline migration

1. Right-click source cluster and select `Migrate to Azure DocumentDB`.
2. In migration details, configure:
   - Migration mode: `Offline`
   - Network connectivity: `Public` (for workshop)
3. Select target subscription, resource group, and Azure DocumentDB cluster.
4. Configure or reuse Azure DMS.
5. Update firewall rules for source and target when prompted.
6. Select database(s) and collection(s).
7. Start migration and monitor until status is `Succeeded`.

### Step 4: Validate offline migration

Connect to target and run:

```javascript
use <your_database_name>

db.getCollectionNames().forEach(function(c) {
  print(c + ": " + db.getCollection(c).countDocuments());
});
```

Compare source and target counts.

Expected result: target collection counts align with source counts for selected databases.

### Step 5: Run online migration

1. Generate source workload (if workshop workload app is provided by instructor).
2. Create a new migration job with mode `Online`.
3. Reuse the same DMS instance.
4. Complete target/firewall/database/collection configuration.
5. Start migration and monitor state transitions:
   - `Provisioning`
   - `Bulk Copy In Progress`
   - `Replication In Progress`
   - `Ready To Cutover`

### Step 6: Perform cutover

1. Stop source workload generation.
2. Wait for pending replication to settle.
3. Click `Cutover`.
4. Confirm final migration status is `Succeeded`.

Expected result: migration job reaches `Succeeded` after cutover.

### Step 7: Post-cutover validation

Run the same collection-count validation against target.

Confirm:

- Collection counts match.
- No pending replication remains.
- Application can connect using Azure DocumentDB connection string.

## Track B: Command-line migration with mongodump/mongorestore

### Step 1: Export from source

```powershell
mongodump --uri "<source_mongodb_connection_string>" --out .\dump
```

### Step 2: Restore to Azure DocumentDB

```powershell
mongorestore --uri "<target_azure_documentdb_connection_string>" .\dump
```

### Step 3: Validate target counts

```powershell
mongosh "<target_azure_documentdb_connection_string>"
```

Then run:

```javascript
use <your_database_name>
db.getCollectionNames().forEach(function(c) {
  print(c + ": " + db.getCollection(c).countDocuments());
});
```

Expected result: restored collection counts match the export source.

## Recommended migration checklist

1. Run assessment first and review blockers.
2. Test offline migration in a non-production environment.
3. Use online migration for minimal downtime cutover.
4. Freeze writes before final cutover.
5. Validate data and application behavior after cutover.
6. Keep rollback plan and DNS/connection-string switch plan ready.

## Expected outcome

You complete an end-to-end MongoDB to Azure DocumentDB migration workflow, validate data consistency, and confirm application compatibility with minimal or no code changes.

## Next module

Continue to search, AI workloads, and RAG patterns:

- [Module 4A: Search and RAG](../3-AI-Vector-Search/README.md)
- [Module 4B: AI agents](../4-AI-Agents/README.md)

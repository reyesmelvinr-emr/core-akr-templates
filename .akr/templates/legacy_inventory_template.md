---
businessCapability: [BUSINESS_CAPABILITY_PASCALCASE]
feature: [FN12345_US678]
domain: [DOMAIN]
layer: Database
component: Legacy Inventory
status: investigation
version: 1.0
componentType: LegacyInventory
priority: P2
lastUpdated: [YYYY-MM-DD]
---

# Legacy Database Object Inventory

**Application**: [Application Name]  
**Database**: [Database Name]  
**Last Reviewed**: [YYYY-MM-DD]  
**Reviewed By**: ❓ [@team-member]

---

## Purpose

This document tracks database objects that are:
- Not modified in 3+ years
- Not clearly referenced by active application code
- Candidates for deprecation, archival, or removal

> ⚠️ **WARNING:** Do not delete objects without thorough investigation. Legacy objects may be used by external systems, scheduled jobs, reports, or have hidden dependencies.

---

## Summary Dashboard

| Status | Count | Description |
|--------|-------|-------------|
| 🔴 **Obsolete** | ❓ | Confirmed not in use, safe to remove |
| 🟡 **Investigate** | ❓ | Unknown usage, needs research |
| 🟢 **Keep** | ❓ | Legacy but required (dependency documented) |
| 📦 **Archived** | ❓ | Data preserved, object removed |
| **Total Legacy Objects** | ❓ | |

### Investigation Progress

| Phase | Status | Date |
|-------|--------|------|
| Initial inventory | ❓ ⬜ Not Started / 🔄 In Progress / ✅ Complete | ❓ |
| Code reference scan | ❓ | ❓ |
| External system check | ❓ | ❓ |
| Team knowledge capture | ❓ | ❓ |
| Final classification | ❓ | ❓ |

---

## Classification Criteria

### How to Classify Legacy Objects

| Question | 🔴 Obsolete | 🟡 Investigate | 🟢 Keep |
|----------|-------------|----------------|---------|
| Referenced in active code? | No | Unknown | Yes (legacy code) |
| Used by scheduled jobs? | No | Unknown | Yes |
| Used by external systems? | No | Unknown | Yes |
| Used by reports (SSRS, PowerBI)? | No | Unknown | Yes |
| Has foreign key dependencies? | No | Unknown | Yes |
| Created for one-time migration? | Yes | Maybe | No |
| Team member knows purpose? | No one | Some uncertainty | Yes, documented |

---

## Legacy Tables

| Table Name | Schema | Last Modified | Status | Created By | Purpose (if known) | Investigation Notes |
|------------|--------|---------------|--------|------------|-------------------|---------------------|
| 🤖 OldUserArchive | dbo | 2019-03 | 🔴 Obsolete | ❓ | Data migration backup | No FK refs, no code refs |
| 🤖 TempProcessing | dbo | 2020-11 | 🟡 Investigate | ❓ | Unknown | May be used by batch job |
| 🤖 BackupOrders_2018 | dbo | 2018-12 | 🔴 Obsolete | ❓ | One-time backup | Archive data, then remove |
| 🤖 LegacyCustomers | dbo | 2017-06 | 🟢 Keep | ❓ | Old CRM sync | Still used by Finance reports |
| ❓ | ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

---

## Legacy Views

| View Name | Schema | Last Modified | Status | Base Tables | Investigation Notes |
|-----------|--------|---------------|--------|-------------|---------------------|
| 🤖 vw_OldDashboard | dbo | 2019-06 | 🔴 Obsolete | Users, Orders | Dashboard retired 2020 |
| 🤖 vw_LegacyReport | dbo | 2018-02 | 🟡 Investigate | Multiple | Check with Finance |
| ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

---

## Legacy Stored Procedures

| Procedure Name | Schema | Last Modified | Status | Called By (if known) | Investigation Notes |
|----------------|--------|---------------|--------|---------------------|---------------------|
| 🤖 sp_OldReport | dbo | 2018-05 | 🔴 Obsolete | Legacy reporting app | Reports migrated to PowerBI |
| 🤖 sp_DataCleanup_v1 | dbo | 2019-08 | 🔴 Obsolete | Replaced by v2 | v2 is active, safe to remove |
| 🤖 sp_UnknownProcess | dbo | 2017-02 | 🟡 Investigate | Unknown | ❓ Who created this? |
| 🤖 sp_NightlyBatch | dbo | 2016-11 | 🟢 Keep | SQL Agent Job | Still runs nightly |
| ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

---

## Legacy Functions

| Function Name | Schema | Type | Last Modified | Status | Investigation Notes |
|---------------|--------|------|---------------|--------|---------------------|
| 🤖 fn_OldCalculation | dbo | Scalar | 2018-03 | 🟡 Investigate | Check stored procedures |
| ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

---

## Legacy Triggers

| Trigger Name | Table | Event | Last Modified | Status | Investigation Notes |
|--------------|-------|-------|---------------|--------|---------------------|
| 🤖 TR_OldAudit | Users | AFTER INSERT | 2017-09 | 🟡 Investigate | May be disabled |
| ❓ | ❓ | ❓ | ❓ | ❓ | ❓ |

---

## Investigation Checklist

> Use this checklist before removing ANY legacy object.

### Code Reference Check

```powershell
# Search for table/procedure name in codebase
grep -r "TableName" src/
grep -r "sp_ProcedureName" src/

# Search in configuration files
grep -r "TableName" *.json *.config *.xml

# Search in SQL files
grep -r "TableName" database/
```

- [ ] No references in application source code
- [ ] No references in configuration files
- [ ] No references in other SQL objects (views, procs)

### External System Check

- [ ] Not used by external APIs
- [ ] Not used by partner integrations
- [ ] Not used by data warehousing/ETL
- [ ] Not used by BI tools (PowerBI, SSRS, Tableau)

### Scheduled Job Check

```sql
-- SQL Server: Check SQL Agent jobs
SELECT j.name AS JobName, s.step_name, s.command
FROM msdb.dbo.sysjobs j
JOIN msdb.dbo.sysjobsteps s ON j.job_id = s.job_id
WHERE s.command LIKE '%ObjectName%';
```

- [ ] Not referenced by SQL Agent jobs
- [ ] Not referenced by Windows Task Scheduler
- [ ] Not referenced by Azure Functions/Logic Apps

### Dependency Check

```sql
-- SQL Server: Check foreign key dependencies
SELECT 
    fk.name AS FK_Name,
    tp.name AS Parent_Table,
    tr.name AS Referenced_Table
FROM sys.foreign_keys fk
JOIN sys.tables tp ON fk.parent_object_id = tp.object_id
JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id
WHERE tp.name = 'TableName' OR tr.name = 'TableName';

-- Check view dependencies
SELECT OBJECT_NAME(referencing_id) AS ReferencingObject
FROM sys.sql_expression_dependencies
WHERE referenced_entity_name = 'TableName';
```

- [ ] No foreign key references TO this table
- [ ] No foreign key references FROM this table
- [ ] Not used by any views
- [ ] Not used by any stored procedures

### Team Knowledge Check

- [ ] Asked developers who've been here 3+ years
- [ ] Checked with DBA or data team
- [ ] Reviewed with business stakeholders
- [ ] Documented in this file

---

## Removal Process

### Before Removal

1. **Create backup script:**
   ```sql
   -- Save DDL
   -- Script: Object Definition
   -- Include: CREATE TABLE/VIEW/PROCEDURE statement
   
   -- Save data (for tables)
   SELECT * INTO BackupSchema.TableName_YYYYMMDD
   FROM dbo.TableName;
   ```

2. **Document in this file:**
   - Add to Removal Log (below)
   - Note backup location
   - Record approver

3. **Get approval:**
   - ❓ *Who must approve?*
   - Minimum: Tech Lead + one other team member

### Removal Script Template

```sql
-- ============================================
-- Legacy Object Removal
-- Object: [ObjectName]
-- Type: [Table/View/Procedure/Function]
-- Date: [YYYY-MM-DD]
-- Approved By: [Name]
-- Backup: [Location]
-- Ticket: [Work Item #]
-- ============================================

-- Step 1: Final verification (run and review)
SELECT TOP 10 * FROM [ObjectName]; -- For tables
-- EXEC [ObjectName]; -- For procedures (if safe)

-- Step 2: Create backup (if not already done)
-- [Backup script here]

-- Step 3: Remove object
-- Uncomment when ready to execute
-- DROP TABLE [ObjectName];
-- DROP VIEW [ObjectName];
-- DROP PROCEDURE [ObjectName];

-- Step 4: Verify removal
-- SELECT * FROM sys.objects WHERE name = 'ObjectName';

PRINT 'Object [ObjectName] removed successfully';
```

---

## Removal Log

| Object Name | Type | Removed Date | Removed By | Approved By | Backup Location | Ticket |
|-------------|------|--------------|------------|-------------|-----------------|--------|
| (none yet) | | | | | | |

---

## Archived Data Log

> For tables with valuable historical data that was archived before removal.

| Original Table | Archive Location | Row Count | Archive Date | Retention Until |
|----------------|------------------|-----------|--------------|-----------------|
| (none yet) | | | | |

---

## Team Contacts for Legacy Knowledge

> People who may have historical knowledge about these objects.

| Name | Role | Tenure | Areas of Knowledge |
|------|------|--------|-------------------|
| ❓ | ❓ | ❓ | ❓ |

---

## Status Legend

| Status | Meaning | Action |
|--------|---------|--------|
| 🔴 **Obsolete** | Confirmed not in use | Safe to remove (follow process) |
| 🟡 **Investigate** | Unknown usage | Research needed before decision |
| 🟢 **Keep** | Legacy but required | Document why, consider modernization |
| 📦 **Archived** | Data preserved, object removed | Data available if needed |
| ⬜ **Not Reviewed** | Not yet analyzed | Add to investigation queue |

---

## Review Schedule

| Review Type | Frequency | Next Review | Owner |
|-------------|-----------|-------------|-------|
| New legacy candidates | ❓ Quarterly | ❓ | ❓ |
| Investigation progress | ❓ Monthly | ❓ | ❓ |
| Removal execution | ❓ As approved | ❓ | ❓ |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | ❓ | ❓ | Initial inventory |

---

## Template Metadata

**Template Version**: 1.0  
**Created**: 2025-12-02  
**Template Type**: Legacy Database Inventory  
**Part of**: Application Knowledge Repo (AKR) system  
**Parent Template**: embedded_database_template.md

**When to use this template:**
- Database has objects unchanged for 3+ years
- Team unsure what legacy objects are still needed
- Planning database cleanup or technical debt reduction
- Preparing for database migration or modernization

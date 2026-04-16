# Recipe: Google Sheets Dedup by Key Column

Complete Apps Script solution that removes duplicate rows from a Google Sheet, keeping the first occurrence of each key value, and creates a timestamped backup tab before any modification.

Pair with [../builders/google-apps-script-builder.md](../builders/google-apps-script-builder.md) and [../patterns/google-apps-script-patterns.md](../patterns/google-apps-script-patterns.md).

---

## What It Does

1. Reads all rows from the source sheet in one batch call.
2. Creates a backup tab (named `SheetName_backup_YYYYMMDD_HHmm`) before touching data.
3. Iterates through rows in order, keeping the first row per unique key value.
4. Writes the deduplicated rows back to a new output sheet (or in-place if configured).
5. Appends a status row to a `Script Log` tab.

---

## Full Script

Paste this into the Apps Script editor (**Extensions → Apps Script**), save, and run `deduplicateSheet`.

```javascript
// ---- Configuration ----
const CONFIG = {
  SOURCE_SHEET:  'Invoices',  // sheet tab to deduplicate
  KEY_COLUMN:    1,           // 1-based column index used as the dedup key (1 = column A)
  HEADER_ROWS:   1,           // number of header rows to preserve and skip
  OUTPUT_SHEET:  'Deduped',   // set to '' to overwrite the source sheet in place
  LOG_SHEET:     'Script Log',
};

// ---- Entry Point ----
function deduplicateSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const src = ss.getSheetByName(CONFIG.SOURCE_SHEET);
  if (!src) throw new Error(`Source sheet not found: "${CONFIG.SOURCE_SHEET}"`);

  const lastRow = src.getLastRow();
  const lastCol = src.getLastColumn();
  if (lastRow <= CONFIG.HEADER_ROWS) {
    log_(ss, 'No data rows found — nothing to deduplicate.');
    return;
  }

  // 1. Read everything in one call
  const allData = src.getRange(1, 1, lastRow, lastCol).getValues();

  // 2. Backup before any write
  backup_(ss, src);

  // 3. Separate headers and data rows
  const headers = allData.slice(0, CONFIG.HEADER_ROWS);
  const dataRows = allData.slice(CONFIG.HEADER_ROWS);

  // 4. Deduplicate — keep first occurrence of each key
  const seen = new Set();
  const deduped = [];
  let removedCount = 0;

  for (const row of dataRows) {
    const key = String(row[CONFIG.KEY_COLUMN - 1]).trim().toLowerCase();
    if (!key) { deduped.push(row); continue; }  // always keep blank-key rows
    if (!seen.has(key)) {
      seen.add(key);
      deduped.push(row);
    } else {
      removedCount++;
    }
  }

  // 5. Write to output sheet (or back to source)
  const dest = getOrCreateSheet_(ss, CONFIG.OUTPUT_SHEET || CONFIG.SOURCE_SHEET);
  dest.clearContents();
  const outputRows = [...headers, ...deduped];
  dest.getRange(1, 1, outputRows.length, lastCol).setValues(outputRows);

  // 6. Log result
  const msg = `Dedup complete — kept ${deduped.length} rows, removed ${removedCount} duplicates → "${dest.getName()}"`;
  log_(ss, msg);
  SpreadsheetApp.getUi().alert(msg);
}

// ---- Helpers ----

function backup_(ss, sheet) {
  const tz = Session.getScriptTimeZone();
  const stamp = Utilities.formatDate(new Date(), tz, 'yyyyMMdd_HHmm');
  const backupName = `${sheet.getName()}_backup_${stamp}`;
  const backup = sheet.copyTo(ss);
  backup.setName(backupName);
  ss.setActiveSheet(sheet);
  Logger.log('Backup created: %s', backupName);
}

function getOrCreateSheet_(ss, name) {
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    Logger.log('Created sheet: %s', name);
  }
  return sheet;
}

function log_(ss, message) {
  let logSheet = ss.getSheetByName(CONFIG.LOG_SHEET);
  if (!logSheet) logSheet = ss.insertSheet(CONFIG.LOG_SHEET);
  const user = Session.getActiveUser().getEmail();
  logSheet.appendRow([new Date(), user, message]);
  Logger.log(message);
}
```

---

## Setup

1. Open your Google Sheet.
2. Go to **Extensions → Apps Script**.
3. Paste the script above and save (Ctrl+S).
4. Edit the `CONFIG` block at the top to match your sheet and column names.
5. Run `deduplicateSheet` — authorize the requested permissions on first run.
6. Check the `Deduped` tab for results and the `Script Log` tab for the summary row.

---

## Validation

- Row count in `Deduped` should equal `source rows − duplicate count`.
- The backup tab `Invoices_backup_YYYYMMDD_HHmm` should match the original row count.
- `Script Log` should show a timestamped entry with the removed count.

---

## Edge Cases

| Case | Behavior |
|---|---|
| Blank key cell | Row is always kept (treated as unique) |
| Key matching is case-insensitive | `INV-001` and `inv-001` are treated as the same key |
| Output sheet same as source | Source is overwritten in-place after backup |
| Sheet with only headers | Script logs "No data rows found" and exits without modifying anything |

---

## Rollback

Open the backup tab (`Invoices_backup_YYYYMMDD_HHmm`), select all data, copy, paste over the source sheet, and delete the `Deduped` tab if needed.

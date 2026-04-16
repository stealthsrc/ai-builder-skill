# Google Apps Script Patterns

Load this reference when the task requires more than a trivial Apps Script function. It provides reusable idioms and anti-patterns for performant, quota-safe Google Workspace automation.

Pair with [../builders/google-apps-script-builder.md](../builders/google-apps-script-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the script sends email, calls external URLs, or modifies Drive files.

---

## 1. Script Skeleton

Keep configurable values in a `CONFIG` object at the top. Never scatter magic strings through the function body.

```javascript
// ---- Configuration ----
const CONFIG = {
  SHEET_NAME: 'Invoices',
  KEY_COLUMN: 1,       // 1-based column index (column A)
  HEADER_ROW: 1,
  OUTPUT_SHEET: 'Cleaned',
};

function cleanInvoices() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const src = ss.getSheetByName(CONFIG.SHEET_NAME);
  if (!src) throw new Error(`Sheet not found: ${CONFIG.SHEET_NAME}`);

  // ... work ...

  SpreadsheetApp.getUi().alert('Done.');
}
```

---

## 2. Batch Read and Write — Never Loop Over Cells

Reading or writing one cell at a time sends a separate API call per cell. For a 500-row sheet that is 500 calls versus 1.

```javascript
// ✓ Read entire range into a 2D array once
const lastRow = src.getLastRow();
const lastCol = src.getLastColumn();
const data = src.getRange(CONFIG.HEADER_ROW + 1, 1, lastRow - CONFIG.HEADER_ROW, lastCol).getValues();

// Mutate in memory
for (let i = 0; i < data.length; i++) {
  data[i][0] = data[i][0].toString().trim(); // trim column A in place
}

// Write back in one call
src.getRange(CONFIG.HEADER_ROW + 1, 1, data.length, lastCol).setValues(data);

// ✗ Never do this inside a loop:
// for (let i = 2; i <= lastRow; i++) {
//   src.getRange(i, 1).setValue(src.getRange(i, 1).getValue().trim());
// }
```

---

## 3. PropertiesService for Secrets and Config

Never hard-code API keys, tokens, or environment-specific values. Store them in Script Properties.

```javascript
// Set once in Apps Script editor: File → Project properties → Script properties
const props = PropertiesService.getScriptProperties();
const apiKey = props.getProperty('EXTERNAL_API_KEY');
if (!apiKey) throw new Error('EXTERNAL_API_KEY not set in Script Properties.');
```

User-specific values (per-user run state) belong in `UserProperties`. Script-wide config belongs in `ScriptProperties`.

---

## 4. UrlFetchApp with Retry

Built-in `UrlFetchApp` is the only HTTP client available in Apps Script. Add a retry wrapper for external APIs.

```javascript
function fetchWithRetry(url, options = {}, maxAttempts = 3) {
  let lastError;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const response = UrlFetchApp.fetch(url, { muteHttpExceptions: true, ...options });
      const code = response.getResponseCode();
      if (code >= 200 && code < 300) return JSON.parse(response.getContentText());
      if (code === 429 || code >= 500) {
        Utilities.sleep(Math.pow(2, attempt) * 1000);
        continue;
      }
      throw new Error(`HTTP ${code}: ${response.getContentText().slice(0, 200)}`);
    } catch (e) {
      lastError = e;
      if (attempt < maxAttempts) Utilities.sleep(Math.pow(2, attempt) * 1000);
    }
  }
  throw lastError;
}
```

---

## 5. GmailApp Safe Send

Always confirm recipient list and content before sending. Prefer creating a draft for review over immediate send.

```javascript
function sendSummaryEmail(recipient, subject, body) {
  const quotaRemaining = MailApp.getRemainingDailyQuota();
  if (quotaRemaining < 1) throw new Error('Daily email quota exhausted.');

  // Draft first — let the user review and send manually if volume is large
  GmailApp.createDraft(recipient, subject, body);
  Logger.log('Draft created for: %s', recipient);

  // Only call GmailApp.sendEmail() directly when volume is small and confirmed
}
```

---

## 6. Time-Based Triggers

Install triggers from the script editor or programmatically. Always delete old triggers before creating new ones to avoid duplicates.

```javascript
function installDailyTrigger() {
  // Remove any existing triggers for this function
  ScriptApp.getProjectTriggers()
    .filter(t => t.getHandlerFunction() === 'cleanInvoices')
    .forEach(t => ScriptApp.deleteTrigger(t));

  ScriptApp.newTrigger('cleanInvoices')
    .timeBased()
    .everyDays(1)
    .atHour(7)
    .create();
  Logger.log('Daily trigger installed.');
}
```

---

## 7. Backup Tab Before Destructive Operations

Always copy data to a timestamped backup sheet before deleting or overwriting rows.

```javascript
function backupSheet(ss, sheet) {
  const timestamp = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyyMMdd_HHmm');
  const backup = sheet.copyTo(ss);
  backup.setName(`${sheet.getName()}_backup_${timestamp}`);
  ss.setActiveSheet(sheet); // return focus to original
  Logger.log('Backup created: %s', backup.getName());
  return backup;
}
```

---

## 8. Logging

Use `Logger.log()` for debugging — view output from **View → Logs**. For persistent logs, write to a dedicated Sheets tab.

```javascript
function logToSheet(ss, message) {
  let logSheet = ss.getSheetByName('Script Log');
  if (!logSheet) logSheet = ss.insertSheet('Script Log');
  logSheet.appendRow([new Date(), Session.getActiveUser().getEmail(), message]);
}
```

---

## 9. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| `getRange(i, j).getValue()` in a loop | One API call per cell → quota exhaustion and slowness | `getValues()` once, mutate array, `setValues()` once |
| Hard-coded API keys in source | Keys exposed in script editor and version history | `PropertiesService.getScriptProperties()` |
| No error handling in trigger functions | Silent failures — trigger runs again and corrupts data | `try/catch` + write error to log sheet |
| Installing triggers every run | Accumulates duplicate triggers; each fires independently | Delete matching triggers before creating new ones |
| `SpreadsheetApp.flush()` inside a loop | Causes a network roundtrip per iteration | Call `flush()` once at the end of the batch |
| Large `UrlFetchApp` calls inside loops | Slow and quota-risky | Batch external calls outside the main loop |

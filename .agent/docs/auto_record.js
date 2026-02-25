
function onEdit(e) {
    // e is undefined if you try to click "Run" inside the Apps Script editor manually.
    // We must return safely if e is undefined so it doesn't crash on manual runs.
    if (!e || !e.source) {
        Logger.log("This script runs automatically when you edit the 'Dashboard' sheet in Google Sheets. It cannot be run manually via the 'Run' button.");
        return;
    }

    // We only care if the edit happens on the "Dashboard" sheet
    var sheet = e.source.getActiveSheet();
    if (sheet.getName() !== "Dashboard") return;

    // We only care if the edit was in the "Actual Input" range (B4:B13)
    // or the "Date" cell (B1)
    var editedRange = e.range;
    var row = editedRange.getRow();
    var col = editedRange.getColumn();

    // If the user clears the entire B4:B13 range at once (multi-cell edit)
    // we do not want to trigger a recording error.
    if (editedRange.getNumRows() > 1) return;

    // If it's the Date Cell (B1), do nothing right now (just a selection)
    if (row == 1 && col == 1) return;

    // If the edit is inside the B4:B13 column...
    if (col == 2 && row >= 4 && row <= 13) {
        recordActualToDatabase();
    }
}

function recordActualToDatabase() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var dash = ss.getSheetByName("Dashboard");
    var db = ss.getSheetByName("Sheet1");

    var targetDate = dash.getRange("B1").getValue();
    if (!targetDate) return;

    // Format Date Safely for Google Apps Script timezone weirdness
    var d = new Date(targetDate);
    var dateStr = d.getFullYear() + "-" +
        ("0" + (d.getMonth() + 1)).slice(-2) + "-" +
        ("0" + d.getDate()).slice(-2);

    // Read all current Database Dates (Column A)
    var dbRange = db.getRange("A:A");
    var dbValues = dbRange.getValues();

    // Find if this Date already exists in the "Sheet1" Database
    var targetRow = -1;
    // Start from row 2 (index 1) to skip headers
    for (var i = 1; i < dbValues.length; i++) {
        if (!dbValues[i][0]) continue; // Skip empty rows

        // Convert the database cells into string dates to compare safely
        var cellData = dbValues[i][0];
        var dbDateStr = "";
        if (Object.prototype.toString.call(cellData) === "[object Date]") {
            dbDateStr = cellData.getFullYear() + "-" +
                ("0" + (cellData.getMonth() + 1)).slice(-2) + "-" +
                ("0" + cellData.getDate()).slice(-2);
        } else {
            dbDateStr = cellData.toString().trim();
        }

        if (dbDateStr === dateStr) {
            targetRow = i + 1; // Apps Script ranges are 1-indexed
            break;
        }
    }

    var actuals = dash.getRange("B4:B13").getValues();

    // If Date does not exist in Database yet, create a new blank row at the very bottom
    if (targetRow === -1) {
        targetRow = db.getLastRow() + 1;
        // Set the Date
        db.getRange(targetRow, 1).setValue(dateStr);
    }

    // Update the 10 Slots (Columns B through K) in that Date's Row
    for (var i = 0; i < 10; i++) {
        var val = actuals[i][0];
        if (val !== "") {
            db.getRange(targetRow, 2 + i).setValue(val);
        }
    }
}

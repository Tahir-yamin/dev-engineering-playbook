/**
 * 🤖 AutoTune AI (Google Sheets -> GitHub Bridge)
 * This script sends a "wake up" signal to GitHub Actions to run train_cloud_model.py
 */

// --- CONFIGURATION ---
// You will need to get a "Personal Access Token" from GitHub
var GITHUB_TOKEN = "paste_your_github_token_here_starting_with_github_pat";
var REPO_OWNER = "your_github_username";
var REPO_NAME = "your_repo_name"; // e.g., "my-dev-knowledge-base"
var WORKFLOW_FILE = "train_model_webhook.yml";

function triggerXGBoostAI() {
    var ui = SpreadsheetApp.getUi();

    var response = ui.alert(
        '🤖 AutoTune AI Initiation',
        'This will trigger the Cloud AI to train on your newest Sheet1 data. Processing takes about 15 seconds.\n\nAre you sure you want to proceed?',
        ui.ButtonSet.YES_NO
    );

    if (response == ui.Button.YES) {
        try {
            var url = "https://api.github.com/repos/" + REPO_OWNER + "/" + REPO_NAME + "/actions/workflows/" + WORKFLOW_FILE + "/dispatches";

            var options = {
                "method": "post",
                "contentType": "application/json",
                "headers": {
                    "Authorization": "Bearer " + GITHUB_TOKEN,
                    "Accept": "application/vnd.github.v3+json"
                },
                "payload": JSON.stringify({
                    "ref": "main" // The branch where your code lives
                })
            };

            UrlFetchApp.fetch(url, options);

            ui.alert('✅ Success', 'The AI Training Engine has been started in the cloud!\n\nWait about 15-20 seconds, and the new predictions will magically appear in the ML_Predictions_Cloud tab.', ui.ButtonSet.OK);

        } catch (e) {
            ui.alert('❌ Error', 'Failed to contact the Cloud Matrix.\n\nError details: ' + e.message, ui.ButtonSet.OK);
        }
    }
}

/**
 * Creates a custom menu in Google Sheets
 */
function onOpen() {
    var ui = SpreadsheetApp.getUi();
    ui.createMenu('🤖 AI Operations')
        .addItem('🚀 Run AutoTune Engine', 'triggerXGBoostAI')
        .addToUi();
}

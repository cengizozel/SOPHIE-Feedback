function toggleSummaryFeedbackButton() {
    var button = document.getElementById("summary-feedback-button");
    if (button.innerHTML === "View Summary Feedback") {
        button.innerHTML = "Hide Summary Feedback";
    } else {
        button.innerHTML = "View Summary Feedback";
    }
}

function toggleSummaryFeedbackButton() {
    var feedbackContainer = document.getElementById("feedback-container");
    var feedbackButton = document.getElementById("summary-feedback-button");
    
    if (feedbackButton.innerHTML == "View Suggestion") {
        feedbackContainer.classList.add("feedback-border");
        feedbackButton.innerHTML = "Hide Suggestion";
    } else {
        feedbackContainer.classList.remove("feedback-border");
        feedbackButton.innerHTML = "View Suggestion";
    }
}


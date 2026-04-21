chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (changeInfo.url) {

        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({url: changeInfo.url})
        })
        .then(res => res.json())
        .then(data => {

            if (data.result === "phishing") {
                alert("⚠️ Phishing Website Detected!");
            }

        });
    }
});
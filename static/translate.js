function postData() {
    fetch('/api', {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            from: document.getElementById('from').value,
            to: document.getElementById('to').value,
            source: document.getElementById('source_content').value
        })
    }).then(response => response.json())
        .then(result => {
            document.getElementById('target_content').value = result.translation
        })
}

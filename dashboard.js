document.addEventListener('DOMContentLoaded', function() {
    fetchStats();
    document.getElementById('blacklist-btn').addEventListener('click', function(event) {
        event.preventDefault();
        blacklistWebsite();
    });
});

function fetchStats() {
    fetch('/api/stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('ads-blocked').textContent = data.total_queries;
            document.getElementById('threats-blocked').textContent = data.queries_blocked;
            document.getElementById('total-queries').textContent = data.domains_blocked;
            document.getElementById('pihole-ip').textContent = data.ip_address; // Assuming your API returns the IP address
        })
        .catch(error => console.error('Error fetching Pi-hole data:', error));
}

function blacklistWebsite() {
    const url = document.getElementById('blacklist-input').value;
    fetch('/api/blacklist', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `url=${encodeURIComponent(url)}`
    })
    .then(response => response.json())
    .then(data => {
        alert('URL added to blacklist!');
        document.getElementById('blacklist-input').value = ''; // Clear input field
        fetchStats(); // Refresh stats to reflect changes
    })
    .catch(error => console.error('Error adding URL to blacklist:', error));
}


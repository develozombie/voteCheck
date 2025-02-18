function updateStandings() {
    fetch('/get_data')
        .then(response => response.json())
        .then(data => {
            const tbody = document.getElementById('standings');
            const newRows = data.items.map((item, index) => `
                <tr style="opacity: 0; animation: fadeIn 0.5s forwards">
                    <td>${index + 1}</td>
                    <td>${item.Nombre}</td>
                    <td>${item.Voto || '0'}</td>
                </tr>
            `).join('');
            tbody.innerHTML = newRows;
        });
}

// Update initially and every 5 seconds
updateStandings();
setInterval(updateStandings, 5000);
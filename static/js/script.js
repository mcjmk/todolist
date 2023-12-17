function toggleTask(taskId) {
    // Wysyłanie żądania AJAX do serwera Flask
    fetch(`/toggle/${taskId}`)
        .then(response => {
            if (response.ok) {
                // Wyświetlenie konfetti
                confetti({
                    particleCount: 150,
                    spread: 180,
                    startVelocity: 60,
                    gravity: 1.2,
                    origin: { x: 0.5, y: 0.1 },
                    zIndex: 9999
                });

                // Zaktualizowanie wyglądu zadania
                document.getElementById(`task-${taskId}`).classList.toggle('completed');
            }
        })
        .catch(error => console.error('Error:', error));
}

function sortTasks() {
    const sortOption = document.getElementById("sort-option").value;

    fetch(`/sort/${sortOption}`)
        .then(response => response.json())
        .then(sortedTasks => {
            const tableBody = document.querySelector("tbody");
            tableBody.innerHTML = '';

            sortedTasks.forEach(task => {
                const row = document.createElement("tr");
                row.id = `task-${task.id}`;
                row.className = task.completed ? 'completed' : '';
                row.setAttribute('onclick', `toggleTask('${task.id}')`);
                row.innerHTML = `
                    <td>${task.name}</td>
                    <td>${task.importance}</td>
                    <td>${task.urgency}</td>
                    <td>${task.priority.toFixed(2)}</td>
                    <td>${task.deadline}</td>
                    <td>${task.estimated_time} godzin</td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
}
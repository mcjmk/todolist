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
            const tasksList = document.getElementById("tasks-list");
            tasksList.innerHTML = ''; // Wyczyszczenie obecnej listy

            sortedTasks.forEach(task => {
                const listItem = document.createElement("li");
                listItem.className = task.completed ? 'completed' : '';
                listItem.setAttribute('onclick', `toggleTask('${task.id}')`);
                listItem.textContent = task.name;
                tasksList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error:', error));
}
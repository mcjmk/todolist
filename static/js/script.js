function toggleTask(taskId) {
    fetch(`/toggle/${taskId}`)
        .then(response => {
            if (response.ok) {
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

function toggleBlock(taskId, blockIndex) {
    const taskProgressBlocks = document.querySelectorAll(`.progress-blocks[data-task-id="${taskId}"] .progress-block`);
    if (taskProgressBlocks[blockIndex]) {
        taskProgressBlocks[blockIndex].classList.toggle('completed');
    }
    updateTaskProgress(taskId, blockIndex);
}

function updateTaskProgress(taskId, blockIndex) {

    const taskProgress = JSON.parse(localStorage.getItem(`task-progress-${taskId}`)) || [];

    if (blockIndex >= 0) {
        taskProgress[blockIndex] = !taskProgress[blockIndex];
    }
    localStorage.setItem(`task-progress-${taskId}`, JSON.stringify(taskProgress));
}
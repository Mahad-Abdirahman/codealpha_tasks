document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("task-form");
  const input = document.getElementById("task-input");
  const taskList = document.getElementById("task-list");

  let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

  function renderTasks() {
    taskList.innerHTML = "";
    tasks.forEach((task, index) => {
      const li = document.createElement("li");
      li.className = task.completed ? "completed" : "";

      const span = document.createElement("span");
      span.textContent = task.text;

      const actions = document.createElement("div");
      actions.className = "actions";

      const completeBtn = document.createElement("button");
      completeBtn.textContent = task.completed ? "Undo" : "Done";
      completeBtn.onclick = () => toggleComplete(index);

      const editBtn = document.createElement("button");
      editBtn.textContent = "Edit";
      editBtn.onclick = () => editTask(index);

      const deleteBtn = document.createElement("button");
      deleteBtn.textContent = "Delete";
      deleteBtn.onclick = () => deleteTask(index);

      actions.appendChild(completeBtn);
      actions.appendChild(editBtn);
      actions.appendChild(deleteBtn);

      li.appendChild(span);
      li.appendChild(actions);
      taskList.appendChild(li);
    });
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }

  function addTask(text) {
    tasks.push({ text, completed: false });
    renderTasks();
  }

  function deleteTask(index) {
    tasks.splice(index, 1);
    renderTasks();
  }

  function editTask(index) {
    const newTask = prompt("Edit your task:", tasks[index].text);
    if (newTask !== null && newTask.trim() !== "") {
      tasks[index].text = newTask.trim();
      renderTasks();
    }
  }

  function toggleComplete(index) {
    tasks[index].completed = !tasks[index].completed;
    renderTasks();
  }

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const taskText = input.value.trim();
    if (taskText) {
      addTask(taskText);
      input.value = "";
    }
  });

  renderTasks();
});

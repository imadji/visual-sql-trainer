<template>
  <div class="tasks">
    <section class="tasks-panel">
      <div class="tasks-title">Задачи</div>
      <div class="tasks-items">
        <div
          v-for="(task, i) in tasks"
          :key="task.id"
          class="task-item"
          :class="{ active: i === activeTask }"
          @click="selectTask(i)"
        >
          <img v-if="task.solved" class="checkmark" src="../assets/checkbox.png" alt="" />
          <div class="task-title">{{ task.title }}</div>
          <div class="task-description">{{ task.description }}</div>
        </div>
      </div>
    </section>

    <section class="task-detail">
      <div class="tasks-title">Описание задачи</div>
      <div class="task-detail-container">
        <h2 class="task-detail-title">{{ selectedTask?.title }}</h2>
        <p class="task-detail-full">{{ selectedTask?.description }}</p>
      </div>
    </section>

    <section class="io-panel">
      <div class="tasks-title">Ввод/вывод</div>
      <div class="io-panel-container">
        <div class="result-table" v-if="queryResult">
          <div
            class="table-header"
            :class="{ solved: selectedTask?.solved, unsolved: !selectedTask?.solved }"
          >
            <h3>{{ queryResult.name || "Результат запроса" }}</h3>
          </div>
          <div class="table-content">
            <table>
              <thead>
                <tr>
                  <th v-for="(header, i) in queryResult.headers" :key="i">{{ header }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, rowIndex) in queryResult.data" :key="rowIndex">
                  <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div class="console-output" ref="consoleOutput">
          <div v-if="errorMessage" class="log-message error">
            {{ errorMessage }}
          </div>
        </div>

        <div class="editor-container">
          <textarea
            v-model="textRequest"
            placeholder="Введите SQL-запрос..."
            @keydown.enter.exact.prevent="sendRequest"
            @keydown.up.prevent="navigateHistory('up')"
            @keydown.down.prevent="navigateHistory('down')"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { useTaskRequest } from "@/stores/store";

interface QueryResult {
  is_result: boolean;
  name: string;
  headers: string[];
  data: any[][];
}

interface TaskData {
  description: string;
  id: number;
  solved: boolean;
  title: string;
  user_solution: string;
}

const props = defineProps({
  isVisible: {
    type: Boolean,
    default: false,
  },
});

const taskStore = useTaskRequest();
const tasks = ref<TaskData[]>([]);
const activeTask = ref<number>(0);
const selectedTask = ref<TaskData | null>(null);
const textRequest = ref<string>("");
const queryResult = ref<QueryResult | null>(null);
const errorMessage = ref<string>("");
const commandHistory = ref<string[]>([]);
const historyIndex = ref(-1);

const userString = computed(() => {
  return localStorage.getItem("authToken");
});

const selectTask = (index: number) => {
  activeTask.value = index;
  selectedTask.value = tasks.value[index];
  queryResult.value = null;
  errorMessage.value = "";
  textRequest.value = "";
};

const loadTasks = async () => {
  if (!userString.value) return;

  try {
    const response = await taskStore.getAllTask(userString.value);
    if (response && response.tasks) {
      tasks.value = response.tasks;
      if (tasks.value.length > 0) {
        selectedTask.value = tasks.value[0];
      }
    }
  } catch (error) {
    console.error("Ошибка загрузки задач:", error);
    errorMessage.value = "Не удалось загрузить список задач";
  }
};

const sendRequest = async (): Promise<void> => {
  if (!userString.value || !selectedTask.value?.id) return;

  const query = textRequest.value.trim();
  if (query === "") {
    errorMessage.value = "Ошибка: запрос не может быть пустым";
    return;
  }

  commandHistory.value.push(query);
  historyIndex.value = commandHistory.value.length;

  try {
    const credentials = {
      query: textRequest.value,
      user: userString.value,
      task_id: selectedTask.value?.id,
    };

    const response = await taskStore.checkSolveTask(credentials);
    errorMessage.value = "";
    queryResult.value = response.result;
    if (response.status === true) {
      const taskIndex = tasks.value.findIndex((t) => t.id === selectedTask.value?.id);
      if (taskIndex !== -1) {
        tasks.value[taskIndex].solved = true;
      }
    }
  } catch (err) {
    console.error("Ошибка запроса:", err);
    errorMessage.value = "Произошла ошибка при выполнении запроса";
    queryResult.value = null;
  }
};

const navigateHistory = (direction: string) => {
  if (commandHistory.value.length === 0) return;

  if (direction === "up" && historyIndex.value > 0) {
    historyIndex.value--;
    textRequest.value = commandHistory.value[historyIndex.value];
  } else if (direction === "down") {
    if (historyIndex.value < commandHistory.value.length - 1) {
      historyIndex.value++;
      textRequest.value = commandHistory.value[historyIndex.value];
    } else {
      historyIndex.value = commandHistory.value.length;
      textRequest.value = "";
    }
  }
};

watch(
  () => props.isVisible,
  (newVal) => {
    if (newVal && tasks.value.length === 0) {
      loadTasks();
    }
  },
  { immediate: true }
);
</script>

<style lang="scss" scoped>
.tasks {
  width: 100%;
  height: 80vh;
  display: flex;
  flex-direction: row;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 15px;
}

.tasks-title {
  width: 100%;
  font-size: 35px;
  font-weight: 900;
  border-bottom: 1px solid rgba(255, 255, 255, 0.5);
  padding: 10px;
}

.tasks-panel {
  height: 100%;
  min-width: 400px;
  display: flex;
  flex-direction: column;

  .tasks-title {
    flex-shrink: 0;
  }

  .tasks-items {
    flex: 1;
    overflow-y: auto;
    padding: 15px 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 20px;

    .task-item {
      width: 360px;
      min-height: 90px;
      border: 1px solid rgba(214, 214, 214, 0.1);
      border-radius: 15px;
      padding: 10px;
      cursor: pointer;
      position: relative;

      .checkmark {
        position: absolute;
        right: 5px;
        width: 25px;
      }

      .task-title {
        font-size: 18px;
      }

      .task-description {
      }
    }

    .task-item.active {
      background-color: rgba(255, 255, 255, 0.1);
    }
  }
}

.task-detail {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255, 255, 255, 0.5);
  border-left: 1px solid rgba(255, 255, 255, 0.5);

  .task-detail-container {
    flex: 1;
    overflow-y: auto;
    margin: 15px;
    padding: 15px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    background-color: rgba(214, 214, 214, 0.3);
    border-radius: 15px;

    .task-detail-title {
      font-size: 27px;
    }

    .task-detail-full {
      font-size: 20px;
    }
  }
}

.io-panel {
  width: 100%;
  display: flex;
  flex-direction: column;

  .io-panel-container {
    display: flex;
    flex-direction: column;
    height: 100%;
    flex: 1;
    padding: 10px;
    gap: 10px;
  }

  .result-table {
    background: #252526;
    border: 1px solid #3c3c3c;
    border-radius: 6px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    overflow: hidden;
    color: #e0e0e0;
    margin-bottom: 10px;

    .table-header {
      &.solved {
        background: #4caf50;
      }
      &.unsolved {
        background: #f44336;
      }
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 15px;
      color: white;
      h3 {
        margin: 0;
        font-size: 14px;
        font-weight: 500;
      }
    }

    .table-content {
      overflow: auto;
      max-height: 300px;

      table {
        width: 100%;
        border-collapse: collapse;

        th,
        td {
          padding: 8px 12px;
          border: 1px solid #3c3c3c;
          text-align: left;
          font-size: 13px;
        }

        th {
          background-color: #2a2d2e;
          position: sticky;
          top: 0;
          font-weight: 500;
          color: #ffffff;
        }

        tr:nth-child(even) {
          background-color: #2d2d2d;
        }

        tr:hover {
          background-color: #37373d;
        }
      }
    }
  }

  .console-output {
    flex: 1;
    background-color: rgba(233, 241, 255, 1);
    border-radius: 6px;
    padding: 12px;
    font-family: "Consolas", monospace;
    font-size: 13px;
    overflow-y: auto;
    min-height: 0;
    scroll-behavior: smooth;

    .log-message {
      position: relative;
      margin-bottom: 8px;
      line-height: 1.4;
      white-space: pre-wrap;
      padding-right: 30px;

      &.error {
        color: #ad2727;
      }
    }
  }

  .editor-container {
    textarea {
      width: 100%;
      height: 120px;
      padding: 12px;
      border: 1px solid #3c3c3c;
      border-radius: 6px;
      font-family: "Consolas", monospace;
      font-size: 14px;
      resize: none;
      background-color: rgba(233, 241, 255, 1);
      color: #000;
      box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3);

      &:focus {
        outline: none;
        border-color: #4a6fa5;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.3), 0 0 0 2px rgba(74, 111, 165, 0.3);
      }

      &::placeholder {
        color: #5a5a5a;
      }
    }
  }
}
</style>

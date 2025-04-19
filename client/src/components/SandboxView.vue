<template>
  <div class="sandbox">
    <div class="main-workspace">
      <div class="left-panel">
        <div class="tabs-container">
          <button
            class="tab-btn"
            :class="{ active: activeTab === 'tables' }"
            @click="activeTab = 'tables'"
          >
            Таблицы
          </button>
          <button
            v-if="showDebuggerTab"
            class="tab-btn"
            :class="{ active: activeTab === 'debugger' }"
            @click="activeTab = 'debugger'"
          >
            Отладчик
          </button>
        </div>

        <div class="content-container">
          <div class="tables-container" ref="tablesContainer" v-show="activeTab === 'tables'">
            <div
              v-for="(table, index) in resultTables"
              :key="index"
              class="result-table"
              :style="{
                left: table.position.x + 'px',
                top: table.position.y + 'px',
                width: table.width + 'px',
              }"
            >
              <div class="table-header" @mousedown="startDrag($event, index)">
                <h3>{{ table.name }}</h3>
                <div class="table-controls">
                  <button class="close-btn" @click="removeTable(index)" title="Закрыть">×</button>
                </div>
              </div>
              <div class="table-content">
                <table>
                  <thead>
                    <tr>
                      <th v-for="(header, i) in table.headers" :key="i">{{ header }}</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(row, rowIndex) in table.data" :key="rowIndex">
                      <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div class="debugger-container" v-show="activeTab === 'debugger'">
            <DebuggerView
              :debugMessage="currentDebugMessage"
              :userString="userString"
              @close="activeTab = 'tables'"
            />
          </div>
        </div>
      </div>

      <div class="right-container">
        <div class="console-panel">
          <span>Инпут:</span>
          <div class="console-btns">
            <img @click="sendRequest" src="../assets/info-icon.png" alt="Информация" />
          </div>
        </div>
        <div class="console-output" ref="consoleOutput">
          <div
            v-for="(log, index) in consoleLogs"
            :key="index"
            class="log-message"
            :class="log.type"
          >
            {{ log.message }}
            <button
              v-if="log.type === 'query'"
              class="debug-btn"
              @click="openDebugger(log.message)"
              title="Открыть в отладчике"
            >
              123
            </button>
          </div>
        </div>
        <div class="editor-container">
          <!-- <textarea v-model="textRequest" placeholder="Введите SQL-запрос..."
            @keydown.enter.exact.prevent="sendRequest"></textarea> -->
          <textarea
            v-model="textRequest"
            placeholder="Введите SQL-запрос..."
            @keydown.enter.exact.prevent="sendRequest"
            @keydown.up.prevent="navigateHistory('up')"
            @keydown.down.prevent="navigateHistory('down')"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, nextTick, computed } from "vue";
import { useAuthStore, useSqlRequest } from "@/stores/authStore";
import DebuggerView from "../components/DebuggerView.vue";

interface TablePosition {
  x: number;
  y: number;
}
interface TableData {
  name: string;
  headers: string[];
  data: any[][];
  position: TablePosition;
  width: number;
  isDragging: boolean;
}
interface LogMessage {
  message: string;
  type: "info" | "error" | "success" | "query";
}

const resultTables = reactive<TableData[]>([]);
const tablesContainer = ref<HTMLElement | null>(null);
const activeDragIndex = ref<number | null>(null);
const consoleOutput = ref<HTMLElement | null>(null);
const textRequest = ref<string>("");
const dragOffset = reactive({ x: 0, y: 0 });
const consoleLogs = reactive<LogMessage[]>([]);
const showDebuggerTab = ref(false);

const sqlStore = useSqlRequest();
const tableStore = useAuthStore();
const commandHistory = ref([]);
const historyIndex = ref(-1);

const activeTab = ref<"tables" | "debugger">("tables");
const currentDebugMessage = ref<string>("");

const logToConsole = (message: string, type: LogMessage["type"] = "info"): void => {
  consoleLogs.push({ message, type });
  nextTick(() => {
    if (consoleOutput.value) {
      consoleOutput.value.scrollTo({
        top: consoleOutput.value.scrollHeight,
        behavior: "smooth",
      });
    }
  });
};

const openDebugger = (message: string): void => {
  currentDebugMessage.value = message;
  showDebuggerTab.value = true;
  activeTab.value = "debugger";
  navigator.clipboard
    .writeText(message)
    .then(() => logToConsole("Переходим в инстурмент Отладчик", "info"))
    .catch((err: Error) => logToConsole(`Ошибка: ${err.message}`, "error"));
};

const userString = computed(() => {
  const user = localStorage.getItem("authToken");
  return user;
});

const sendRequest = async (): Promise<void> => {
  if (!textRequest.value.trim()) {
    logToConsole("Ошибка: запрос пустой", "error");
    return;
  }

  const query = textRequest.value.trim();
  if (!query) {
    logToConsole("Ошибка: запрос пустой", "error");
    return;
  }

  const userString = localStorage.getItem("authToken");
  if (!userStrin.value) {
    logToConsole("Ошибка: пользователь не авторизован", "error");
    return;
  }

  commandHistory.value.push(query);
  historyIndex.value = commandHistory.value.length;

  try {
    logToConsole("Выполнение запроса:", "info");
    logToConsole(textRequest.value, "query");
    const credentials = {
      query: textRequest.value,
      user: userString.value,
    };
    const response = await sqlStore.executeSqlReq(credentials);
    if (response.name) {
      const newTable: TableData = {
        name: response.name || "Результат запроса",
        headers: response.headers || [],
        data: response.data || [],
        position: {
          x: Math.floor(Math.random() * 100),
          y: Math.floor(Math.random() * 100),
        },
        width: 450,
        isDragging: false,
      };
      const existingIndex = resultTables.findIndex((t) => t.name === response.name);
      if (existingIndex >= 0) {
        resultTables[existingIndex] = newTable;
      } else {
        resultTables.push(newTable);
      }

      logToConsole("Запрос выполнен успешно", "success");
      textRequest.value = "";
    }
  } catch (error: unknown) {
    const err = error as Error;
    logToConsole(`Ошибка: ${err.message}`, "error");
    console.error("Ошибка запроса:", err);
  }
  textRequest.value = "";
};

const startDrag = (e: MouseEvent, index: number): void => {
  activeDragIndex.value = index;
  resultTables[index].isDragging = true;
  dragOffset.x = e.clientX - resultTables[index].position.x;
  dragOffset.y = e.clientY - resultTables[index].position.y;
  document.addEventListener("mousemove", handleDrag);
  document.addEventListener("mouseup", stopDrag);
  e.preventDefault();
};

const navigateHistory = (direction) => {
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

const navigateHistory = (direction) => {
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

const handleDrag = (e: MouseEvent): void => {
  if (activeDragIndex.value === null || !tablesContainer.value) return;

  const containerRect = tablesContainer.value.getBoundingClientRect();
  const table = document.querySelectorAll(".result-table")[activeDragIndex.value] as HTMLElement;
  const tableWidth = table.offsetWidth;
  const tableHeight = table.offsetHeight;

  let newX = e.clientX - dragOffset.x;
  let newY = e.clientY - dragOffset.y;

  newX = Math.max(0, Math.min(newX, containerRect.width - tableWidth));
  newY = Math.max(0, Math.min(newY, containerRect.height - tableHeight));

  resultTables[activeDragIndex.value].position.x = newX;
  resultTables[activeDragIndex.value].position.y = newY;
};

const stopDrag = (): void => {
  if (activeDragIndex.value !== null) {
    resultTables[activeDragIndex.value].isDragging = false;
    activeDragIndex.value = null;
  }
  document.removeEventListener("mousemove", handleDrag);
  document.removeEventListener("mouseup", stopDrag);
};

const removeTable = (index: number): void => {
  resultTables.splice(index, 1);
  logToConsole(`Таблица удалена`, "info");
};

onMounted((): void => {
  if (tableStore.tables?.length) {
    tableStore.tables.forEach((table: TableData) => {
      resultTables.push({
        name: table.name,
        headers: [...table.headers],
        data: table.data.map((row) => [...row]),
        position: { ...table.position },
        width: table.width,
        isDragging: false,
      });
    });
  }
});
</script>

<style lang="scss" scoped>
.sandbox {
  display: flex;
  flex-direction: column;
  height: 80vh;
  padding: 20px;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #1e1e1e;
  color: #e0e0e0;
}

.main-workspace {
  display: flex;
  gap: 20px;
  flex: 1;
  min-height: 0;
}

.left-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  background-color: #2d2d2d;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.tabs-container {
  display: flex;
  background-color: #252526;
  padding: 8px 8px 0 8px;
  border-bottom: 1px solid #3c3c3c;

  .tab-btn {
    padding: 8px 16px;
    background: none;
    border: none;
    cursor: pointer;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
    border-radius: 4px 4px 0 0;
    margin-right: 4px;
    font-size: 14px;
    color: #d4d4d4;

    &.active {
      border-bottom-color: #4a6fa5;
      font-weight: 600;
      color: #ffffff;
      background-color: #1e1e1e;
    }

    &:hover {
      background-color: #2a2d2e;
    }
  }
}

.content-container {
  flex: 1;
  position: relative;
  min-height: 0;
}

.tables-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 15px;
  overflow: hidden;
  background-color: #1e1e1e;
}

.debugger-container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 15px;
  overflow: auto;
  background-color: #1e1e1e;
  color: #e0e0e0;
}

.right-container {
  width: 450px;
  display: flex;
  flex-direction: column;
  min-height: 0;
  gap: 10px;
  background-color: #2d2d2d;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.console-panel {
  display: flex;
  justify-content: space-between;
  align-items: center;

  span {
    font-size: 16px;
    font-weight: 600;
    color: #e0e0e0;
  }

  .console-btns {
    display: flex;
    gap: 10px;

    img {
      width: 20px;
      height: 20px;
      cursor: pointer;
      opacity: 0.7;
      transition: opacity 0.2s;

      &:hover {
        opacity: 1;
      }
    }
  }
}

.console-output {
  flex: 1;
  background-color: #1e1e1e;
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

    &.info {
      color: #1f95cc;
    }

    &.error {
      color: #ad2727;
    }

    &.success {
      color: #23ad38;
    }

    &.query {
      color: #b0bec5;
      background-color: rgba(0, 0, 0, 0.3);
      padding: 8px;
      color: #ffffff;
      background-color: rgba(0, 0, 0, 1);
      padding: 4px 8px;
      border-radius: 4px;
      font-family: "Consolas", monospace;
    }

    .debug-btn {
      position: absolute;
      right: 5px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      cursor: pointer;
      opacity: 0.5;
      transition: opacity 0.2s;
      padding: 0;

      &:hover {
        opacity: 1;
      }

      img {
        width: 16px;
        height: 16px;
        filter: invert(1);
      }
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
    background-color: #1e1e1e;
    color: #e0e0e0;
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

.result-table {
  position: absolute;
  background: #252526;
  border: 1px solid #3c3c3c;
  border-radius: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  z-index: 10;
  color: #e0e0e0;

  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
    background: #4a6fa5;
    color: white;
    cursor: move;

    h3 {
      margin: 0;
      font-size: 14px;
      font-weight: 500;
    }
  }

  .table-controls {
    .close-btn {
      background: transparent;
      border: none;
      color: white;
      cursor: pointer;
      font-size: 18px;
      line-height: 1;
      padding: 0 5px;

      &:hover {
        color: #ffdddd;
      }
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
</style>

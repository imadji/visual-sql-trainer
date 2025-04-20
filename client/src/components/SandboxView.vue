<template>
  <div class="sandbox">
    <div class="main-workspace">
      <div class="left-panel">
        <div class="tabs-container">
          <button class="tab-btn" :class="{ active: activeTab === 'tables' }" @click="activeTab = 'tables'">
            Таблицы
          </button>
          <button v-if="showDebuggerTab" class="tab-btn" :class="{ active: activeTab === 'debugger' }"
            @click="activeTab = 'debugger'">
            Отладчик
          </button>
        </div>

        <div class="content-container">
          <div class="tables-container" ref="tablesContainer" v-show="activeTab === 'tables'">
            <div v-for="(table, index) in resultTables" :key="index" class="result-table" :style="{
              left: table.position.x + 'px',
              top: table.position.y + 'px',
              width: table.width + 'px',
            }">
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
            <DebuggerView :debugMessage="currentDebugMessage" :userString="userString" @close="activeTab = 'tables'" />
          </div>
        </div>
      </div>

      <div class="right-container">
        <div class="console-panel">
          <span>Консоль :</span>
          <!-- <div class="console-btns" @click="uploadData">ВЫГРУЗКА</div> -->

          <div class="console-btns">
            <img class="download" @click="uploadData" src="../assets/download.png" title="Выгрузка" />
            <img @click="openAImodal" src="../assets/info-icon.png" :class="{ disabled: isAIButtonDisabled }"
              title="Задача от AI" />
          </div>
        </div>
        <div class="console-output" ref="consoleOutput">
          <div v-for="(log, index) in consoleLogs" :key="index" class="log-message" :class="log.type">
            {{ log.message }}
            <button v-if="log.type === 'query'" class="debug-btn" @click="openDebugger(log.message)"
              title="Открыть в отладчике">
              <img src="../assets/info-helper.png" alt="" />
            </button>
            <!-- <button
              v-if="log.type === 'ai-task'"
              class="debug-btn"
              @click="helpForAI(log.message)"
              title="Показать SQL подсказку"
            >
            </button> -->
            <img src="../assets/lamp.png" v-if="log.type === 'ai-task'" class="debug-btn"
              @click="helpForAI(log.message)" title="Показать SQL подсказку" alt="">
          </div>
        </div>
        <div class="editor-container">
          <textarea v-model="textRequest" placeholder="Введите SQL-запрос..." @keydown.enter.exact.prevent="sendRequest"
            @keydown.up.prevent="navigateHistory('up')" @keydown.down.prevent="navigateHistory('down')" />
        </div>
      </div>
    </div>

    <!-- AI Modal -->
    <div v-if="showAIModal" class="ai-modal-overlay" @click.self="closeAIModal">
      <div class="ai-modal">
        <div class="ai-modal-header">
          <h3>Генератор задач AI</h3>
          <button class="close-btn" @click="closeAIModal">×</button>
        </div>
        <div class="ai-modal-content">
          <p>AI проанализирует все таблицы в вашей базе данных и создаст задачу SQL запроса.</p>
          <p>Выберите уровень сложности:</p>
          <div class="difficulty-options">
            <button v-for="level in difficultyLevels" :key="level.value" @click="selectDifficulty(level.value)"
              :class="{ active: selectedDifficulty === level.value }">
              {{ level.label }}
            </button>
          </div>
        </div>
        <div class="ai-modal-footer">
          <button @click="generateTask" :disabled="!selectedDifficulty || isGenerating" class="start-btn">
            {{ isGenerating ? "Генерация..." : "Старт" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted, nextTick, computed } from "vue";
import { useAuthStore, useSqlRequest, useAIrequest } from "@/stores/store";
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
  type: "info" | "error" | "success" | "query" | "ai-task";
}

const resultTables = reactive<TableData[]>([]);
const tablesContainer = ref<HTMLElement | null>(null);
const activeDragIndex = ref<number | null>(null);
const consoleOutput = ref<HTMLElement | null>(null);
const textRequest = ref<string>("");
const dragOffset = reactive({ x: 0, y: 0 });
const consoleLogs = reactive<LogMessage[]>([]);
const showDebuggerTab = ref(false);
const commandHistory = ref<string[]>([]);
const sqlCommandHelp = ref<string[]>([]);
const historyIndex = ref(-1);

const sqlStore = useSqlRequest();
const taskStore = useAIrequest();
const tableStore = useAuthStore();

const activeTab = ref<"tables" | "debugger">("tables");
const currentDebugMessage = ref<string>("");

const showAIModal = ref(false);
const selectedDifficulty = ref<string>("");
const isGenerating = ref(false);
const isAIButtonDisabled = ref(false);
const difficultyLevels = ref([
  { value: "easy", label: "Легкий" },
  { value: "medium", label: "Средний" },
  { value: "hard", label: "Сложный" },
]);

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

const helpForAI = (message: string): void => {
  const logIndex = consoleLogs.findIndex((log) => log.message === message);
  if (logIndex === -1) return;
  const taskIndex = sqlCommandHelp.value.indexOf(message);
  if (taskIndex === -1 || taskIndex + 1 >= sqlCommandHelp.value.length) return;
  let sqlHint = sqlCommandHelp.value[taskIndex + 1];
  sqlHint = sqlHint
    .replace(/^```sql\s*/, "")
    .replace(/\s*```$/, "")
    .trim();
  consoleLogs.splice(logIndex + 1, 0, {
    message: `${sqlHint}`,
    type: "query",
  });
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
  if (query === "") {
    logToConsole("Ошибка: запрос пустой", "error");
    return;
  }
  if (!userString.value) {
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
        resultTables[existingIndex].headers = response.headers || [];
        resultTables[existingIndex].data = response.data || [];
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

const uploadData = async (): Promise<void> => {
  if (!userString.value) return;
  try {
    await tableStore.uploadDump(userString.value);
  } catch (error) {
    logToConsole(`Ошибка запроса на сервер: ${error}`, "error");
  }
};

const openAImodal = async (): Promise<void> => {
  if (!userString.value) return;
  showAIModal.value = true;
};

const closeAIModal = (): void => {
  showAIModal.value = false;
  selectedDifficulty.value = "";
};

const selectDifficulty = (level: string): void => {
  selectedDifficulty.value = level;
};

const generateTask = async (): Promise<void> => {
  if (!userString.value || !selectedDifficulty.value) return;

  isGenerating.value = true;
  isAIButtonDisabled.value = true;

  try {
    const response = await tableStore.getAllTables(userString.value);
    if (!response?.tables?.length) {
      logToConsole(`Ошибка: Нет таблиц для отправки данных в AI`, "error");
      return;
    }
    const requestData = {
      tables: response.tables.map((table) => ({
        is_result: true,
        name: table.name,
        headers: table.headers,
        data: table.data,
      })),
      difficulty: selectedDifficulty.value,
    };
    const genTaskResponse = await taskStore.genTask(requestData);
    if (genTaskResponse.task !== "") {
      sqlCommandHelp.value.push(genTaskResponse.task, genTaskResponse.sql);
      logToConsole(genTaskResponse.task, "ai-task");
    } else {
      logToConsole(`Ошибка генерации задачи: ${genTaskResponse.error}`, "error");
    }
  } catch (error) {
    logToConsole(`Ошибка запроса на сервер: ${error}`, "error");
  } finally {
    isGenerating.value = false;
    showAIModal.value = false;
    selectedDifficulty.value = "";
    setTimeout(() => {
      isAIButtonDisabled.value = false;
    }, 30000);
  }
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
@import url(../assets/sandbox.scss);
</style>

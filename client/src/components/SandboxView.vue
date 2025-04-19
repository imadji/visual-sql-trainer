<template>
  <div class="sandbox">
    <div class="main-workspace">
      <div class="tables-container" ref="tablesContainer">
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
      <div class="right-container">
        <div class="console-output">
          <div
            v-for="(log, index) in consoleLogs"
            :key="index"
            class="log-message"
            :class="log.type"
          >
            {{ log.message }}
          </div>
        </div>
        <div class="editor-container">
          <textarea
            v-model="textRequest"
            placeholder="Введите SQL-запрос..."
            @keydown.enter.exact.prevent="sendRequest"
          ></textarea>
          <button @click="sendRequest" class="submit-btn">Выполнить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore, useSqlRequest } from "@/stores/authStore";
import { ref, reactive, onMounted } from "vue";

const resultTables = reactive([]);
const tablesContainer = ref(null);
const activeDragIndex = ref(null);
const textRequest = ref("");
const dragOffset = reactive({ x: 0, y: 0 });
const consoleLogs = reactive([]);
const sqlStore = useSqlRequest();
const tableStore = useAuthStore();

const logToConsole = (message, type = "info") => {
  consoleLogs.push({ message, type });
};

const sendRequest = async () => {
  if (!textRequest.value.trim()) {
    logToConsole("Ошибка: запрос пустой", "error");
    return;
  }
  const userString = localStorage.getItem("authToken");
  if (!userString) {
    logToConsole("Ошибка: пользователь не авторизован", "error");
    return;
  }

  try {
    logToConsole("Выполнение запроса:", "info");
    logToConsole(textRequest.value, "query");
    const credentials = {
      query: textRequest.value,
      user: userString,
    };
    const response = await sqlStore.executeSqlReq(credentials);
    if (response) {
      const newTable = {
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
      resultTables.push(newTable);
      logToConsole("Запрос выполнен успешно", "success");
    }
  } catch (error) {
    console.error("Ошибка запроса:", error);
    logToConsole(`Ошибка: ${error.message}`, "error");
  }
};

const startDrag = (e, index) => {
  activeDragIndex.value = index;
  resultTables[index].isDragging = true;
  dragOffset.x = e.clientX - resultTables[index].position.x;
  dragOffset.y = e.clientY - resultTables[index].position.y;

  document.addEventListener("mousemove", handleDrag);
  document.addEventListener("mouseup", stopDrag);
  e.preventDefault();
};

const handleDrag = (e) => {
  if (activeDragIndex.value === null) return;

  const containerRect = tablesContainer.value.getBoundingClientRect();
  const table = document.querySelectorAll(".result-table")[activeDragIndex.value];
  const tableWidth = table.offsetWidth;
  const tableHeight = table.offsetHeight;

  let newX = e.clientX - dragOffset.x;
  let newY = e.clientY - dragOffset.y;

  newX = Math.max(0, Math.min(newX, containerRect.width - tableWidth));
  newY = Math.max(0, Math.min(newY, containerRect.height - tableHeight));

  resultTables[activeDragIndex.value].position.x = newX;
  resultTables[activeDragIndex.value].position.y = newY;
};

const stopDrag = () => {
  if (activeDragIndex.value !== null) {
    resultTables[activeDragIndex.value].isDragging = false;
    activeDragIndex.value = null;
  }

  document.removeEventListener("mousemove", handleDrag);
  document.removeEventListener("mouseup", stopDrag);
};

const removeTable = (index) => {
  resultTables.splice(index, 1);
  logToConsole(`Таблица удалена`, "info");
};

onMounted(() => {
  if (tableStore.tables?.length) {
    tableStore.tables.forEach((table) => {
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
  height: calc(100vh - 40px);
  padding: 20px;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f7fa;
}

.main-workspace {
  display: flex;
  gap: 20px;
  flex: 1;
  min-height: 0;
  margin-bottom: 10px;
}

.tables-container {
  flex: 1;
  position: relative;
  min-height: 100%;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #ffffff;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.right-container {
  width: 450px;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.console-output {
  flex: 1;
  background-color: #1e1e1e;
  color: #e0e0e0;
  border-radius: 6px;
  padding: 12px;
  font-family: "Consolas", monospace;
  font-size: 13px;
  overflow-y: auto;
  min-height: 0;
  .log-message {
    margin-bottom: 8px;
    line-height: 1.4;
    white-space: pre-wrap;

    &.info {
      color: #4fc3f7;
    }

    &.error {
      color: #ff5252;
    }

    &.success {
      color: #69f0ae;
    }

    &.query {
      color: #b0bec5;
      background-color: rgba(0, 0, 0, 0.1);
      padding: 4px 8px;
      border-radius: 4px;
      margin-left: 12px;
      font-family: "Consolas", monospace;
      display: block;
      margin-top: 4px;
    }
  }
}

.editor-container {
  color: #1e1e1e;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 15px;

  textarea {
    width: 100%;
    height: 120px;
    padding: 12px;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    font-family: "Consolas", monospace;
    font-size: 14px;
    resize: none;
    background-color: #ffffff;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);

    &:focus {
      outline: none;
      border-color: #4a6fa5;
      box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1), 0 0 0 2px rgba(74, 111, 165, 0.2);
    }
  }

  .submit-btn {
    padding: 10px 20px;
    background-color: #4a6fa5;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: background-color 0.2s;

    &:hover {
      background-color: #3a5a8f;
    }

    &:active {
      background-color: #2a4a7f;
    }
  }
}

.result-table {
  position: absolute;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  z-index: 10;

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
    color: #1e1e1e;
    overflow: auto;
    max-height: 300px;

    table {
      width: 100%;
      border-collapse: collapse;

      th,
      td {
        padding: 8px 12px;
        border: 1px solid #e0e0e0;
        text-align: left;
        font-size: 13px;
      }

      th {
        background-color: #f2f6ff;
        position: sticky;
        top: 0;
        font-weight: 500;
      }

      tr:nth-child(even) {
        background-color: #f9f9f9;
      }

      tr:hover {
        background-color: #f0f5ff;
      }
    }
  }
}
</style>

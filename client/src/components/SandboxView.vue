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
                  <td v-for="(cell, cellIndex) in row" :key="cellIndex">
                    <div class="cell-content">{{ cell }}</div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="right-container">
        <h3>Вывод данных SQL запросов</h3>
        <div class="right-content">
          <div v-if="testDataTable?.name" class="result-table">
            <div class="table-header">
              <h3>{{ testDataTable.name }}</h3>
            </div>
            <div class="table-content">
              <table v-if="testDataTable.headers?.length">
                <thead>
                  <tr>
                    <th v-for="(header, i) in testDataTable.headers" :key="i">
                      {{ header }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, rowIndex) in testDataTable.data || []" :key="rowIndex">
                    <td v-for="(cell, cellIndex) in row" :key="cellIndex">
                      {{ cell }}
                    </td>
                  </tr>
                  <tr v-if="!testDataTable.data?.length">
                    <td :colspan="testDataTable.headers?.length || 1" class="empty-message">
                      Нет данных для отображения
                    </td>
                  </tr>
                </tbody>
              </table>
              <div v-else class="no-headers">Нет заголовков для отображения</div>
            </div>
          </div>
          <div v-else class="empty-state">Результаты запроса будут отображены здесь</div>
        </div>
      </div>
    </div>

    <div class="status-section">
      <h3>Статус:</h3>
      <ul class="status-list">
        <li>{{ status }}</li>
      </ul>
    </div>

    <div class="editor">
      <textarea v-model="textRequest" placeholder="Введите SQL-запрос..."></textarea>
      <button @click="sendRequest" class="submit-btn">Отправить запрос</button>
    </div>
  </div>
</template>

<script setup>
import { useSqlRequest } from "@/stores/authStore";
import { ref, reactive } from "vue";

const resultTables = reactive([]);
const testDataTable = ref([]);
const tablesContainer = ref(null);
const activeDragIndex = ref(null);
const status = ref("Готов к работе");
const textRequest = ref("");
const dragOffset = reactive({ x: 0, y: 0 });
const sqlStore = useSqlRequest();

const sendRequest = async () => {
  if (!textRequest.value.trim()) {
    status.value = "Ошибка: запрос пустой";
    return;
  }
  const userString = localStorage.getItem("authToken");
  if (!userString) {
    status.value = "Ошибка: пользователь не авторизован";
    return;
  }
  try {
    status.value = "Выполнение запроса...";
    const credentials = {
      query: textRequest.value,
      user: userString,
    };
    const response = await sqlStore.executeSqlReq(credentials);
    if (response) {
      if (!response.is_result) {
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
      } else {
        testDataTable.value = {
          name: response.name || "Результат запроса",
          headers: response.headers || [],
          data: response.data || [],
        };
      }
      status.value = "Запрос выполнен успешно";
    }
  } catch (error) {
    console.error("Ошибка запроса:", error);
    status.value = "Ошибка при выполнении запроса";
    testDataTable.value = null;
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
};
</script>

<style lang="scss" scoped>
.sandbox {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  padding: 20px;
  font-family: Arial, sans-serif;
  max-width: 1800px;
  margin: 0 auto;
  position: relative;
}

.main-workspace {
  display: flex;
  gap: 20px;
  flex: 1;
  margin-bottom: 20px;
}

.tables-container {
  flex: 1;
  position: relative;
  min-height: 400px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  padding: 15px;
}

.right-container {
  background: white;
  border: 1px solid #ddd;
  width: 450px;
  border-radius: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  .result-table {
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    overflow: hidden;
    .table-header {
      padding: 10px;
      background-color: #4a6fa5;
      color: white;
      h3 {
        margin: 0;
        font-size: 16px;
      }
    }
    .table-content {
      max-height: 300px;
      overflow-y: auto;
      table {
        width: 100%;
        border-collapse: collapse;
        th,
        td {
          padding: 8px 12px;
          border: 1px solid #e0e0e0;
        }
        th {
          background-color: #f2f2f2;
          position: sticky;
          top: 0;
        }
        .empty-message {
          text-align: center;
          color: #888;
          font-style: italic;
        }
      }
    }
  }

  h3 {
    color: #000;
  }

  .empty-state {
    color: #888;
    text-align: center;
    padding: 20px;
  }
}

.result-table {
  position: absolute;
  color: #000; // удалить
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;

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
      font-size: 16px;
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
        padding: 10px 12px;
        border: 1px solid #e0e0e0;
        text-align: left;
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

      .cell-content {
        max-width: 200px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
    }
  }
}

.status-section {
  margin: 20px 0;

  h3 {
    margin-bottom: 10px;
    font-size: 18px;
    color: #444;
  }

  .status-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
    color: #000;

    li {
      padding: 8px 12px;
      background-color: #f5f5f5;
      border-radius: 4px;
      margin-bottom: 5px;
    }
  }
}

.editor {
  margin: 30px 0;

  textarea {
    width: 100%;
    min-height: 120px;
    padding: 12px;
    border: 1px solid #ccc;
    border-radius: 6px;
    font-family: monospace;
    font-size: 14px;
    resize: vertical;
    margin-bottom: 15px;

    &:focus {
      outline: none;
      border-color: #4a6fa5;
      box-shadow: 0 0 0 2px rgba(74, 111, 165, 0.2);
    }
  }

  .submit-btn {
    padding: 12px 25px;
    background-color: #4a6fa5;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.2s;

    &:hover {
      background-color: #3a5a8f;
    }

    &:active {
      background-color: #2a4a7f;
    }
  }
}
</style>

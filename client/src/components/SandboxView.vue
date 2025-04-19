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
          {{ testDataTable }}
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
import { ref, reactive, onMounted } from "vue";

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
  testDataTable.value = null;
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
      status.value = "Запрос выполнен успешно";
      testDataTable.value = response;
    }
  } catch (error) {
    console.error("Ошибка запроса:", error);
    status.value = "Ошибка при выполнении запроса";
  }
};

const executeQuery = () => {
  const newTables = [
    {
      name: "Сотрудники",
      headers: ["ID", "Имя", "Должность", "Зарплата"],
      data: [
        [1, "Ivan", "Developer", "100т.р"],
        [2, "Arseniy", "Developer", "100 т.р"],
        [3, "Daniil", "Developer", "100 т.р"],
        [3, "Ilya", "Developer", "100 т.р"],
        [4, "Artem", "Designer", "100 т.р"],
      ],
      position: { x: 20, y: 20 },
      width: 450,
      isDragging: false,
    },
    {
      name: "Отделы",
      headers: ["ID", "название", "оценка"],
      data: [
        [1, "ekra", 4],
        [2, "alkona", 3],
        [3, "ekra dss", 5],
      ],
      position: { x: 100, y: 100 },
      width: 400,
      isDragging: false,
    },
  ];

  resultTables.push(...newTables);
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

onMounted(() => {
  executeQuery();
});
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
  width: 300px;
  min-height: 400px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  padding: 15px;

  h3 {
    margin-top: 0;
    color: #444;
    padding-bottom: 10px;
    border-bottom: 1px solid #ddd;
  }

  .right-content {
    padding: 10px 0;
    color: #000;

    p {
      margin: 8px 0;
      padding: 8px 12px;
      background: #f0f0f0;
      border-radius: 4px;
      cursor: pointer;

      &:hover {
        background-color: #e0e0e0;
      }
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

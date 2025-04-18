<template>
  <div class="sandbox">
    <h2>Песочница</h2>
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
            <!-- вместо буквы Х иконку креста -->
            <button class="close-btn" @click="removeTable(index)" title="Закрыть">х</button>
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
    <div class="status">Статус: Готов к работе</div>

    <div class="editor">
      <textarea placeholder="Введите SQL-запрос..."></textarea>
    </div>

    <button @click="executeQuery">Выполнить</button>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";

const resultTables = reactive([]);
const tablesContainer = ref(null);
const activeDragIndex = ref(null);
const dragOffset = reactive({ x: 0, y: 0 });

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
  position: relative;
  padding: 20px;
  height: calc(100vh - 60px);
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;

  .editor {
    margin: 20px 0;

    textarea {
      width: 100%;
      min-height: 100px;
      padding: 12px;
      border: 1px solid #ddd;
      border-radius: 6px;
      resize: vertical;
      font-size: 14px;

      &:focus {
        outline: none;
        border-color: #42b983;
        box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
      }
    }
  }

  button {
    padding: 10px 20px;
    background-color: #42b983;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    margin-bottom: 20px;
    align-self: flex-start;
    font-size: 14px;
    transition: background-color 0.2s;

    &:hover {
      background-color: #3aa876;
    }

    &:active {
      transform: translateY(1px);
    }
  }

  .tables-container {
    position: relative;
    flex-grow: 1;
    border: 1px dashed #d1d5db;
    border-radius: 8px;
    overflow: hidden;
    background-color: #f9fafb;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
  }

  .result-table {
    position: absolute;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 10;
    user-select: none;
    min-width: 200px;
    max-width: 800px;
    display: flex;
    flex-direction: column;
    overflow: hidden;

    .table-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 15px;
      background-color: #42b983;
      color: white;
      cursor: grab;
      user-select: none;

      &:active {
        cursor: grabbing;
      }

      h3 {
        margin: 0;
        font-size: 15px;
        font-weight: 500;
      }

      .table-controls {
        display: flex;
        gap: 8px;
        align-items: center;

        button {
          margin: 0;
          padding: 2px 6px;
          background: rgba(255, 255, 255, 0.2);
          border-radius: 4px;
          font-size: 14px;
          line-height: 1;
          transition: background 0.2s;

          &:hover {
            background: rgba(255, 255, 255, 0.3);
          }
        }
      }
    }

    .table-content {
      overflow-x: auto;
      flex-grow: 1;
      max-height: 400px;
    }

    table {
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;

      th,
      td {
        padding: 10px 12px;
        border: 1px solid #e5e7eb;
        text-align: left;
      }

      .cell-content {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        max-width: 100%;
      }

      th {
        background-color: #f9fafb;
        position: sticky;
        top: 0;
        font-weight: 500;
        color: #374151;
      }

      tr:nth-child(even) {
        background-color: #f9fafb;
      }

      tr:hover {
        background-color: #f3f4f6;
      }
    }
  }
}
</style>

<template>
  <div class="debugger-container">
    <div class="debugger-controls">
      <button class="nav-btn" :disabled="currentStep <= 0" @click="moveCursor(-1)">&larr;</button>
      <button class="nav-btn" :disabled="currentStep >= steps.length - 1" @click="moveCursor(1)">
        &rarr;
      </button>
      <span class="step-info">Шаг {{ currentStep + 1 }} из {{ steps.length }}</span>
    </div>

    <div class="sql-preview">
      <div class="code-line active-line">
        <span class="cursor">&#9658;</span>
        {{ steps[currentStep]?.sql || "" }}
      </div>
    </div>

    <div class="result-table static-table" v-if="currentResult">
      <div class="table-header">
        <h3>{{ currentResult.name || "Результат шага" }}</h3>
      </div>
      <div class="table-content">
        <table>
          <thead>
            <tr>
              <th v-for="(header, i) in currentResult.headers" :key="i">{{ header }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(row, rowIndex) in currentResult.data" :key="rowIndex">
              <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch } from "vue";
import { useSqlRequest } from "@/stores/store";

const sqlStore = useSqlRequest();
const currentStep = ref(0);
const executionSteps = ref<any[]>([]);

const props = defineProps({
  debugMessage: {
    type: String,
    required: false,
    default: "",
  },
  userString: {
    type: String,
    required: false,
    default: "",
  },
});

const steps = computed(() => {
  return executionSteps.value.map((step) => ({
    sql: step.sql,
    result: step.result,
  }));
});

const currentResult = computed(() => {
  return executionSteps.value[currentStep.value]?.result || null;
});

const moveCursor = (direction: number): void => {
  const newStep = currentStep.value + direction;
  if (newStep >= 0 && newStep < steps.value.length) {
    currentStep.value = newStep;
  }
};

const parseExecutionSteps = (response: any): any[] => {
  const steps = [];
  for (const [key, result] of Object.entries(response)) {
    steps.push({
      sql: key,
      result: result,
    });
  }
  if (steps.length === 0) {
    steps.push({
      sql: props.debugMessage,
      result: response,
    });
  }
  return steps;
};

const executeStepSqlRequest = async (): Promise<void> => {
  if (!props.debugMessage.trim() || !props.userString) return;
  try {
    const credentials = {
      query: props.debugMessage,
      user: props.userString,
    };
    const response = await sqlStore.executeSqlStep(credentials);
    executionSteps.value = parseExecutionSteps(response);
    currentStep.value = 0;
  } catch (error) {
    console.error("Step execution error:", error);
  }
};

watch(
  () => props.debugMessage,
  (newVal) => {
    if (newVal) {
      executeStepSqlRequest();
    }
  },
  { immediate: true }
);
</script>

<style lang="scss" scoped>
.debugger-container {
  height: 100%;
  padding: 15px;
  background-color: #1e1e1e;
  border-radius: 6px;
  border: 1px solid #3c3c3c;
  color: #e0e0e0;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.debugger-controls {
  display: flex;
  gap: 10px;

  .nav-btn {
    background: #4a6fa5;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 5px 15px;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.2s;

    &:hover:not(:disabled) {
      background: #3a5a8a;
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
}

.sql-preview {
  background-color: #252526;
  border-radius: 4px;
  padding: 10px;
  font-family: "Consolas", monospace;
  font-size: 13px;
  white-space: pre;
}

.code-line {
  padding: 2px 0;
  position: relative;
  line-height: 1.5;

  &.active-line {
    background-color: rgba(74, 111, 165, 0.2);
  }
}

.cursor {
  color: #69f0ae;
  margin-right: 5px;
  animation: blink 1s infinite;
}

.static-table {
  position: relative !important;
  left: auto !important;
  top: auto !important;
  width: 100% !important;
  margin-top: 10px;
  cursor: default;

  .table-header {
    cursor: default;
  }
}

.result-table {
  background: #252526;
  border: 1px solid #3c3c3c;
  border-radius: 6px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  overflow: hidden;
  color: #e0e0e0;

  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 15px;
    background: #4a6fa5;
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

@keyframes blink {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-thumb {
  background-color: #4a4a4a;
  border-radius: 4px;
}

::-webkit-scrollbar-track {
  background-color: #2d2d2d;
}
</style>

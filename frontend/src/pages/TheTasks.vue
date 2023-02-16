<template>
  <div class="grid-container">
    <the-header class="header" />
    <div class="grid-item-todo">
      <post-it>
        <div
          v-if="!display && !isLoading"
          class="no-tasks"
          style="display: flex; flex-direction: column"
        >
          <div>
            {{ formatDate(new Date(date)) }}
          </div>
          <h2>No Tasks to Display</h2>
        </div>

        <div v-else>
          <h1 class="unselectable">
            {{
              formatDate(new Date(tasksSlice.date)) !== "Invalid Date"
                ? formatDate(new Date(tasksSlice.date))
                : ""
            }}
          </h1>
          <div class="flex-headers">
            <div class="header-number">#</div>
            <div class="header-text">Description</div>
            <div class="header-edit" v-show="showButtons">Edit</div>
            <div class="header-delete" v-show="showButtons">Del.</div>
            <div class="header-completed">Status</div>
          </div>
        </div>
        <draggable
          :list="tasksSlice.tasks"
          item-key="task_id"
          @change="taskStore.updatePriority"
        >
          <template #item="{ element }">
            <div class="flexbox">
              <div class="flex-id">
                <p>{{ element.priority }}</p>
              </div>
              <div
                class="flex-text"
                :class="{ editSelectedBorder: element.editable }"
                @dblclick="taskStore.checkUncheck(element)"
              >
                <p
                  :contenteditable="element.editable"
                  @input="editText"
                  @blur="taskStore.applyEditChanges(element)"
                >
                  {{ element.text }}
                </p>
              </div>
              <div
                class="flex-buttons"
                @mouseover="showButtons = element.priority"
                @mouseout="showButtons = null"
              >
                <img
                  src="@/assets/tasks/edit.png"
                  class="edit-img"
                  v-show="showButtons === element.priority"
                  @click="makeEditable(element)"
                  :class="{ editSelected: element.editable }"
                />
                <img
                  src="@/assets/tasks/delete.png"
                  alt="delete-image"
                  class="delete-img"
                  @click="taskStore.deleteTask(element)"
                  v-show="showButtons === element.priority"
                />
                <img
                  @click="taskStore.checkUncheck(element)"
                  :src="element.completed ? urls[0] : urls[1]"
                  alt="status"
                  class="status-img"
                />
              </div>
            </div>
          </template>
        </draggable>
        <div>
          <form
            class="form-control"
            @submit.prevent="taskStore.addNewTask"
            v-if="!isLoading"
          >
            <input
              class="task-input"
              @blur="taskStore.clearInvalidInput"
              @keyup="taskStore.clearInvalidInput"
              v-model="enteredText"
              type="text"
              aria-label="Add task"
            />
            <button class="button-74">add task</button>
          </form>
          <the-spinner v-else></the-spinner>
        </div>
        <span v-if="invalidInput" class="invalid-input">Please Enter Text</span>
      </post-it>
    </div>

    <div class="grid-item-calendar">
      <h1>{{ date }}</h1>
      <Datepicker
        inline
        :enableTimePicker="false"
        :monthChangeOnScroll="false"
        v-model="date"
        autoApply
        @update:modelValue="handleDate"
      />
      <div v-if="totalTasks" class="task-status">
        <p>
          # Tasks: <span id="total-tasks">{{ totalTasks }}</span>
        </p>
        <p>
          # Completed tasks:
          <span id="complete-tasks">{{ completedTasks }}</span>
        </p>
        <p>
          # Not completed tasks:
          <span id="uncomplete-tasks">{{ notCompletedTasks }}</span>
        </p>
      </div>
    </div>
    <the-footer class="footer" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import draggable from "vuedraggable";
import PostIt from "../components/layout/PostIt.vue";

import TheSpinner from "@/components/layout/TheSpinner.vue";

import { storeToRefs } from "pinia";
import { useTaskStore } from "../components/store/TaskStore";
import { useAuthStore } from "../components/store/userAuth";

import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
// eslint-disable-next-line
const authStore = useAuthStore();
const taskStore = useTaskStore();

const {
  display,
  tasksList,
  tasksSlice,
  date,
  invalidInput,
  enteredText,
  editedText,
  isLoading,
} = storeToRefs(taskStore);

// const editedText = ref("");

const showButtons = ref(null);

// Count the number of tasks WILL BE USED IN WATCHER
const notCompletedTasks = ref(null);
const completedTasks = ref(null);
const totalTasks = ref(null);
// count number of Not completed tasks
if (tasksSlice.value.length > 0) {
  notCompletedTasks.value = tasksSlice.value.tasks.filter(
    (ob) => !ob.completed
  ).length;
}

onMounted(async () => {
  tasksList.value = await taskStore.loadTasks();
  taskStore.loadOneTask(date.value);
});

watch([tasksSlice], () => {
  if ("date" in tasksSlice.value) {
    totalTasks.value = tasksSlice.value.tasks.length;
    notCompletedTasks.value = tasksSlice.value.tasks.filter(
      (ob) => !ob.completed
    ).length;
    completedTasks.value = totalTasks.value - notCompletedTasks.value;
  } else {
    totalTasks.value = null;
    completedTasks.value = null;
    notCompletedTasks.value = null;
  }
});

// custom function to return date in DD month-long YYYY format
function formatDate(dateInput) {
  return dateInput.toLocaleDateString("en-US", {
    month: "long",
    year: "numeric",
    day: "numeric",
  });
}

// WORKING WITH CALENDAR

const handleDate = (modelData) => {
  date.value = modelData.toISOString().slice(0, 10);
  // getting new slice based on picked date
  tasksSlice.value = tasksList.value.filter(
    (arr) => arr["date"] === date.value
  )[0];
  display.value = true;
  // creating empty array if there no tasks on picked date
  if (!tasksSlice.value) {
    tasksSlice.value = ref([]);
    display.value = false;
  }
  taskStore.loadOneTask(date.value);
};

// listen to input inside edited paragraph text
function editText(event) {
  editedText.value = event.target.innerText;
}

// make SELECTED paragraph tag editable
// No link with backend here - elements become uneditable after refresh
function makeEditable(element) {
  tasksSlice.value.tasks.forEach((el, idx) => {
    if (element.task_id == el.task_id) {
      tasksSlice.value.tasks[idx].editable =
        !tasksSlice.value.tasks[idx].editable;
    }
  });
}

// WORKING WITH IMAGES
const urls = ref([
  require("@/assets/tasks/checked_box.png"),
  require("@/assets/tasks/uncheck.png"),
]);
</script>

<style scoped>
* {
  font-family: "Kalam", cursive;
}

h1 {
  text-align: center;
}
.unselectable {
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  -o-user-select: none;
  user-select: none;
}

.form-control {
  margin-top: 20px;
  display: flex;
  height: 40px;
  justify-content: space-between;
  margin-bottom: 10px;
}

.task-input {
  width: 80%;
  margin-left: 30px;
  margin-right: 10px;
  line-height: 25px;
  font-size: 18px;
  background-color: #fbeee0;
  border: 2px solid #422800;
}

.no-tasks {
  height: 100px;
  justify-content: center;
  display: flex;
  align-items: center;
  font-weight: bold;
  font-size: 20px;
  margin-top: 40px;
}

/* GENERAL PAGE LAYOUT WITH GRIDS */
.grid-container {
  min-height: 100vh;
  display: grid;
  grid-template-areas:
    "header header"
    "todo calendar"
    "footer footer";
  grid-template-rows: 60px 1fr 60px;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.grid-item-todo {
  grid-area: todo;
}
.grid-item-calendar {
  grid-area: calendar;
  /* background: #e7e7b6; */
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: 1fr;
    grid-template-rows: 50px 1fr 1fr 50px;
    gap: 1px;
  }
  .header {
    grid-row: 1;
  }
  .grid-item-todo {
    margin-top: 2px;
    grid-row: 2;
    grid-column: 1;
  }
  .grid-item-calendar {
    grid-row: 3;
    grid-column: 1;
  }
  .footer {
    grid-row: 4/5;
  }
  .form-control {
    flex-direction: column;
    align-items: center;
    margin-bottom: 60px;
  }
  .button-74 {
    width: 90px;
    flex-shrink: 0;
    margin-top: 10px;
    margin-right: 40px;
  }
}

/* TO-DO HEADINGS WITH FLEXBOX */

.flex-headers {
  display: flex;
  /* background-color: rgb(153, 185, 66); */
  border-bottom: 2px solid black;
  margin: 0px 10px;
  font-size: 16px;
  padding: 5px 0px;
  font-weight: bold;
}
.header-number {
  text-align: center;
  justify-content: center;
  align-content: center;
  align-items: center;
  flex-basis: 20px;
}
.header-text {
  /* flex-grow: 1; */
  margin-right: auto;
  margin-left: 10px;
}

.header-edit,
.header-delete,
.header-completed {
  margin-right: 5px;
}

/* TO-DO INNER LAYOUT WITH FLEXBOX */

.flexbox {
  display: flex;
  justify-content: space-between;
  margin: 0 10px;
  cursor: default;
}

.flex-id {
  flex-basis: 15px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 3px;
}
.flex-id p {
  font-weight: bold;
  margin-block-start: 0px;
  margin-block-end: 0px;
}
.flex-text {
  /* background: lightgray; */
  text-align: justify;
  margin-left: 15px;
  flex: 1;
  line-height: 12pt;
}
.flex-text p {
  outline: none;
}
p {
  margin-block-start: 10px;
  margin-block-end: 0px;
}

/* Change border of the text if edit is selected*/

.editSelectedBorder {
  border: 0.5px solid orange;
  cursor: auto;
}
.flex-buttons {
  /* background: lightyellow; */
  flex-basis: 70px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 3px;
}

/* EDIT */
.edit-img {
  width: 30px;
  height: 30px;
  margin-right: -5px;
}
.editSelected {
  transform: rotate(19deg);
}
/* DELETE */
.delete-img {
  width: 30px;
  height: 30px;
}
.delete-img:hover {
  filter: invert(39%) sepia(5%) saturate(4834%) hue-rotate(314deg)
    brightness(91%) contrast(100%);
}
/* CHECKBOX */
.status-img {
  width: 30px;
  height: 30px;
  margin-left: auto;
  margin-right: 5px;
}

/* BUTTON */
.button-74 {
  background-color: #fbeee0;
  border: 2px solid #422800;
  border-radius: 25px;
  box-shadow: #422800 3px 3px 0 0;
  color: #422800;
  cursor: pointer;
  font-weight: 300;
  font-size: 16px;
  padding: 0 18px;
  line-height: 20px;
  text-align: center;
  text-decoration: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  flex: 0;
  margin-right: 15px;
  flex-basis: 100px;
}

.button-74:hover {
  background-color: #fff;
}

.button-74:active {
  box-shadow: #422800 2px 2px 0 0;
  transform: translate(2px, 2px);
}

.invalid-input {
  color: #b04b4b;
  margin-right: 50px;
  font-weight: bold;
}
.task-status p {
  display: inline-block;
  margin-right: 20px;
}
#total-tasks {
  color: black;
  font-weight: bold;
}
#complete-tasks {
  color: #479d16;
  font-weight: bold;
}
#uncomplete-tasks {
  color: #841460;
  font-weight: bold;
}
</style>

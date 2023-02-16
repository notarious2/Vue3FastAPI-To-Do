<template>
  <div class="grid-container">
    <the-header class="header" />
    <div class="demo">
      <p>
        This page is for demonstration purposes only. All data will be lost
        after a page refresh
      </p>
    </div>
    <div class="grid-item-todo">
      <post-it>
        <div
          v-if="!display"
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
          @change="updateList"
        >
          <template #item="{ element }">
            <div class="flexbox">
              <div class="flex-id">
                <p>{{ element.priority }}</p>
              </div>
              <div
                class="flex-text"
                :class="{ editSelectedBorder: element.editable }"
              >
                <p
                  :contenteditable="element.editable"
                  @input="editText"
                  @blur="applyEditChanges(element)"
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
                  @click="deleteTask(element)"
                  v-show="showButtons === element.priority"
                />
                <img
                  @click="checkUncheck(element)"
                  :src="element.completed ? urls[0] : urls[1]"
                  alt="status"
                  class="status-img"
                />
              </div>
            </div>
          </template>
        </draggable>
        <div>
          <form class="form-control" @submit.prevent="addTask">
            <input
              class="task-input"
              @blur="clearInvalidInput"
              @keyup="clearInvalidInput"
              v-model="enteredText"
              type="text"
              aria-label="Add task"
            />
            <button class="button-74">add task</button>
          </form>
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
import { ref, watch, reactive } from "vue";
import draggable from "vuedraggable";
import PostIt from "../components/layout/PostIt.vue";

import Datepicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";

const date = ref(new Date().toISOString().slice(0, 10));
const invalidInput = ref(false);
const enteredText = ref("");
const editedText = ref("");
const tasksList = reactive([]);

// Getting array for specific date
const tasksSlice = ref([]);
const display = ref(false);
if (tasksList.filter((arr) => arr["date"] === "2022-11-28").length === 0) {
  // eslint-disable-next-line
  display.value = false;
} else {
  tasksSlice.value = tasksList.filter((arr) => arr["date"] === "2022-11-28")[0];
  display.value = true;
}
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

watch(
  [tasksSlice],
  () => {
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
  },
  { deep: true }
);

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
  tasksSlice.value = tasksList.filter((arr) => arr["date"] === date.value)[0];
  display.value = true;
  // creating empty array if there no tasks on picked date
  if (!tasksSlice.value) {
    tasksSlice.value = ref([]);
    display.value = false;
  }
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
// apply changes
function applyEditChanges(element) {
  if (editedText.value) {
    tasksSlice.value.tasks.forEach((el, idx) => {
      if (element.task_id === el.task_id) {
        tasksSlice.value.tasks[idx].text = editedText.value;
      }
    });
  }
}
// WORKING WITH IMAGES
const urls = ref([
  require("@/assets/tasks/checked_box.png"),
  require("@/assets/tasks/uncheck.png"),
]);

// adding the task
function addTask() {
  if (enteredText.value !== "") {
    // add date if empty object
    if (!("date" in tasksSlice.value)) {
      tasksSlice.value = { date: date.value, tasks: [] };
    }
    tasksSlice.value.tasks.push({
      text: enteredText.value,
      priority: tasksSlice.value.tasks.length + 1,
      completed: false,
      task_id: (Math.random() + 1).toString(36).substring(7),
    });
    enteredText.value = "";
    display.value = true;
    tasksList.push(tasksSlice.value);
  } else {
    invalidInput.value = true;
  }
}
// clear invalid input - to be used at blur
function clearInvalidInput() {
  invalidInput.value = false;
}
// Deleting tasks
function deleteTask(element) {
  let index = tasksSlice.value.tasks.indexOf(element);
  tasksSlice.value.tasks.splice(index, 1);
  if (tasksSlice.value.tasks.length === 0) {
    display.value = false;
  }
  updateList();
}
// Checking or unchecking specific object in an array
function checkUncheck(element) {
  let index = tasksSlice.value.tasks.indexOf(element);
  tasksSlice.value.tasks[index].completed =
    !tasksSlice.value.tasks[index].completed;
}
// update tasks index/id on change - on drag
function updateList() {
  tasksSlice.value.tasks.forEach((element, index) => {
    tasksSlice.value.tasks[index].priority = index + 1;
  });
}
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
    "demo demo"
    "todo calendar"
    "footer footer";
  grid-template-rows: 60px 60px 1fr 60px;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.grid-item-todo {
  grid-area: todo;
}
.demo {
  grid-area: demo;
  margin: 5px;
  border: 2px solid rgb(107, 4, 4);
  background-color: #a48399;
  max-width: 800px;
  min-width: 600px;
  align-self: center;
  justify-self: center;
  padding: 5px;
}
.demo p {
  display: inline;
  font-weight: bold;
}
.grid-item-calendar {
  grid-area: calendar;
  /* background: #e7e7b6; */
}

@media (max-width: 768px) {
  .grid-container {
    grid-template-columns: 1fr;
    grid-template-rows: 50px 50px 1fr 1fr 50px;
    gap: 1px;
  }
  .header {
    grid-row: 1;
  }
  .demo {
    grid-row: 2;
  }
  .grid-item-todo {
    margin-top: 2px;
    grid-row: 3;
    grid-column: 1;
  }
  .grid-item-calendar {
    grid-row: 4;
    grid-column: 1;
  }
  .footer {
    grid-row: 5/6;
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

import { defineStore } from "pinia";
import axios from "axios";
import authHeader from "../services/auth-header";

export const useTaskStore = defineStore("tasks", {
  state: () => ({
    display: false,
    tasksList: [],
    tasksSlice: [],
    date: new Date().toISOString().slice(0, 10),
    enteredText: "",
    editedText: "",
    invalidInput: false,
    isLoading: false,
  }),
  actions: {
    async loadTasks() {
      this.isLoading = true;
      try {
        const response = await axios.get("task/", {
          headers: authHeader(),
        });
        // working with response
        const result = response.data;
        const newArray = [];
        result.forEach((element) => {
          if (
            !newArray.filter((arr) => arr["date"] === element.date).length > 0
          ) {
            newArray.push({
              date: element.date,
              tasks: [{ ...element, editable: false }],
            });
          } else {
            const idx = newArray.findIndex((arr) => arr.date === element.date);
            newArray[idx].tasks.push({ ...element, editable: false });
          }
        });
        // tasksList.value = newArray;
        this.isLoading = false;
        console.log("Load...");
        return newArray;
      } catch (err) {
        console.log(err);
      }
    },
    loadOneTask(task_date) {
      if (
        this.tasksList.filter((arr) => arr["date"] === task_date).length === 0
      ) {
        this.display = false;
        this.tasksSlice = [];
      } else {
        // console.log(tasksList.value.filter((arr) => arr["date"] === task_date)[0]);
        this.tasksSlice = this.tasksList.filter(
          (arr) => arr["date"] === task_date
        )[0];
        this.display = true;
        // SORT THE SLICE
        this.tasksSlice.tasks.sort((a, b) =>
          a.priority > b.priority ? 1 : b.priority > a.priority ? -1 : 0
        );
      }
    },

    // Checking or unchecking specific object in an array
    async checkUncheck(element) {
      try {
        await axios.patch(
          "task/" + element.task_id,
          { completed: element.completed ? false : true },
          { headers: authHeader() }
        );
        console.log("Completed!");
        // rerender ALL to-do tasks
        this.tasksList = await this.loadTasks();
        // get selected date's slice
        this.loadOneTask(this.date);
      } catch (err) {
        console.log(err);
      }
    },
    // adding the task - Post Request
    async addNewTask() {
      // priority is 1 if there are not tasks on that day, else it is autoincremented
      const priority =
        "date" in this.tasksSlice ? this.tasksSlice.tasks.length + 1 : 1;
      if (this.enteredText !== "") {
        try {
          await axios.post(
            "task/",
            {
              priority: priority,
              date: this.date,
              text: this.enteredText,
              completed: false,
            },
            {
              headers: authHeader(),
            }
          );
          console.log("Added!");

          // rerender ALL to-do tasks
          this.tasksList = await this.loadTasks();
          // get selected date's slice
          this.loadOneTask(this.date);
          //clear input field
          this.enteredText = "";
        } catch (err) {
          console.log(err);
        }
      } else {
        this.invalidInput = true;
      }
    },
    // clear invalid input - to be used at blur
    clearInvalidInput() {
      this.invalidInput = false;
    },
    // Deleting specific task

    async deleteTask(element) {
      try {
        await axios.delete("task/" + element.task_id, {
          headers: authHeader(),
        });

        // rerender ALL to-do tasks
        console.log("Deleted!");
        this.tasksList = await this.loadTasks();
        // get selected date's slice
        this.loadOneTask(this.date);
      } catch (err) {
        console.log(err);
      }
      this.updatePriority();
    },
    // update tasks index/id on change - on drag / also used for deletion
    async updatePriority() {
      // GET changed priorities FIRST
      const prioritiesList = {};
      for (const idx in this.tasksSlice.tasks) {
        if (this.tasksSlice.tasks[idx].priority !== Number(idx) + 1) {
          prioritiesList[this.tasksSlice.tasks[idx].task_id] = Number(idx) + 1;
        }
      }
      if (Object.keys(prioritiesList).length > 0) {
        const payload = {};
        payload["update"] = prioritiesList;
        // Update MULTIPLE field with ONE PATCH Request
        try {
          await axios.patch(
            "task/update/order",
            {
              ...payload,
            },
            {
              headers: authHeader(),
            }
          );
          console.log("Multiple Rows Update!");
        } catch (err) {
          console.log(err);
        }
        this.tasksList = await this.loadTasks();
        this.loadOneTask(this.date);
      }
    },

    // Apply EDIT changes at blur
    async applyEditChanges(element) {
      // No need to send HTTP request if Text is unchanged
      if (this.editedText && this.editedText !== element.text) {
        try {
          await axios.patch(
            "task/" + element.task_id,
            { text: this.editedText },
            { headers: authHeader() }
          );
          console.log("Edited!");
          // rerender ALL to-do tasks
          this.tasksList = await this.loadTasks();
          // get selected date's slice
          this.loadOneTask(this.date);
        } catch (err) {
          console.log(err);
        }
      }
    },
  },
});

import { defineStore } from "pinia";
import authHeader from "@/components/services/auth-header";
import axios from "@/axios"


export const useTaskStore = defineStore("tasks", {
  state: () => ({
    currentDate: new Date().toISOString().slice(0, 10),
    enteredText: "",
    editedText: "",
    invalidInput: false,
    isLoading: false,
    currentTasks: []
  }),
  actions: {
    formattedDate(date) {
      return date.toISOString().split('T')[0]
    },
    // TODO: make it a getter
    getChangedPriorities() {
      const changedPriorities = {};
      for (const [index, task] of this.currentTasks.entries()) {
        if (task.priority !== index + 1) {
          changedPriorities[task.id] = index + 1
          task.priority = index + 1;
        }
      }
      return changedPriorities;
    },
    async loadTasksByDate(date) {
      const formatted_date = this.formattedDate(date)
      try {
        const response = await axios.get("task/", { params: { selected_date: formatted_date }, headers: authHeader() })
        this.currentTasks = response.data
        // add editable false
        this.currentTasks.forEach((task) => {
          task.editable = false;
        })

      } catch (err) {
        console.log(`Error when getting task for date ${date}, $(err)`)
      }

    },

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
        this.isLoading = false;
        console.log("Load...");
        return newArray;
      } catch (err) {
        console.log(err);
      }
    },
    async updateTask(updatedTask) {
      const index = this.currentTasks.findIndex(task => task.id === updatedTask.id);
      if (index !== -1) {
        // Replace the object at the found index with the new object
        this.currentTasks[index] = updatedTask;
      }
    },

    // Checking or unchecking specific object in an array
    async checkUncheck(task) {
      try {
        const response = await axios.patch(
          `task/${task.id}/`,
          { completed: task.completed ? false : true },
          { headers: authHeader() }
        );
        await this.updateTask(response.data)
      } catch (err) {
        console.log(err);
      }
    },
    async applyEditChanges(task) {
      if (this.editedText && this.editedText !== task.text) {
        try {
          const response = await axios.patch(
            `task/${task.id}/`,
            { text: this.editedText },
            { headers: authHeader() }
          );
          await this.updateTask(response.data)
        } catch (err) {
          console.log(err);
        }
      }
    },
    // adding the task - Post Request
    async addNewTask() {
      // priority is 1 if there are not tasks on that day, else it is autoincremented
      const priority = this.currentTasks.length === 0 ? 1 : this.currentTasks.length + 1
      if (this.enteredText !== "") {
        this.isLoading = true;
        try {
          const response = await axios.post(
            "task/",
            {
              priority: priority,
              text: this.enteredText,
              posted_at: this.currentDate
            },
            {
              headers: authHeader(),
            }
          );
          this.currentTasks.push(response.data)
          this.enteredText = "";
        } catch (err) {
          console.log(err);
        }
        this.isLoading = false;
      } else {
        this.invalidInput = true;
      }
    },
    // clear invalid input - to be used at blur
    clearInvalidInput() {
      this.invalidInput = false;
    },
    // Deleting specific task

    async deleteTask(task) {
      try {
        await axios.delete(`task/${task.id}/`, {
          headers: authHeader(),
        });

        // remove deleted task from the array
        this.currentTasks = this.currentTasks.filter(element => element.id !== task.id);

      } catch (err) {
        console.log(err);
      }
      this.updateTaskPriorities();
    },
    async updateTaskPriorities() {
      const changedPriorities = this.getChangedPriorities();
      if (Object.keys(changedPriorities).length === 0) {
        return
      }

      // taskPriorities hold id/newPriority key-value pairs
      try {
        await axios.patch("task/update-order/",
          {
            priorities: changedPriorities,
          },
          {
            headers: authHeader(),
          }
        )
      }
      catch (err) {
        console.log("Error updating priorities", err);
      }
    },
  },
});

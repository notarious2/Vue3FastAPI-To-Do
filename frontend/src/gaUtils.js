import { event } from "vue-gtag";

export const trackTaskCreatedGA = async () => {
    event("task-created", {
        event_category: "analytics",
        event_label: "Task",
        value: 1,
    });
};

export const trackTaskDeletedGA = async () => {
    event("task-deleted", {
        event_category: "analytics",
        event_label: "Task",
        value: 1,
    });
};

export const trackTaskCheckedUncheckedGA = async () => {
    event("task-checked-unchecked", {
        event_category: "analytics",
        event_label: "Task",
        value: 1,
    });
};

export const trackTaskDraggedGA = async () => {
    event("task-dragged", {
        event_category: "analytics",
        event_label: "Task",
        value: 1,
    });
};

export const trackTaskEditedGA = async () => {
    event("task-edited", {
        event_category: "analytics",
        event_label: "Task",
        value: 1,
    });
};

export const trackUserLoggedInGA = async () => {
    event("user-logged-in", {
        event_category: "analytics",
        event_label: "User",
        value: 1,
    });
};

export const trackUserRegistrationGA = async () => {
    event("user-registered", {
        event_category: "analytics",
        event_label: "User",
        value: 1,
    });
};


export const TASK_STATUS = [
  "PENDING",
  "IN_PROGRESS",
  "COMPLETED",
  "OVERDUE",
] as const;

export const TASK_STATUS_OPTIONS = [
  { value: "PENDING", label: "Pending" },
  { value: "IN_PROGRESS", label: "In Progress" },
  { value: "COMPLETED", label: "Completed" },
  { value: "OVERDUE", label: "Overdue" },
];

export const TASK_PRIORITY = [
  "OPTIONAL",
  "NORMAL",
  "HIGH",
  "IMPORTANT",
] as const;

export const TASK_PRIORITY_OPTIONS = [
  { value: "OPTIONAL", label: "Optional" },
  { value: "NORMAL", label: "Normal" },
  { value: "HIGH", label: "High" },
  { value: "IMPORTANT", label: "Important" },
];

export type TaskItem = {
  task_id: string;
  user_id: string;
  title: string;
  description: string | null;
  file_storage_id: string | null;
  image_url: string | null;
  status: string;
  priority: TaskPriority;
  due_at: string | null;
  completed_at: string | null;
  created_by: string | null;
  updated_by: string | null;
  created_at: string;
  updated_at: string;
};

export type TasksGetResponse = {
  items: TaskItem[];
  limit: number;
  offset: number;
  has_more: boolean;
  total_tasks: number;
  page: number;
  total_pages: number;
};

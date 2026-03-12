export interface ProgressLog {
  id: number;
  user_id: number;
  weight: number;
  body_fat: number | null;
  date: string;
}

export interface ProgressHistory {
  logs: ProgressLog[];
  total: number;
  page: number;
  page_size: number;
}

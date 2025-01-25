import { ComplexityLevel } from "../types";

export interface EstimationFeed {
  id?: string;
  title: string;
  description: string;
  complexity: ComplexityLevel;
  developer_id: string;
  estimated_time_hours: number;
  actual_time_hours: number;
  tech_stack: string[];
}

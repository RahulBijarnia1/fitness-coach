export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface Profile {
  id: number;
  user_id: number;
  name: string;
  age: number;
  sex: string;
  height: number;
  weight: number;
  body_fat: number | null;
}

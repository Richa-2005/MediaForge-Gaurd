export type AuthUser = {
  id: number;
  email: string;
  full_name: string | null;
  is_active: boolean;
  created_at: string;
};

export type AuthResponse = {
  access_token: string;
  token_type: "bearer";
  user: AuthUser;
};

export type RegisterPayload = {
  email: string;
  password: string;
  full_name?: string;
};

export type LoginPayload = {
  email: string;
  password: string;
};

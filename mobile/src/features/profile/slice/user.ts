import { createSlice, PayloadAction } from "@reduxjs/toolkit";

export type UserState = {
  user_id: string;
  email: string;
  profile_img: string | null;
  role: string;
  is_deleted: boolean;
  deleted_at: string | null;
  created_by: string | null;
  updated_by: string | null;
  created_at: string;
  updated_at: string;
};

const initialState: UserState = {
  user_id: "",
  email: "",
  profile_img: null,
  role: "",
  is_deleted: false,
  deleted_at: null,
  created_by: null,
  updated_by: null,
  created_at: "",
  updated_at: "",
};

export const userSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setUserInfo: (state, action: PayloadAction<UserState>) => {
      state.user_id = action.payload.user_id;
      state.email = action.payload.email;
      state.profile_img = action.payload.profile_img;
      state.role = action.payload.role;
      state.is_deleted = action.payload.is_deleted;
      state.deleted_at = action.payload.deleted_at;
      state.created_by = action.payload.created_by;
      state.updated_by = action.payload.updated_by;
      state.created_at = action.payload.created_at;
      state.updated_at = action.payload.updated_at;
    },
    setUserId: (state, action: PayloadAction<string>) => {
      state.user_id = action.payload;
    },
    setEmail: (state, action: PayloadAction<string>) => {
      state.email = action.payload;
    },
    setProfileImg: (state, action: PayloadAction<string | null>) => {
      state.profile_img = action.payload;
    },
    setRole: (state, action: PayloadAction<string>) => {
      state.role = action.payload;
    },
    setIsDeleted: (state, action: PayloadAction<boolean>) => {
      state.is_deleted = action.payload;
    },
    setDeletedAt: (state, action: PayloadAction<string | null>) => {
      state.deleted_at = action.payload;
    },
    setCreatedBy: (state, action: PayloadAction<string | null>) => {
      state.created_by = action.payload;
    },
    setUpdatedBy: (state, action: PayloadAction<string | null>) => {
      state.updated_by = action.payload;
    },
    setCreatedAt: (state, action: PayloadAction<string>) => {
      state.created_at = action.payload;
    },
    setUpdatedAt: (state, action: PayloadAction<string>) => {
      state.updated_at = action.payload;
    },
    clearUser: () => initialState,
  },
});

export const {
  setUserInfo,
  setUserId,
  setEmail,
  setProfileImg,
  setRole,
  setIsDeleted,
  setDeletedAt,
  setCreatedBy,
  setUpdatedBy,
  setCreatedAt,
  setUpdatedAt,
  clearUser,
} = userSlice.actions;
export const userReducer = userSlice.reducer;

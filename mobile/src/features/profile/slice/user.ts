import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { UserState } from "../types";

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
      Object.assign(state, action.payload);
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
    setUpdatedBy: (state, action: PayloadAction<string | null>) => {
      state.updated_by = action.payload;
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

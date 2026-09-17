import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { UserState } from "../types";

const initialState: UserState = {
  user_id: null,
  email: null,
  profile_img: null,
  role: null,
  is_onboarding_completed: false,
  is_profile_completed: false,
  is_deleted: false,
  deleted_at: null,
  created_by: null,
  updated_by: null,
  created_at: null,
  updated_at: null,
  isProfileCompletionSkipped: false,
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
    setIsOnboardingCompleted: (state, action: PayloadAction<boolean>) => {
      state.is_onboarding_completed = action.payload;
    },
    setIsProfileCompleted: (state, action: PayloadAction<boolean>) => {
      state.is_profile_completed = action.payload;
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
    setIsProfileCompletionSkipped: (state, action: PayloadAction<boolean>) => {
      state.isProfileCompletionSkipped = action.payload;
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
  setIsOnboardingCompleted,
  setIsProfileCompleted,
  setIsDeleted,
  setDeletedAt,
  setUpdatedBy,
  setUpdatedAt,
  clearUser,
  setIsProfileCompletionSkipped,
} = userSlice.actions;

export const userReducer = userSlice.reducer;

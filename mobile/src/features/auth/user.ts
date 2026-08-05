import { createSlice } from "@reduxjs/toolkit";

type UserInfo = {
  hasAccessToken: boolean;
  type: string;
  user: {
    email: string;
    user_id: string;
    role: string;
  };
};

const userInitalState: UserInfo = {
  hasAccessToken: false,
  type: "",
  user: {
    email: "",
    user_id: "",
    role: "",
  },
};

export const userSlice = createSlice({
  name: "user",
  initialState: userInitalState,
  reducers: {
    setUserInfo: (state, action) => {
      // if (state?.hasAccessToken) {
      // need to implement expo secure store here
      // }
      state.hasAccessToken = action.payload.access_token;
      state.type = action.payload.type;
      state.type = action.payload.user;
    },
  },
});

export const { setUserInfo } = userSlice.actions;


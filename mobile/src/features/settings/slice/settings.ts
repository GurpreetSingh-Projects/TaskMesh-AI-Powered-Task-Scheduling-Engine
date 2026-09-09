import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { SettingsState } from "../types";

const initialState: SettingsState = {
  user_settings_id: "",
  needs_reminders: false,
  timezone: "Asia/Kolkata",
  notification_enabled: true,
  preferred_lang: ["en"],
  available_lang: ["en"],
  theme: "light",
  supported_media_types: ["image/jpeg", "image/png", "image/webp"],
  max_image_width: 720,
  max_media_size: 5120,
  image_conversion_format: "image/webp",
  image_quality: 0.75,
};

export const settingsSlice = createSlice({
  name: "settings",
  initialState,
  reducers: {
    setSettings: (state, action: PayloadAction<SettingsState>) => {
      Object.assign(state, action.payload);
    },

    setNeedsReminders: (state, action: PayloadAction<boolean>) => {
      state.needs_reminders = action.payload;
    },

    setTimezone: (state, action: PayloadAction<string | null>) => {
      state.timezone = action.payload;
    },

    setNotificationEnabled: (state, action: PayloadAction<boolean | null>) => {
      state.notification_enabled = action.payload;
    },

    setPreferredLang: (state, action: PayloadAction<string[]>) => {
      state.preferred_lang = action.payload;
    },

    setAvailableLang: (state, action: PayloadAction<string[]>) => {
      state.available_lang = action.payload;
    },

    setTheme: (state, action: PayloadAction<string>) => {
      state.theme = action.payload;
    },

    clearSettings: () => initialState,
  },
});

export const {
  setSettings,
  setNeedsReminders,
  setTimezone,
  setNotificationEnabled,
  setPreferredLang,
  setAvailableLang,
  setTheme,
  clearSettings,
} = settingsSlice.actions;

export const settingsReducer = settingsSlice.reducer;

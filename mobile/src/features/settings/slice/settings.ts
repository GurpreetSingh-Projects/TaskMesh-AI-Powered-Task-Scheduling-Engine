import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { SettingsState } from "../types";

const initialState: SettingsState = {
  user_settings_id: "",
  needs_reminders: false,
  timezone: null,
  notification_enabled: null,
  preferred_lang: [],
  available_lang: [],
  theme: "",
  supported_media_types: [],
  max_image_dimension: null,
  image_conversion_format: null,
  image_quality: null,
};

export const SettingsSlice = createSlice({
  name: "settings",
  initialState,
  reducers: {
    setUserSettings: (state, action: PayloadAction<SettingsState>) => {
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

    setSupportedImageFormats: (state, action: PayloadAction<string[]>) => {
      state.supported_media_types = action.payload;
    },

    setMaxImageDimension: (state, action: PayloadAction<number | null>) => {
      state.max_image_dimension = action.payload;
    },

    setImageConversionFormat: (state, action: PayloadAction<string | null>) => {
      state.image_conversion_format = action.payload;
    },

    setImageQuality: (state, action: PayloadAction<number | null>) => {
      state.image_quality = action.payload;
    },

    clearUserSettings: () => initialState,
  },
});

export const {
  setUserSettings,
  setNeedsReminders,
  setTimezone,
  setNotificationEnabled,
  setPreferredLang,
  setAvailableLang,
  setTheme,
  setSupportedImageFormats,
  setMaxImageDimension,
  setImageConversionFormat,
  setImageQuality,
  clearUserSettings,
} = SettingsSlice.actions;

export const userSettingsReducer = SettingsSlice.reducer;

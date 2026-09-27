export type SettingsState = {
  user_settings_id: string;
  needs_reminders: boolean;
  timezone: string | null;
  notification_enabled: boolean | null;
  preferred_lang: string[];
  available_lang: string[];
  theme: string;
  supported_media_types: string[];
  max_image_dimension: number | null;
  image_conversion_format: string | null;
  image_quality: number | null;
};

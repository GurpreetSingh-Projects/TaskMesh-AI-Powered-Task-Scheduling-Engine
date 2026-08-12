export const themeColors = {
  ink: "#000000",
  obsidian: "#030303",
  graphite: "#070707",
  charcoal: "#121212",
  carbon: "#1A1A1A",
  slate: "#242424",
  ash: "#3A3A3A",
  smoke: "#5A5A5A",
  steel: "#8A8A8A",
  cloud: "#B8B8B8",
  mist: "#D7D7D7",
  canvas: "#FFFFFF",
} as const;

export const primaryWeights = {
  regular: "300",
  medium: "400",
  semibold: "500",
  bold: "600",
  extrabold: "700",
  black: "800",
};

export const primarySizes = {
  xs: [12, { lineHeight: "18px" }],
  sm: [14, { lineHeight: "22px" }],
  base: [16, { lineHeight: "24px" }],
  lg: [20, { lineHeight: "28px" }],
  xl: [22, { lineHeight: "30px" }],
};

export const primarySpacing = {
  default: 16,
  "default-half": 8,
  16: "16px",
  14: "14px",
  12: "12px",
  btn: "8px 12px",
  xs: "18px",
  sm: "22px",
  base: "24px",
  lg: "28px",
  xl: "30px",
};

export const primaryBorderRadius = {
  default: 15,
  drawerRadius: primarySpacing?.default,
};

export const primaryScreens = {
  xs: "320px",
  sm: "375px",
  md: "768px",
};

export type AppColors = keyof typeof themeColors;

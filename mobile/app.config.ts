import { ExpoConfig } from "expo/config";

const config: ExpoConfig = {
  name: "TaskMesh AI",
  slug: "taskmesh-ai",
  version: "1.0.5",
  orientation: "portrait",
  icon: "./assets/images/taskmesh-logo.png",
  scheme: "taskmesh",
  userInterfaceStyle: "automatic",
  ios: {
    icon: "./assets/images/taskmesh-logo.png",
  },
  android: {
    adaptiveIcon: {
      foregroundImage: "./assets/images/taskmesh-logo.png",
      backgroundColor: "#ffffff",
    },
    predictiveBackGestureEnabled: false,
    package: "com.gsc_projects.taskmesh",
  },
  assetBundlePatterns: ["assets/fonts/*", "assets/images/*", "assets/sounds/*"],
  plugins: [
    [
      "expo-splash-screen",
      {
        backgroundColor: "#ffffff",
        android: {
          image: "./assets/images/taskmesh-logo.png",
          imageWidth: 125,
        },
      },
    ],
    [
      "expo-secure-store",
      {
        configureAndroidBackup: true,
        faceIDPermission: "Allow TaskMesh AI access to store securely",
      },
    ],
    [
      "react-native-edge-to-edge",
      {
        android: {
          parentTheme: "Default",
          enforceNavigationBarContrast: true,
        },
      },
    ],
    "expo-font",
    "expo-image",
    "expo-status-bar",
    "react-native-edge-to-edge",
  ],
  experiments: {
    reactCompiler: true,
  },
  extra: {
    eas: {
      projectId: "5a494fa3-be41-49f9-89bb-1d360361056b",
    },
  },
  owner: "gsc-projects",
};

export default config;

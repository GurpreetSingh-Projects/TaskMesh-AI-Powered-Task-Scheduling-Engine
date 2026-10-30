import { Pressable, StyleSheet, Text, View } from "react-native";
import React, { useEffect, useRef, useState } from "react";
import ThemePage from "@/components/ThemePage";
import { themeColors } from "@/theme";
import {
  Camera,
  CameraRef,
  useCameraDevice,
  useCameraPermission,
  usePhotoOutput,
} from "react-native-vision-camera";
import { Circle, SwitchCamera } from "lucide-react-native";
import { Image } from "expo-image";
import { images } from "@/assets";
import { FileType } from "@/features/auth/types";
import { useMediaPicker } from "@/hooks/useMediaPicker";

const CreateTask = () => {
  const camera = useRef<CameraRef>(null);
  const { hasPermission, requestPermission } = useCameraPermission();
  const [cameraPosition, setCameraPosition] = useState<"back" | "front">(
    "back",
  );
  const device = useCameraDevice(cameraPosition);

  const photoOutput = usePhotoOutput({
    containerFormat: "jpeg",
    quality: 0.75,
  });

  const { pickFromGallery } = useMediaPicker();
  const flipCamera = () => {
    setCameraPosition((prev) => (prev === "back" ? "front" : "back"));
  };

  const capturePhoto = async () => {
    try {
      const { filePath } = await photoOutput.capturePhotoToFile(
        { flashMode: "on" },
        {},
      );

      console.log("Photo:", filePath);
    } catch (error) {
      console.log("Capture error:", error);
    }
  };

  const handlePicker = async (source: "gallery" | "camera" = "gallery") => {
    try {
      const uri: FileType =
        source === "gallery" ? await pickFromGallery() : null;

      if (uri) {
        console.log(uri);
      }
    } catch (error) {
      console.log("Media picker error:", error);
    }
  };

  useEffect(() => {
    if (!hasPermission) {
      requestPermission();
    }
  }, [hasPermission, requestPermission]);

  console.log(photoOutput);

  return (
    <ThemePage
      noSafeArea
      isScrollable={false}
      backgroundColor={themeColors?.ink}
    >
      <View className="flex-1 relative">
        <Camera
          ref={camera}
          style={{
            position: "absolute",
            inset: 0,
          }}
          enableNativeZoomGesture
          enableNativeTapToFocusGesture
          device={device}
          isActive={true}
          outputs={[photoOutput]}
        />
        <View className="absolute bottom-10 left-0 right-0">
          <View className="relative flex-row items-center px-page">
            <Pressable
              className="absolute left-page"
              onPress={() => handlePicker("gallery")}
              hitSlop={15}
            >
              <Image
                source={images?.icons?.galleryIcon}
                style={{
                  width: 37.5,
                  height: 37.5,
                }}
                contentFit="contain"
              />
            </Pressable>

            <View className="flex-1 items-center">
              <Pressable
                onPress={capturePhoto}
                className="rounded-full border-2 border-canvas!"
                hitSlop={15}
              >
                <Circle size={65} fill={themeColors?.canvas} stroke="none" />
              </Pressable>
            </View>

            <View className="absolute right-page">
              <Pressable
                onPress={flipCamera}
                className="h-15 w-15 items-center justify-center"
                hitSlop={15}
              >
                <SwitchCamera
                  size={35}
                  color={themeColors?.canvas}
                  strokeWidth={1.25}
                />
              </Pressable>
            </View>
          </View>
        </View>
      </View>
    </ThemePage>
  );
};

export default CreateTask;

const styles = StyleSheet.create({});

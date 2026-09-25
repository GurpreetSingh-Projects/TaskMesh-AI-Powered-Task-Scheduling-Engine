import React from "react";
import { Pressable, View } from "react-native";
import ThemeText from "./ThemeText";
import { CameraIcon, GalleryIcon } from "@/Icon";

const MediaPicker = () => {
  const handlePick = async (source: "gallery" | "camera") => {
    // const uri =
    //   source === "gallery" ? await pickFromLibrary() : await pickFromCamera();
    // drawerRef.current?.dismiss();
    // resolveRef.current?.(uri);
    // resolveRef.current = null;
  };

  return (
    <View className="gap-3 p-4">
      <Pressable
        onPress={() => handlePick("camera")}
        className="flex-row items-center gap-3 rounded-xl border border-ash p-4"
      >
        <CameraIcon width={20} height={20} />
        <ThemeText>Take Photo</ThemeText>
      </Pressable>

      <Pressable
        onPress={() => handlePick("gallery")}
        className="flex-row items-center gap-3 rounded-xl border border-ash p-4"
      >
        <GalleryIcon width={20} height={20} />
        <ThemeText>Choose from Gallery</ThemeText>
      </Pressable>
    </View>
  );
};

export default MediaPicker;

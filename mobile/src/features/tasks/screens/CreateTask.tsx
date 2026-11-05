import ThemePage from "@/components/ThemePage";
import { themeColors } from "@/theme";
import { images } from "@/assets";
import { useEffect, useRef, useState } from "react";
import { Pressable, View } from "react-native";
import { Image } from "expo-image";
import { Circle, SwitchCamera } from "lucide-react-native";
import {
  Camera,
  CameraRef,
  CommonResolutions,
  useCameraDevice,
  useCameraPermission,
  usePhotoOutput,
} from "react-native-vision-camera";
import { formatImgTypes, useMediaPicker } from "@/hooks/useMediaPicker";
import ImageClickedView from "../components/ImageClickedView";
import { FileType } from "@/features/auth/types";
import ReactNativeBlobUtil from "react-native-blob-util";

const CreateTask = () => {
  const { processImage } = useMediaPicker();

  const [media, setMedia] = useState<FileType | null>(null);
  const camera = useRef<CameraRef>(null);
  const { hasPermission, requestPermission } = useCameraPermission();
  const [cameraPosition, setCameraPosition] = useState<"back" | "front">(
    "front",
  );
  const device = useCameraDevice(cameraPosition);
  const photoOutput = usePhotoOutput({
    containerFormat: "jpeg",
    quality: 0.75,
    targetResolution: CommonResolutions.FHD_16_9,
  });
  const { pickFromGallery } = useMediaPicker();

  const flipCamera = () => {
    setCameraPosition((prev) => (prev === "back" ? "front" : "back"));
  };

  const capturePhoto = async () => {
    try {
      const { filePath } = await photoOutput.capturePhotoToFile({}, {});
      if (filePath) {
        let processedImage = await processImage({
          uri: `file://${filePath}`,
          name: "image",
          type: "image/jpeg",
        });

        ReactNativeBlobUtil.fs
          .unlink(filePath)
          .catch((err) => console.log("unlink failed:", err));

        setMedia(processedImage);
      }
    } catch (error) {
      console.log("Capture error:", error);
    }
  };

  const handlePicker = async () => {
    try {
      const file = await pickFromGallery();
      if (file) {
        setMedia(file.uri);
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

  return (
    <ThemePage
      noSafeArea
      isScrollable={false}
      backgroundColor={themeColors?.ink}
    >
      <View className="flex-1 relative" collapsable={true}>
        {!media ? (
          <>
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
                  onPress={handlePicker}
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
                    <Circle
                      size={65}
                      fill={themeColors?.canvas}
                      stroke="none"
                    />
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
          </>
        ) : (
          <ImageClickedView media={media} />
        )}
      </View>
    </ThemePage>
  );
};

export default CreateTask;

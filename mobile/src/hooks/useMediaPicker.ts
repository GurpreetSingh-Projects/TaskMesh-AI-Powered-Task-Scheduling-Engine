import * as ImagePicker from "expo-image-picker";
import { ImageManipulator, SaveFormat } from "expo-image-manipulator";
import { Alert } from "react-native";
import { useAppSelector } from "@/app/store";

const formatImgTypes: Record<string, SaveFormat> = {
  "image/webp": SaveFormat.WEBP,
  "image/jpg": SaveFormat.JPEG,
  "image/jpeg": SaveFormat.JPEG,
  "image/png": SaveFormat.PNG,
};

export function useMediaPicker() {
  const settings = useAppSelector((state) => state?.settings);

  const processImage = async (uri: string) => {
    const context = ImageManipulator.manipulate(uri).resize({
      width: settings?.max_image_width,
    });

    const image = await context.renderAsync();

    try {
      const result = await image.saveAsync({
        compress: settings?.image_quality,
        format:
          formatImgTypes[settings?.image_conversion_format] ?? SaveFormat?.WEBP,
      });
      return result.uri;
    } catch (error) {
      console.log("Image compression error:", error);
    } finally {
      context.release();
      image.release();
    }
    return null;
  };

  const pickFromLibrary = async () => {
    try {
      const permissionResult =
        await ImagePicker.requestMediaLibraryPermissionsAsync();

      if (!permissionResult.granted) {
        return null;
      }

      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ["images"],
        quality: 1,
      });

      if (result.canceled) {
        return null;
      }

      return await processImage(result.assets[0].uri);
    } catch (error) {
      console.error("Failed to pick library image:", error);
      return null;
    }
  };

  const pickFromCamera = async () => {
    try {
      const permissionResult =
        await ImagePicker.requestCameraPermissionsAsync();

      if (!permissionResult.granted) {
        return null;
      }

      const result = await ImagePicker.launchCameraAsync({
        quality: 1,
      });

      if (result.canceled) {
        return null;
      }

      return await processImage(result.assets[0].uri);
    } catch (error) {
      console.error("Failed to pick camera image:", error);
      return null;
    }
  };

  return { pickFromLibrary, pickFromCamera };
}

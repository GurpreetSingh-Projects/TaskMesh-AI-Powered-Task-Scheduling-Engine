import * as ImagePicker from "expo-image-picker";
import { Alert } from "react-native";

export function useMediaPicker() {
  const pickFromLibrary = async () => {
    const permissionResult =
      await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (!permissionResult.granted) {
      Alert.alert(
        "Permission required",
        "Permission to access the media library is required.",
      );
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ["images"],
      quality: 1,
    });

    console.log(result);
    return result.canceled ? null : result.assets[0].uri;
  };

  const pickFromCamera = async () => {
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();

    if (!permissionResult.granted) {
      Alert.alert(
        "Permission required",
        "Permission to access the camera is required.",
      );
      return;
    }

    let result = await ImagePicker.launchCameraAsync({
      quality: 1,
    });
    console.log(result);
    return result.canceled ? null : result.assets[0].uri;
  };

  return { pickFromLibrary, pickFromCamera };
}

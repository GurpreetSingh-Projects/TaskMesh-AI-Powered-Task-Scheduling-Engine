import { Pressable, View } from "react-native";
import { Image } from "expo-image";
import { images } from "@/assets";
import ThemeText from "./ThemeText";

const MediaPicker = () => {
  const handlePick = async (source: "gallery" | "camera") => {
    // const uri =
    //   source === "gallery" ? await pickFromLibrary() : await pickFromCamera();
    // drawerRef.current?.dismiss();
    // resolveRef.current?.(uri);
    // resolveRef.current = null;
  };
  return (
    <View className="px-default gap-3">
      <View className="gap-default-half">
        <ThemeText variant="heading" className="text-start">
          Add Profile Photo
        </ThemeText>
        <ThemeText variant="body" className="text-sm text-steel">
          Choose how you'd like to add your profile photo
        </ThemeText>
      </View>

      <View className="flex-row items-cneter justify-between py-3">
        <Pressable
          onPress={() => handlePick("camera")}
          className="flex-1 items-center"
          style={({ pressed }) => ({
            opacity: pressed ? 0.7 : 1,
            transform: [{ scale: pressed ? 0.97 : 1 }],
          })}
        >
          <View className="items-center justify-center rounded-3xl">
            <Image
              source={images?.icons?.cameraIcon}
              style={{
                width: 50,
                height: 50,
              }}
              contentFit="contain"
            />
          </View>

          <ThemeText className="mt-3 text-base font-medium! text-ink">
            Camera
          </ThemeText>

          <ThemeText className="mt-1 text-xs text-steel">
            Take a photo
          </ThemeText>
        </Pressable>

        <Pressable
          onPress={() => handlePick("gallery")}
          className="flex-1 items-center"
          style={({ pressed }) => ({
            opacity: pressed ? 0.7 : 1,
            transform: [{ scale: pressed ? 0.97 : 1 }],
          })}
        >
          <View className="items-center justify-center rounded-3xl">
            <Image
              source={images?.icons?.galleryIcon}
              style={{
                width: 50,
                height: 50,
              }}
              contentFit="contain"
            />
          </View>

          <ThemeText className="mt-3 text-base font-medium! text-ink">
            Gallery
          </ThemeText>

          <ThemeText className="mt-1 text-xs text-steel">
            Choose existing
          </ThemeText>
        </Pressable>
      </View>
    </View>
  );
};

export default MediaPicker;

import { Keyboard, Pressable, View } from "react-native";
import { Image } from "expo-image";
import { useRef } from "react";
import type { BottomSheetModal } from "@gorhom/bottom-sheet";
import ThemeDrawer from "@/components/ThemeDrawer";
import MediaPicker from "@/components/MediaPicker";
import { CameraIcon, UserRoundIcon } from "@/Icon";
import { themeColors } from "@/theme";
import { FileType } from "@/features/auth/types";

type ProfileImagePickerType = {
  image_path: FileType;
  onChange: (file: FileType) => void;
  size?: number;
  badgeSize?: number;
};

const ProfileImagePicker = (props: ProfileImagePickerType) => {
  const size = props?.size ?? 100;
  const badgeSize = props?.badgeSize ?? Math.round(size * 0.35);

  const drawerRef = useRef<BottomSheetModal>(null);

  return (
    <>
      <Pressable
        onPress={() => {
          Keyboard.dismiss();
          drawerRef.current?.present();
        }}
        style={{ width: size, height: size, borderRadius: 9999 }}
        className="items-center justify-center bg-neutral-100 border border-neutral-200"
      >
        {props.image_path?.uri ? (
          <Image
            style={{ height: "100%", width: "100%", borderRadius: 9999 }}
            source={props.image_path.uri}
            contentFit="cover"
            allowDownscaling={false}
          />
        ) : (
          <UserRoundIcon
            width={size * 0.65}
            height={size * 0.65}
            stroke={themeColors?.steel}
            fill="transparent"
          />
        )}

        <View
          style={{
            position: "absolute",
            bottom: 0,
            right: 0,
            width: badgeSize,
            height: badgeSize,
            borderRadius: badgeSize / 2,
          }}
          className="bg-ink items-center justify-center border-2 border-white"
        >
          <CameraIcon
            width={badgeSize * 0.5}
            height={badgeSize * 0.5}
            stroke="#fff"
            fill="transparent"
          />
        </View>
      </Pressable>

      <ThemeDrawer
        ref={drawerRef}
        snapPoints={["25%"]}
        closable
        backdropPressBehavior="close"
      >
        <MediaPicker
          onMediaSelected={(file) => {
            props?.onChange(file);
            drawerRef.current?.dismiss();
          }}
        />
      </ThemeDrawer>
    </>
  );
};

export default ProfileImagePicker;

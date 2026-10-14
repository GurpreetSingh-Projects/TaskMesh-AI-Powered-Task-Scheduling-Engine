import { useAppSelector } from "@/app/store";
import ProfileImagePicker from "@/components/ProfileImagePicker";
import ThemeButton from "@/components/ThemeButton";
import ThemePage from "@/components/ThemePage";
import ThemePageHeader from "@/components/ThemePageHeader";
import ThemeText from "@/components/ThemeText";
import ThemeTextInput from "@/components/ThemeTextInput";
import { FileType } from "@/features/auth/types";
import { setAuth } from "@/features/auth/utils";
import { useEffect, useState } from "react";
import {
  Keyboard,
  StyleSheet,
  Text,
  useWindowDimensions,
  View,
} from "react-native";
import { ProfileFormValues } from "../types";
import { useUpdateProfileMutation } from "../profileApi";

const ProfileDetailsPending = () => {
  const { width, height } = useWindowDimensions();
  const IMG_HEIGHT = height * 0.15;

  const user = useAppSelector((state) => state?.user);
  const [profileImg, setProfileImg] = useState<FileType>({
    name: "",
    type: "",
    uri: null,
  });
  const [fullName, setFullName] = useState<string>("");
  const [isSubmitButtonEnabled, setIsSubmitButtonEnabled] =
    useState<boolean>(false);

  const [
    updateProfile,
    {
      data: updateProfileData,
      isLoading: isUpdateProfileLoading,
      isError: isUpdateProfileError,
      error: updateProfileError,
    },
  ] = useUpdateProfileMutation();

  const submitHandler = async () => {
    console.log(fullName, profileImg);

    try {
      const response = await updateProfile({
        fullName: fullName,
        profile_img: profileImg,
      }).unwrap();

      setTimeout(() => {
        setAuth(response);
      }, 2500);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    setIsSubmitButtonEnabled(
      Boolean(profileImg || fullName?.trim()?.length > 3),
    );
  }, [profileImg, fullName]);

  return (
    <ThemePage className="bg-canvas">
      <ThemePageHeader heading="Complete Profile" />

      <View className="flex-1 w-full items-center gap-10 mt-10 px-page">
        <View className="gap-3">
          <ThemeText variant="heading" className="w-full text-start">
            Almost there!
          </ThemeText>

          <ThemeText variant="body" className="text-sm text-steel!">
            Finish completing your profile to help us customize the best
            experience of TaskMesh for you.
          </ThemeText>
        </View>
        <View className="items-center justify-center">
          <ProfileImagePicker
            image_path={!profileImg?.uri && user?.profile_img}
            onChange={setProfileImg}
            size={IMG_HEIGHT}
          />
        </View>
        <View className="w-full gap-3">
          <ThemeText variant="title">What should we call you ?</ThemeText>
          <ThemeTextInput
            placeholder="Your name"
            value={fullName}
            onBlur={() => Keyboard.dismiss()}
            onChangeText={(value) => {
              setFullName(value);
            }}
            keyboardType="email-address"
          />
        </View>
      </View>
      <View className="w-full px-page">
        <ThemeButton
          className="bg-canvas w-full rounded-full border border-0.25! border-steel"
          textColor="text-white!"
          text="SUBMIT"
          status={isUpdateProfileLoading ? "loading" : "default"}
          onPress={submitHandler}
        />
        <ThemeButton
          textColor="text-white!"
          text="SUBMIT"
          status={isUpdateProfileLoading ? "loading" : "default"}
          onPress={submitHandler}
        />
      </View>
    </ThemePage>
  );
};

export default ProfileDetailsPending;

const styles = StyleSheet.create({});

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
import { Keyboard, useWindowDimensions, View } from "react-native";
import { useUpdateProfileMutation } from "../profileApi";

const ProfileDetailsPending = () => {
  const { height } = useWindowDimensions();
  const IMG_HEIGHT = height * 0.15;

  const user = useAppSelector((state) => state.user);

  const [profileImg, setProfileImg] = useState<FileType>(null);
  const [fullName, setFullName] = useState("");

  const [isSubmitButtonEnabled, setIsSubmitButtonEnabled] = useState(false);

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
    try {
      const response = await updateProfile({
        fullName: fullName.trim() || null,
        profile_img: profileImg,
      }).unwrap();

      setTimeout(() => {
        setAuth(response);
      }, 1500);
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    setIsSubmitButtonEnabled(
      Boolean(profileImg?.uri || fullName?.trim()?.length > 3),
    );
  }, [profileImg, fullName]);

  return (
    <ThemePage className="bg-canvas">
      <ThemePageHeader heading="Complete Profile" />

      <View className="mt-10 w-full flex-1 items-center gap-10 px-page">
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
            image_path={profileImg?.uri ? profileImg?.uri : user?.profile_img}
            onChange={setProfileImg}
            size={IMG_HEIGHT}
          />
        </View>

        <View className="w-full gap-3">
          <ThemeText variant="title">What should we call you?</ThemeText>

          <ThemeTextInput
            placeholder="Your name"
            value={fullName}
            onBlur={() => Keyboard.dismiss()}
            onChangeText={setFullName}
            keyboardType="default"
          />
        </View>
      </View>

      <View className="w-full gap-3 px-page">
        <ThemeButton
          className="my-3"
          variant="secondary"
          text="I'LL SKIP FOR NOW"
        />

        <ThemeButton
          className="my-3"
          variant="primary"
          text="SUBMIT"
          status={isUpdateProfileLoading ? "loading" : "default"}
          onPress={submitHandler}
        />
      </View>
    </ThemePage>
  );
};

export default ProfileDetailsPending;

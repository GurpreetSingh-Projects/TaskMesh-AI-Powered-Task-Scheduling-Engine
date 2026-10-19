import { useAppDispatch, useAppSelector } from "@/app/store";
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
import {
  setIsProfileCompleted,
  setIsProfileCompletionSkipped,
  setUserInfo,
} from "../slice/user";
import { useNavigation } from "@react-navigation/native";
import { HomeStackNavigationProp } from "@/navigation/routes";

const ProfileDetailsPending = () => {
  const { height } = useWindowDimensions();
  const IMG_HEIGHT = height * 0.15;

  const user = useAppSelector((state) => state.user);

  const [profileImg, setProfileImg] = useState<FileType>(null);
  const [fullName, setFullName] = useState("");

  const [isSubmitButtonEnabled, setIsSubmitButtonEnabled] = useState(false);
  const dispatch = useAppDispatch();

  const [
    updateProfile,
    {
      data: updateProfileData,
      isLoading: isUpdateProfileLoading,
      isError: isUpdateProfileError,
      error: updateProfileError,
    },
  ] = useUpdateProfileMutation();

  const buttonStatusChecker = () => {
    if (isUpdateProfileLoading) return "loading";
    else if (!isUpdateProfileLoading && updateProfileData) return "success";
    else if (!isUpdateProfileLoading && isUpdateProfileError) return "error";
    return "default";
  };

  const submitHandler = async (isSubmitButtonEnabled: boolean) => {
    if (isSubmitButtonEnabled) {
      try {
        const response = await updateProfile({
          fullName: fullName.trim() || null,
          profile_img: profileImg,
        }).unwrap();

        if (response?.is_profile_completed) {
          dispatch(setIsProfileCompletionSkipped(false));
          dispatch(setIsProfileCompleted(true));
        } else {
          dispatch(setIsProfileCompletionSkipped(true));
          dispatch(setIsProfileCompleted(false));
        }

        setTimeout(() => {
          dispatch(dispatch(setUserInfo(response)));
        }, 2500);
      } catch (error) {
        console.log(error);
        dispatch(setIsProfileCompletionSkipped(false));
      }
    } else {
      dispatch(setIsProfileCompletionSkipped(true));
    }
  };

  useEffect(() => {
    setIsSubmitButtonEnabled(
      Boolean(profileImg?.uri || fullName?.trim()?.length > 3),
    );
  }, [profileImg, fullName]);

  return (
    <ThemePage
      footer={
        <View className="w-full gap-3 px-page py-3">
          <ThemeButton
            className="my-3"
            variant={isSubmitButtonEnabled ? "primary" : "secondary"}
            text={isSubmitButtonEnabled ? "SUBMIT" : "i'LL SKIP FOR NOW"}
            status={buttonStatusChecker()}
            onPress={() => submitHandler(isSubmitButtonEnabled)}
          />
        </View>
      }
      keyboardOffsetOpened={-(height * 0.75)}
      keyboardOffsetClosed={-25}
    >
      <ThemePageHeader heading="Complete Profile" />

      <View className="f lex-1 h-f ull w-full items-center mt-10 gap-10 px-page">
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
    </ThemePage>
  );
};

export default ProfileDetailsPending;

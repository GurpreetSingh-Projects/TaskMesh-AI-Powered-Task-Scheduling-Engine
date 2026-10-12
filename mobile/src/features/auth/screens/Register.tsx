import { Keyboard, Pressable, View } from "react-native";
import ThemeButton from "@/components/ThemeButton";
import ThemeText from "@/components/ThemeText";
import ThemePage from "@/components/ThemePage";
import OnboardingBg from "@/features/onboarding/components/OnboardingBg";
import { Image } from "expo-image";
import { animations, images } from "@/assets";
import ThemeTextInput from "@/components/ThemeTextInput";
import { EmailIcon, LockIcon } from "@/Icon";
import { themeColors } from "@/theme";
import { Controller, useForm } from "react-hook-form";
import { z } from "zod/v4";
import { zodResolver } from "@hookform/resolvers/zod";
import { useRegisterMutation } from "@/api/baseApi";
import OrSeparator from "@/components/OrSeparator";
import { useNavigation } from "@react-navigation/native";
import ThemeDrawer from "@/components/ThemeDrawer";
import { useRef, useState } from "react";
import type { BottomSheetModal } from "@gorhom/bottom-sheet";
import LottieView from "lottie-react-native";
import { DrawerMode, FileType } from "../types";
import { getAuthMessage, setAuth } from "../utils";
import ProfileImagePicker from "@/components/ProfileImagePicker";
import { useWindowDimensions } from "react-native-keyboard-controller";

const registerSchema = z.object({
  email: z.email(),
  password: z.string().min(3, "Password is Required"),
});

type RegisterForm = z.infer<typeof registerSchema>;

const Register = () => {
  const { width, height } = useWindowDimensions();

  const BG_CAROUSEL_HEIGHT = height * 0.375;
  const IMG_HEIGHT = height * 0.125;

  const [register, { isLoading, reset }] = useRegisterMutation();
  const registerDrawerRef = useRef<BottomSheetModal>(null);
  const [drawerMode, setDrawerMode] = useState<DrawerMode>("default");
  const [drawerMsg, setDrawerMsg] = useState({
    title: "",
    description: "",
  });

  const [profileImg, setProfileImg] = useState<FileType>(null);

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const navigation = useNavigation();

  const submitHandler = async (values: RegisterForm) => {
    try {
      const response = await register({
        email: values.email,
        password: values.password,
        profile_img: profileImg,
      }).unwrap();

      setDrawerMsg({
        title: "Account Created!!",
        description: "Registered successfully, setting up...",
      });
      setDrawerMode("success");
      registerDrawerRef?.current?.present();

      setTimeout(() => {
        registerDrawerRef?.current?.dismiss();
        setAuth(response);
        reset();
      }, 2500);
    } catch (error) {
      setDrawerMsg(getAuthMessage(error?.status_code));
      setDrawerMode("fail");
      registerDrawerRef?.current?.present();

      setTimeout(() => {
        registerDrawerRef?.current?.dismiss();
      }, 2500);
    }
  };

  return (
    <ThemePage className="bg-canvas" noSafeArea isScrollable>
      <View className="flex-1 items-center">
        <OnboardingBg
          className="relative items-center justify-start"
          style={{ height: "37.5%", width }}
        >
          <Image
            style={{ height: "100%", width: "100%", zIndex: 0 }}
            source={images?.onboarding?.register}
            contentFit="cover"
            allowDownscaling={false}
          />
        </OnboardingBg>

        <View
          className="flex-1 w-full pt-5 bg-canvas px-page gap-3"
          style={{ zIndex: 99999 }}
        >
          <View className="gap-1">
            <ThemeText variant="heading" className="text-start">
              Create Account
            </ThemeText>

            <ThemeText className="text-sm font-normal! text-graphite!">
              Setup your profile and start planning your day
            </ThemeText>
          </View>

          <View className="w-full gap-5 faj">
            <View className="items-center justify-center">
              <ProfileImagePicker
                image_path={profileImg}
                onChange={setProfileImg}
                size={IMG_HEIGHT}
              />
            </View>

            <View>
              <Controller
                control={control}
                name="email"
                render={({ field: { value, onChange, onBlur } }) => (
                  <ThemeTextInput
                    placeholder="Email"
                    value={value}
                    onChangeText={onChange}
                    onBlur={onBlur}
                    keyboardType="email-address"
                    icon={
                      <EmailIcon
                        height={22.5}
                        width={22.5}
                        stroke={themeColors?.steel}
                      />
                    }
                  />
                )}
              />

              {errors?.email?.message && (
                <ThemeText className="mt-1 text-xs text-red-500">
                  {errors.email.message}
                </ThemeText>
              )}
            </View>

            <View>
              <Controller
                control={control}
                name="password"
                render={({ field: { value, onChange, onBlur } }) => (
                  <ThemeTextInput
                    placeholder="Password"
                    value={value}
                    onChangeText={onChange}
                    onBlur={onBlur}
                    icon={
                      <LockIcon
                        height={22.5}
                        width={22.5}
                        stroke={themeColors?.steel}
                      />
                    }
                    secure
                  />
                )}
              />

              {errors?.password?.message && (
                <ThemeText className="mt-1 text-xs text-red-500">
                  {errors.password.message}
                </ThemeText>
              )}
            </View>

            <ThemeButton
              className="bg-ink mx-default! rounded-full"
              textColor="text-white!"
              text="REGISTER NOW"
              status={isLoading ? "loading" : "default"}
              onPress={() => {
                Keyboard.dismiss();
                handleSubmit(submitHandler)();
              }}
            />

            <>
              <OrSeparator />

              <View className="flex-row w-full items-center justify-center mt-5">
                <Pressable
                  onPress={() => {
                    if (navigation.canGoBack()) {
                      navigation.goBack();
                    }
                  }}
                  className="flex-row items-center justify-center gap-1"
                >
                  <ThemeText className="text-sm text-steel">
                    Already have an account ?
                  </ThemeText>

                  <ThemeText className="font-bold! text-sm text-ink">
                    Login Now
                  </ThemeText>
                </Pressable>
              </View>
            </>
          </View>
        </View>
      </View>

      <ThemeDrawer
        ref={registerDrawerRef}
        snapPoints={["30%"]}
        closable={false}
        backdropPressBehavior="none"
      >
        <View className="h-full w-full flex-1 items-center justify-center gap-3 z-10">
          <LottieView
            source={
              drawerMode === "success"
                ? animations?.tickIcon
                : animations?.crossIcon
            }
            autoPlay
            loop={false}
            style={{ width: 75, height: 75 }}
          />

          <View className="gap-3 py-3">
            <ThemeText variant="subheading" className="text-center">
              {drawerMsg.title}
            </ThemeText>

            <ThemeText className="text-graphite! text-center">
              {drawerMsg.description}
            </ThemeText>
          </View>
        </View>

        {drawerMode === "success" && (
          <Image
            source={images.illustrations.illustration2}
            contentFit="cover"
            style={{
              width,
              height: 150,
              position: "absolute",
              bottom: 0,
              opacity: 0.25,
            }}
          />
        )}
      </ThemeDrawer>
    </ThemePage>
  );
};

export default Register;

import { Keyboard, useWindowDimensions, View } from "react-native";
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
import OrSeparator from "@/components/OrSeparator";
import { Link, useNavigation } from "@react-navigation/native";
import ThemeDrawer from "@/components/ThemeDrawer";
import { useRef, useState } from "react";
import type { BottomSheetModal } from "@gorhom/bottom-sheet";
import LottieView from "lottie-react-native";
import { DrawerMode } from "../types";
import { getAuthMessage, setAuth } from "../utils";
import { useLoginMutation } from "../authApi";

const loginSchema = z.object({
  email: z.email(),
  password: z.string().min(3, "Password is Required"),
});

type LoginForm = z.infer<typeof loginSchema>;

const Login = () => {
  const { height } = useWindowDimensions();
  const [login, { isLoading, isSuccess, isError, error, reset }] =
    useLoginMutation();
  const loginDrawerRef = useRef<BottomSheetModal>(null);
  const [drawerMode, setDrawerMode] = useState<DrawerMode>("default");
  const [drawerMsg, setDrawerMsg] = useState({
    title: "",
    description: "",
  });

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const submitHandler = async (values: LoginForm) => {
    try {
      const response = await login({
        email: values.email,
        password: values.password,
      }).unwrap();

      setDrawerMsg({
        title: "Welcome back!!",
        description: "Logged in successfully, setting up...",
      });
      setDrawerMode("success");
      loginDrawerRef?.current?.present();

      setTimeout(() => {
        loginDrawerRef?.current?.dismiss();
        setAuth(response);
        reset();
      }, 2500);
    } catch (error) {
      console.log("Login api error:", error);
      setDrawerMsg(getAuthMessage(error?.status));
      setDrawerMode("fail");
      loginDrawerRef?.current?.present();

      setTimeout(() => {
        loginDrawerRef?.current?.dismiss();
      }, 2500);
    }
  };

  return (
    <ThemePage
      noSafeArea
      isScrollable
      footer={
        <View
          className="w-full pt-5 bg-canvas px-page gap-3"
          style={{ zIndex: 99999 }}
        >
          <View className="gap-1">
            <ThemeText variant="heading" className="text-start">
              Welcome back
            </ThemeText>
            <ThemeText className="text-sm font-normal! text-steel!">
              Login to continue managing your day
            </ThemeText>
          </View>

          <View className="w-full pt-5 gap-5">
            <View className="">
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
                    // autoFocus
                  />
                )}
              />
              {errors && errors?.email?.message && (
                <ThemeText className="mt-1 text-xs text-red-500">
                  {errors?.email?.message}
                </ThemeText>
              )}
            </View>
            <View className="">
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
              {errors && errors?.password?.message && (
                <ThemeText className="mt-1 text-xs text-red-500">
                  {errors?.password?.message}
                </ThemeText>
              )}
            </View>

            <ThemeButton
              className="my-3"
              text="GET STARTED"
              status={isLoading ? "loading" : "default"}
              onPress={() => {
                Keyboard.dismiss();
                handleSubmit(submitHandler)();
              }}
            />
            <>
              <OrSeparator />
              <View className="w-full items-center justify-center my-3">
                <Link screen="Register">
                  <View className="flex-row items-center gap-1">
                    <ThemeText className="text-sm text-steel">
                      Don't have an account ?
                    </ThemeText>

                    <ThemeText className="font-bold! text-sm text-ink">
                      Register Now
                    </ThemeText>
                  </View>
                </Link>
              </View>
            </>
          </View>
        </View>
      }
      keyboardOffsetClosed={-(height * 0.075)}
      keyboardOffsetOpened={0}
    >
      <View className="items-center">
        <OnboardingBg
          className="relative items-center justify-start"
          style={{
            height: height * 0.5,
          }}
        >
          {/* <BackButton goBack /> */}
          <Image
            style={{
              height: 450,
              width: 450,
              zIndex: 0,
            }}
            source={images?.onboarding?.login}
            contentFit="cover"
            allowDownscaling={false}
          />
        </OnboardingBg>
      </View>
      {/* </KeyboardAvoidingView> */}
      <ThemeDrawer ref={loginDrawerRef} snapPoints={["30%"]} closable={false}>
        <View className="w-full flex-1 items-center justify-center gap-3">
          <LottieView
            source={
              drawerMode == "success"
                ? animations?.tickIcon
                : animations?.crossIcon
            }
            autoPlay
            loop={false}
            style={{
              width: 100,
              height: 100,
            }}
          />
          <View className="gap-3 py-3">
            <ThemeText variant="subheading" className="text-center">
              {drawerMsg?.title}
            </ThemeText>
            <ThemeText className="text-graphite! text-center">
              {drawerMsg?.description}
            </ThemeText>
          </View>
        </View>
      </ThemeDrawer>
    </ThemePage>
  );
};

export default Login;

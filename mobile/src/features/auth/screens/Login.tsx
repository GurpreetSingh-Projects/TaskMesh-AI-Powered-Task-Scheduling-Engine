import { Keyboard, View } from "react-native";
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
import { useSignInMutation } from "@/api/baseApi";
import OrSeparator from "@/components/OrSeparator";
import { Link } from "@react-navigation/native";
import ThemeDrawer from "@/components/ThemeDrawer";
import { useEffect, useRef, useState } from "react";
import type { BottomSheetModal } from "@gorhom/bottom-sheet";
import LottieView from "lottie-react-native";
import { DrawerMode } from "../types";
import { setAuth } from "../utils";

const loginSchema = z.object({
  email: z.email(),
  password: z.string().min(3, "Password is Required"),
});

type LoginForm = z.infer<typeof loginSchema>;

const Login = () => {
  const [signIn, { isLoading, isSuccess, isError, error, reset }] =
    useSignInMutation();
  const loginDrawerRef = useRef<BottomSheetModal>(null);
  const [drawerMode, setDrawerMode] = useState<DrawerMode>("default");

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
      const response = await signIn({
        email: values.email,
        password: values.password,
      }).unwrap();
      console.log(response);
      await setAuth(response);
      setDrawerMode("success");
    } catch (error) {
      console.log("Login api error:", error);
      setDrawerMode("fail");
    }
    loginDrawerRef?.current?.present();
    setTimeout(() => {
      loginDrawerRef?.current?.dismiss();
    }, 3500);
  };

  return (
    <ThemePage className="bg-canvas" noSafeArea isScrollable>
      <View className="flex-1 items-center">
        <OnboardingBg className="h-1/2 relative items-center justify-start">
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
        <View
          className="flex-1 w-full pt-5 bg-canvas px-page gap-3"
          style={{ zIndex: 99999 }}
        >
          <View className="gap-1">
            <ThemeText variant="heading" className="text-start">
              Welcome back
            </ThemeText>
            <ThemeText className="text-sm font-normal! text-graphite!">
              Sign in to continue managing your day
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
                    autoFocus
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
              className="bg-ink mx-default! rounded-full"
              textColor="text-white!"
              text="GET STARTED"
              status={
                isLoading
                  ? "loading"
                  : isSuccess
                    ? "success"
                    : isError
                      ? "error"
                      : "default"
              }
              onPress={() => {
                Keyboard.dismiss();
                handleSubmit(submitHandler)();
              }}
            />
            <>
              <OrSeparator />
              <View className="flex-row w-full items-center justify-center gap-1 mt-5">
                <ThemeText className="text-sm text-steel">
                  Don't have an account ?
                </ThemeText>
                <Link screen="Register">
                  <ThemeText className="font-bold! text-sm text-ink">
                    Register Now
                  </ThemeText>
                </Link>
              </View>
            </>
          </View>
        </View>
      </View>
      {/* </KeyboardAvoidingView> */}
      <ThemeDrawer ref={loginDrawerRef} snapPoints={["30%"]} closable={false}>
        <View className="h-full w-full flex-1 items-center justify-center gap-3">
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
              {drawerMode === "success" ? "Login Successfull" : "Login Failed"}
              !!
            </ThemeText>
            <ThemeText className="text-graphite! text-center">
              {error?.data?.detail}
            </ThemeText>
          </View>
        </View>
      </ThemeDrawer>
    </ThemePage>
  );
};

export default Login;

import { View } from "react-native";
import ThemeButton from "@/components/ThemeButton";
import ThemeText from "@/components/ThemeText";
import ThemePage from "@/components/ThemePage";
import OnboardingBg from "@/components/OnboardingBg";
import { Image } from "expo-image";
import { images } from "@/assets";
import ThemeTextInput from "@/components/ThemeTextInput";
import { EmailIcon, LockIcon } from "@/Icon";
import { themeColors } from "@/theme";
import { Controller, useForm } from "react-hook-form";
import { z } from "zod/v4";
import { zodResolver } from "@hookform/resolvers/zod";
import { useSignInMutation } from "@/features/baseApi";
import OrSeparator from "@/components/OrSeparator";
import { Link } from "@react-navigation/native";

const loginSchema = z.object({
  email: z.email(),
  password: z.string().min(3, "Password is Required"),
});

type LoginForm = z.infer<typeof loginSchema>;

const Login = () => {
  const [signIn, { isSuccess, isError, error }] = useSignInMutation();
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
      console.log(values);
      const response = await signIn({
        email: values.email,
        password: values.password,
      }).unwrap();
      console.log(response);
    } catch (error) {
      console.error("Login api error:", error);
    }
  };

  return (
    <ThemePage className="bg-canvas" noSafeArea isScrollable>
      {/* <KeyboardAvoidingView
        behavior={"height"}
        className="h-full"
        // keyboardVerticalOffset={150}
      > */}
      <View className="flex-1 items-center">
        <OnboardingBg className="h-1/2 relative items-center justify-start">
          {/* <BackButton goBack /> */}
          <Image
            style={{
              height: 450,
              width: 450,
              position: "absolute",
              // zIndex: -1,
            }}
            source={images?.onboarding?.login}
            contentFit="cover"
            allowDownscaling={false}
          />
        </OnboardingBg>
        <View
          className="flex-1 w-full pt-5 bg-canvas px-page"
          style={{ zIndex: 99999 }}
        >
          <View className="gap-1">
            <ThemeText className="font-medium text-3xl text-start">
              Welcome back
            </ThemeText>
            <ThemeText className="font-normal! text-graphite!">
              Sign in to continue managing your day
            </ThemeText>
          </View>

          <View className="w-full pt-5">
            <View className="pb-5">
              <Controller
                control={control}
                name="email"
                render={({ field: { value, onChange, onBlur } }) => (
                  <ThemeTextInput
                    placeholder="Email"
                    value={value}
                    onChangeText={onChange}
                    onBlur={onBlur}
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
              {errors && errors?.email?.message && (
                <ThemeText className="mt-1 text-xs text-red-500">
                  {errors?.email?.message}
                </ThemeText>
              )}
            </View>
            <View className="pb-5">
              <Controller
                control={control}
                name="password"
                render={({ field: { value, onChange, onBlur } }) => (
                  <ThemeTextInput
                    placeholder="Password"
                    value={value}
                    onChangeText={onChange}
                    onBlur={onBlur}
                    keyboardType="email-address"
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
              onPress={handleSubmit(submitHandler)}
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
    </ThemePage>
  );
};

export default Login;

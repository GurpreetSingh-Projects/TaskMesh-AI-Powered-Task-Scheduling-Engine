import { Pressable, StyleSheet, Text, View } from "react-native";
import React from "react";
import ThemePage from "@/components/ThemePage";
import OnboardingBg from "@/features/onboarding/components/OnboardingBg";
import { Image } from "expo-image";
import { images } from "@/assets";
import ThemeText from "@/components/ThemeText";
import { Controller, useForm } from "react-hook-form";
import ThemeTextInput from "@/components/ThemeTextInput";
import { EmailIcon, LockIcon } from "@/Icon";
import { themeColors } from "@/theme";
import { z } from "zod/v4";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link, useNavigation } from "@react-navigation/native";
import ThemeButton from "@/components/ThemeButton";
import OrSeparator from "@/components/OrSeparator";
import BackButton from "@/components/BackButton";

const registerSchema = z.object({
  email: z.email(),
  password: z.string().min(3, "Password is Required"),
});

type RegisterForm = z.infer<typeof registerSchema>;

const Register = () => {
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
  return (
    <ThemePage className="bg-canvas" noSafeArea isScrollable>
      {/* <KeyboardAvoidingView
            behavior={"height"}
            className="h-full"
            // keyboardVerticalOffset={150}
          > */}
      {/* <BackButton goBack /> */}
      <View className="flex-1 items-center">
        <OnboardingBg className="h-1/2 relative items-center justify-start">
          <Image
            style={{
              height: 450,
              width: 450,
              zIndex: 0,
            }}
            source={images?.onboarding?.register}
            contentFit="cover"
            allowDownscaling={false}
          />
        </OnboardingBg>
        <View
          className="flex-1 w-full pt-5 bg-canvas px-page"
          style={{ zIndex: 99999 }}
        >
          <View className="gap-1">
            <ThemeText variant="heading" className="text-start">
              Create Account
            </ThemeText>
            <ThemeText className="font-normal! text-graphite!">
              Setup your profile and start planning your day
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
              text="REGISTER NOW"
              onPress={() => {}}
            />
            <>
              <OrSeparator />
              <View className="flex-row w-full items-center justify-center gap-1 mt-5">
                <ThemeText className="text-sm text-steel">
                  Already have an account ?
                </ThemeText>
                <Pressable
                  onPress={() => navigation.canGoBack() && navigation.goBack()}
                >
                  <ThemeText className="font-bold! text-sm text-ink">
                    Login Now
                  </ThemeText>
                </Pressable>
              </View>
            </>
          </View>
        </View>
      </View>
      {/* </KeyboardAvoidingView> */}
    </ThemePage>
  );
};

export default Register;

const styles = StyleSheet.create({});

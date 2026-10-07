import React, { useEffect } from "react";
import { Pressable, useWindowDimensions, View } from "react-native";
import { useLazyOnboardingQuestionnaireQuery } from "@/api/baseApi";
import LottieView from "lottie-react-native";
import { animations, images } from "@/assets";
import { primaryBorderRadius, themeColors } from "@/theme";
import ThemeText from "@/components/ThemeText";
import ThemePage from "@/components/ThemePage";
import {
  Carousel,
  CarouselItemAnimation as TAnimationStyle,
} from "react-native-reanimated-carousel";
import {
  interpolate,
  useSharedValue,
  withTiming,
} from "react-native-reanimated";
import { Image } from "expo-image";
import { colors } from "react-native-keyboard-controller/lib/typescript/components/KeyboardToolbar/colors";
const OnboardingQuestionnaire = () => {
  const { height, width } = useWindowDimensions();

  const [onboardingQuestionnaire, { data, isLoading, isError, error }] =
    useLazyOnboardingQuestionnaireQuery();

  useEffect(() => {
    onboardingQuestionnaire();
  }, [onboardingQuestionnaire]);

  console.log(data);

  return (
    <ThemePage className="bg-canvas" noSafeArea>
      <View className="flex-1 items-center gap-10">
        <View className="w-full pt-[30%] px-page">
          <ThemeText
            variant="subheading"
            className="font-thin! text-start text-steel text-base!"
          >
            Tell us a little about yourself
          </ThemeText>
        </View>
        <View className="w-full items-center justify-center px-page">
          <View className="w-full gap-10">
            <View className="gap-2">
              <ThemeText variant="heading" style={{ color: themeColors.ink }}>
                What best describes you?
              </ThemeText>

              <ThemeText variant="body" style={{ color: themeColors.steel }}>
                Choose the option that best describes you.
              </ThemeText>
            </View>

            <View className="gap-3">
              <Pressable
                className="w-full flex-row items-center rounded-2xl border px-5 py-4"
                style={{
                  borderColor: themeColors.mist,
                  backgroundColor: themeColors.canvas,
                }}
              >
                <View
                  className="h-6 w-6 items-center justify-center rounded-full border-2"
                  style={{ borderColor: themeColors.steel }}
                />

                <View className="ml-4 flex-1 gap-1">
                  <ThemeText variant="body" style={{ color: themeColors.ink }}>
                    Student
                  </ThemeText>

                  <ThemeText style={{ color: themeColors.steel }}>
                    Currently studying
                  </ThemeText>
                </View>
              </Pressable>
            </View>
          </View>
        </View>
        <Image
          source={images.illustrations.illustration1}
          contentFit="cover"
          style={{
            width,
            height: 150,
            position: "absolute",
            bottom: 0,
          }}
        />
      </View>
    </ThemePage>
  );
};
export default OnboardingQuestionnaire;

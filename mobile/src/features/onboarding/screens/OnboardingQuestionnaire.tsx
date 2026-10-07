import React, { useEffect, useState } from "react";
import { Pressable, useWindowDimensions, View } from "react-native";
import { useLazyOnboardingQuestionnaireQuery } from "@/api/baseApi";
import LottieView from "lottie-react-native";
import { animations, images } from "@/assets";
import { primaryBorderRadius, themeColors, themeSpacing } from "@/theme";
import ThemeText from "@/components/ThemeText";
import ThemePage from "@/components/ThemePage";
import {
  Carousel,
  CarouselItemAnimation as TAnimationStyle,
} from "react-native-reanimated-carousel";
import Animated, {
  interpolate,
  useSharedValue,
  withTiming,
} from "react-native-reanimated";
import { Image } from "expo-image";

const OnboardingQuestionnaire = () => {
  const { height, width } = useWindowDimensions();

  const [currentQuestion, setCurrentQuestion] = useState(1);

  const [onboardingQuestionnaire, { data, isLoading, isError, error }] =
    useLazyOnboardingQuestionnaireQuery();

  const totalQuestions = data?.items?.length ?? 0;

  useEffect(() => {
    onboardingQuestionnaire();
  }, [onboardingQuestionnaire]);

  console.log(JSON.stringify(data));

  return (
    <ThemePage className="bg-canvas" noSafeArea>
      <View className="h-2 w-full overflow-hidden rounded-full">
        <Animated.View
          className="h-full rounded-full"
          style={{
            width: `${
              totalQuestions > 0 ? (currentQuestion / totalQuestions) * 100 : 0
            }%`,
            backgroundColor: themeColors.ink,
            transitionProperty: "width",
            transitionDuration: "250ms",
            transitionTimingFunction: "ease-in-out",
          }}
        />
      </View>

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
          <Carousel
            data={data?.items}
            onSnapToItem={(index) => {
              console.log(index);
              setCurrentQuestion(index + 1);
            }}
            renderItem={({ item }) => {
              return (
                <View
                  className="flex-1 gap-10"
                  style={{ paddingHorizontal: themeSpacing?.page }}
                >
                  <View className="gap-3">
                    <ThemeText
                      variant="heading"
                      style={{ color: themeColors.ink }}
                    >
                      {item?.title}
                    </ThemeText>

                    <ThemeText
                      variant="body"
                      style={{ color: themeColors.steel }}
                    >
                      {item?.description}
                    </ThemeText>
                  </View>

                  <View className="gap-3">
                    {item?.options?.map((option) => (
                      <Pressable
                        className="flex-row items-center rounded-2xl border px-5 py-4"
                        style={{
                          borderColor: themeColors.mist,
                          backgroundColor: themeColors.canvas,
                        }}
                        key={option?.option_order}
                      >
                        <View
                          className="h-6 w-6 items-center justify-center rounded-full border-2"
                          style={{ borderColor: themeColors.steel }}
                        />

                        <View className="ml-4 flex-1 gap-1">
                          <ThemeText
                            variant="body"
                            style={{ color: themeColors.ink }}
                          >
                            {option?.title}
                          </ThemeText>

                          {option?.descrioptio && (
                            <ThemeText style={{ color: themeColors.steel }}>
                              {option?.descrioptio}
                            </ThemeText>
                          )}
                        </View>
                      </Pressable>
                    ))}
                  </View>
                </View>
              );
            }}
            style={{
              width: width,
            }}
          />
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

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
import {
  OnboardingQuestion,
  OnboardingQuestionnaireResponse,
  OnboardingQuestionOption,
} from "../types";

const OnboardingQuestionnaire = () => {
  const { height, width } = useWindowDimensions();

  const [currentQuestion, setCurrentQuestion] = useState(1);
  const [responses, setResponses] = useState([]);

  const [onboardingQuestionnaire, { data, isLoading, isError, error }] =
    useLazyOnboardingQuestionnaireQuery();

  const totalQuestions = data?.items?.length ?? 0;

  const areOptionsEqual = (option1, option2) =>
    JSON.stringify(option1) === JSON.stringify(option2);

  const optionPressHandler = (
    onboarding_question_id: string,
    option: OnboardingQuestionOption,
    isMultiSelect: boolean,
  ) => {
    setResponses((prev) => {
      const currSelections = prev[onboarding_question_id] ?? [];

      const isPreviouslySelected = currSelections.some((selections) => {
        return areOptionsEqual(selections, option);
      });

      const selectedOptions = isMultiSelect
        ? isPreviouslySelected
          ? currSelections?.filter(
              (selectedOption) => !areOptionsEqual(selectedOption, option),
            )
          : [...currSelections, option]
        : [option];

      return {
        ...prev,
        [onboarding_question_id]: selectedOptions,
      };
    });
  };

  const isOptionSelected = (
    onboardingQuestionId: string,
    option: OnboardingQuestionOption,
  ) => {
    const result =
      responses[onboardingQuestionId]?.some((selectedOption) =>
        areOptionsEqual(selectedOption, option),
      ) ?? false;

    return result;
  };

  useEffect(() => {
    onboardingQuestionnaire();
  }, [onboardingQuestionnaire]);

  console.log(responses);

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
              setCurrentQuestion(index + 1);
            }}
            renderItem={({ item }: { item: OnboardingQuestion }) => {
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
                    {item?.options?.map((option) => {
                      const selected = isOptionSelected(
                        item.onboarding_question_id,
                        option,
                      );
                      return (
                        <Pressable
                          className="flex-row items-center rounded-2xl border px-5 py-4"
                          style={{
                            borderColor: themeColors.mist,
                            backgroundColor: themeColors.canvas,
                          }}
                          key={option?.option_order}
                          onPress={() =>
                            optionPressHandler(
                              item.onboarding_question_id,
                              option,
                              item?.question_type == "MCQ_MULTI_SELECT",
                            )
                          }
                        >
                          <View
                            className="h-6 w-6 items-center justify-center rounded-full border-2"
                            style={{
                              borderColor: selected
                                ? themeColors.ink
                                : themeColors.steel,
                            }}
                          >
                            {selected && (
                              <View
                                className="h-3 w-3 rounded-full"
                                style={{
                                  backgroundColor: themeColors.ink,
                                }}
                              />
                            )}
                          </View>

                          <View className="ml-4 flex-1 gap-1">
                            <ThemeText
                              variant="body"
                              style={{ color: themeColors.ink }}
                            >
                              {item?.options ==
                                responses[item.onboarding_question_id]?.options}
                              {option?.title}
                            </ThemeText>

                            {option?.description && (
                              <ThemeText style={{ color: themeColors.steel }}>
                                {option?.description}
                              </ThemeText>
                            )}
                          </View>
                        </Pressable>
                      );
                    })}
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

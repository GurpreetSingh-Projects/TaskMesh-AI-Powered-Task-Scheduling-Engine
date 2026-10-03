import { useEffect } from "react";
import { View } from "react-native";
import { useLazyOnboardingQuestionnaireQuery } from "@/api/baseApi";
import LottieView from "lottie-react-native";
import { animations } from "@/assets";
import { themeColors } from "@/theme";
import ThemeText from "@/components/ThemeText";

const OnboardingQuestionnaire = () => {
  const [onboardingQuestionnaire, { data, isLoading, isError, error }] =
    useLazyOnboardingQuestionnaireQuery();

  useEffect(() => {
    onboardingQuestionnaire();
  }, [onboardingQuestionnaire]);

  if (isLoading) {
    return (
      <View className="flex-1 items-center justify-center bg-red-100">
        <LottieView
          source={animations.loadingIcon}
          autoPlay
          loop={true}
          style={{ width: 50, height: 50 }}
          colorFilters={[{ keypath: "**", color: themeColors?.ink }]}
        />
      </View>
    );
  }

  if (isError) {
    console.log("Onboarding questionnaire error:", error);

    return (
      <View className="flex-1 items-center justify-center px-6">
        <ThemeText className="text-center text-white">
          Failed to load questionnaire.
        </ThemeText>

        <ThemeText
          className="mt-4 text-white underline"
          onPress={() => onboardingQuestionnaire()}
        >
          Try Again
        </ThemeText>
      </View>
    );
  }

  return (
    <View className="flex-1">
      {data?.items?.map((question) => (
        <View key={question.onboarding_question_id} className="mb-6">
          <ThemeText className="text-lg font-semibold text-white">
            {question.title}
          </ThemeText>

          <ThemeText className="mt-2 text-sm text-gray-400">
            {question.description}
          </ThemeText>
        </View>
      ))}
    </View>
  );
};

export default OnboardingQuestionnaire;

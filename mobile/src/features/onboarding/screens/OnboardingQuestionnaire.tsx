import React, { useEffect } from "react";
import { useWindowDimensions, View } from "react-native";
import { useLazyOnboardingQuestionnaireQuery } from "@/api/baseApi";
import LottieView from "lottie-react-native";
import { animations } from "@/assets";
import { primaryBorderRadius, themeColors } from "@/theme";
import ThemeText from "@/components/ThemeText";
import ThemePage from "@/components/ThemePage";
import { Carousel, CarouselItemAnimation as TAnimationStyle } from "react-native-reanimated-carousel";
import { interpolate, useSharedValue, withTiming, } from "react-native-reanimated";
const OnboardingQuestionnaire = () => {
    const { height, width } = useWindowDimensions();
    const pressAnim = useSharedValue<number>(0);
    const animationStyle: TAnimationStyle = React.useCallback((value: number) => {
        "worklet";
        const zIndex = interpolate(value, [-1, 0, 1], [-1000, 0, 1000]);
        const translateX = interpolate(value, [-1, 0, 1], [-width, 0, width]);
        return {
            transform: [{ translateX }],
            zIndex,
        };
    }, []);
    const [onboardingQuestionnaire, { data, isLoading, isError, error }] = useLazyOnboardingQuestionnaireQuery();
    useEffect(() => {
        onboardingQuestionnaire();
    }, [onboardingQuestionnaire]);
    return (<ThemePage className="bg-canvas" noSafeArea>
      <View className="flex-1 gap-default items-center justify-center">
        {/* <Carousel
          loop={true}
          autoPlay
          width={width}
          height={height / 1.5}
          data={}
          onScrollStart={() => {
            pressAnim.value = withTiming(1);
          }}
          onScrollEnd={() => {
            pressAnim.value = withTiming(0);
          }}
          renderItem={({ index }) => {
            return (
              <CustomItem index={index} key={index} pressAnim={pressAnim} />
            );
          }}
          customAnimation={animationStyle}
          scrollAnimationDuration={1500}
          style={{
            borderRadius: primaryBorderRadius?.default,
            zIndex: -10,
          }}
          autoPlayInterval={2500}
        /> */}
      </View>
    </ThemePage>);
};
export default OnboardingQuestionnaire;

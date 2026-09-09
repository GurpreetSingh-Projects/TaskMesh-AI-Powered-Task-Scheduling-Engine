import { useWindowDimensions, View } from "react-native";
import React from "react";
import ThemePage from "@/components/ThemePage";
import Animated, {
  interpolate,
  useAnimatedStyle,
  useSharedValue,
  withTiming,
} from "react-native-reanimated";
import type { SharedValue } from "react-native-reanimated";
import Carousel, { TAnimationStyle } from "react-native-reanimated-carousel";
import { carouselImages, images } from "@/assets";
import { SlideItem } from "@/components/SlideItem";
import { primaryBorderRadius } from "@/theme";
import ThemeButton from "@/components/ThemeButton";
import ThemeText from "@/components/ThemeText";
import OnboardingBg from "@/features/onboarding/components/OnboardingBg";
import { useNavigation } from "@react-navigation/native";
import { AuthStackParamList } from "@/features/auth/types";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";

const OnboardingCarousel = () => {
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

  const navigation =
    useNavigation<NativeStackNavigationProp<AuthStackParamList>>();

  return (
    <ThemePage className="bg-canvas" noSafeArea>
      <View className="flex-1 gap-default items-center justify-center">
        <OnboardingBg className="relative">
          <Carousel
            loop={true}
            autoPlay
            width={width}
            height={height / 1.5}
            data={carouselImages}
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
          />
        </OnboardingBg>
        <View className="flex-1 w-full items-center pt-5 gap-5 z-10 px-page relative">
          <View className="gap-1">
            <ThemeText variant="heading" className="text-center">
              Meet TaskMesh, Organizing your day just got smarter
            </ThemeText>
          </View>
          <ThemeText className="text-sm font-normal! text-center text-graphite!">
            A smart app for helping you manage your daily tasks effectively,
            with timely reminders, ease of use and powered by{" "}
            <ThemeText className="font-bold!">AI</ThemeText>
          </ThemeText>
          <View className="w-full absolute bottom-5">
            {/* <ThemeButton
              className="bg-ink mx-default! rounded-full"
              textColor="text-white!"
              text="GET STARTED"
              onPress={() => {
                navigation.navigate("Login");
              }}
            /> */}
            <ThemeButton
              className="bg-ink mx-default! rounded-full items-center justify-center"
              onPress={() => navigation.navigate("Login")}
            >
              <ThemeText className="font-bold text-white text-center text-base">
                GET STARTED
              </ThemeText>
            </ThemeButton>
          </View>
        </View>
      </View>
    </ThemePage>
  );
};

export default OnboardingCarousel;

interface ItemProps {
  pressAnim: SharedValue<number>;
  index: number;
}

const CustomItem: React.FC<ItemProps> = ({ pressAnim, index }) => {
  const animStyle = useAnimatedStyle(() => {
    const scale = interpolate(pressAnim.value, [0, 1], [1, 0.9]);
    const borderRadius = interpolate(pressAnim.value, [0, 1], [0, 30]);

    return {
      transform: [{ scale }],
      borderRadius,
    };
  }, []);

  return (
    <Animated.View style={[{ flex: 1, overflow: "hidden" }, animStyle]}>
      <SlideItem source={carouselImages[index]} index={index} />
    </Animated.View>
  );
};

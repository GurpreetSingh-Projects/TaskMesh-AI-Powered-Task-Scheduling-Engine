import Animated from "react-native-reanimated";

const pulse = { from: { opacity: 1 }, to: { opacity: 0.4 } };

export function ThemeSkeleton({ style }: { style?: any }) {
  return (
    <Animated.View
      style={[
        {
          backgroundColor: "#262626",
          borderRadius: 8,
          animationName: pulse,
          animationDuration: "800ms",
          animationIterationCount: "infinite",
          animationDirection: "alternate",
          animationTimingFunction: "ease-in-out",
        },
        style,
      ]}
    />
  );
}

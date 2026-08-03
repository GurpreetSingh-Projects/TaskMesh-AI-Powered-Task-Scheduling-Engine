import React, { useMemo } from "react";
import {
  ImageSourcePropType,
  type ImageStyle,
  type StyleProp,
  StyleSheet,
  Text,
  View,
  type ViewProps,
} from "react-native";
import type { AnimatedProps } from "react-native-reanimated";
import Animated from "react-native-reanimated";
import { Image } from "expo-image";
import { primaryBorderRadius } from "@/theme";

interface Props extends AnimatedProps<ViewProps> {
  style?: StyleProp<ImageStyle>;
  index?: number;
  source?: ImageSourcePropType;
}

export const SlideItem: React.FC<Props> = (props) => {
  const { style, index = 0, ...animatedViewProps } = props;

  const source = useMemo(() => props.source, [index, props.source]);

  return (
    <Animated.View style={{ flex: 1 }} {...animatedViewProps}>
      <Image
        style={[
          style,
          {
            height: "100%",
            width: "100%",
            borderRadius: primaryBorderRadius?.default,
            paddingHorizontal: 50,
          },
        ]}
        source={source}
        contentFit="cover"
        allowDownscaling={false}
      />
    </Animated.View>
  );
};

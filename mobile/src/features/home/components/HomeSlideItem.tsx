import React, { useMemo } from "react";
import {
  ImageSourcePropType,
  type ImageStyle,
  type StyleProp,
  type ViewProps,
} from "react-native";
import type { AnimatedProps } from "react-native-reanimated";
import Animated from "react-native-reanimated";
import { Image } from "expo-image";
import { primaryBorderRadius } from "@/theme";
import { TaskItem } from "@/features/tasks/types";

interface Props extends AnimatedProps<ViewProps> {
  style?: StyleProp<ImageStyle>;
  task: TaskItem;
}

export const HomeSlideItem: React.FC<Props> = (props) => {
  const { style, ...animatedViewProps } = props;

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
        source={{ uri: props?.task?.image_url }}
        contentFit="cover"
        allowDownscaling={false}
      />
    </Animated.View>
  );
};

// const CustomItem = ({
//   pressAnim,
//   index,
//   animStyle,
//   carouselImages,
//   isActive,
// }) => {
//   return (
//     <Animated.View
//       className="w-[280px] h-[480px] items-center"
//       style={[animStyle]}
//     >
//       {/* Main Card */}
//       <View className="flex-1 w-full rounded-[36px] overflow-hidden border-[1.5px] border-white bg-black shadow-xl">
//         <SlideItem source={carouselImages[index]} index={index} />

//         {/* Dark gradient overlay covering bottom 45% */}
//         <View className="absolute inset-x-0 bottom-0 top-[55%] bg-black/40 backdrop-blur-md" />

//         {/* Content Container */}
//         <View className="absolute bottom-6 left-5 right-5 items-start">
//           {/* Title */}
//           <ThemeText
//             variant="heading"
//             className="text-white mb-2"
//             numberOfLines={1}
//           >
//             Submit quarterly report
//           </ThemeText>

//           {/* Description */}
//           <ThemeText
//             variant="body"
//             className="text-[#A0A0A5] mb-4"
//             numberOfLines={2}
//           >
//             Finalize the numbers and send the report to the finance team for
//             review.
//           </ThemeText>

//           {/* Glass Chips Row */}
//           <View className="flex-row gap-2 mb-5">
//             <View className="flex-row items-center bg-white/15 px-3 py-1.5 rounded-full border border-white/20">
//               <ThemeText variant="body" className="text-white text-xs">
//                 ⏳ Pending
//               </ThemeText>
//             </View>
//             <View className="flex-row items-center bg-white/15 px-3 py-1.5 rounded-full border border-white/20">
//               <ThemeText variant="body" className="text-white text-xs">
//                 🚩 Normal
//               </ThemeText>
//             </View>
//           </View>

//           {/* Full-width White Pill Button */}
//           <View className="w-full bg-white py-3.5 rounded-full items-center justify-center">
//             <ThemeText variant="button" className="text-[#1C1C1E]">
//               Mark as done
//             </ThemeText>
//           </View>
//         </View>
//       </View>

//       {/* Overdue text displayed directly below the main card */}
//       {isActive && (
//         <ThemeText variant="body" className="mt-3 text-[#FF3B30] text-center">
//           Overdue by 5 hours
//         </ThemeText>
//       )}
//     </Animated.View>
//   );
// };

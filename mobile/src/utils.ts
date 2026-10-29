import { Image } from "expo-image";
import Animated from "react-native-reanimated";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";
import duration from "dayjs/plugin/duration";
import relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(utc);
dayjs.extend(timezone);
dayjs.extend(relativeTime);
dayjs.extend(duration);

export function getISTTime(time?: Date) {
  if (time) {
    return dayjs(time).format("YYYY-MM-DD HH:mm:ss");
  }
  return dayjs().format("YYYY-MM-DD HH:mm:ss");
}

export function timeLeft(time?: Date) {
  return dayjs(time).fromNow();
}

export const AnimatedImage = Animated.createAnimatedComponent(Image);

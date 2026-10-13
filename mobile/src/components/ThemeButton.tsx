import { Pressable, PressableProps } from "react-native";
import ThemeText from "./ThemeText";
import LottieView from "lottie-react-native";
import { animations } from "@/assets";
import { ReactNode } from "react";

type ThemeButtonVariant = "primary" | "secondary";
type ButtonStatus = "default" | "loading" | "success" | "error";

type ThemeButtonProps = PressableProps & {
  className?: string;
  textColor?: string;
  textClassName?: string;
  text?: string;
  status?: ButtonStatus;
  variant?: ThemeButtonVariant;
  children?: ReactNode;
};

const variantClasses: Record<ThemeButtonVariant, string> = {
  primary: "text-canvas bg-ink border border-ink",
  secondary: "text-ink bg-canvas border-mist",
};

const ThemeButton = (props: ThemeButtonProps) => {
  const statusAnimation =
    props?.status === "loading"
      ? animations.loadingIcon
      : props?.status === "success"
        ? animations.tickIconSimple
        : props?.status === "error" && animations.crossIconSimple;

  return (
    <Pressable
      onPress={props?.onPress}
      className={`p-default gap-default items-center justify-center rounded-default my-default font-semibold max-h-[50px] ${props?.className}`}
      style={{
        elevation: 8,
      }}
    >
      {props.children ? (
        props.children
      ) : props?.status == "default" ? (
        <ThemeText
          className={`font-extrabold text-center text-base border mx-default! rounded-full ${variantClasses[props?.variant ?? "primary"]} ${props?.textColor} ${props?.textClassName}`}
        >
          {props?.text}
        </ThemeText>
      ) : (
        <LottieView
          source={statusAnimation}
          autoPlay
          loop={false}
          style={{ width: 50, height: 50 }}
          colorFilters={[{ keypath: "**", color: "#ffffff" }]}
        />
      )}
    </Pressable>
  );
};

export default ThemeButton;

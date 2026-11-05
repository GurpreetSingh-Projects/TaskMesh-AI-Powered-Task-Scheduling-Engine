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

const variantClasses: Record<
  ThemeButtonVariant,
  {
    button: string;
    text: string;
    disabledButton: string;
    disabledText: string;
  }
> = {
  primary: {
    button: "bg-ink border border-ink",
    text: "text-canvas",
    disabledButton: "bg-steel border border-steel",
    disabledText: "text-mist",
  },
  secondary: {
    button: "bg-canvas border border-mist",
    text: "text-ink",
    disabledButton: "bg-canvas border border-mist",
    disabledText: "text-steel",
  },
};

const ThemeButton = (props: ThemeButtonProps) => {
  const status = props?.status ?? "default";
  const variant = variantClasses[props?.variant ?? "primary"];
  const disabled = props?.disabled || status === "loading";

  const statusAnimation =
    status === "loading"
      ? animations.loadingIcon
      : status === "success"
        ? animations.tickIconSimple
        : status === "error"
          ? animations.crossIconSimple
          : null;

  return (
    <Pressable
      onPress={props?.onPress}
      disabled={disabled}
      accessibilityState={{ disabled: disabled }}
      className={`p-default gap-default items-center justify-center rounded-full max-h-[50px] ${disabled ? variant.disabledButton : variant.button} ${props.className ?? ""}`}
      style={{ elevation: 8 }}
    >
      {props.children ? (
        props.children
      ) : status === "default" ? (
        <ThemeText
          className={`font-extrabold text-center text-base mx-default! rounded-full ${disabled ? variant.disabledText : variant.text} ${props.textClassName ?? ""}`}
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

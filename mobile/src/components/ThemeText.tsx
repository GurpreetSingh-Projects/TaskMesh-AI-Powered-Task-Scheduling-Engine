import { Text, TextProps } from "react-native";

type TextVariant = "button" | "heading" | "subheading" | "body";

type ThemeTextProps = TextProps & {
  className?: string;
  variant?: TextVariant;
};

const variantClasses: Record<TextVariant, string> = {
  button: "font-bold text-base leading-[16px]",
  heading: "font-bold! text-2xl leading-tight",
  subheading: "font-semibold! text-xl leading-tight",
  body: "font-medium text-sm leading-normal",
};

const ThemeText = (props: ThemeTextProps) => {
  return (
    <Text
      {...props}
      className={`wrap-break-word ${variantClasses[props?.variant ?? "body"]} ${props?.className}`}
      style={[
        {
          includeFontPadding: false,
          textAlignVertical: "center",
        },
        props?.style,
      ]}
    >
      {props?.children}
    </Text>
  );
};

export default ThemeText;

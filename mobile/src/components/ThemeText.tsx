import { Text, TextProps } from "react-native";

type TextVariant =
  | "button"
  | "heading"
  | "subheading"
  | "title"
  | "body"
  | "cardTitle"
  | "cardDescription"
  | "label";

type ThemeTextProps = TextProps & {
  className?: string;
  variant?: TextVariant;
};

const variantClasses: Record<TextVariant, string> = {
  button: "font-bold text-base leading-[16px]",
  heading: "font-bold! text-2xl leading-tight",
  subheading: "font-semibold! text-xl leading-tight",
  title: "font-semibold! text-base leading-normal",
  body: "font-medium text-sm leading-normal",
  cardTitle: "font-semibold text-2xl leading-tight",
  cardDescription: "font-medium leading-normal",
  label: "font-normal text-xs",
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
      {""}
    </Text>
  );
};

export default ThemeText;

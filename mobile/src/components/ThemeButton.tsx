import { Pressable } from "react-native";
import ThemeText from "./ThemeText";

const ThemeButton = (props) => {
  const pressHandler = (): void => {
    if (props.onPress) {
      props.onPress();
    }
  };

  return (
    <Pressable
      onPress={pressHandler}
      className={`p-default gap-default items-center rounded-default my-default font-semibold max-h-[50px] ${props?.className}`}
      style={{
        elevation: 8,
      }}
    >
      {props.children ? (
        props.children
      ) : (
        <ThemeText
          className={`font-extrabold text-white text-center text-base ${props?.textColor} ${props?.textClassName}`}
        >
          {props?.text}
        </ThemeText>
      )}
    </Pressable>
  );
};

export default ThemeButton;

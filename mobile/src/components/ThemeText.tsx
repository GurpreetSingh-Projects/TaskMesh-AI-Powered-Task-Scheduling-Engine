import { Text } from "react-native";

const ThemeText = (props) => {
  return (
    <Text className={`font-medium ${props?.className}`} style={props?.style}>
      {props?.children}
    </Text>
  );
};

export default ThemeText;

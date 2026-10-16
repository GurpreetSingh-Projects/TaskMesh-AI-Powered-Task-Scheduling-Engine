import { Pressable, TextInputProps, View } from "react-native";
import React, { memo, useState } from "react";
import { TextInput } from "react-native-gesture-handler";
import { themeColors } from "@/theme";
import { Eye, EyeOff } from "lucide-react-native";
import { BottomSheetTextInput } from "@gorhom/bottom-sheet";

type ThemeTextInputProps = TextInputProps & {
  icon?: React.ReactNode;
  secure?: boolean;
  mode?: "default" | "bottom-sheet";
  variant?: "primary" | "secondary";
};

const variants = {
  primary: {
    box: "",
    focused: "border-ash",
    idle: "border-mist",
    text: themeColors?.ash,
    placeholder: themeColors?.steel,
    cursor: themeColors?.obsidian,
    icon: themeColors?.obsidian,
  },
  secondary: {
    box: "",
    focused: "border-mist",
    idle: "border-steel",
    text: themeColors?.canvas,
    placeholder: themeColors?.steel,
    cursor: themeColors?.steel,
    icon: themeColors?.ink,
  },
};

const ThemeTextInput = memo((props: ThemeTextInputProps) => {
  const Container =
    props?.mode === "bottom-sheet" ? BottomSheetTextInput : TextInput;

  const variant = variants[props?.variant ?? "primary"];

  const [isFocussed, setIsFocussed] = useState<boolean>(false);
  const [isSecure, setIsSecure] = useState<boolean>(false);

  const { onChangeText, ...rest } = props;

  const changeHandler = (text: string) => {
    onChangeText(text);
  };

  return (
    <View
      className={`w-full border items-center ${variant.box} ${isFocussed ? variant.focused : variant.idle} px-3 ${
        props?.numberOfLines ? "h-[100px]" : "h-[45px]"
      } flex-row gap-default-half rounded-default`}
    >
      {props?.icon && props.icon}

      <Container
        {...rest}
        keyboardType={props?.keyboardType ? props?.keyboardType : "default"}
        onChangeText={changeHandler}
        maxLength={props?.maxLength ?? 255}
        value={props?.value}
        onFocus={() => {
          setIsFocussed(true);
        }}
        onBlur={() => {
          setIsFocussed(false);
        }}
        style={{
          width: isSecure || props?.icon ? "85%" : "100%",
          height: "100%",
          color: variant.text,
        }}
        placeholderTextColor={
          props?.placeholderTextColor ?? variant.placeholder
        }
        cursorColor={props?.cursorColor ?? variant.cursor}
        secureTextEntry={isSecure}
        textAlignVertical={props?.textAlignVertical}
      />

      {props?.secure && (
        <Pressable
          onPress={() => {
            setIsSecure((prev) => !prev);
          }}
          className="h-full items-center justify-center flex-1 pr-5"
        >
          {isSecure ? (
            <Eye
              height={25}
              width={25}
              strokeWidth={1.5}
              color={variant.icon}
            />
          ) : (
            <EyeOff
              height={25}
              width={25}
              strokeWidth={1.5}
              color={variant.icon}
            />
          )}
        </Pressable>
      )}
    </View>
  );
});

export default ThemeTextInput;

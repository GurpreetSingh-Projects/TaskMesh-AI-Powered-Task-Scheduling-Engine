import { Pressable, TextInputProps, View } from "react-native";
import React, { memo, useState } from "react";
import { TextInput } from "react-native-gesture-handler";
import { themeColors } from "@/theme";
import ThemeText from "./ThemeText";
import { HideVisibilityIcon, VisibilityIcon } from "@/Icon";

type ThemeTextInputProps = TextInputProps & {
  icon?: React.ReactNode;
  secure?: boolean;
};

const ThemeTextInput = memo((props: ThemeTextInputProps) => {
  const [isFocussed, setIsFocussed] = useState<boolean>(false);
  const [isSecure, setIsSecure] = useState<boolean>(true);

  const { onChangeText, ...rest } = props;

  const changeHandler = (text: string) => {
    onChangeText(text);
  };

  return (
    <View
      className={`w-full border items-center ${isFocussed ? "border-ash" : "border-mist"} px-3 ${
        props?.numberOfLines ? "h-[100px]" : "h-[45px]"
      } flex-row gap-default-half rounded-default`}
    >
      {props?.icon && props.icon}

      <TextInput
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
          color: themeColors?.ash,
        }}
        placeholderTextColor={themeColors?.steel}
        cursorColor={themeColors?.obsidian}
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
            <VisibilityIcon
              height={25}
              width={25}
              strokeWidth={1.5}
              color={themeColors?.obsidian}
            />
          ) : (
            <HideVisibilityIcon
              height={25}
              width={25}
              strokeWidth={1.5}
              color={themeColors?.obsidian}
            />
          )}
        </Pressable>
      )}
    </View>
  );
});

export default ThemeTextInput;

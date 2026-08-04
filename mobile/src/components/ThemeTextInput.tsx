import { Pressable, View } from "react-native";
import React, { memo, useState } from "react";
import { TextInput } from "react-native-gesture-handler";
import { themeColors } from "@/theme";
import ThemeText from "./ThemeText";
import { HideVisibilityIcon, VisibilityIcon } from "@/Icon";

const ThemeTextInput = memo((props: any) => {
  const [isFocussed, setIsFocussed] = useState<boolean>(false);
  const [isSecure, setIsSecure] = useState<boolean>(props?.secure ?? false);

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
        onChangeText={changeHandler}
        maxLength={props?.maxLength ?? 255}
        onFocus={() => {
          setIsFocussed(true);
        }}
        onBlur={() => {
          setIsFocussed(false);
        }}
        style={{
          width: props?.secure || props?.icon ? "85%" : "100%",
          height: "100%",
        }}
        placeholderTextColor={themeColors?.mist}
        cursorColor={themeColors?.obsidian}
        secureTextEntry={isSecure}
        textAlignVertical={props?.textAlignVertical}
      />

      {props?.secure && (
        <Pressable
          onPress={() => {
            setIsSecure((prev) => !prev);
          }}
          className="h-full items-center justify-center flex-1"
        >
          {isSecure ? (
            <VisibilityIcon
              height={25}
              width={25}
              strokeWidth={2.0}
              color={themeColors?.obsidian}
            />
          ) : (
            <HideVisibilityIcon
              height={25}
              width={25}
              strokeWidth={2.0}
              color={themeColors?.obsidian}
            />
          )}
        </Pressable>
      )}
    </View>
  );
});

export default ThemeTextInput;

import { Pressable, StyleSheet, Text, View } from "react-native";
import React from "react";
import { useNavigation } from "@react-navigation/native";
import { themeColors } from "@/theme";
import { ChevronLeftIcon } from "@/Icon";

const BackButton = (props) => {
  const navigation = useNavigation();
  function clickHandler() {
    navigation.goBack();
  }
  return (
    <Pressable
      onPress={() => {
        props?.goBack && clickHandler();
      }}
      className="shadow-sm z-999 rounded-default"
      hitSlop={15}
    >
      <View className="items-center justify-center h-11.5 w-11.5 rounded-full">
        <ChevronLeftIcon stroke={themeColors?.ink} height={20} width={20} />
      </View>
    </Pressable>
  );
};

export default BackButton;

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
      style={{ zIndex: 9999 }}
      onPress={() => {
        props?.goBack && clickHandler();
        console.log("Back button clicked");
      }}
    >
      <View
        className="border! border-disabled rounded-default px-0! h-[35px] w-[35px] mb-5 bg-canvas items-center justify-center"
        style={{
          elevation: 8,
        }}
      >
        <ChevronLeftIcon stroke={themeColors?.ink} height={20} width={20} />
      </View>
    </Pressable>
  );
};

export default BackButton;

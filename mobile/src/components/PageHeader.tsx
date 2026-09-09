import { Platform, View } from "react-native";
import React from "react";
import BackButton from "./BackButton";
import ThemeText from "./ThemeText";

const PageHeader = (props) => {
  return (
    <>
      {!props?.backMode ? (
        <View className="w-full">
          <View className="absolute left-0 p-3 top-[12.5%]">
            <BackButton goBack />
          </View>
          <View className="items-center">
            <ThemeText
              className="font-bold! text-lg h-[40px] mt-[25px] mb-[15px] opacity-55 max-w-[72%] truncate"
              numberOfLines={1}
            >
              {props?.heading ? props?.heading : ""}
            </ThemeText>
          </View>
        </View>
      ) : (
        <View
          className="absolute left-0 p-3 z-50"
          style={{
            top:
              Platform.OS == "ios"
                ? props?.noSafeArea
                  ? "7.5%"
                  : "1%"
                : props?.noSafeArea
                  ? "2.5%"
                  : "1.5%",
          }}
        >
          <BackButton goBack />
        </View>
      )}
    </>
  );
};

export default PageHeader;

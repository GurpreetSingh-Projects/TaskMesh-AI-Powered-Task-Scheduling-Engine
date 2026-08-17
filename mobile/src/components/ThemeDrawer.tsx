import { StyleSheet, Text, View } from "react-native";
import React, { useCallback, useEffect, useRef } from "react";
import {
  BottomSheetBackdrop,
  BottomSheetModal,
  BottomSheetProps,
  BottomSheetView,
} from "@gorhom/bottom-sheet";
import { themeColors } from "@/theme";
import ThemeText from "./ThemeText";
import { LinearGradient } from "expo-linear-gradient";

type ThemeDrawerProps = {
  ref?: any;
  children?: React.ReactNode;
  snapPoints?: BottomSheetProps["snapPoints"];
  minHeight?: string;
  onOpen?: () => void;
  onDismiss?: () => void;
  closable?: boolean;
  className?: string;
  backdropPressBehavior?: string;
};

const ThemeDrawer = (props: ThemeDrawerProps) => {
  const ThemeDrawerBackdrop = useCallback(
    (backdropProps) => (
      <BottomSheetBackdrop
        {...backdropProps}
        disappearsOnIndex={-1}
        appearsOnIndex={0}
        pressBehavior={props?.backdropPressBehavior ?? "none"}
        style={[
          backdropProps?.style,
          {
            backgroundColor: themeColors?.ash,
          },
        ]}
      />
    ),
    [props?.backdropPressBehavior],
  );

  const ThemeDrawerPill = () =>
    props?.closable ? (
      <View className="h-1.5 w-1/10 rounded-full bg-cloud self-center my-3" />
    ) : (
      <></>
    );

  return (
    <BottomSheetModal
      ref={props.ref}
      stackBehavior="replace"
      backdropComponent={ThemeDrawerBackdrop}
      enableDynamicSizing={props?.closable}
      snapPoints={props?.snapPoints ?? ["25%", "50%", "75%", "95%"]}
      enablePanDownToClose={props?.closable}
      onDismiss={props?.onDismiss}
      handleComponent={ThemeDrawerPill}
    >
      <BottomSheetView className="h-full w-full">
        {props?.children}
      </BottomSheetView>
    </BottomSheetModal>
  );
};

export default ThemeDrawer;

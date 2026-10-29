import { View } from "react-native";
import React, { useCallback } from "react";
import BottomSheet, {
  BottomSheetBackdrop,
  BottomSheetModal,
  BottomSheetProps,
  BottomSheetView,
} from "@gorhom/bottom-sheet";
import { themeColors } from "@/theme";

type ThemeSheetProps = {
  ref?: any;
  children?: React.ReactNode;
  snapPoints?: BottomSheetProps["snapPoints"];
  minHeight?: string;
  onDismiss?: () => void;
  closable?: boolean;
  className?: string;
  style?: any;
  backgroundStyle?: any;
};

const ThemeSheet = (props: ThemeSheetProps & BottomSheetProps) => {
  const ThemeDrawerPill = () =>
    props?.closable ? (
      <View className="h-1.5 w-1/10 relative self-center bg-cloud rounded-full my-3" />
    ) : (
      <View className="h-2.5 bg-transparent" />
    );
  return (
    <BottomSheet
      ref={props?.ref}
      snapPoints={props?.snapPoints ?? ["25%", "50%", "75%", "95%"]}
      enablePanDownToClose={props?.closable}
      handleComponent={ThemeDrawerPill}
      style={props?.style}
      backgroundStyle={props?.backgroundStyle}
      enableDynamicSizing={props?.enableDynamicSizing}
      keyboardBehavior="interactive"
      keyboardBlurBehavior="restore"
      {...props}
    >
      <BottomSheetView className={`h-full w-full relative`}>
        {props?.children}
      </BottomSheetView>
    </BottomSheet>
  );
};

export default ThemeSheet;

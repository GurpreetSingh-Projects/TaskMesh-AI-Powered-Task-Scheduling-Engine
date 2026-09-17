import { ReactNode, useState } from "react";
import { View } from "react-native";
import {
  KeyboardAwareScrollView,
  KeyboardStickyView,
} from "react-native-keyboard-controller";
import { SafeAreaView } from "react-native-safe-area-context";
import { useKeepAwake } from "expo-keep-awake";
import { themeColors } from "@/theme";

export type ThemePageProps = {
  children: ReactNode;
  footer?: ReactNode;
  className?: string;
  noSafeArea?: boolean;
  isScrollable?: boolean;
  backgroundColor?: string;
  keyboardOffsetOpened?: number;
  keyboardOffsetClosed?: number;
};

const ThemePage = (props: ThemePageProps) => {
  useKeepAwake();

  const Container = props?.noSafeArea ? View : SafeAreaView;

  const content = (
    <View className={`flex-1 ${props?.className}`}>{props?.children}</View>
  );

  const [footerHeight, setFooterHeight] = useState<number>(0);

  return (
    <Container
      style={{
        flex: 1,
        backgroundColor: props?.backgroundColor ?? themeColors?.canvas,
      }}
    >
      {props?.isScrollable ? (
        <KeyboardAwareScrollView
          contentContainerStyle={{
            flexGrow: 1,
            paddingBottom: footerHeight,
          }}
          bottomOffset={footerHeight * 1.25}
          // mode="layout"
          mode="insets"
          // showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        >
          {content}
        </KeyboardAwareScrollView>
      ) : (
        content
      )}

      {props?.footer && (
        <KeyboardStickyView
          offset={{
            closed: props?.keyboardOffsetClosed ?? 0,
            opened: props?.keyboardOffsetOpened ?? 0,
          }}
          onLayout={(e) => setFooterHeight(e.nativeEvent.layout.height)}
        >
          {props.footer}
        </KeyboardStickyView>
      )}
    </Container>
  );
};

export default ThemePage;

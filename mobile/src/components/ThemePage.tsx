import { ReactNode } from "react";
import { View } from "react-native";
import {
  KeyboardAwareScrollView,
  KeyboardStickyView,
} from "react-native-keyboard-controller";
import { SafeAreaView } from "react-native-safe-area-context";
import { useKeepAwake } from "expo-keep-awake";

export type ThemePageProps = {
  children: ReactNode;
  footer?: ReactNode;
  className?: string;
  noSafeArea?: boolean;
  isScrollable?: boolean;
};

const ThemePage = (props: ThemePageProps) => {
  useKeepAwake();
  const Container = props?.noSafeArea ? View : SafeAreaView;
  const content = (
    <View className={`flex-1 ${props?.className}`}>{props?.children}</View>
  );
  return (
    <Container style={{ flex: 1 }}>
      {props?.isScrollable ? (
        <KeyboardAwareScrollView
          contentContainerStyle={{ flexGrow: 1 }}
          mode="layout"
          // showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        >
          {content}
        </KeyboardAwareScrollView>
      ) : (
        content
      )}
      {props?.footer && (
        <KeyboardStickyView offset={{ closed: 0, opened: 0 }}>
          {props.footer}
        </KeyboardStickyView>
      )}
    </Container>
  );
};

export default ThemePage;

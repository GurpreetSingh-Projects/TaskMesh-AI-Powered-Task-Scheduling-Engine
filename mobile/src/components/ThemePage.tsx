import { ReactNode } from "react";
import { View } from "react-native";
import { KeyboardAwareScrollView } from "react-native-keyboard-controller";
import { SafeAreaView } from "react-native-safe-area-context";
import { useKeepAwake } from "expo-keep-awake";

export type ThemePageProps = {
  children: ReactNode;
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
          contentContainerStyle={{ flex: 1 }}
          mode="layout"
          // showsVerticalScrollIndicator={false}
          keyboardShouldPersistTaps="handled"
        >
          {content}
        </KeyboardAwareScrollView>
      ) : (
        content
      )}
    </Container>
  );
};

export default ThemePage;

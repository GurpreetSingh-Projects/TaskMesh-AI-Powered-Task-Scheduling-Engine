import { GestureHandlerRootView } from "react-native-gesture-handler";
import { NavigationContainer } from "@react-navigation/native";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { KeyboardProvider } from "react-native-keyboard-controller";
import { BottomSheetModalProvider } from "@gorhom/bottom-sheet";
import { Provider } from "react-redux";
import RootNavigator from "@/navigation/RootNavigator";
import { store } from "@/app/store";
// @ts-ignore
import "@/global.css";

const App = () => {
  return (
    <Provider store={store}>
      <GestureHandlerRootView style={{ flex: 1 }}>
        <NavigationContainer>
          <SafeAreaProvider>
            <KeyboardProvider>
              <BottomSheetModalProvider>
                <RootNavigator />
              </BottomSheetModalProvider>
            </KeyboardProvider>
          </SafeAreaProvider>
        </NavigationContainer>
      </GestureHandlerRootView>
    </Provider>
  );
};

export default App;

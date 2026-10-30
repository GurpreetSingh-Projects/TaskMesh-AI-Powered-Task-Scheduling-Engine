import { useState, useRef, useEffect } from "react";
import { View, useWindowDimensions } from "react-native";
import { Image } from "expo-image";
import Animated from "react-native-reanimated";
import ThemeDrawer from "@/components/ThemeDrawer";
import ThemeText from "@/components/ThemeText";

interface ImageClickedViewProps {
  uri: string;
  onConfirm: (details: unknown) => void;
}

const ImageClickedView = ({ uri, onConfirm }: ImageClickedViewProps) => {
  const { height, width } = useWindowDimensions();
  const drawerRef = useRef(null);
  const [shrunk, setShrunk] = useState(false);

  const boxHeight = shrunk ? height * 0.65 : height;
  const boxTop = shrunk ? 50 : 0;
  const boxPaddingHorizontal = shrunk ? 25 : 0;

  useEffect(() => {
    const timeout = setTimeout(() => {
      drawerRef.current?.present();
    }, 750);

    return () => clearTimeout(timeout);
  }, []);

  return (
    <View className="flex-1" onLayout={() => setShrunk(true)}>
      <Animated.View
        style={{
          position: "absolute",
          width: width,
          height: boxHeight,
          top: boxTop,
          left: 0,
          paddingHorizontal: boxPaddingHorizontal,
          transitionProperty: ["height", "top", "paddingHorizontal"],
          transitionDuration: 750,
          transitionTimingFunction: "ease-out",
        }}
        onCSSTransitionEnd={
          (event: any) => console.log("Running now")
          // if (event.propertyName === "height") {
          //   drawerRef.current?.present();
          // }
        }
      >
        <View style={{ flex: 1, borderRadius: 35, overflow: "hidden" }}>
          <Image source={{ uri: `file://${uri}` }} style={{ flex: 1 }} />
        </View>
      </Animated.View>

      <ThemeDrawer
        ref={drawerRef}
        snapPoints={["45%"]}
        closable
        backdropPressBehavior="close"
      >
        <ThemeText>Lorem ipsum dolor sit amet</ThemeText>
      </ThemeDrawer>
    </View>
  );
};

export default ImageClickedView;

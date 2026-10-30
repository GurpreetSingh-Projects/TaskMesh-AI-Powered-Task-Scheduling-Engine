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
  const { width, height } = useWindowDimensions();
  const drawerRef = useRef(null);
  const [shrunk, setShrunk] = useState(false);

  const targetWidth = width - 30;

  const boxWidth = shrunk ? targetWidth : width;
  const boxHeight = shrunk ? height - 150 : height;
  const boxTop = shrunk ? 50 : 0;
  const boxLeft = shrunk ? (width - targetWidth) / 2 : 0;

  return (
    <View className="flex-1" onLayout={() => setShrunk(true)}>
      <Animated.View
        style={{
          position: "absolute",
          width: boxWidth,
          height: boxHeight,
          top: boxTop,
          left: boxLeft,
          borderRadius: 35,
          overflow: "hidden",
          transitionProperty: ["width", "height", "top", "left"],
          transitionDuration: 750,
          transitionTimingFunction: "ease-out",
        }}
        onCSSTransitionEnd={(event) => {
          if (event.propertyName === "width") {
            drawerRef.current?.present();
          }
        }}
      >
        <Image source={{ uri: `file://${uri}` }} style={{ flex: 1 }} />
      </Animated.View>

      <ThemeDrawer
        ref={drawerRef}
        snapPoints={["45%"]}
        closable
        backdropPressBehavior="close"
      >
        <ThemeText>
          Lorem ipsum dolor sit amet, consectetur adipisicing elit. Consectetur,
          quas! Numquam est culpa, optio perferendis quam voluptate earum fugit
          adipisci distinctio consectetur? Suscipit hic earum veniam excepturi
          non obcaecati unde harum doloremque omnis quidem, ratione sed adipisci
          dolor atque impedit dicta at enim soluta! Labore minima, maxime rerum
          accusantium sequi voluptates porro non veritatis iure perspiciatis
          quidem dignissimos cupiditate ipsam quaerat dolorem delectus
          voluptatem voluptatum voluptas? Ut nesciunt sunt quam obcaecati animi,
          cupiditate neque exercitationem repellendus veritatis, molestiae,
          beatae ad! Repellat minus molestiae, necessitatibus, minima quis nihil
          dignissimos ipsa voluptas dolor provident veniam reprehenderit odit
          tenetur nemo sint doloremque dolore.
        </ThemeText>
        {/* task/subtask form fields go here */}
      </ThemeDrawer>
    </View>
  );
};

export default ImageClickedView;

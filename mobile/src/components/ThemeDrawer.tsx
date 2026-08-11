import { StyleSheet, Text, View } from "react-native";
import React, { useCallback, useEffect, useRef } from "react";
import { BottomSheetBackdrop, BottomSheetModal, BottomSheetView } from "@gorhom/bottom-sheet";

const ThemeDrawer = () => {
  const themeDrawerRef = useRef(null);

  const renderBackdrop = useCallback(
    (props) => (
      <BottomSheetBackdrop
        {...props}
        disappearsOnIndex={1}
        appearsOnIndex={2}
      />
    ),
    [],
  );

  return (
    <View>
      <BottomSheetModal ref={themeDrawerRef} backdropComponent={renderBackdrop}>
        <BottomSheetView>
          <Text>Awesome 🎉</Text>
        </BottomSheetView>
      </BottomSheetModal>
    </View>
  );
};

export default ThemeDrawer;

const styles = StyleSheet.create({});

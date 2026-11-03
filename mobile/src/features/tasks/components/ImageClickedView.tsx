import { useState, useRef, useEffect } from "react";
import { View, useWindowDimensions } from "react-native";
import { Image } from "expo-image";
import Animated from "react-native-reanimated";
import ThemeSheet from "@/components/ThemeSheet";
import ThemeTextInput from "@/components/ThemeTextInput";
import { themeColors, themeSpacing } from "@/theme";
import ThemeButton from "@/components/ThemeButton";
import { z } from "zod/v4";
import {
  TASK_PRIORITY,
  TASK_PRIORITY_OPTIONS,
  TASK_STATUS,
  TASK_STATUS_OPTIONS,
} from "../utils";
import { Controller, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import ThemeText from "@/components/ThemeText";
import ThemeTabGroup from "@/components/ThemeTabGroup";
import PagerView from "react-native-pager-view";
import DatePicker from "react-native-date-picker";
import BackButton from "@/components/BackButton";

interface ImageClickedViewProps {
  uri: string;
  onConfirm: (details: unknown) => void;
}

const taskCreateSchema = z.object({
  title: z.string().min(3, "Title is Required"),
  description: z.string().optional(),
  due_at: z.iso.datetime().nullable().optional(),
  status: z.enum(TASK_STATUS),
  priority: z.enum(TASK_PRIORITY),
});

type TaskCreateType = z.infer<typeof taskCreateSchema>;

const ImageClickedView = ({ uri }: ImageClickedViewProps) => {
  const { height, width } = useWindowDimensions();
  const sheetRef = useRef(null);
  const [shrunk, setShrunk] = useState(false);
  const [isAnimationCompleted, setIsAnimationCompleted] = useState(false);
  const [page, setPage] = useState<number>(0);
  const [date, setDate] = useState(new Date());

  const boxHeight = shrunk ? height * 0.65 : height;
  const boxTop = shrunk ? 50 : 0;
  const boxPaddingHorizontal = shrunk ? 25 : 0;

  const createTaskSheetRef = useRef<PagerView>(null);
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<TaskCreateType>({
    resolver: zodResolver(taskCreateSchema),
    defaultValues: {
      title: "",
      description: "",
      status: "PENDING",
      priority: "NORMAL",
    },
  });

  const nextPageHandler = () => {
    createTaskSheetRef?.current?.setPage(page + 1);
  };

  const prevPageHandler = () => {
    console.log("prev");

    createTaskSheetRef?.current?.setPage(page - 1);
  };

  const submitHandler = () => {};

  console.log(page);

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
          transitionDuration: 1500,
          transitionTimingFunction: "ease-out",
        }}
        onCSSTransitionEnd={(event: any) => {
          if (event.propertyName === "height") {
            setIsAnimationCompleted(true);
            sheetRef?.current?.snapToIndex(1);
          }
        }}
      >
        <View style={{ flex: 1, borderRadius: 35, overflow: "hidden" }}>
          <Image source={{ uri: `file://${uri}` }} style={{ flex: 1 }} />
        </View>
      </Animated.View>
      {isAnimationCompleted && (
        <ThemeSheet
          ref={sheetRef}
          snapPoints={["50%"]}
          backgroundStyle={{ backgroundColor: themeColors?.charcoal }}
          closable={false}
        >
          <PagerView
            ref={createTaskSheetRef}
            initialPage={0}
            scrollEnabled
            pageMargin={themeSpacing?.page}
            onPageSelected={(e) => setPage(e.nativeEvent.position)}
            style={{ height: height * 0.35 }}
          >
            <View key={"1"} className="fle x-1 gap-5 px-5 mt-default-half">
              <View className="gap-2">
                <ThemeText variant="title" className="text-xs! text-mist">
                  What's the name of this task?
                </ThemeText>
                <Controller
                  control={control}
                  name="title"
                  render={({ field: { value, onChange, onBlur } }) => (
                    <ThemeTextInput
                      placeholder=""
                      value={value}
                      onChangeText={onChange}
                      onBlur={onBlur}
                      keyboardType="default"
                    />
                  )}
                />
                {errors?.title?.message && (
                  <ThemeText className="text-xs text-red-500">
                    {errors.title.message}
                  </ThemeText>
                )}
              </View>

              <View className="gap-2">
                <ThemeText variant="title" className="text-xs! text-mist">
                  What's the purpose of this task?
                </ThemeText>
                <Controller
                  control={control}
                  name="description"
                  render={({ field: { value, onChange, onBlur } }) => (
                    <ThemeTextInput
                      placeholder="What's the purpose of this task?"
                      value={value}
                      onChangeText={onChange}
                      onBlur={onBlur}
                      keyboardType="default"
                      numberOfLines={3}
                      textAlignVertical="top"
                    />
                  )}
                />
              </View>

              <View className="gap-2">
                <ThemeText variant="title" className="text-xs! text-mist">
                  Priority
                </ThemeText>
                <Controller
                  control={control}
                  name="priority"
                  render={({ field: { value, onChange } }) => (
                    <ThemeTabGroup
                      value={value}
                      onChange={onChange}
                      options={TASK_PRIORITY_OPTIONS}
                    />
                  )}
                />
              </View>
            </View>
            <View key={"2"} className="fle x-1 gap-5 px-5 mt-default-half">
              <BackButton variant="light" onPress={prevPageHandler} />

              <ThemeText variant="title" className="text-xs! text-mist">
                Expected Completion Time
              </ThemeText>
              <Controller
                control={control}
                name="priority"
                render={({ field: { value, onChange } }) => (
                  <View className="items-center justify-center">
                    <DatePicker
                      mode="datetime"
                      locale="en"
                      minuteInterval={5}
                      date={date}
                      onDateChange={setDate}
                      hitSlop={25}
                      style={{ opacity: 0.75 }}
                    />
                  </View>
                )}
              />
            </View>
          </PagerView>
          <View className="px-page">
            <ThemeButton
              className="border-0.25 border-steel mt-default"
              text={page == 0 ? "Next" : "Submit"}
              onPress={page == 0 ? nextPageHandler : submitHandler}
            />
          </View>
        </ThemeSheet>
      )}
    </View>
  );
};

export default ImageClickedView;

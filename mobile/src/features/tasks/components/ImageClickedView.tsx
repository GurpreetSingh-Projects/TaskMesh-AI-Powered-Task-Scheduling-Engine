import { useState, useRef, useEffect } from "react";
import { Keyboard, View, useWindowDimensions } from "react-native";
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
import { DrawerMode, FileType } from "@/features/auth/types";
import { useCreateTaskMutation } from "../taskApi";
import LottieView from "lottie-react-native";
import { animations, images } from "@/assets";

type ImageClickedViewProps = {
  media: FileType;
};

const taskCreateSchema = z.object({
  title: z.string().min(3, "Title is Required"),
  description: z.string().optional(),
  due_at: z.iso.datetime().nullable().optional(),
  status: z.enum(TASK_STATUS),
  priority: z.enum(TASK_PRIORITY),
});

type TaskCreateType = z.infer<typeof taskCreateSchema>;

const ImageClickedView = (props: ImageClickedViewProps) => {
  const { height, width } = useWindowDimensions();
  const sheetRef = useRef(null);
  const [shrunk, setShrunk] = useState(false);
  const [isAnimationCompleted, setIsAnimationCompleted] = useState(false);
  const [page, setPage] = useState<number>(0);
  const [date, setDate] = useState(new Date());
  const [drawerMode, setDrawerMode] = useState<DrawerMode>("default");
  const [drawerMsg, setDrawerMsg] = useState({ title: "", description: "" });

  const boxHeight = shrunk ? height * 0.65 : height;
  const boxTop = shrunk ? 50 : 0;
  const boxPaddingHorizontal = shrunk ? 25 : 0;

  const createTaskSheetRef = useRef<PagerView>(null);
  const [createTask, { isLoading, reset }] = useCreateTaskMutation();

  const {
    control,
    trigger,
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

  const nextPageHandler = async () => {
    const isValid = await trigger(["title"]);

    if (isValid) createTaskSheetRef?.current?.setPage(page + 1);
  };

  const prevPageHandler = () => {
    console.log("prev");

    createTaskSheetRef?.current?.setPage(page - 1);
  };

  const submitHandler = async (values: TaskCreateType) => {
    try {
      const response = await createTask({
        title: values.title,
        description: values.description,
        due_at: values.due_at,
        status: values.status,
        priority: values.priority,
        task_img: props?.media,
      }).unwrap();

      console.log(response);

      setDrawerMsg({
        title: "Task Created!!",
        description: "Task created successfully.",
      });

      setDrawerMode("success");
      // registerDrawerRef?.current?.present();

      // setTimeout(() => {
      //   registerDrawerRef?.current?.dismiss();
      //   reset();
      // }, 2500);
    } catch (error) {
      console.log(error);

      setDrawerMsg({
        title: "Task Creation Failed",
        description: "Unable to create task. Please try again.",
      });
      setDrawerMode("fail");
      // registerDrawerRef?.current?.present();

      // setTimeout(() => {
      //   registerDrawerRef?.current?.dismiss();
      // }, 2500);
    }
  };

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
          <Image source={{ uri: props?.media?.uri }} style={{ flex: 1 }} />
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
            pageMargin={themeSpacing?.page}
            onPageSelected={(e) => setPage(e.nativeEvent.position)}
            // scrollEnabled={false}
            style={{ height: height * 0.5 }}
          >
            <View key={"1"} className="gap-5 px-page mt-default-half">
              <View className="gap-2">
                <ThemeText variant="title" className="text-xs! text-mist">
                  What's the name of this task?
                </ThemeText>
                <Controller
                  control={control}
                  name="title"
                  render={({ field: { value, onChange, onBlur } }) => (
                    <ThemeTextInput
                      mode="bottom-sheet"
                      placeholder="Title"
                      value={value}
                      onChangeText={onChange}
                      onBlur={onBlur}
                      keyboardType="default"
                      cursorColor={themeColors?.steel}
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
                      mode="bottom-sheet"
                      value={value}
                      onChangeText={onChange}
                      onBlur={onBlur}
                      keyboardType="default"
                      cursorColor={themeColors?.steel}
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

              <ThemeButton
                className="mt-default border-0.25 border-steel absolute w-full left-page right page bottom-20"
                text="Next"
                onPress={nextPageHandler}
              />
            </View>
            <View key={"2"} className="gap-5 px-page mt-default-half">
              <BackButton variant="light" onPress={prevPageHandler} />
              <ThemeText variant="title" className="text-xs! text-mist mt-3">
                Expected Completion Time
              </ThemeText>
              <Controller
                control={control}
                name="due_at"
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
              <ThemeButton
                className="mt-default border-0.25 border-steel absolute w-full left-page right page bottom-20"
                text="Submit"
                onPress={() => {
                  Keyboard.dismiss();
                  handleSubmit(submitHandler)();
                }}
              />
            </View>
            <View key="3">
              <View className="h-full w-full flex-1 items-center justify-center gap-3 z-10">
                <LottieView
                  source={
                    drawerMode === "success"
                      ? animations?.tickIcon
                      : animations?.crossIcon
                  }
                  autoPlay
                  loop={false}
                  style={{ width: 75, height: 75 }}
                />
                <View className="gap-3 py-3">
                  <ThemeText variant="subheading" className="text-center">
                    {drawerMsg.title}
                  </ThemeText>
                  <ThemeText className="text-graphite! text-center">
                    {drawerMsg.description}
                  </ThemeText>
                </View>
              </View>

              {drawerMode === "success" && (
                <Image
                  source={images?.illustrations?.illustration2}
                  contentFit="cover"
                  style={{
                    width,
                    height: 150,
                    position: "absolute",
                    bottom: 0,
                    opacity: 0.25,
                  }}
                />
              )}
            </View>
          </PagerView>
        </ThemeSheet>
      )}
    </View>
  );
};

export default ImageClickedView;

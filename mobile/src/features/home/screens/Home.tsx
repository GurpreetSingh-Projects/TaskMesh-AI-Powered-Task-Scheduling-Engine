import { useRef, useState } from "react";
import { Pressable, ScrollView, useWindowDimensions, View } from "react-native";
import { DrawerActions, useNavigation } from "@react-navigation/native";
import { useAppSelector } from "@/app/store";
import { themeColors } from "@/theme";
import ThemePage from "@/components/ThemePage";
import ThemeText from "@/components/ThemeText";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Check, ChevronDown, Menu } from "lucide-react-native";
import { ImageBackground } from "expo-image";
import { images } from "@/assets";
import { useGetTasksQuery } from "@/features/tasks/taskApi";
import { Carousel, CarouselRef } from "react-native-reanimated-carousel";
import Animated from "react-native-reanimated";
import { HomeSlideItem } from "../components/HomeSlideItem";
import { TaskItem } from "@/features/tasks/types";
import { useGetSummaryQuery } from "../homeApi";
import dayjs from "dayjs";

const ranges = ["Daily", "Weekly", "Monthly"] as const;

type AnalyticsRange = (typeof ranges)[number];

const analyticsData = {
  Daily: {
    subtitle: "Daily scheduling report",
    metricLabel: "Tasks",
    metricValue: "48",
    labels: ["9 AM", "12 PM", "3 PM"],
    bars: [
      { primary: 48, secondary: 22 },
      { primary: 72, secondary: 34 },
      { primary: 56, secondary: 28 },
    ],
  },
  Weekly: {
    subtitle: "Weekly scheduling report",
    metricLabel: "Tasks",
    metricValue: "326",
    labels: ["Mon", "Wed", "Fri"],
    bars: [
      { primary: 42, secondary: 24 },
      { primary: 78, secondary: 38 },
      { primary: 58, secondary: 30 },
    ],
  },
  Monthly: {
    subtitle: "Monthly scheduling report",
    metricLabel: "Orders",
    metricValue: "1,790",
    labels: ["Jan", "Feb", "Mar"],
    bars: [
      { primary: 46, secondary: 22 },
      { primary: 80, secondary: 38 },
      { primary: 52, secondary: 30 },
    ],
  },
};

const Home = () => {
  const { height, width } = useWindowDimensions();
  const insets = useSafeAreaInsets();
  const navigation = useNavigation();
  const user = useAppSelector((state) => state.user);

  const end_date = dayjs().format("YYYY-MM-DD");
  const start_date = dayjs().subtract(90, "day").format("YYYY-MM-DD");

  const carouselRef = useRef<CarouselRef>(null);
  const [homeRange, setHomeRange] = useState<AnalyticsRange>("Weekly");
  const [isHomeRangeMenuOpen, setIsHomeRangeMenuOpen] = useState(false);

  const displayName =
    user.full_name.trim().length > 0
      ? user?.full_name?.trim()
      : "Taskmesh User";

  const analytics = analyticsData[homeRange];

  const {
    data: tasksData,
    isLoading: areTasksLoading,
    isError: areTasksError,
    error: tasksError,
  } = useGetSummaryQuery({
    start_date,
    end_date,
    limit: 10,
  });

  console.log("Tasks:", tasksData, start_date, end_date);

  return (
    <ThemePage
      noSafeArea
      isScrollable={false}
      backgroundColor={themeColors?.ink}
    >
      <View className="flex-1 bg-ink gap-5">
        {/* Fixed hero — does not scroll */}
        <ImageBackground
          source={images?.backgrounds?.homeBg}
          style={{ flex: 1, paddingTop: insets?.top }}
        >
          <View className="py-3 gap-5 h-3/4">
            <View className="flex-row items-center justify-between px-page">
              <Pressable
                onPress={() => navigation.dispatch(DrawerActions.openDrawer())}
                className="p-2 rounded-full border"
              >
                <Menu
                  height={25}
                  width={25}
                  stroke={themeColors?.canvas}
                  strokeWidth={1.5}
                />
              </Pressable>

              <View className="relative z-30">
                <Pressable
                  onPress={() =>
                    setIsHomeRangeMenuOpen((previous) => !previous)
                  }
                  className="flex-row items-center justify-center gap-2 rounded-full border border-steel bg-carbon p-2 px-4 active:opacity-70"
                >
                  <ThemeText className="text-xs font-semibold text-mist">
                    {homeRange}
                  </ThemeText>
                  <ChevronDown
                    width={15}
                    height={15}
                    stroke={themeColors.canvas}
                    strokeWidth={1.5}
                  />
                </Pressable>

                {isHomeRangeMenuOpen && (
                  <View
                    className="absolute right-0 overflow-hidden rounded-default border border-ash bg-slate"
                    style={{
                      top: 40,
                      width: width * 0.35,
                    }}
                  >
                    {ranges.map((range) => {
                      const isSelected = homeRange === range;
                      return (
                        <Pressable
                          key={range}
                          onPress={() => {
                            setHomeRange(range);
                            setIsHomeRangeMenuOpen(false);
                          }}
                          className={`min-h-[42px] flex-row items-center justify-between rounded-[13px] px-3 ${
                            isSelected ? "bg-ash" : ""
                          }`}
                        >
                          <ThemeText
                            className={`text-sm ${
                              isSelected
                                ? "font-semibold text-canvas"
                                : "font-medium text-cloud"
                            }`}
                          >
                            {range}
                          </ThemeText>
                          {isSelected && (
                            <Check
                              width={17.5}
                              height={17.5}
                              stroke={themeColors.canvas}
                              strokeWidth={1.5}
                            />
                          )}
                        </Pressable>
                      );
                    })}
                  </View>
                )}
              </View>
            </View>

            <View className="gap-1 px-page">
              <ThemeText className="text-base font-medium text-cloud">
                Welcome back,
              </ThemeText>
              <ThemeText
                variant="heading"
                numberOfLines={1}
                className="mt-1 font-bold tracking-tight text-canvas capitalize"
              >
                {displayName}
              </ThemeText>
            </View>

            <View className="flex-1 items-center justify-center">
              <Carousel
                loop
                ref={carouselRef}
                data={tasksData?.top_tasks}
                style={{
                  height: height * 0.65,
                  width: width,
                }}
                contentContainerStyle={{ width: width }}
                layout={{
                  type: "parallax",
                  scale: 0.75,
                  offset: 150,
                }}
                renderItem={({ item, index }) => {
                  return <CustomItem key={index} task={item} />;
                }}
              />
            </View>
          </View>

          <View className="mt-4 flex-1 rounded-t-[36px] bg-canvas pt-5 px-page">
            <View className="mb-5 flex-row items-center justify-between">
              <View>
                <ThemeText
                  variant="subheading"
                  className="font-bold tracking-tight text-ink"
                >
                  Quick actions
                </ThemeText>
                <ThemeText className="mt-1 text-steel">
                  Stay on top of your work.
                </ThemeText>
              </View>
              <View className="h-11 w-11 items-center justify-center rounded-full bg-mist">
                <ThemeText className="text-lg text-charcoal">✦</ThemeText>
              </View>
            </View>

            <View className="flex-row gap-3">
              <Pressable
                onPress={() => {}}
                className="min-h-[174px] flex-1 overflow-hidden rounded-[24px] bg-charcoal p-4 active:opacity-80"
              >
                <View className="mb-7 h-10 w-10 items-center justify-center rounded-full bg-slate">
                  <ThemeText className="text-xl font-light text-canvas">
                    ＋
                  </ThemeText>
                </View>
                <ThemeText className="text-[15px] font-bold text-canvas">
                  New task
                </ThemeText>
                <ThemeText className="mt-1 text-[11px] text-cloud">
                  Create something new
                </ThemeText>
                <ThemeText className="absolute bottom-4 right-4 text-lg text-steel">
                  ↗
                </ThemeText>
              </Pressable>

              <Pressable
                onPress={() => {}}
                className="min-h-[174px] flex-1 overflow-hidden rounded-[24px] border border-mist bg-canvas p-4 active:opacity-70"
              >
                <View className="mb-7 h-10 w-10 items-center justify-center rounded-full bg-mist">
                  <ThemeText className="text-base font-bold text-charcoal">
                    ✓
                  </ThemeText>
                </View>
                <ThemeText className="text-[15px] font-bold text-ink">
                  My tasks
                </ThemeText>
                <ThemeText className="mt-1 text-[11px] text-steel">
                  View your schedule
                </ThemeText>
                <ThemeText className="absolute bottom-4 right-4 text-lg text-steel">
                  ↗
                </ThemeText>
              </Pressable>
            </View>

            <View className="mt-8">
              <View className="mb-3.5 flex-row items-center justify-between">
                <ThemeText className="text-[21px] font-bold tracking-tight text-ink">
                  Recent activity
                </ThemeText>
                <Pressable onPress={() => {}}>
                  <ThemeText className="text-[13px] font-semibold text-steel">
                    View all
                  </ThemeText>
                </Pressable>
              </View>

              <View className="min-h-[78px] flex-row items-center rounded-[22px] border border-mist bg-canvas p-3.5">
                <View className="h-11 w-11 items-center justify-center rounded-full bg-mist">
                  <ThemeText className="text-lg font-bold text-charcoal">
                    ✓
                  </ThemeText>
                </View>
                <View className="ml-3 flex-1">
                  <ThemeText className="text-[13px] font-semibold text-ink">
                    Your schedule is up to date
                  </ThemeText>
                  <ThemeText className="mt-1 text-[11px] text-steel">
                    Everything looks organized.
                  </ThemeText>
                </View>
                <ThemeText className="ml-2 text-2xl text-steel">›</ThemeText>
              </View>
            </View>

            <View className="h-[200px] overflow-hidden rounded-lg border border-ash bg-charcoal px-5 pb-[18px] pt-5 gap-10">
              <View className="flex-row items-start justify-between">
                <View>
                  <ThemeText
                    variant="title"
                    className="font-bold tracking-tight text-canvas"
                  >
                    Tasks Summary
                  </ThemeText>
                  <ThemeText className="mt-1 text-xs text-steel">
                    {analytics.subtitle}
                  </ThemeText>
                </View>

                <View className="flex-row items-center gap-1.5 rounded-2xl bg-slate px-3 py-2">
                  <ThemeText className="text-[11px] font-semibold text-cloud">
                    {homeRange}
                  </ThemeText>
                  <ChevronDown
                    width={24}
                    height={24}
                    stroke={themeColors.ink}
                    strokeWidth={1.5}
                  />
                </View>
              </View>

              <View className="flex-1 flex-row items-end">
                <View className="w-[39%] justify-end pb-1">
                  <ThemeText className="text-[13px] font-medium text-cloud">
                    {analytics.metricLabel}
                  </ThemeText>
                  <ThemeText className="mt-1 text-[31px] font-bold tracking-tight text-canvas">
                    {analytics.metricValue}
                  </ThemeText>
                  <ThemeText className="mt-1 text-[10px] text-smoke">
                    13 Sept - 19 Sept
                  </ThemeText>
                </View>

                <View className="flex-1 pl-2">
                  <View className="h-[112px] flex-row items-end justify-around gap-3">
                    {analytics.bars.map((bar, index) => (
                      <View
                        key={index}
                        className="relative h-full flex-1 justify-end"
                      >
                        <View
                          className="w-full rounded-t-[17px] bg-smoke"
                          style={{ height: Math.min(bar.primary, 112) }}
                        />
                        <View
                          className="absolute bottom-0 left-0 right-0 rounded-t-[17px] bg-mist"
                          style={{ height: Math.min(bar.secondary, 112) }}
                        />
                      </View>
                    ))}
                  </View>

                  <View className="mt-2 flex-row justify-around">
                    {analytics.labels.map((label) => (
                      <ThemeText
                        key={label}
                        className="flex-1 text-center text-[10px] text-steel"
                      >
                        {label}
                      </ThemeText>
                    ))}
                  </View>
                </View>
              </View>
            </View>
          </View>
        </ImageBackground>
      </View>
    </ThemePage>
  );
};

export default Home;

type ItemProps = {
  task: TaskItem;
};

const CustomItem: React.FC<ItemProps> = ({ task }) => {
  return (
    <Animated.View className="flex-1 overflow-hidden">
      <HomeSlideItem task={task} />
    </Animated.View>
  );
};

//

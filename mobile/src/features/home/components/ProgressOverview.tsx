import { View } from "react-native";
import ThemeText from "@/components/ThemeText";
import { CartesianChart, Bar } from "victory-native";
import { themeColors } from "@/theme";
import { useFont, Text } from "react-native-skia";

export type ProgressStats = {
  created: number;
  pending: number;
  in_progress: number;
  completed: number;
  overdue: number;
};

const MAX_H = 105;

export const ProgressOverview = (props: ProgressStats) => {
  const font = useFont(require("@/assets/fonts/Poppins-Regular.ttf"), 10);
  const labelFont = useFont(require("@/assets/fonts/Poppins-Medium.ttf"), 12);

  const bars = [
    { label: "Pending", value: props?.stats?.pending ?? 0 },
    { label: "In Preogress", value: props?.stats?.in_progress ?? 0 },
    { label: "Completed", value: props?.stats?.completed ?? 0 },
  ];
  const BAR_COLORS = ["#888888", "#ffffff", "#D0D0D0"];
  return (
    <View className="gap-subsection rounded-[25px] bg-ink">
      <View className="gap-1 px-page pt-page">
        <ThemeText
          variant="title"
          className="font-bold tracking-tight text-canvas"
        >
          Progress Overview
        </ThemeText>
        <ThemeText className="text-steel">
          View your progress at a glance
        </ThemeText>
      </View>

      <View className="flex-row items-end justify-between gap-3 px-page pb-page">
        <View className="pb-1">
          <ThemeText className="text-md font-semibold text-cloud!">
            Tasks
          </ThemeText>
          <ThemeText className="text-3xl! font-extrabold text-canvas">
            {props?.stats?.created}
          </ThemeText>
          <ThemeText className="text-xs text-ash">
            {props?.stats?.overdue} overdue
          </ThemeText>
        </View>

        <View className="w-2/3" style={{ height: MAX_H }}>
          <CartesianChart
            data={bars}
            xKey="label"
            yKeys={["value"]}
            domain={{ y: [0, Math.max(...bars.map((b) => b.value), 1)] }}
            domainPadding={{ left: 50, right: 50, top: 12, bottom: 5 }}
            axisOptions={{
              font,
              labelColor: "transparent",
              lineColor: "transparent",
            }}
            xAxis={{
              font,
              labelColor: themeColors.mist,
              lineColor: "transparent",
              tickCount: bars.length,
            }}
          >
            {({ points, chartBounds }) =>
              points.value.map((point, index) => (
                <>
                  <Bar
                    key={bars[index].label}
                    points={[point]}
                    chartBounds={chartBounds}
                    barWidth={65}
                    color={
                      bars[index].label === "Pending"
                        ? themeColors.ash
                        : bars[index].label === "Active"
                          ? themeColors.steel
                          : themeColors.mist
                    }
                    roundedCorners={{
                      topLeft: 17,
                      topRight: 17,
                    }}
                    animate={{ type: "spring" }}
                  />
                  {labelFont && (
                    <Text
                      x={point.x}
                      y={point.y + 18}
                      text={String(point.yValue)}
                      font={labelFont}
                      color={themeColors?.mist}
                    />
                  )}
                </>
              ))
            }
          </CartesianChart>
        </View>
      </View>
    </View>
  );
};

import { View } from "react-native";
import ThemeText from "@/components/ThemeText";

export type ProgressStats = {
  created: number;
  pending: number;
  in_progress: number;
  completed: number;
  overdue: number;
};

type Props = {
  stats: ProgressStats;
};

const MAX_H = 105;

export const ProgressOverview = ({
  stats: { created, pending, in_progress, completed, overdue },
}: Props) => {
  const bars = [
    { label: "Pending", value: pending, className: "bg-ash" },
    { label: "Active", value: in_progress, className: "bg-steel" },
    { label: "Done", value: completed, className: "bg-mist" },
  ];

  return (
    <View className="gap-subsection rounded-[25px] bg-ink">
      <View className="gap-2 px-page pt-page">
        <ThemeText className="text-xl text-canvas">Progress Overview</ThemeText>
        <ThemeText className="text-steel">
          View your progress at a glance
        </ThemeText>
      </View>

      <View className="flex-row items-end justify-between px-page">
        <View className="pb-page">
          <ThemeText className="text-xs text-steel">Tasks</ThemeText>
          <ThemeText className="text-3xl! font-extrabold text-canvas">
            {created}
          </ThemeText>
          <ThemeText className="text-xs text-ash">{overdue} overdue</ThemeText>
        </View>

        <View className="flex-row gap-3">
          {bars.map(({ label, value, className }) => (
            <View key={label} className="items-center">
              <ThemeText className="text-[10px] text-cloud text-center">
                {label}
              </ThemeText>
              <View style={{ height: MAX_H }} className="justify-end gap-0.5">
                <View
                  className={`w-14 rounded-t-2xl ${className}`}
                  style={{
                    height: `${created ? (value / created) * 100 : 0}%`,
                    minHeight: 6,
                  }}
                />
              </View>
            </View>
          ))}
        </View>
      </View>
    </View>
  );
};

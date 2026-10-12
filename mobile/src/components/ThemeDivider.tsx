import { View, ViewProps } from "react-native";

interface SectionDividerProps extends ViewProps {
  className?: string;
}

export function SectionDivider({
  className,
  style,
  ...props
}: SectionDividerProps) {
  return (
    <View className={`h-px bg-mist ${className}`} style={style} {...props} />
  );
}

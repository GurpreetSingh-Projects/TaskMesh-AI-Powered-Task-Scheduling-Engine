import Svg, { Circle, ClipPath, Defs, G, Path, Rect } from "react-native-svg";
import { themeColors } from "./theme";

export type IconProps = {
  fill?: string;
  stroke?: string;
  color?: string;
  height?: number;
  width?: number;
  rotation?: number;
  strokeWidth?: number;
};

export function VisibilityIcon(props: IconProps) {
  return (
    <Svg
      fill={props?.fill ?? themeColors?.canvas}
      strokeWidth={props?.strokeWidth ?? 1.5}
      stroke={props?.stroke ?? themeColors?.ink}
      viewBox="0 0 25 25"
      style={{ width: props?.width, height: props?.height }}
      className="flex-1 items-center justify-start! rounded-sm"
    >
      <Path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z"
      />
      <Path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z"
      />
    </Svg>
  );
}

export function HideVisibilityIcon(props: IconProps) {
  return (
    <Svg
      fill={props?.fill ?? themeColors?.canvas}
      strokeWidth={props?.strokeWidth ?? 1.5}
      stroke={props?.stroke ?? themeColors?.ink}
      viewBox="0 0 25 25"
      style={{ width: props?.width, height: props?.height }}
      className="flex-1 items-center justify-start! rounded-sm"
    >
      <Path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88"
      />
    </Svg>
  );
}

export function EmailIcon(props: IconProps) {
  return (
    <Svg
      fill={props?.fill ?? themeColors?.canvas}
      strokeWidth={props?.strokeWidth ?? 1.5}
      stroke={props?.stroke ?? themeColors?.ink}
      viewBox="0 0 25 25"
      style={{ width: props?.width, height: props?.height }}
      className="flex-1 items-center justify-start! rounded-sm"
    >
      <Path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75"
      />
    </Svg>
  );
}

export function LockIcon(props: IconProps) {
  return (
    <Svg
      fill={props?.fill ?? themeColors?.canvas}
      strokeWidth={props?.strokeWidth ?? 1.5}
      stroke={props?.stroke ?? themeColors?.ink}
      viewBox="0 0 25 25"
      style={{ width: props?.width, height: props?.height }}
      className="flex-1 items-center justify-start! rounded-sm"
    >
      <Path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z"
      />
    </Svg>
  );
}

export function ChevronLeftIcon(props: IconProps) {
  return (
    <Svg
      fill={props?.fill ?? themeColors?.canvas}
      strokeWidth={props?.strokeWidth ?? 1.5}
      stroke={props?.stroke ?? themeColors?.ink}
      viewBox="0 0 25 25"
      style={{ width: props?.width, height: props?.height }}
      className="flex-1 items-center justify-start! rounded-sm"
    >
      <Path
        strokeLinecap="round"
        strokeLinejoin="round"
        d="M15.75 19.5 8.25 12l7.5-7.5"
      />
    </Svg>
  );
}

export function CameraIcon(props: IconProps) {
  return (
    <Svg
      fill={props?.fill ?? themeColors?.canvas}
      strokeWidth={props?.strokeWidth ?? 1.5}
      stroke={props?.stroke ?? themeColors?.ink}
      viewBox="0 0 25 25"
      style={{ width: props?.width, height: props?.height }}
      className="flex-1 items-center justify-start! rounded-sm"
    >
      <Path d="M13.997 4a2 2 0 0 1 1.76 1.05l.486.9A2 2 0 0 0 18.003 7H20a2 2 0 0 1 2 2v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9a2 2 0 0 1 2-2h1.997a2 2 0 0 0 1.759-1.048l.489-.904A2 2 0 0 1 10.004 4z" />
      <Circle cx="12" cy="13" r="3" />
    </Svg>
  );
}

export function GalleryIcon(props: IconProps) {
  return (
    <Svg
      fill={props?.fill ?? themeColors?.canvas}
      strokeWidth={props?.strokeWidth ?? 1.5}
      stroke={props?.stroke ?? themeColors?.ink}
      viewBox="0 0 25 25"
      style={{ width: props?.width, height: props?.height }}
      className="flex-1 items-center justify-start! rounded-sm"
    >
      <Rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
      <Circle cx="9" cy="9" r="2" />
      <Path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" />
    </Svg>
  );
}

export function UserRoundIcon(props: IconProps) {
  return (
    <Svg
      fill={props?.fill ?? themeColors?.canvas}
      strokeWidth={props?.strokeWidth ?? 1.5}
      stroke={props?.stroke ?? themeColors?.ink}
      viewBox="0 0 25 25"
      style={{ width: props?.width, height: props?.height }}
      className="flex-1 items-center justify-start! rounded-sm"
    >
      <Circle cx="12" cy="8" r="5" />
      <Path d="M20 21a8 8 0 0 0-16 0" />
    </Svg>
  );
}

export function ChevronRightIcon(props: IconProps) {
  return (
    <Svg
      fill={props?.fill ?? "none"}
      strokeWidth={props?.strokeWidth ?? 1.5}
      stroke={props?.stroke ?? themeColors?.ink}
      viewBox="0 0 24 24"
      style={{ width: props?.width, height: props?.height }}
    >
      <Path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="m8.25 4.5 7.5 7.5-7.5 7.5"
      />
    </Svg>
  );
}

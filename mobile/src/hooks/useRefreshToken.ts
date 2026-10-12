import { useRefreshTokenMutation } from "@/features/auth/authApi";
import { getRefreshToken, setAuth } from "@/features/auth/utils";

export const useRefreshToken = () => {
  const [refreshTokenData] = useRefreshTokenMutation();

  const refreshToken = async () => {
    try {
      const refreshToken = await getRefreshToken();
      const response = await refreshTokenData(refreshToken).unwrap();
      console.log("Refresh Token Response", response);
      await setAuth(response);
    } catch (error) {
      console.log("Refresh Token error", error);
    }
  };

  return refreshToken;
};

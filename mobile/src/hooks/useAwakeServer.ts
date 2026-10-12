import { useLazyAwakeServerQuery } from "@/api/baseApi";

export const useAwakeServerCall = () => {
  const [awakeServer] = useLazyAwakeServerQuery();

  const callAwakeServer = async () => {
    try {
      const response = await awakeServer().unwrap();
      console.log("Server Response", response);
      return response;
    } catch (error) {
      console.log("Server awake error", error);
    }
  };

  return callAwakeServer;
};

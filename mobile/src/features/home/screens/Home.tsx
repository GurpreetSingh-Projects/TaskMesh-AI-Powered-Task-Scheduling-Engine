import { useAppSelector } from "@/app/store";
import OnboardingQuestionnaire from "@/features/onboarding/screens/OnboardingQuestionnaire";
import ProfileDetailsPending from "@/features/profile/screens/ProfileDetailsPending";
import { HomeStackNavigationProp } from "@/navigation/routes";
import { useNavigation } from "@react-navigation/native";
import { useEffect } from "react";
import { StyleSheet, Text, View } from "react-native";
const Home = () => {
  const navigation = useNavigation<HomeStackNavigationProp>();
  const user = useAppSelector((state) => state?.user);

  useEffect(() => {
    console.log(user);

    if (!user.is_onboarding_completed) {
      navigation.navigate("OnboardingQuestionnaire");
      return;
    }

    if (!user.is_profile_completed && !user.isProfileCompletionSkipped) {
      navigation.navigate("ProfileDetailsPending");
      return;
    }

    navigation.navigate("Home");
  }, [
    user?.is_onboarding_completed,
    user?.is_profile_completed,
    user?.isProfileCompletionSkipped,
  ]);

  return (
    <View>
      <Text>Home</Text>
    </View>
  );
};

export default Home;

const styles = StyleSheet.create({});

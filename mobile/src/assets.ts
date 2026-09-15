import { ImageSourcePropType } from "react-native";

export const images = {
  carousel: {
    carouselImg1: require("@/assets/images/carousel-images/carousel-image-1.webp"),
    carouselImg2: require("@/assets/images/carousel-images/carousel-image-2.webp"),
    carouselImg3: require("@/assets/images/carousel-images/carousel-image-3.webp"),
    carouselImg4: require("@/assets/images/carousel-images/carousel-image-4.webp"),
    carouselImg5: require("@/assets/images/carousel-images/carousel-image-5.webp"),
    carouselImg6: require("@/assets/images/carousel-images/carousel-image-6.webp"),
    carouselImg7: require("@/assets/images/carousel-images/carousel-image-7.webp"),
    carouselImg8: require("@/assets/images/carousel-images/carousel-image-8.webp"),
  },
  onboarding: {
    login: require("@/assets/images/onboarding/login.webp"),
    register: require("@/assets/images/onboarding/register.webp"),
  },
};

export const animations = {
  tickIcon: require("@/assets/animations/tick-icon.lottie"),
  tickIconSimple: require("@/assets/animations/tick-icon.lottie"),
  crossIcon: require("@/assets/animations/cross-icon.lottie"),
  crossIconSimple: require("@/assets/animations/cross-icon.lottie"),
  loadingIcon: require("@/assets/animations/loading-icon.lottie"),
};

export const sounds: Record<string, ImageSourcePropType> = {};

export const carouselImages = [
  images?.carousel?.carouselImg1,
  images?.carousel?.carouselImg2,
  images?.carousel?.carouselImg3,
  images?.carousel?.carouselImg4,
  images?.carousel?.carouselImg5,
  images?.carousel?.carouselImg6,
  images?.carousel?.carouselImg7,
  images?.carousel?.carouselImg8,
];

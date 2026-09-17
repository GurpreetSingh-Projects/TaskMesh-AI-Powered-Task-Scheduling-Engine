import { configureStore, combineReducers } from '@reduxjs/toolkit';
import { persistStore, persistReducer, createMigrate } from 'redux-persist';
import { useDispatch, useSelector } from 'react-redux';
import translationReducer from './features/Translations/TranslationSlice';
import routeDetailsReducer from './features/RouteDetailsSlice/RouteDetailsSlice';
import isOnlineReducer from './features/ConnectivitySlice/ConnectivitySlice';

import settingsReducer, { SettingsSlice } from './features/SettingsSlice/SettingsSlice';
import healthCheckReducer from './features/DeviceHealthSlice/DeviceHealthSlice';
import gpsBufferReducer from './features/GPSBufferSlice/GPSBufferSlice';
import { createMMKV } from 'react-native-mmkv';

import { workerApi } from './features/fetchData/api';

export const mmkvStorage = createMMKV({
  id: 'worker-app-storage',
});

export const mmkvReduxStorage = {
  setItem: (key: string, value: string) => {
    mmkvStorage.set(key, value);
    return Promise.resolve(true);
  },
  getItem: (key: string) => {
    const value = mmkvStorage.getString(key);
    return Promise.resolve(value ?? null);
  },
  removeItem: (key: string) => {
    mmkvStorage.remove(key);
    return Promise.resolve();
  },
};

const appReducer = combineReducers({
  isOnline: isOnlineReducer,
  routeDetails: routeDetailsReducer,
  translations: translationReducer,
  settings: settingsReducer,
  deviceHealth: healthCheckReducer,
  gpsBuffer: gpsBufferReducer,
  [workerApi.reducerPath]: workerApi.reducer,
});

const rootReducer = (
  state: ReturnType<typeof appReducer> | undefined,
  action: { type: string }
) => {
  if (action.type === 'RESET_STORE') {
    state = undefined;
  }
  return appReducer(state, action);
};

const migrations = {
  1: (state: ReturnType<typeof appReducer>) => {
    const newSettingDefaults = SettingsSlice.getInitialState();

    if (state?.settings) {
      state.settings = {
        ...newSettingDefaults,
        ...state.settings,
      };
    }
    return state;
  },
};

const persistConfig = {
  key: 'root',
  storage: mmkvReduxStorage,
  version: 1,
  migrate: createMigrate(migrations, { debug: __DEV__ }),
  whitelist: ['translations', 'routeDetails', 'settings', 'deviceHealth'],
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const workerStore = configureStore({
  reducer: persistedReducer,
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
      immutableCheck: false,
      actionCreatorCheck: false,
    }).concat(workerApi.middleware),
  devTools: false,
});

export const resetReduxStore = async () => {
  try {
    workerStore.dispatch({ type: 'RESET_STORE' });
    await persistor.purge();
    await mmkvStorage.clearAll();
    return { success: true };
  } catch (error) {
    console.error('Failed to reset Redux store:', error);
    return { success: false, error };
  }
};

export const persistor = persistStore(workerStore);

export type RootState = ReturnType<typeof workerStore.getState>;
export type AppDispatch = typeof workerStore.dispatch;

// Typed hooks for use throughout the app
export const useAppDispatch = useDispatch.withTypes<AppDispatch>();
export const useAppSelector = useSelector.withTypes<RootState>();

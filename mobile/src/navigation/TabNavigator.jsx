import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeScreen from '../screens/HomeScreen';
import BenefitsScreen from '../screens/BenefitsScreen';
import AcademicScreen from '../screens/AcademicScreen';
import UsageScreen from '../screens/UsageScreen';
import ProfileScreen from '../screens/ProfileScreen';
import { colors } from '../theme/colors';

/**
 * TabNavigator — bottom tab bar for the main authenticated area.
 */
const Tab = createBottomTabNavigator();

export default function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textSecondary,
        headerShown: false,
      }}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Benefits" component={BenefitsScreen} />
      <Tab.Screen name="Academic" component={AcademicScreen} />
      <Tab.Screen name="Usage" component={UsageScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}

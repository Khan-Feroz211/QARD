import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { useAuthStore } from '../store/authStore';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

/**
 * ProfileScreen — displays the student's profile and account settings.
 */
export default function ProfileScreen({ navigation }) {
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Logout', style: 'destructive', onPress: () => { logout(); navigation.replace('Onboarding'); } },
    ]);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.name}>{user?.full_name ?? 'Student'}</Text>
      <Text style={styles.email}>{user?.email ?? ''}</Text>
      <Text style={styles.id}>ID: {user?.student_id ?? ''}</Text>
      <Text style={styles.plan}>Plan: {user?.plan ?? 'free'}</Text>
      <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
        <Text style={styles.logoutText}>Logout</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, padding: 24, alignItems: 'center' },
  name: { ...typography.h1, color: colors.primary, marginTop: 40, marginBottom: 8 },
  email: { ...typography.body, color: colors.text, marginBottom: 4 },
  id: { ...typography.caption, color: colors.textSecondary, marginBottom: 4 },
  plan: { ...typography.caption, color: colors.textSecondary, marginBottom: 40 },
  logoutButton: { backgroundColor: colors.error, padding: 14, borderRadius: 12, width: '100%', alignItems: 'center' },
  logoutText: { ...typography.button, color: colors.white },
});

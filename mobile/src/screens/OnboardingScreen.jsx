import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

/**
 * OnboardingScreen — introduces QARD features to first-time users.
 */
export default function OnboardingScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Welcome to QARD</Text>
      <Text style={styles.subtitle}>Pakistan's first virtual student ID platform</Text>
      <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('Register')}>
        <Text style={styles.buttonText}>Get Started</Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={styles.link}>Already have an account? Login</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, justifyContent: 'center', alignItems: 'center', padding: 24 },
  title: { ...typography.h1, color: colors.primary, marginBottom: 12 },
  subtitle: { ...typography.body, color: colors.textSecondary, textAlign: 'center', marginBottom: 40 },
  button: { backgroundColor: colors.primary, paddingVertical: 14, paddingHorizontal: 40, borderRadius: 12, marginBottom: 16 },
  buttonText: { ...typography.button, color: colors.white },
  link: { ...typography.body, color: colors.primary },
});

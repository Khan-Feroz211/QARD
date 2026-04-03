import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert, ScrollView } from 'react-native';
import { useAuthStore } from '../store/authStore';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

/**
 * RegisterScreen — new student account creation form.
 */
export default function RegisterScreen({ navigation }) {
  const [form, setForm] = useState({ fullName: '', email: '', phone: '', studentId: '', password: '', universitySlug: '' });
  const register = useAuthStore((s) => s.register);

  const update = (field) => (val) => setForm((prev) => ({ ...prev, [field]: val }));

  const handleRegister = async () => {
    try {
      await register(form);
      navigation.replace('Main');
    } catch (err) {
      Alert.alert('Registration Failed', err.message || 'Please check your details.');
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>Create Account</Text>
      {[
        { field: 'universitySlug', placeholder: 'University slug (e.g. nust)' },
        { field: 'fullName', placeholder: 'Full Name' },
        { field: 'email', placeholder: 'Email', keyboardType: 'email-address' },
        { field: 'phone', placeholder: 'Phone (+92...)', keyboardType: 'phone-pad' },
        { field: 'studentId', placeholder: 'Student ID / Roll Number' },
        { field: 'password', placeholder: 'Password', secureTextEntry: true },
      ].map(({ field, placeholder, ...props }) => (
        <TextInput key={field} style={styles.input} placeholder={placeholder} value={form[field]} onChangeText={update(field)} autoCapitalize="none" {...props} />
      ))}
      <TouchableOpacity style={styles.button} onPress={handleRegister}>
        <Text style={styles.buttonText}>Register</Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={() => navigation.navigate('Login')}>
        <Text style={styles.link}>Already have an account? Login</Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flexGrow: 1, backgroundColor: colors.background, justifyContent: 'center', padding: 24 },
  title: { ...typography.h1, color: colors.primary, marginBottom: 24, textAlign: 'center' },
  input: { borderWidth: 1, borderColor: colors.border, borderRadius: 8, padding: 12, marginBottom: 12, ...typography.body },
  button: { backgroundColor: colors.primary, padding: 14, borderRadius: 12, alignItems: 'center', marginBottom: 16 },
  buttonText: { ...typography.button, color: colors.white },
  link: { ...typography.body, color: colors.primary, textAlign: 'center' },
});

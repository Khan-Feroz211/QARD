import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { api } from '../services/api';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

/**
 * BenefitCard — renders a single student benefit/discount offer.
 */
export default function BenefitCard({ benefit }) {
  const handleClaim = () => {
    api.post(`/benefits/${benefit.id}/claim`).catch(() => {});
  };

  return (
    <View style={styles.card}>
      <View style={styles.row}>
        <Text style={styles.title}>{benefit.title}</Text>
        <Text style={styles.discount}>{benefit.discount_percent}% OFF</Text>
      </View>
      <Text style={styles.partner}>{benefit.partner_name}</Text>
      <Text style={styles.category}>{benefit.category}</Text>
      {benefit.valid_until && (
        <Text style={styles.expiry}>Valid until: {new Date(benefit.valid_until).toLocaleDateString()}</Text>
      )}
      <TouchableOpacity style={styles.button} onPress={handleClaim}>
        <Text style={styles.buttonText}>Claim Benefit</Text>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  card: { backgroundColor: colors.card, borderRadius: 12, padding: 16, marginBottom: 12, elevation: 2 },
  row: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 4 },
  title: { ...typography.body, color: colors.text, fontWeight: 'bold', flex: 1 },
  discount: { ...typography.body, color: colors.primary, fontWeight: 'bold' },
  partner: { ...typography.caption, color: colors.textSecondary, marginBottom: 2 },
  category: { ...typography.caption, color: colors.primary, textTransform: 'capitalize', marginBottom: 4 },
  expiry: { ...typography.caption, color: colors.textSecondary, marginBottom: 8 },
  button: { backgroundColor: colors.primary, padding: 10, borderRadius: 8, alignItems: 'center' },
  buttonText: { ...typography.button, color: colors.white, fontSize: 13 },
});

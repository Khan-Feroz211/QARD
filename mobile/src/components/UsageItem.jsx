import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

/**
 * UsageItem — renders a single card usage event row.
 */
export default function UsageItem({ event }) {
  const date = new Date(event.timestamp).toLocaleString();

  return (
    <View style={styles.item}>
      <View style={styles.left}>
        <Text style={styles.merchant}>{event.merchant_name || 'Unknown Merchant'}</Text>
        <Text style={styles.location}>{event.location || ''}</Text>
        <Text style={styles.date}>{date}</Text>
      </View>
      <View style={styles.right}>
        <Text style={styles.type}>{event.event_type}</Text>
        {event.amount_pkr != null && (
          <Text style={styles.amount}>PKR {event.amount_pkr.toFixed(0)}</Text>
        )}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  item: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 12, borderBottomWidth: 1, borderColor: colors.border },
  left: { flex: 3 },
  right: { flex: 1, alignItems: 'flex-end' },
  merchant: { ...typography.body, color: colors.text, fontWeight: '600' },
  location: { ...typography.caption, color: colors.textSecondary },
  date: { ...typography.caption, color: colors.textSecondary, marginTop: 2 },
  type: { ...typography.caption, color: colors.primary, textTransform: 'capitalize' },
  amount: { ...typography.body, color: colors.text, fontWeight: 'bold' },
});

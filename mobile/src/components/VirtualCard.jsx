import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import QRCode from './QRCode';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

/**
 * VirtualCard — renders the student's digital ID card UI.
 */
export default function VirtualCard({ card }) {
  if (!card) return null;

  return (
    <LinearGradient colors={[colors.primary, colors.primaryDark]} style={styles.card}>
      <View style={styles.header}>
        <Text style={styles.university}>{card.university_name}</Text>
        <Text style={styles.cardLabel}>STUDENT ID</Text>
      </View>
      <View style={styles.body}>
        <View style={styles.info}>
          <Text style={styles.name}>{card.holder_name}</Text>
          <Text style={styles.detail}>ID: {card.student_id}</Text>
          {card.program && <Text style={styles.detail}>{card.program}</Text>}
          <Text style={styles.cardNumber}>{card.card_number}</Text>
        </View>
        <QRCode data={card.qr_code_data} size={90} />
      </View>
      <Text style={styles.expiry}>
        Valid until: {card.expires_at ? new Date(card.expires_at).toLocaleDateString() : 'N/A'}
      </Text>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  card: { borderRadius: 16, padding: 20, marginVertical: 8, elevation: 6 },
  header: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 16 },
  university: { ...typography.caption, color: 'rgba(255,255,255,0.85)', flex: 1 },
  cardLabel: { ...typography.caption, color: 'rgba(255,255,255,0.7)', fontWeight: 'bold' },
  body: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  info: { flex: 1 },
  name: { ...typography.h2, color: colors.white, marginBottom: 4 },
  detail: { ...typography.caption, color: 'rgba(255,255,255,0.8)', marginBottom: 2 },
  cardNumber: { ...typography.caption, color: 'rgba(255,255,255,0.6)', letterSpacing: 2, marginTop: 8 },
  expiry: { ...typography.caption, color: 'rgba(255,255,255,0.7)', marginTop: 16 },
});

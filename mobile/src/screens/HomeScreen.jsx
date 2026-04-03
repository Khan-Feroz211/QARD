import React, { useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { useCardStore } from '../store/cardStore';
import VirtualCard from '../components/VirtualCard';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

/**
 * HomeScreen — displays the student's virtual card and quick actions.
 */
export default function HomeScreen() {
  const { card, fetchCard, loading } = useCardStore();

  useEffect(() => { fetchCard(); }, []);

  return (
    <ScrollView
      style={styles.container}
      refreshControl={<RefreshControl refreshing={loading} onRefresh={fetchCard} />}
    >
      <Text style={styles.greeting}>My QARD</Text>
      {card ? <VirtualCard card={card} /> : <Text style={styles.placeholder}>Loading your card…</Text>}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, padding: 16 },
  greeting: { ...typography.h2, color: colors.primary, marginBottom: 20 },
  placeholder: { ...typography.body, color: colors.textSecondary, textAlign: 'center', marginTop: 40 },
});

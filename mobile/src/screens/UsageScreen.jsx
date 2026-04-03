import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { api } from '../services/api';
import UsageItem from '../components/UsageItem';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

/**
 * UsageScreen — lists card usage events and unread alerts.
 */
export default function UsageScreen() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    api.get('/usage').then((res) => setEvents(res.data)).catch(() => {});
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Card Usage History</Text>
      <FlatList
        data={events}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => <UsageItem event={item} />}
        contentContainerStyle={styles.list}
        ListEmptyComponent={<Text style={styles.empty}>No usage events yet.</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  title: { ...typography.h2, color: colors.primary, padding: 16 },
  list: { paddingHorizontal: 16 },
  empty: { ...typography.body, color: colors.textSecondary, textAlign: 'center', marginTop: 40 },
});

import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { api } from '../services/api';
import BenefitCard from '../components/BenefitCard';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

/**
 * BenefitsScreen — shows the student discounts and partner offers catalog.
 */
export default function BenefitsScreen() {
  const [benefits, setBenefits] = useState([]);

  useEffect(() => {
    api.get('/benefits').then((res) => setBenefits(res.data)).catch(() => {});
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Student Benefits</Text>
      <FlatList
        data={benefits}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => <BenefitCard benefit={item} />}
        contentContainerStyle={styles.list}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background },
  title: { ...typography.h2, color: colors.primary, padding: 16 },
  list: { paddingHorizontal: 16 },
});

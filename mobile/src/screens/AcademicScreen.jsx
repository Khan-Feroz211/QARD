import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { api } from '../services/api';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

/**
 * AcademicScreen — shows current semester GPA and course results.
 */
export default function AcademicScreen() {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.get('/academic').then((res) => setData(res.data)).catch(() => {});
  }, []);

  if (!data) return <View style={styles.container}><Text style={styles.loading}>Loading academic data…</Text></View>;

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{data.semester} {data.year}</Text>
      <Text style={styles.gpa}>GPA: {data.gpa ?? 'N/A'}  |  CGPA: {data.cgpa ?? 'N/A'}</Text>
      <Text style={styles.label}>Program: {data.program}</Text>
      <FlatList
        data={data.courses}
        keyExtractor={(item) => item.course_code}
        renderItem={({ item }) => (
          <View style={styles.course}>
            <Text style={styles.courseCode}>{item.course_code}</Text>
            <Text style={styles.courseName}>{item.course_name}</Text>
            <Text style={styles.grade}>{item.grade ?? '-'}</Text>
          </View>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.background, padding: 16 },
  loading: { ...typography.body, color: colors.textSecondary, textAlign: 'center', marginTop: 40 },
  title: { ...typography.h2, color: colors.primary, marginBottom: 4 },
  gpa: { ...typography.body, color: colors.text, marginBottom: 4 },
  label: { ...typography.caption, color: colors.textSecondary, marginBottom: 16 },
  course: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 8, borderBottomWidth: 1, borderColor: colors.border },
  courseCode: { ...typography.caption, color: colors.textSecondary, flex: 1 },
  courseName: { ...typography.body, color: colors.text, flex: 3 },
  grade: { ...typography.body, color: colors.primary, flex: 1, textAlign: 'right' },
});

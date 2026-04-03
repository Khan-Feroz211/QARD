import React from 'react';
import QRCodeSVG from 'react-native-qrcode-svg';
import { View, StyleSheet } from 'react-native';
import { colors } from '../theme/colors';

/**
 * QRCode — renders a QR code for a given data string.
 */
export default function QRCode({ data, size = 120 }) {
  if (!data) return null;
  return (
    <View style={styles.container}>
      <QRCodeSVG value={data} size={size} color={colors.white} backgroundColor="transparent" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { padding: 4, backgroundColor: 'rgba(255,255,255,0.1)', borderRadius: 8 },
});

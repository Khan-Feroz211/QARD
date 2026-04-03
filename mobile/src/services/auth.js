/**
 * auth.js — authentication API calls (register, login, OTP).
 */
import { api } from './api';
import { saveToken, removeToken } from './storage';

export async function registerStudent(form) {
  const response = await api.post('/auth/register', {
    full_name: form.fullName,
    email: form.email,
    phone: form.phone,
    student_id: form.studentId,
    password: form.password,
    university_slug: form.universitySlug,
  });
  await saveToken(response.data.access_token);
  return response.data;
}

export async function loginStudent(email, password, universitySlug) {
  const response = await api.post('/auth/login', { email, password, university_slug: universitySlug });
  await saveToken(response.data.access_token);
  return response.data;
}

export async function sendOTP(phone) {
  return api.post('/auth/otp/send', null, { params: { phone } });
}

export async function verifyOTP(phone, otpCode) {
  return api.post('/auth/otp/verify', { phone, otp_code: otpCode });
}

export async function logoutUser() {
  await removeToken();
}

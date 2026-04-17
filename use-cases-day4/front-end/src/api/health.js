const BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export async function checkReadiness() {
  const res = await fetch(`${BASE_URL}/health/readiness`);
  return res.json();
}

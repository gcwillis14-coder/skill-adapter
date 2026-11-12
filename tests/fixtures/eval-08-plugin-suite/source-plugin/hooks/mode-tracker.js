// Persists concise-dev mode across turns via session hook.
export function onSessionStart() {
  return { mode: "full" };
}

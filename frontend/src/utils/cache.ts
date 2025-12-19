const STORAGE_KEY = "latest_data";
const STORAGE_TIME_KEY = "latest_data_time";
const PREDICTIONS_KEY = "predictions";

export function getCachedLatestData() {
  const data = localStorage.getItem(STORAGE_KEY);
  const time = localStorage.getItem(STORAGE_TIME_KEY);

  if (!data || !time) return null;

  const lastFetch = new Date(time);
  const now = new Date();

  const sameDay =
    lastFetch.getFullYear() === now.getFullYear() &&
    lastFetch.getMonth() === now.getMonth() &&
    lastFetch.getDate() === now.getDate();

  if (!sameDay) return null;

  return JSON.parse(data);
}

export function setCachedLatestData(data: any) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  localStorage.setItem(STORAGE_TIME_KEY, new Date().toISOString());
}

export function getCachedPredictions() {
  const data = localStorage.getItem(PREDICTIONS_KEY);
  const latestTime = localStorage.getItem("latest_data_time"); // use latest-data timestamp
  const predictionsTime = localStorage.getItem("predictions_time");

  // Must have data, a previous timestamp, and timestamps must match
  if (!data || !predictionsTime || predictionsTime !== latestTime) return null;

  return JSON.parse(data);
}

// Store predictions with the latest-data timestamp
export function setCachedPredictions(data: any) {
  localStorage.setItem(PREDICTIONS_KEY, JSON.stringify(data));

  // Tie predictions timestamp to latest-data timestamp
  const latestTime = localStorage.getItem("latest_data_time");
  if (latestTime) localStorage.setItem("predictions_time", latestTime);
}
import axios from "axios";
import { getCachedLatestData, setCachedLatestData, getCachedPredictions, setCachedPredictions } from "../utils/cache";


const baseURL = "http://localhost:8000"
// Base Axios instance
const api = axios.create({
  baseURL: "http://localhost:8000", // change if backend is on a different port
  timeout: 1000000, // 10 seconds
});

// -----------------------
// API calls
// -----------------------

export async function fetchLatestData() {
  const cached = getCachedLatestData();
  if (cached) return cached;

  const res = await fetch(`${baseURL}/api/v1/latest-data-snapshot`);
  if (!res.ok) throw new Error("Failed to fetch latest data");

  const data = await res.json();
  setCachedLatestData(data);

  return data;
}

export async function fetchPredictions() {
  const cached = getCachedPredictions();
  if (cached) return cached;

  const res = await fetch(`${ baseURL}/api/v1/predict`);
  if (!res.ok) throw new Error("Failed to fetch predictions");

  const data = await res.json();
  setCachedPredictions(data);

  return data;
}

export async function fetchHistory() {
  const res = await api.get("/history");
  return res.data;
}

export async function fetchNewsSentiment() {
  const res = await api.get("/news-sentiment");
  return res.data;
}

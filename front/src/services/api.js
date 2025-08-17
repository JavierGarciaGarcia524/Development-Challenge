const API_BASE = "http://127.0.0.1:5000"; // change when running backend

export async function fetchWeather({ station, startDate, endDate, features, aggregation }) {
  const params = new URLSearchParams();
  params.append("station", station);
  params.append("init_date", startDate);
  params.append("end_date", endDate);

  features.forEach(f => params.append("desired_features", f));
  
  if (aggregation && aggregation !== "Default") {
    params.append("aggregation_value", aggregation);
  }

  console.log(`${API_BASE}/api/weather?${params.toString()}`);
  const res = await fetch(`${API_BASE}/api/weather?${params.toString()}`);
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.error || "Error in the request");
  }
  return res.json();
}

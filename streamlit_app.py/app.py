from data_loader import load_laps, load_weather, load_results

laps = load_laps()
weather = load_weather()
results = load_results()

st.write("laps:", laps.shape)
st.write("weather:", weather.shape)
st.write("results:", results.shape)

# 🌤️ Weather API Setup for Doctor Dashboard

## Overview
The Doctor Dashboard now includes real-time weather information displayed beside the search bar. Currently, it uses mock data for demonstration purposes, but you can easily integrate with real weather APIs.

## Current Implementation
- **Real-time Clock**: Updates every second
- **Real Weather API**: OpenWeatherMap integration with live data
- **Auto-refresh**: Weather updates every 30 minutes
- **Responsive Design**: Works on all screen sizes
- **Geolocation**: Uses user's location or defaults to Manila

## Real Weather API Integration

### Option 1: OpenWeatherMap API (Recommended)

1. **Get Free API Key**:
   - Visit: https://openweathermap.org/api
   - Sign up for a free account
   - Get your API key

2. **Update the Code**:
   Replace the mock weather function in `frontend/src/pages/DoctorDashboard.vue`:

```typescript
const fetchWeather = async () => {
  weatherLoading.value = true
  weatherError.value = false
  
  try {
    // Get user's location
    let latitude = 14.5995 // Default: Manila
    let longitude = 120.9842
    
    if (navigator.geolocation) {
      const position = await new Promise<GeolocationPosition>((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          timeout: 5000,
          enableHighAccuracy: false
        })
      })
      latitude = position.coords.latitude
      longitude = position.coords.longitude
    }
    
    // Use OpenWeatherMap API
    const apiKey = '5c328a0059938745d143138d206eb570' 
    const response = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=${apiKey}&units=metric`
    )
    
    if (!response.ok) {
      throw new Error('Weather API request failed')
    }
    
    const data = await response.json()
    
    weatherData.value = {
      temperature: Math.round(data.main.temp),
      condition: data.weather[0].main.toLowerCase(),
      location: data.name,
      description: data.weather[0].description
    }
  } catch (error) {
    console.error('Weather fetch error:', error)
    weatherError.value = true
    
    // Fallback weather data
    weatherData.value = {
      temperature: 22,
      condition: 'clear',
      location: 'Local Area',
      description: 'Partly cloudy'
    }
  } finally {
    weatherLoading.value = false
  }
}
```

### Option 2: WeatherAPI.com

1. **Get API Key**:
   - Visit: https://www.weatherapi.com/
   - Sign up for free tier (1M calls/month)

2. **Update the Code**:
```typescript
const response = await fetch(
  `http://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=${latitude},${longitude}&aqi=no`
)
```

### Option 3: AccuWeather API

1. **Get API Key**:
   - Visit: https://developer.accuweather.com/
   - Sign up for free tier

2. **Update the Code**:
```typescript
const response = await fetch(
  `http://dataservice.accuweather.com/currentconditions/v1/${locationKey}?apikey=YOUR_API_KEY`
)
```

## Environment Variables (Recommended)

For security, store your API key in environment variables:

1. **Create `.env` file** in frontend directory:
```env
VITE_WEATHER_API_KEY=your_api_key_here
```

2. **Update the code**:
```typescript
const apiKey = import.meta.env.VITE_WEATHER_API_KEY
```

## Features

### Real-time Clock
- Updates every second
- 12-hour format with AM/PM
- Automatic timezone detection

### Weather Display
- Current temperature in Celsius
- Weather condition with appropriate icon
- Location name
- Auto-refresh every 30 minutes

### Weather Icons
The system maps weather conditions to Material Design icons:
- ☀️ Clear: `wb_sunny`
- ☁️ Clouds: `cloud`
- 🌧️ Rain: `opacity`
- ❄️ Snow: `ac_unit`
- ⚡ Thunderstorm: `flash_on`
- 🌫️ Mist/Fog: `cloud`

### Error Handling
- Graceful fallback to mock data
- Loading states
- Error indicators
- Geolocation fallback

## Customization

### Change Update Intervals
```typescript
// Update time every second
timeInterval = setInterval(updateTime, 1000)

// Update weather every 30 minutes
setInterval(fetchWeather, 30 * 60 * 1000)
```

### Custom Weather Icons
Add more weather conditions to the `iconMap`:
```typescript
const iconMap: Record<string, string> = {
  'clear': 'wb_sunny',
  'clouds': 'cloud',
  'rain': 'opacity',
  // Add more conditions here
}
```

### Styling
Modify the CSS in the component to change appearance:
```css
.real-time-info {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-left: 20px;
}
```

## Troubleshooting

### Weather Not Loading
1. Check browser console for errors
2. Verify API key is correct
3. Check network connectivity
4. Ensure CORS is enabled for API calls

### Geolocation Not Working
1. Check if HTTPS is enabled (required for geolocation)
2. Verify browser permissions
3. Check if location services are enabled

### API Rate Limits
- OpenWeatherMap: 60 calls/minute (free tier)
- WeatherAPI: 1M calls/month (free tier)
- AccuWeather: 50 calls/day (free tier)

## Security Notes

1. **Never expose API keys** in client-side code for production
2. **Use environment variables** for API keys
3. **Implement server-side proxy** for production apps
4. **Add rate limiting** to prevent abuse
5. **Use HTTPS** for all API calls

## Production Deployment

For production, consider:
1. **Server-side weather fetching** to hide API keys
2. **Caching weather data** to reduce API calls
3. **CDN integration** for better performance
4. **Error monitoring** for API failures
5. **Fallback strategies** for API downtime

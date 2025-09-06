# 🌐 Burnout Prediction Frontend

A modern, responsive web interface for the Employee Burnout Risk Prediction API.

## 🚀 Quick Start

### 1. Start the API Server
First, make sure your FastAPI server is running:
```bash
cd api
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Start the Frontend Server
In a new terminal:
```bash
cd frontend
python server.py
```

### 3. Open in Browser
The frontend will automatically open at: http://localhost:3000

## 📱 Features


### 🔧 Functionality
- **Form Validation**: Ensures all required fields are filled
- **Real-time Updates**: Slider values update as you move them
- **Error Handling**: Clear error messages for troubleshooting
- **Loading States**: Visual feedback during API calls
- **Risk Categorization**: Color-coded results (Low/Medium/High)

### 📊 Input Fields

| Field | Type | Description |
|-------|------|-------------|
| **Job Designation** | Dropdown | Employee level (0-5) |
| **Gender** | Dropdown | Male/Female |
| **Company Type** | Dropdown | Product/Service company |
| **Work From Home** | Dropdown | WFH availability |
| **Resource Allocation** | Slider | Workload level (0-10) |
| **Mental Fatigue** | Slider | Stress level (0-10) |

### 🎯 Results Display

The results are displayed with:
- **Risk Category**: Low Risk, Medium Risk, or High Risk
- **Burn Rate Percentage**: Numerical score (0-100%)
- **Color Coding**: 
  - 🟢 Green: Low Risk
  - 🟡 Orange: Medium Risk
  - 🔴 Red: High Risk
- **Confidence Score**: Model confidence in prediction
- **Recommendations**: Actionable advice based on risk level

## 🔧 Technical Details

### Architecture
```
Frontend (Port 3000) ← HTTP → API (Port 8000) ← → ML Model (.pkl)
```

### API Communication
- **Endpoint**: `POST /predict`
- **Format**: JSON
- **CORS**: Enabled for cross-origin requests
- **Error Handling**: Comprehensive error messages

### Browser Compatibility
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

## 🛠️ Development

### File Structure
```
frontend/
├── index.html          # Main application
├── server.py           # Development server
└── README.md          # This file
```

### Customization

#### Changing API URL
Edit the `API_BASE_URL` in `index.html`:
```javascript
const API_BASE_URL = 'http://your-api-url:8000';
```

#### Styling
All CSS is embedded in `index.html`. Key sections:
- **Color Scheme**: Modify gradient colors
- **Layout**: Adjust grid and spacing
- **Animations**: Update transition effects

#### Form Fields
To add new input fields:
1. Add HTML form element
2. Update JavaScript form data collection
3. Ensure API compatibility

## 🐛 Troubleshooting

### Common Issues

**1. "Cannot connect to API"**
- ✅ Ensure API server is running on port 8000
- ✅ Check API health: http://localhost:8000/health
- ✅ Verify model file exists: `models/burnout_prediction_model.pkl`

**2. "CORS Error"**
- ✅ API should include CORS headers
- ✅ Use the provided `server.py` for development

**3. "422 Validation Error"**
- ✅ Check all form fields are filled
- ✅ Ensure values are within valid ranges
- ✅ Verify data types match API expectations

**4. "Model not loaded"**
- ✅ Train the model first: `python burnout_prediction_model.py`
- ✅ Check model file path in API configuration

### Debug Mode
Open browser developer tools (F12) to see:
- Network requests to API
- JavaScript console errors
- Response data from API

## 🚀 Deployment

### Production Deployment
For production, consider:

1. **Static Hosting**: Deploy HTML to CDN/static host
2. **API Hosting**: Deploy FastAPI to cloud service
3. **HTTPS**: Enable SSL certificates
4. **Environment Variables**: Configure API URLs

### Docker Deployment
```dockerfile
# Frontend Dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
EXPOSE 80
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

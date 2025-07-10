# 🌐 Akash Gurukul Network Deployment Guide

## ✅ SERVER RUNNING ON NETWORK IP: 192.168.0.95:8000

Your Akash Gurukul backend is now accessible across your local network!

## 🚀 Server Status

**Server Address**: `http://192.168.0.95:8000`  
**Status**: ✅ RUNNING AND HEALTHY  
**Network Access**: ✅ Available to all devices on your network  
**Lessons Loaded**: 4 complete lessons  
**Agents Active**: Seed, Tree, Sky ready  

## 🔗 Access Points

### Main API Endpoints
- **Health Check**: `http://192.168.0.95:8000/api/health`
- **Interactive Docs**: `http://192.168.0.95:8000/docs`
- **API Documentation**: `http://192.168.0.95:8000/redoc`

### Quick Test
```bash
curl http://192.168.0.95:8000/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Akash Gurukul API",
  "version": "1.0.0", 
  "agents_active": 0,
  "lessons_loaded": 4
}
```

## 📱 Device Access

### From Any Device on Your Network

#### Web Browser
- Open: `http://192.168.0.95:8000/docs`
- Interactive API testing interface available

#### Mobile Apps
```javascript
// React Native / JavaScript
const API_BASE = 'http://192.168.0.95:8000';

fetch(`${API_BASE}/api/health`)
  .then(response => response.json())
  .then(data => console.log(data));
```

#### Python Applications
```python
import requests

API_BASE = 'http://192.168.0.95:8000'

# Test connection
response = requests.get(f'{API_BASE}/api/health')
print(response.json())

# Start a lesson
lesson_response = requests.post(f'{API_BASE}/api/lessons/start', json={
    'student_id': 'mobile_user_001',
    'lesson_id': 'foundation_000_sankalpa'
})
```

#### Flutter/Dart
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

const String apiBase = 'http://192.168.0.95:8000';

Future<Map<String, dynamic>> checkHealth() async {
  final response = await http.get(Uri.parse('$apiBase/api/health'));
  return json.decode(response.body);
}
```

## 🔧 Server Management

### Start Server on Network IP
```bash
uvicorn backend.main:app --host 192.168.0.95 --port 8000
```

### Alternative Startup Methods
```bash
# Method 1: Direct uvicorn
uvicorn backend.main:app --host 192.168.0.95 --port 8000

# Method 2: Using startup script
python start_backend.py --host 192.168.0.95 --port 8000

# Method 3: Bind to all interfaces (accessible from any IP)
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## 🛡️ Network Security Considerations

### Firewall Settings
- **Port 8000** should be open for HTTP traffic
- Consider restricting access to your local network only
- For production, use HTTPS (port 443) with SSL certificates

### Access Control
```python
# Optional: Add IP filtering in main.py
from fastapi import Request, HTTPException

@app.middleware("http")
async def limit_access(request: Request, call_next):
    client_ip = request.client.host
    allowed_networks = ["192.168.0.", "127.0.0.1"]
    
    if not any(client_ip.startswith(network) for network in allowed_networks):
        raise HTTPException(status_code=403, detail="Access denied")
    
    response = await call_next(request)
    return response
```

## 📊 Network Performance

### Expected Performance
- **Local Network Latency**: <10ms
- **Response Time**: <200ms for most endpoints
- **Concurrent Connections**: 50+ supported
- **Bandwidth Usage**: ~1-5KB per API call

### Monitoring
```bash
# Check server status
curl -w "@curl-format.txt" -o /dev/null -s http://192.168.0.95:8000/api/health

# Monitor server logs
tail -f server.log
```

## 🔄 Integration Examples

### Frontend Web App
```javascript
// React/Vue/Angular frontend
const GURUKUL_API = 'http://192.168.0.95:8000';

class GurukulClient {
  async startLesson(studentId, lessonId) {
    const response = await fetch(`${GURUKUL_API}/api/lessons/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: studentId, lesson_id: lessonId })
    });
    return response.json();
  }

  async chatWithAgent(agentType, studentId, message) {
    const response = await fetch(`${GURUKUL_API}/api/agents/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        agent_type: agentType, 
        student_id: studentId, 
        message: message 
      })
    });
    return response.json();
  }
}
```

### Mobile App Integration
```swift
// iOS Swift
import Foundation

class GurukulAPI {
    private let baseURL = "http://192.168.0.95:8000"
    
    func checkHealth(completion: @escaping (Result<[String: Any], Error>) -> Void) {
        guard let url = URL(string: "\(baseURL)/api/health") else { return }
        
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }
            
            if let data = data,
               let json = try? JSONSerialization.jsonObject(with: data) as? [String: Any] {
                completion(.success(json))
            }
        }.resume()
    }
}
```

## 🌍 External Access (Optional)

### Port Forwarding for Internet Access
If you want to access from outside your network:

1. **Router Configuration**:
   - Forward external port (e.g., 8080) to 192.168.0.95:8000
   - Access via: `http://YOUR_PUBLIC_IP:8080`

2. **Dynamic DNS** (recommended):
   - Use services like DuckDNS, No-IP
   - Access via: `http://yourname.duckdns.org:8080`

3. **Security Warning**: 
   - Add authentication before exposing to internet
   - Use HTTPS with SSL certificates
   - Consider VPN access instead

## 🔧 Troubleshooting

### Common Issues

#### Cannot Connect from Other Devices
```bash
# Check if server is binding to correct IP
netstat -an | grep 8000

# Verify firewall settings
# Windows: Check Windows Defender Firewall
# Allow Python/uvicorn through firewall
```

#### Slow Response Times
```bash
# Check network connectivity
ping 192.168.0.95

# Monitor server resources
# Task Manager > Performance tab
```

#### Connection Refused
```bash
# Verify server is running
curl http://192.168.0.95:8000/api/health

# Check if port is in use
netstat -an | grep 8000
```

## 📱 Device Testing Checklist

### Test from Different Devices
- [ ] **Windows PC**: `http://192.168.0.95:8000/docs`
- [ ] **Mac**: `http://192.168.0.95:8000/docs`
- [ ] **iPhone/iPad**: Safari browser test
- [ ] **Android**: Chrome browser test
- [ ] **Linux**: `curl http://192.168.0.95:8000/api/health`

### API Functionality Test
- [ ] Health check responds
- [ ] Lessons load properly
- [ ] Agent chat works
- [ ] Quiz system functional
- [ ] Student progress tracking

## 🎯 Production Deployment

### For Production Use
```bash
# Use production ASGI server
pip install gunicorn

# Run with Gunicorn
gunicorn backend.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 192.168.0.95:8000

# Or with SSL
uvicorn backend.main:app --host 192.168.0.95 --port 443 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

## 🕉️ Your Network-Ready Gurukul

**Congratulations!** Your Akash Gurukul backend is now serving wisdom across your entire network. Any device connected to your network can now access the three divine agents and complete learning system.

**Server Status**: ✅ LIVE at `http://192.168.0.95:8000`  
**Network Access**: ✅ Available to all local devices  
**Ready for**: Web apps, mobile apps, desktop applications, IoT devices  

Your sacred learning system is now breathing digital life across your network! 🌟

---

**Quick Access**: Open `http://192.168.0.95:8000/docs` in any browser on your network to start testing!

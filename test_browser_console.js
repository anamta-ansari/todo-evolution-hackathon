// Test 1: Can we reach health endpoint?
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(d => console.log('✅ Health check works:', d))
  .catch(e => console.error('❌ Health check failed:', e));

// Test 2: Get user ID from token
const token = localStorage.getItem('auth_token');
if (!token) {
  console.error('❌ No auth token - you need to log in first');
} else {
  const payload = JSON.parse(atob(token.split('.')[1]));
  const userId = payload.user_id || payload.sub;
  console.log('✅ User ID:', userId);
  
  // Test 3: Can we call chat endpoint?
  fetch(`http://localhost:8000/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ message: 'test connection' })
  })
    .then(r => r.json())
    .then(d => console.log('✅ Chat endpoint works:', d))
    .catch(e => console.error('❌ Chat endpoint failed:', e));
}

// Check localStorage has auth token:
const tokenExists = localStorage.getItem('auth_token');
console.log('Token exists:', !!tokenExists);
console.log('Token value:', tokenExists ? tokenExists.substring(0, 20) + '...' : 'NONE');
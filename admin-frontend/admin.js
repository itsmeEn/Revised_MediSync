// Configuration
const API_BASE_URL = 'http://localhost:8000/api/admin';

// Global variables
let currentUser = null;
let verifications = [];
let selectedVerification = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    setupEventListeners();
});

// Check if user is authenticated
function checkAuth() {
    const token = localStorage.getItem('admin_access_token');
    if (token) {
        showDashboard();
        loadDashboardData();
    } else {
        showLogin();
    }
}

// Setup event listeners
function setupEventListeners() {
    // Login form
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Filters
    document.getElementById('statusFilter').addEventListener('change', filterVerifications);
    document.getElementById('searchInput').addEventListener('input', filterVerifications);
}

// Show login screen
function showLogin() {
    document.getElementById('loginScreen').style.display = 'flex';
    document.getElementById('dashboard').style.display = 'none';
}

// Show dashboard
function showDashboard() {
    document.getElementById('loginScreen').style.display = 'none';
    document.getElementById('dashboard').style.display = 'block';
}

// Handle login
async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    showLoading(true);
    
    try {
        const response = await fetch(`${API_BASE_URL}/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('admin_access_token', data.access);
            localStorage.setItem('admin_refresh_token', data.refresh);
            currentUser = data.admin_user;
            
            showToast('Success', 'Login successful!', 'success');
            showDashboard();
            loadDashboardData();
        } else {
            showToast('Error', data.error || 'Login failed', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showToast('Error', 'Network error. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
}

// Logout
function logout() {
    localStorage.removeItem('admin_access_token');
    localStorage.removeItem('admin_refresh_token');
    currentUser = null;
    showLogin();
}

// Load dashboard data
async function loadDashboardData() {
    showLoading(true);
    
    try {
        await Promise.all([
            loadStats(),
            loadVerifications()
        ]);
        
        updateAdminName();
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showToast('Error', 'Failed to load dashboard data', 'error');
    } finally {
        showLoading(false);
    }
}

// Load statistics
async function loadStats() {
    const response = await apiCall('/dashboard/stats/');
    if (response) {
        document.getElementById('pendingCount').textContent = response.pending;
        document.getElementById('approvedCount').textContent = response.approved;
        document.getElementById('declinedCount').textContent = response.declined;
        document.getElementById('archivedCount').textContent = response.archived;
    }
}

// Load verifications
async function loadVerifications() {
    const response = await apiCall('/verifications/');
    if (response) {
        verifications = response.verifications;
        renderVerificationsTable(verifications);
    }
}

// Render verifications table
function renderVerificationsTable(data) {
    const tbody = document.getElementById('verificationsTable');
    tbody.innerHTML = '';
    
    if (data.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No verification requests found</td></tr>';
        return;
    }
    
    data.forEach(verification => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${verification.user_full_name}</td>
            <td>${verification.user_email}</td>
            <td><span class="badge bg-info">${verification.user_role}</span></td>
            <td>${getStatusBadge(verification.status)}</td>
            <td>${formatDate(verification.submitted_at)}</td>
            <td>${getActionButtons(verification)}</td>
        `;
        tbody.appendChild(row);
    });
}

// Get status badge
function getStatusBadge(status) {
    const colors = {
        'pending': 'warning',
        'approved': 'success',
        'declined': 'danger',
        'archived': 'secondary'
    };
    
    return `<span class="badge bg-${colors[status] || 'secondary'}">${status}</span>`;
}

// Get action buttons
function getActionButtons(verification) {
    let buttons = '';
    
    if (verification.status === 'pending') {
        buttons += `<button class="btn btn-success btn-sm btn-action" onclick="acceptVerification(${verification.id})">
            <i class="fas fa-check"></i> Accept
        </button>`;
        buttons += `<button class="btn btn-danger btn-sm btn-action" onclick="showDeclineModal(${verification.id})">
            <i class="fas fa-times"></i> Decline
        </button>`;
    }
    
                    buttons += `<button class="btn btn-primary btn-sm btn-action" onclick="viewDocument(${verification.id}).catch(console.error)">
                    <i class="fas fa-eye"></i> View
                </button>`;
    
    buttons += `<button class="btn btn-warning btn-sm btn-action" onclick="archiveVerification(${verification.id})">
        <i class="fas fa-archive"></i> Archive
    </button>`;
    
    return buttons;
}

// Accept verification
async function acceptVerification(id) {
    if (!confirm('Are you sure you want to approve this verification?')) {
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await apiCall(`/verifications/${id}/accept/`, 'POST');
        if (response) {
            showToast('Success', 'Verification approved successfully', 'success');
            loadDashboardData();
        }
    } catch (error) {
        console.error('Error accepting verification:', error);
        showToast('Error', 'Failed to approve verification', 'error');
    } finally {
        showLoading(false);
    }
}

// Show decline modal
function showDeclineModal(id) {
    selectedVerification = verifications.find(v => v.id === id);
    document.getElementById('declineReason').value = '';
    document.getElementById('sendEmail').checked = true;
    
    const modal = new bootstrap.Modal(document.getElementById('declineModal'));
    modal.show();
}

// Confirm decline
async function confirmDecline() {
    const reason = document.getElementById('declineReason').value.trim();
    const sendEmail = document.getElementById('sendEmail').checked;
    
    if (!reason) {
        showToast('Error', 'Please provide a reason for declining', 'error');
        return;
    }
    
    if (!selectedVerification) {
        showToast('Error', 'No verification selected', 'error');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await apiCall(`/verifications/${selectedVerification.id}/decline/`, 'POST', {
            reason: reason,
            send_email: sendEmail
        });
        
        if (response) {
            showToast('Success', 'Verification declined successfully', 'success');
            
            const modal = bootstrap.Modal.getInstance(document.getElementById('declineModal'));
            modal.hide();
            
            loadDashboardData();
        }
    } catch (error) {
        console.error('Error declining verification:', error);
        showToast('Error', 'Failed to decline verification', 'error');
    } finally {
        showLoading(false);
        selectedVerification = null;
    }
}

// View document
async function viewDocument(id) {
    const verification = verifications.find(v => v.id === id);
    if (!verification) {
        showToast('Error', 'Verification not found', 'error');
        return;
    }
    
    // Update document info
    document.getElementById('documentInfo').innerHTML = `
        <div class="row">
            <div class="col-md-6">
                <p><strong>Name:</strong> ${verification.user_full_name}</p>
                <p><strong>Email:</strong> ${verification.user_email}</p>
            </div>
            <div class="col-md-6">
                <p><strong>Role:</strong> ${verification.user_role}</p>
                <p><strong>Status:</strong> ${verification.status}</p>
            </div>
        </div>
    `;
    
    // Show document if available
    const iframe = document.getElementById('documentFrame');
    if (verification.verification_document) {
        // Fetch document with authentication and create blob URL
        try {
            const token = localStorage.getItem('admin_access_token');
            if (!token) {
                throw new Error('No authentication token');
            }
            
            const response = await fetch(`${API_BASE_URL}/verifications/${verification.id}/document/`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const blobUrl = URL.createObjectURL(blob);
                iframe.src = blobUrl;
                iframe.style.display = 'block';
            } else {
                throw new Error('Failed to fetch document');
            }
        } catch (error) {
            console.error('Error loading document:', error);
            iframe.style.display = 'none';
            document.getElementById('documentInfo').innerHTML += '<p class="text-danger">Error loading document. Please try again.</p>';
        }
    } else {
        iframe.style.display = 'none';
        document.getElementById('documentInfo').innerHTML += '<p class="text-muted">No document uploaded</p>';
    }
    
    const modal = new bootstrap.Modal(document.getElementById('documentModal'));
    modal.show();
}

// Archive verification
async function archiveVerification(id) {
    if (!confirm('Are you sure you want to archive this verification?')) {
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await apiCall(`/verifications/${id}/archive/`, 'POST');
        if (response) {
            showToast('Success', 'Verification archived successfully', 'success');
            loadDashboardData();
        }
    } catch (error) {
        console.error('Error archiving verification:', error);
        showToast('Error', 'Failed to archive verification', 'error');
    } finally {
        showLoading(false);
    }
}

// Filter verifications
function filterVerifications() {
    const statusFilter = document.getElementById('statusFilter').value;
    const searchQuery = document.getElementById('searchInput').value.toLowerCase();
    
    let filtered = verifications;
    
    // Filter by status
    if (statusFilter) {
        filtered = filtered.filter(v => v.status === statusFilter);
    }
    
    // Filter by search query
    if (searchQuery) {
        filtered = filtered.filter(v => 
            v.user_full_name.toLowerCase().includes(searchQuery) ||
            v.user_email.toLowerCase().includes(searchQuery)
        );
    }
    
    renderVerificationsTable(filtered);
}

// Update admin name
function updateAdminName() {
    if (currentUser) {
        document.getElementById('adminName').textContent = currentUser.full_name;
    }
}

// API call helper
async function apiCall(endpoint, method = 'GET', data = null) {
    const token = localStorage.getItem('admin_access_token');
    if (!token) {
        logout();
        return null;
    }
    
    const options = {
        method: method,
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (response.status === 401) {
            // Token expired, try to refresh
            const refreshed = await refreshToken();
            if (refreshed) {
                return apiCall(endpoint, method, data);
            } else {
                logout();
                return null;
            }
        }
        
        const responseData = await response.json();
        
        if (!response.ok) {
            throw new Error(responseData.error || 'API request failed');
        }
        
        return responseData;
    } catch (error) {
        console.error('API call error:', error);
        throw error;
    }
}

// Refresh token
async function refreshToken() {
    const refreshToken = localStorage.getItem('admin_refresh_token');
    if (!refreshToken) {
        return false;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/token/refresh/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ refresh: refreshToken })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('admin_access_token', data.access);
            return true;
        }
    } catch (error) {
        console.error('Token refresh error:', error);
    }
    
    return false;
}

// Show toast notification
function showToast(title, message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastTitle = document.getElementById('toastTitle');
    const toastMessage = document.getElementById('toastMessage');
    
    toastTitle.textContent = title;
    toastMessage.textContent = message;
    
    // Remove existing classes
    toast.className = 'toast';
    
    // Add type-specific classes
    if (type === 'success') {
        toast.classList.add('bg-success', 'text-white');
    } else if (type === 'error') {
        toast.classList.add('bg-danger', 'text-white');
    } else if (type === 'warning') {
        toast.classList.add('bg-warning', 'text-dark');
    } else {
        toast.classList.add('bg-info', 'text-white');
    }
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// Show/hide loading
function showLoading(show) {
    const loading = document.getElementById('loading');
    if (show) {
        loading.classList.add('show');
    } else {
        loading.classList.remove('show');
    }
}

// Format date
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

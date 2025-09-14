// Global variables
let sensorData = [];
let charts = {};

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    fetchData();
    setInterval(fetchData, 300000); // Update every 5 minutes
});

// Initialize charts
function initializeCharts() {
    // Moisture chart
    const moistureCtx = document.getElementById('moisture-chart').getContext('2d');
    charts.moisture = new Chart(moistureCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Soil Moisture (%)',
                data: [],
                borderColor: '#4ca1af',
                backgroundColor: 'rgba(76, 161, 175, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // Nutrient chart
    const nutrientCtx = document.getElementById('nutrient-chart').getContext('2d');
    charts.nutrient = new Chart(nutrientCtx, {
        type: 'bar',
        data: {
            labels: ['Nitrogen', 'Phosphorus', 'Potassium'],
            datasets: [{
                label: 'Nutrient Level (mg/kg)',
                data: [0, 0, 0],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Fetch data from server
async function fetchData() {
    try {
        const response = await fetch('http://localhost:5000/api/analytics/current');
        const data = await response.json();
        
        updateCurrentReadings(data.current);
        updateCharts(data.historical);
        updateHealthScore(data.healthScore);
        updateAlerts(data.alerts);
        
        // Fetch recommendations
        const cropResponse = await fetch('http://localhost:5000/api/recommendations/crops');
        const cropData = await cropResponse.json();
        
        const fertilizerResponse = await fetch('http://localhost:5000/api/recommendations/fertilizer?crop=' + encodeURIComponent(cropData.recommendations[0].crop));
        const fertilizerData = await fertilizerResponse.json();
        
        const yieldResponse = await fetch('http://localhost:5000/api/analytics/yield-prediction?crop=' + encodeURIComponent(cropData.recommendations[0].crop));
        const yieldData = await yieldResponse.json();
        
        updateRecommendations({
            crops: cropData.recommendations,
            fertilizer: fertilizerData.recommendation
        });
        
        updatePredictions({
            yield: yieldData.predictedYield,
            crop: yieldData.crop,
            risks: yieldData.waterStress ? [{type: 'Water Stress', level: 'High'}] : []
        });
        
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Update current readings
function updateCurrentReadings(data) {
    document.getElementById('moisture-reading').querySelector('.value').textContent = `${data.moisture}%`;
    document.getElementById('temperature-reading').querySelector('.value').textContent = `${data.temperature}°C`;
    document.getElementById('humidity-reading').querySelector('.value').textContent = `${data.humidity}%`;
    document.getElementById('nitrogen-reading').querySelector('.value').textContent = `${data.nitrogen} mg/kg`;
    document.getElementById('phosphorus-reading').querySelector('.value').textContent = `${data.phosphorus} mg/kg`;
    document.getElementById('potassium-reading').querySelector('.value').textContent = `${data.potassium} mg/kg`;
}

// Update charts with historical data
function updateCharts(historicalData) {
    // Update moisture chart
    charts.moisture.data.labels = historicalData.timestamps;
    charts.moisture.data.datasets[0].data = historicalData.moisture;
    charts.moisture.update();
    
    // Update nutrient chart
    charts.nutrient.data.datasets[0].data = [
        historicalData.nitrogen[historicalData.nitrogen.length - 1],
        historicalData.phosphorus[historicalData.phosphorus.length - 1],
        historicalData.potassium[historicalData.potassium.length - 1]
    ];
    charts.nutrient.update();
}

// Update recommendations
function updateRecommendations(recommendations) {
    // Crop recommendations
    const cropContainer = document.getElementById('crop-recommendations');
    cropContainer.innerHTML = '';
    
    recommendations.crops.forEach(crop => {
        const div = document.createElement('div');
        div.className = 'recommendation-item';
        div.innerHTML = `
            ${crop.crop} <span class="probability">${(crop.probability * 100).toFixed(1)}%</span>
        `;
        cropContainer.appendChild(div);
    });
    
    // Fertilizer recommendations
    const fertilizerContainer = document.getElementById('fertilizer-recommendations');
    fertilizerContainer.innerHTML = '';
    
    const div = document.createElement('div');
    div.className = 'recommendation-item';
    div.innerHTML = `
        ${recommendations.fertilizer.fertilizer} for ${recommendations.fertilizer.crop} 
        <span class="probability">${(recommendations.fertilizer.probability * 100).toFixed(1)}%</span>
    `;
    fertilizerContainer.appendChild(div);
}

// Update alerts
function updateAlerts(alerts) {
    const alertsContainer = document.getElementById('alerts-container');
    alertsContainer.innerHTML = '';
    
    if (alerts.length === 0) {
        alertsContainer.innerHTML = '<div class="alert low">No current alerts</div>';
        return;
    }
    
    alerts.forEach(alert => {
        const div = document.createElement('div');
        div.className = `alert ${alert.severity}`;
        div.innerHTML = `
            <span class="alert-icon">⚠️</span>
            <span>${alert.message}</span>
        `;
        alertsContainer.appendChild(div);
    });
}

// Update predictions
function updatePredictions(predictions) {
    // Yield prediction
    document.getElementById('yield-prediction').innerHTML = `
        <p>Estimated yield: <strong>${predictions.yield} kg/ha</strong></p>
        <p>For crop: ${predictions.crop}</p>
    `;
    
    // Risk assessment
    const risks = predictions.risks.map(risk => `
        <p>${risk.type}: ${risk.level} probability</p>
    `).join('');
    
    document.getElementById('risk-assessment').innerHTML = risks || '<p>No significant risks detected</p>';
}

// Update health score
function updateHealthScore(score) {
    const scoreElement = document.getElementById('health-score');
    scoreElement.textContent = `${score}`;
    
    const scoreCircle = document.querySelector('.score-circle');
    scoreCircle.style.setProperty('--score', `${score}%`);
    
    // Change color based on score
    if (score >= 80) {
        scoreCircle.style.background = `conic-gradient(#4caf50 0% ${score}%, #e0e0e0 ${score}% 100%)`;
    } else if (score >= 50) {
        scoreCircle.style.background = `conic-gradient(#ffc107 0% ${score}%, #e0e0e0 ${score}% 100%)`;
    } else {
        scoreCircle.style.background = `conic-gradient(#f44336 0% ${score}%, #e0e0e0 ${score}% 100%)`;
    }
}
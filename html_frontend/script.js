// Chart.js Configuration for Strategic Engine Dashboard

document.addEventListener("DOMContentLoaded", function() {
    
    // Bar Chart Initialization (Intelligence Extraction Yield)
    const ctxBar = document.getElementById('barChart');
    if (ctxBar) {
        new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: ['S', 'M', 'T', 'W', 'T', 'F', 'S'],
                datasets: [{
                    label: 'Analyzed',
                    data: [12, 19, 25, 29, 15, 14, 10],
                    backgroundColor: [
                        '#e2e8f0', // dashed/muted replacement
                        '#155e3e',
                        '#2dc479',
                        '#0d3826',
                        '#e2e8f0',
                        '#e2e8f0',
                        '#e2e8f0'
                    ],
                    borderRadius: 20,
                    borderSkipped: false,
                    barThickness: 30
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { display: false, drawBorder: false },
                        ticks: { color: '#94a3b8', font: { family: "'Plus Jakarta Sans', sans-serif" } }
                    },
                    y: {
                        display: false,
                        grid: { display: false, drawBorder: false }
                    }
                }
            }
        });
    }

    // Doughnut Chart Initialization (Action Resolution)
    const ctxDoughnut = document.getElementById('doughnutChart');
    if (ctxDoughnut) {
        new Chart(ctxDoughnut, {
            type: 'doughnut',
            data: {
                labels: ['Resolved', 'Active', 'Pending'],
                datasets: [{
                    data: [41, 35, 24],
                    backgroundColor: [
                        '#155e3e',
                        '#2dc479',
                        '#e2e8f0'
                    ],
                    borderWidth: 0,
                    cutout: '75%'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                rotation: -90,
                circumference: 180,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                }
            }
        });
    }

});

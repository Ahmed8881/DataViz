document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const themeToggle = document.getElementById('theme-toggle');
    const datasetInfoToggle = document.getElementById('dataset-info-toggle');
    const datasetInfoPanel = document.getElementById('dataset-info-panel');
    const closePanel = document.getElementById('close-panel');
    const libraryButtons = document.querySelectorAll('.library-btn');
    const visualizationContainer = document.getElementById('visualization-container');
    const loadingIndicator = document.getElementById('loading');
    const welcomeMessage = document.getElementById('welcome-message');

    // Toggle sidebar on mobile
    menuToggle.addEventListener('click', function() {
        sidebar.classList.toggle('active');
    });

    // Toggle theme
    themeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-theme');
        
        // Update icon based on theme
        if (document.body.classList.contains('dark-theme')) {
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }
        
        // Store theme preference
        const isDarkTheme = document.body.classList.contains('dark-theme');
        localStorage.setItem('darkTheme', isDarkTheme);
    });

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('darkTheme');
    if (savedTheme === 'true') {
        document.body.classList.add('dark-theme');
        themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
    }

    // Toggle dataset info panel
    datasetInfoToggle.addEventListener('click', function() {
        datasetInfoPanel.classList.add('active');
    });

    // Close dataset info panel
    closePanel.addEventListener('click', function() {
        datasetInfoPanel.classList.remove('active');
    });

    // Close panel when clicking outside
    document.addEventListener('click', function(e) {
        if (!datasetInfoPanel.contains(e.target) && 
            !datasetInfoToggle.contains(e.target) && 
            datasetInfoPanel.classList.contains('active')) {
            datasetInfoPanel.classList.remove('active');
        }
    });

    // Library buttons
    libraryButtons.forEach(button => {
        button.addEventListener('click', function() {
            libraryButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            const library = this.getAttribute('data-library');
            loadVisualizations(library);
        });
    });

    // Check localStorage for last selected library
    const lastSelectedLibrary = localStorage.getItem('selectedLibrary');
    if (lastSelectedLibrary) {
        const savedLibBtn = document.querySelector(`.library-btn[data-library="${lastSelectedLibrary}"]`);
        if (savedLibBtn) {
            libraryButtons.forEach(btn => btn.classList.remove('active'));
            savedLibBtn.classList.add('active');
            loadVisualizations(lastSelectedLibrary);
        }
    }

    function loadVisualizations(library) {
        // Store selected library
        localStorage.setItem('selectedLibrary', library);
        
        // Hide welcome message and show loading
        welcomeMessage.style.display = 'none';
        loadingIndicator.style.display = 'flex';
        visualizationContainer.innerHTML = '';
        
        // Send request to backend
        const formData = new FormData();
        formData.append('library', library);
        
        fetch('http://127.0.0.1:5000/get_visualizations', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            loadingIndicator.style.display = 'none';
            
            if (data.error) {
                showErrorMessage(data.error);
                return;
            }
            
            displayVisualizations(data);
        })
        .catch(error => {
            loadingIndicator.style.display = 'none';
            showErrorMessage('Failed to load visualizations. Please try again.');
            console.error('Error:', error);
        });
    }

    function showErrorMessage(message) {
        visualizationContainer.innerHTML = `
            <div class="error-card">
                <div class="error-icon">
                    <i class="fas fa-exclamation-triangle"></i>
                </div>
                <h3>Oops! Something went wrong</h3>
                <p>${message}</p>
                <button class="retry-btn">
                    <i class="fas fa-redo"></i> Try Again
                </button>
            </div>
        `;
        
        // Add event listener to retry button
        const retryBtn = visualizationContainer.querySelector('.retry-btn');
        if (retryBtn) {
            retryBtn.addEventListener('click', () => {
                const activeLibBtn = document.querySelector('.library-btn.active');
                if (activeLibBtn) {
                    loadVisualizations(activeLibBtn.getAttribute('data-library'));
                }
            });
        }
    }

    function displayVisualizations(data) {
        visualizationContainer.innerHTML = '';
        
        // Add library info at the top
        const libraryInfo = document.createElement('div');
        libraryInfo.className = 'library-info';
        libraryInfo.innerHTML = `
            <h2>${getLibraryDisplayName(data.library)} Visualizations</h2>
            <p>Exploring customer shopping trends with ${getLibraryDisplayName(data.library)}</p>
        `;
        visualizationContainer.appendChild(libraryInfo);
        
        if (data.library === 'plotly') {
            // Special handling for Plotly charts
            data.visualizations.forEach(viz => {
                const vizCard = document.createElement('div');
                vizCard.className = 'visualization-card';
                
                vizCard.innerHTML = `
                    <div class="card-header">
                        <h3 class="card-title">${viz.title}</h3>
                        <div class="card-actions">
                            <button class="card-action info-btn" title="Chart Info">
                                <i class="fas fa-info-circle"></i>
                            </button>
                            <button class="card-action fullscreen-btn" title="Fullscreen">
                                <i class="fas fa-expand"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <div id="plotly-${viz.title.replace(/\s+/g, '-').toLowerCase()}" class="visualization-plot"></div>
                    </div>
                    <div class="card-footer">
                        <button class="download-btn">
                            <i class="fas fa-download"></i> Download
                        </button>
                        <span class="chart-meta">${formatDate(new Date())}</span>
                    </div>
                `;
                
                visualizationContainer.appendChild(vizCard);
                
                // Handle Plotly chart rendering
                const plotElement = vizCard.querySelector(`#plotly-${viz.title.replace(/\s+/g, '-').toLowerCase()}`);
                const image = new Image();
                image.onload = function() {
                    const img = document.createElement('img');
                    img.src = viz.image;
                    img.className = 'visualization-image';
                    img.alt = viz.title;
                    plotElement.appendChild(img);
                };
                image.src = viz.image;
                
                // Add download event listener
                const downloadBtn = vizCard.querySelector('.download-btn');
                downloadBtn.addEventListener('click', () => downloadImage(viz.image, viz.title));
                
                // Fullscreen button functionality
                const fullscreenBtn = vizCard.querySelector('.fullscreen-btn');
                fullscreenBtn.addEventListener('click', () => {
                    toggleFullscreen(vizCard);
                });
                
                // Info button functionality
                const infoBtn = vizCard.querySelector('.info-btn');
                infoBtn.addEventListener('click', () => {
                    showChartInfo(viz.title);
                });
            });
        } else {
            // For other libraries (Matplotlib, Seaborn, Pandas)
            data.visualizations.forEach(viz => {
                const vizCard = document.createElement('div');
                vizCard.className = 'visualization-card';
                
                vizCard.innerHTML = `
                    <div class="card-header">
                        <h3 class="card-title">${viz.title}</h3>
                        <div class="card-actions">
                            <button class="card-action info-btn" title="Chart Info">
                                <i class="fas fa-info-circle"></i>
                            </button>
                            <button class="card-action fullscreen-btn" title="Fullscreen">
                                <i class="fas fa-expand"></i>
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <img src="${viz.image}" class="visualization-image" alt="${viz.title}">
                    </div>
                    <div class="card-footer">
                        <button class="download-btn">
                            <i class="fas fa-download"></i> Download
                        </button>
                        <span class="chart-meta">${formatDate(new Date())}</span>
                    </div>
                `;
                
                visualizationContainer.appendChild(vizCard);
                
                // Add download event listener
                const downloadBtn = vizCard.querySelector('.download-btn');
                downloadBtn.addEventListener('click', () => downloadImage(viz.image, viz.title));
                
                // Fullscreen button functionality
                const fullscreenBtn = vizCard.querySelector('.fullscreen-btn');
                fullscreenBtn.addEventListener('click', () => {
                    toggleFullscreen(vizCard);
                });
                
                // Info button functionality
                const infoBtn = vizCard.querySelector('.info-btn');
                infoBtn.addEventListener('click', () => {
                    showChartInfo(viz.title);
                });
            });
        }
        
        // Add animation for cards
        const cards = visualizationContainer.querySelectorAll('.visualization-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100 * index);
        });
    }
    
    function downloadImage(imageData, title) {
        const formData = new FormData();
        formData.append('image_data', imageData);
        formData.append('chart_title', title);
        
        fetch('/download_image', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            }
            throw new Error('Download failed');
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${title}.png`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            // Show download success notification
            showNotification('Chart downloaded successfully!', 'success');
        })
        .catch(error => {
            showNotification('Failed to download image', 'error');
            console.error('Error:', error);
        });
    }
    
    function toggleFullscreen(element) {
        if (!document.fullscreenElement) {
            if (element.requestFullscreen) {
                element.requestFullscreen();
            } else if (element.mozRequestFullScreen) { /* Firefox */
                element.mozRequestFullScreen();
            } else if (element.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
                element.webkitRequestFullscreen();
            } else if (element.msRequestFullscreen) { /* IE/Edge */
                element.msRequestFullscreen();
            }
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
            }
        }
    }
    
    function showChartInfo(chartTitle) {
        // Create modal for chart info
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <div class="modal-header">
                    <h3>${chartTitle} - Details</h3>
                    <button class="close-modal"><i class="fas fa-times"></i></button>
                </div>
                <div class="modal-body">
                    <div class="chart-info">
                        <h4>About this visualization</h4>
                        <p>This chart displays analysis of customer shopping trends data for ${chartTitle.toLowerCase()}.</p>
                        
                        <h4>Insights</h4>
                        <ul>
                            <li>Visualization created using advanced data analysis techniques</li>
                            <li>Data filtered to show the most relevant information</li>
                            <li>Patterns extracted from customer behavior metrics</li>
                        </ul>
                        
                        <h4>Data Processing</h4>
                        <p>Data was cleaned and preprocessed to ensure accuracy of results.</p>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Add event listener to close modal
        const closeModal = modal.querySelector('.close-modal');
        closeModal.addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        // Close modal when clicking outside
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                document.body.removeChild(modal);
            }
        });
        
        // Add animation
        setTimeout(() => {
            modal.style.opacity = '1';
            modal.querySelector('.modal-content').style.transform = 'translateY(0)';
        }, 10);
    }
    
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        
        let icon;
        switch(type) {
            case 'success':
                icon = 'fas fa-check-circle';
                break;
            case 'error':
                icon = 'fas fa-exclamation-circle';
                break;
            case 'warning':
                icon = 'fas fa-exclamation-triangle';
                break;
            default:
                icon = 'fas fa-info-circle';
        }
        
        notification.innerHTML = `
            <i class="${icon}"></i>
            <span>${message}</span>
        `;
        
        document.body.appendChild(notification);
        
        // Animation
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                document.body.removeChild(notification);
            }, 300);
        }, 3000);
    }
    
    function formatDate(date) {
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    }
    
    function getLibraryDisplayName(library) {
        switch(library) {
            case 'matplotlib':
                return 'Matplotlib';
            case 'seaborn':
                return 'Seaborn';
            case 'pandas':
                return 'Pandas';
            case 'plotly':
                return 'Plotly';
            default:
                return library.charAt(0).toUpperCase() + library.slice(1);
        }
    }
    
    // Add these styles for new components (modal and notification)
    const styleElement = document.createElement('style');
    styleElement.textContent = `
        /* Modal Styles */
        .modal {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 100;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .modal-content {
            background-color: var(--card-bg);
            border-radius: var(--border-radius-md);
            width: 90%;
            max-width: 600px;
            max-height: 90vh;
            overflow-y: auto;
            box-shadow: var(--shadow-md);
            transform: translateY(-20px);
            transition: transform 0.3s ease;
        }
        
        .modal-header {
            padding: 20px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .modal-header h3 {
            margin: 0;
            color: var(--primary-color);
        }
        
        .close-modal {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 1.2rem;
            cursor: pointer;
        }
        
        .close-modal:hover {
            color: var(--danger-color);
        }
        
        .modal-body {
            padding: 20px;
        }
        
        .chart-info h4 {
            color: var(--primary-color);
            margin: 20px 0 10px;
        }
        
        .chart-info p {
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        .chart-info ul {
            padding-left: 20px;
            margin-bottom: 15px;
        }
        
        .chart-info li {
            margin-bottom: 8px;
        }
        
        /* Notification Styles */
        .notification {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: var(--border-radius-md);
            background-color: var(--card-bg);
            box-shadow: var(--shadow-md);
            display: flex;
            align-items: center;
            transform: translateX(150%);
            transition: transform 0.3s ease;
            z-index: 90;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        .notification i {
            margin-right: 10px;
            font-size: 1.2rem;
        }
        
        .notification.info i {
            color: var(--info-color);
        }
        
        .notification.success i {
            color: var(--success-color);
        }
        
        .notification.warning i {
            color: var(--warning-color);
        }
        
        .notification.error i {
            color: var(--danger-color);
        }
        
        /* Error Card Styles */
        .error-card {
            background-color: var(--card-bg);
            border-radius: var(--border-radius-md);
            padding: 30px;
            text-align: center;
            box-shadow: var(--shadow-sm);
            max-width: 500px;
            margin: 0 auto;
        }
        
        .error-icon {
            font-size: 3rem;
            color: var(--danger-color);
            margin-bottom: 20px;
        }
        
        .error-card h3 {
            color: var(--text-primary);
            margin-bottom: 15px;
        }
        
        .error-card p {
            color: var(--text-secondary);
            margin-bottom: 25px;
        }
        
        .retry-btn {
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: var(--border-radius-sm);
            cursor: pointer;
            display: inline-flex;
            align-items: center;
        }
        
        .retry-btn i {
            margin-right: 8px;
        }
        
        .retry-btn:hover {
            background-color: var(--secondary-color);
        }
        
        /* Animation for visualization cards */
        .visualization-card {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.3s ease, transform 0.3s ease;
        }
        
        /* Library info section */
        .library-info {
            margin-bottom: 30px;
            grid-column: 1 / -1;
        }
        
        .library-info h2 {
            color: var(--primary-color);
            font-size: 1.8rem;
            margin-bottom: 10px;
        }
        
        .library-info p {
            color: var(--text-secondary);
        }
    `;
    
    document.head.appendChild(styleElement);
});
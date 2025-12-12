// ===================================
// Yanii - Chinese Learning App
// Main JavaScript File
// ===================================

// ===================================
// UTILITY FUNCTIONS
// ===================================

// Debounce function to limit execution rate
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function for high-frequency events
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ===================================
// GLOBAL VARIABLES
// ===================================

// Global Variables
let currentData = [];
let allScriptData = []; // All data for current script type (all levels combined)
let loadedLevels = {}; // Cache for loaded levels {scriptType_level: data}
let currentPage = 1;
let itemsPerPage = 12;
let gameMode = null;
let gameData = [];
let currentQuestion = 0;
let score = 0;
let correctAnswers = 0;
let wrongAnswers = 0;
let currentAnswer = null;
let wrongAttempts = 0;
let searchCache = {};
let lastSearchTerm = '';
let lastFocusedElement = null; // For focus restoration

// LRU Cache for translations with max size
const MAX_CACHE_SIZE = 100;
class LRUCache {
    constructor(maxSize) {
        this.maxSize = maxSize;
        this.cache = new Map();
    }
    
    get(key) {
        if (!this.cache.has(key)) return undefined;
        const value = this.cache.get(key);
        this.cache.delete(key);
        this.cache.set(key, value);
        return value;
    }
    
    set(key, value) {
        if (this.cache.has(key)) {
            this.cache.delete(key);
        } else if (this.cache.size >= this.maxSize) {
            const firstKey = this.cache.keys().next().value;
            this.cache.delete(firstKey);
        }
        this.cache.set(key, value);
    }
    
    clear() {
        this.cache.clear();
    }
}

let translatorCache = new LRUCache(MAX_CACHE_SIZE);
let eventCleanupHandlers = []; // Track event listeners for cleanup
let translatorInitialized = false; // Flag to prevent duplicate initialization

// Data paths
const dataPaths = {
    simplified: {
        hsk1: 'data/simplified/hsk1.json',
        hsk2: 'data/simplified/hsk2.json',
        hsk3: 'data/simplified/hsk3.json',
        hsk4: 'data/simplified/hsk4.json',
        hsk5: 'data/simplified/hsk5.json',
        hsk6: 'data/simplified/hsk6.json'
    },
    traditional: {
        tocfl_a1: 'data/traditional/tocfl_a1.json',
        tocfl_a2: 'data/traditional/tocfl_a2.json',
        tocfl_b1: 'data/traditional/tocfl_b1.json',
        tocfl_b2: 'data/traditional/tocfl_b2.json',
        tocfl_c1: 'data/traditional/tocfl_c1.json',
        tocfl_c2: 'data/traditional/tocfl_c2.json'
    }
};

// Reading data paths
const readingDataPaths = {
    simplified: {
        hsk1: 'data/simplified/reading_hsk1.json',
        hsk2: 'data/simplified/reading_hsk2.json',
        hsk3: 'data/simplified/reading_hsk3.json',
        hsk4: 'data/simplified/reading_hsk4.json',
        hsk5: 'data/simplified/reading_hsk5.json',
        hsk6: 'data/simplified/reading_hsk6.json'
    },
    traditional: {
        tocfl_a1: 'data/traditional/reading_tocfl_a1.json',
        tocfl_a2: 'data/traditional/reading_tocfl_a2.json',
        tocfl_b1: 'data/traditional/reading_tocfl_b1.json',
        tocfl_b2: 'data/traditional/reading_tocfl_b2.json',
        tocfl_c1: 'data/traditional/reading_tocfl_c1.json',
        tocfl_c2: 'data/traditional/reading_tocfl_c2.json'
    }
};

// ===================================
// INITIALIZATION
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
        // Kết nối chọn khóa học và loại sách để mở PDF
        document.addEventListener('DOMContentLoaded', function() {
            let selectedCourse = null;
            let selectedType = null;
            // Lưu lại khi chọn khóa học
            document.querySelectorAll('.course-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    selectedCourse = btn.getAttribute('data-course');
                });
            });
            // Khi chọn loại sách
            document.querySelectorAll('.book-type-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    selectedType = btn.getAttribute('data-type');
                    let pdfFile = '';
                    if (selectedCourse && selectedType && selectedCourse.startsWith('td')) {
                            let courseNum = selectedCourse.replace(/[^0-9]/g, '');
                            let basePath = `data/traditional/${selectedCourse}`;
                            if (selectedType === 'giaokhoa') {
                                pdfFile = `${basePath}/sgk${courseNum}.pdf`;
                            } else {
                                pdfFile = `${basePath}/sbt${courseNum}.pdf`;
                            }
                        if (typeof openPdfModal === 'function') {
                            // Đảm bảo truyền vào pdf.js đường dẫn tuyệt đối    
                            // Đảm bảo truyền vào pdf.js đường dẫn tuyệt đối bắt đầu bằng www/
                            let absolutePdfFile = pdfFile;
                            if (!pdfFile.startsWith('www/')) {
                                absolutePdfFile = 'www/' + pdfFile.replace(/^\/*/, '');
                            }
                            openPdfModal(absolutePdfFile);
                        } else {
                            alert('Không tìm thấy hàm mở PDF!');
                        }
                    }
                });
            });
        });
});

function initializeApp() {
    // Hide preloader after content is loaded and show UI
    setTimeout(() => {
        const preloader = document.getElementById('preloader');
        if (preloader) preloader.classList.add('hidden');
        // Remove global preloading state so UI appears
        document.body.classList.remove('preloading');
    }, 1500);

    // Setup navigation
    setupNavigation();
    setupOffcanvasNavEffects();
    
    // Setup scroll to top button
    setupScrollToTop();
    
    // Setup dictionary
    setupDictionary();
    
    // Initialize level options
    updateLevelOptions();
    updateGameLevelOptions();
    
    // Setup event listeners
    setupEventListeners();
    
    // Setup keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Initialize reading game level options
    updateReadingLevelOptions();
    
    // Initialize translator
    initTranslator();
    
    // Don't load dictionary data immediately - lazy load when user opens Dictionary tab
}

// ===================================
// NAVIGATION
// ===================================

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Get section to show
            const sectionId = this.getAttribute('data-section');
            navigateToSection(sectionId);
        });
    });
}

// Setup blur and behavior for offcanvas navbar (mobile/tablet)
function setupOffcanvasNavEffects() {
    const offcanvasEl = document.getElementById('mobileNav');
    if (!offcanvasEl) return;

    // Toggle body class for blur when offcanvas open/close
    offcanvasEl.addEventListener('shown.bs.offcanvas', function () {
        document.body.classList.add('nav-open');
    });
    offcanvasEl.addEventListener('hidden.bs.offcanvas', function () {
        document.body.classList.remove('nav-open');
    });

    // Close offcanvas when clicking a nav link inside it
    const offcanvasLinks = offcanvasEl.querySelectorAll('.nav-link');
    offcanvasLinks.forEach(link => {
        link.addEventListener('click', () => {
            try {
                const offcanvas = bootstrap.Offcanvas.getOrCreateInstance(offcanvasEl);
                offcanvas.hide();
            } catch (e) {
                // Bootstrap might not be available; fail silently
            }
        });
    });
}

function navigateToSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section-container');
    sections.forEach(section => section.classList.remove('active'));
    
    // Close game areas when navigating away from games section
    if (sectionId !== 'games') {
        const gameArea = document.getElementById('gameArea');
        const readingGameArea = document.getElementById('readingGameArea');
        
        if (gameArea && gameArea.style.display === 'block') {
            gameArea.style.display = 'none';
            gameMode = null;
        }
        
        if (readingGameArea && readingGameArea.style.display === 'block') {
            readingGameArea.style.display = 'none';
            // Reset display and page
            currentReadingPage = 1;
            const topicsList = document.getElementById('topicsList');
            const dialogDisplay = document.getElementById('dialogDisplay');
            if (topicsList) topicsList.style.display = 'grid';
            if (dialogDisplay) dialogDisplay.style.display = 'none';
        }
    } else {
        // When navigating TO games section, ensure title and game modes are visible
        const gameTitle = document.querySelector('#games .section-header');
        const gameModes = document.querySelector('#games .row.g-4.mb-5');
        const gameArea = document.getElementById('gameArea');
        const readingGameArea = document.getElementById('readingGameArea');
        
        // Hide game areas if they're open
        if (gameArea && gameArea.style.display === 'block') {
            gameArea.style.display = 'none';
            gameMode = null;
        }
        
        if (readingGameArea && readingGameArea.style.display === 'block') {
            readingGameArea.style.display = 'none';
            currentReadingPage = 1;
            const topicsList = document.getElementById('topicsList');
            const dialogDisplay = document.getElementById('dialogDisplay');
            if (topicsList) topicsList.style.display = 'grid';
            if (dialogDisplay) dialogDisplay.style.display = 'none';
        }
        
        // Reset and show title and game modes with proper styles
        if (gameTitle) {
            gameTitle.style.display = 'block';
            gameTitle.style.opacity = '1';
            gameTitle.style.transform = 'translateY(0)';
        }
        
        if (gameModes) {
            gameModes.style.display = 'flex';
            gameModes.style.opacity = '1';
            gameModes.style.transform = 'translateY(0)';
        }
    }
    
    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        
        // Lazy load dictionary data when user opens Dictionary section
        if (sectionId === 'dictionary' && currentData.length === 0) {
            loadDictionaryData();
        }
        
        // Focus management for better UX
        setTimeout(() => {
            if (sectionId === 'dictionary') {
                const searchInput = document.getElementById('searchInput');
                if (searchInput) searchInput.focus();
            }
        }, 100);
        
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Update nav links
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        if (link.getAttribute('data-section') === sectionId) {
            link.classList.add('active');
        } else {
            link.classList.remove('active');
        }
    });
}

// ===================================
// KEYBOARD SHORTCUTS
// ===================================

function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // ESC - Close modals and popups
        if (e.key === 'Escape') {
            // Close word modal
            const wordModal = document.getElementById('wordModal');
            if (wordModal && wordModal.style.display === 'flex') {
                closeWordModal();
                return;
            }
            
            // Close translator if open
            const translatorPopup = document.getElementById('translatorPopup');
            if (translatorPopup && !translatorPopup.classList.contains('collapsed')) {
                toggleTranslator();
                return;
            }
        }
        
        // / (slash) - Focus search (like GitHub)
        if (e.key === '/' && !isInputFocused()) {
            e.preventDefault();
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                navigateToSection('dictionary');
                setTimeout(() => searchInput.focus(), 150);
            }
            return;
        }
        
        // Ctrl/Cmd + K - Focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.getElementById('searchInput');
            if (searchInput) {
                navigateToSection('dictionary');
                setTimeout(() => searchInput.focus(), 150);
            }
            return;
        }
        
        // Ctrl/Cmd + 1,2,3,4 - Navigate tabs
        if ((e.ctrlKey || e.metaKey) && ['1','2','3','4'].includes(e.key)) {
            e.preventDefault();
            const sections = ['home', 'dictionary', 'games', 'about'];
            const index = parseInt(e.key) - 1;
            if (sections[index]) {
                navigateToSection(sections[index]);
            }
            return;
        }
        
        // Arrow keys for pagination (when not in input)
        if (!isInputFocused()) {
            if (e.key === 'ArrowLeft') {
                const prevBtn = document.querySelector('.page-btn[onclick*="currentPage--"]');
                if (prevBtn && !prevBtn.disabled) {
                    prevBtn.click();
                }
            } else if (e.key === 'ArrowRight') {
                const nextBtn = document.querySelector('.page-btn[onclick*="currentPage++"]');
                if (nextBtn && !nextBtn.disabled) {
                    nextBtn.click();
                }
            }
        }
    });
}

function isInputFocused() {
    const activeElement = document.activeElement;
    return activeElement && (
        activeElement.tagName === 'INPUT' ||
        activeElement.tagName === 'TEXTAREA' ||
        activeElement.isContentEditable
    );
}

// Cleanup function to prevent memory leaks
function cleanupEventListeners() {
    eventCleanupHandlers.forEach(cleanup => {
        if (typeof cleanup === 'function') {
            cleanup();
        }
    });
    eventCleanupHandlers = [];
}

// ===================================
// SCROLL TO TOP
// ===================================

function setupScrollToTop() {
    const scrollBtn = document.getElementById('scrollToTop');
    
    // Debounced scroll handler for better performance
    const handleScroll = debounce(function() {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('visible');
        } else {
            scrollBtn.classList.remove('visible');
        }
    }, 100);
    
    window.addEventListener('scroll', handleScroll, { passive: true });
    
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ===================================
// DICTIONARY
// ===================================

function showSkeletonLoading(container, type = 'cards') {
    const resultsContainer = document.getElementById(container);
    
    if (type === 'cards') {
        resultsContainer.innerHTML = `
            <div class="skeleton-grid" style="grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; width: 100%;">
                ${Array(12).fill(0).map(() => `
                    <div class="skeleton-card">
                        <div class="skeleton skeleton-header"></div>
                        <div class="skeleton skeleton-text short"></div>
                        <div class="skeleton skeleton-text shorter"></div>
                    </div>
                `).join('')}
            </div>
        `;
    } else if (type === 'list') {
        resultsContainer.innerHTML = `
            ${Array(6).fill(0).map(() => `
                <div class="skeleton-card">
                    <div class="skeleton skeleton-text"></div>
                    <div class="skeleton skeleton-text short"></div>
                </div>
            `).join('')}
        `;
    }
}

function setupDictionary() {
    const scriptType = document.getElementById('scriptType');
    const levelSelect = document.getElementById('levelSelect');
    
    scriptType.addEventListener('change', function() {
        updateLevelOptions();
        updateSearchPlaceholder();
        loadDictionaryData();
    });
    
    levelSelect.addEventListener('change', function() {
        loadDictionaryData();
    });
    
    // Set initial placeholder
    updateSearchPlaceholder();
}

function updateLevelOptions() {
    const scriptType = document.getElementById('scriptType').value;
    const levelSelect = document.getElementById('levelSelect');
    
    levelSelect.innerHTML = '';
    
    if (scriptType === 'simplified') {
        levelSelect.innerHTML = `
            <option value="hsk1">HSK 1</option>
            <option value="hsk2">HSK 2</option>
            <option value="hsk3">HSK 3</option>
            <option value="hsk4">HSK 4</option>
            <option value="hsk5">HSK 5</option>
            <option value="hsk6">HSK 6</option>
        `;
    } else {
        levelSelect.innerHTML = `
            <option value="tocfl_a1">TOCFL A1</option>
            <option value="tocfl_a2">TOCFL A2</option>
            <option value="tocfl_b1">TOCFL B1</option>
            <option value="tocfl_b2">TOCFL B2</option>
            <option value="tocfl_c1">TOCFL C1</option>
            <option value="tocfl_c2">TOCFL C2</option>
        `;
    }
}

async function loadDictionaryData() {
    const scriptType = document.getElementById('scriptType').value;
    const level = document.getElementById('levelSelect').value;
    
    // Show skeleton loading
    showSkeletonLoading('dictionaryResults', 'cards');
    
    // Bắt đầu đếm thời gian loading
    const loadStartTime = Date.now();
    
    try {
        // Only load current level initially (performance optimization)
        const levelKey = `${scriptType}_${level}`;
        const levelPaths = dataPaths[scriptType];
        const currentLevelPath = levelPaths[level];
        
        // Check cache first
        if (!loadedLevels[levelKey]) {
            const response = await fetch(currentLevelPath);
            const data = await response.json();
            loadedLevels[levelKey] = data.entries || [];
        }
        
        currentData = loadedLevels[levelKey];
        
        // For search across all levels, we'll load on-demand
        allScriptData = currentData;
        
        currentPage = 1;
        
        // Đảm bảo skeleton loading hiển thị ít nhất 1 giây để tránh giật
        const loadTime = Date.now() - loadStartTime;
        const minLoadTime = 1000; // 1 giây
        
        if (loadTime < minLoadTime) {
            await new Promise(resolve => setTimeout(resolve, minLoadTime - loadTime));
        }
        
        displayDictionary();
    } catch (error) {
        console.error('Error loading dictionary data:', error);
        
        // Đảm bảo hiển thị lỗi sau 1 giây
        const loadTime = Date.now() - loadStartTime;
        const minLoadTime = 1000;
        
        if (loadTime < minLoadTime) {
            await new Promise(resolve => setTimeout(resolve, minLoadTime - loadTime));
        }
        
        document.getElementById('dictionaryResults').innerHTML = `
            <div class="col-12">
                <div class="glass-card p-4 text-center">
                    <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: var(--warning-color);"></i>
                    <h3 class="mt-3">Không thể tải dữ liệu</h3>
                    <p class="text-secondary">Vui lòng kiểm tra lại đường dẫn file JSON.</p>
                </div>
            </div>
        `;
    }
}

// Load all levels for search (on-demand)
async function loadAllLevelsForSearch(scriptType) {
    const levelPaths = dataPaths[scriptType];
    const promises = [];
    
    for (const [level, path] of Object.entries(levelPaths)) {
        const levelKey = `${scriptType}_${level}`;
        if (!loadedLevels[levelKey]) {
            promises.push(
                fetch(path)
                    .then(res => res.json())
                    .then(data => {
                        loadedLevels[levelKey] = data.entries || [];
                    })
            );
        }
    }
    
    if (promises.length > 0) {
        await Promise.all(promises);
    }
    
    // Combine all loaded levels
    allScriptData = Object.keys(loadedLevels)
        .filter(key => key.startsWith(scriptType))
        .flatMap(key => loadedLevels[key]);
}

async function displayDictionary() {
    const searchTerm = document.getElementById('searchInput').value.trim();
    const normalizedSearch = normalizeText(searchTerm);
    
    // Filter data based on search with normalized text
    // If searching, search ALL levels; otherwise show current level only
    let filteredData;
    if (searchTerm) {
        // Load all levels on first search (lazy load optimization)
        const scriptType = document.getElementById('scriptType').value;
        if (allScriptData.length === currentData.length) {
            showSkeletonLoading('dictionaryResults', 'cards');
            await loadAllLevelsForSearch(scriptType);
        }
        
        // Search across ALL levels of current script type
        filteredData = allScriptData.filter(entry => {
            const normalizedHanzi = normalizeText(entry.hanzi);
            const normalizedPinyin = normalizeText(entry.pinyin);
            const normalizedMeaning = normalizeText(entry.meaning_vi);
            
            return normalizedHanzi.includes(normalizedSearch) ||
                   normalizedPinyin.includes(normalizedSearch) ||
                   normalizedMeaning.includes(normalizedSearch) ||
                   entry.hanzi.toLowerCase().includes(searchTerm.toLowerCase()) ||
                   entry.pinyin.toLowerCase().includes(searchTerm.toLowerCase()) ||
                   entry.meaning_vi.toLowerCase().includes(searchTerm.toLowerCase());
        });
    } else {
        // No search, show current level only
        filteredData = currentData;
    }
    
    // Calculate pagination
    const startIndex = (currentPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedData = filteredData.slice(startIndex, endIndex);
    
    // Display results
    const resultsContainer = document.getElementById('dictionaryResults');
    
    if (paginatedData.length === 0) {
        resultsContainer.innerHTML = `
            <div class="col-12">
                <div class="glass-card p-4 text-center">
                    <i class="fas fa-search" style="font-size: 3rem; color: var(--text-secondary);"></i>
                    <h3 class="mt-3">Không tìm thấy kết quả</h3>
                    <p class="text-secondary">${searchTerm ? 'Thử tìm kiếm với từ khóa khác.' : 'Nhập từ khóa để tìm kiếm.'}</p>
                </div>
            </div>
        `;
        document.getElementById('pagination').innerHTML = '';
        return;
    }
    
    // Display with highlighting (pagination = lightweight virtual scrolling)
    // Only render 24 items per page instead of all results for better performance
    resultsContainer.innerHTML = paginatedData.map((entry, index) => `
        <div class="col-lg-3 col-md-4 col-sm-6">
            <div class="word-card animate-word-card" style="animation-delay: ${index * 0.05}s" onclick='showWordDetail(${JSON.stringify(entry).replace(/'/g, "&apos;")})'>
                <div class="word-hanzi">${highlightText(entry.hanzi, searchTerm)}</div>
                <div class="word-pinyin">${highlightText(entry.pinyin, searchTerm)}</div>
                <div class="word-meaning">${highlightText(entry.meaning_vi, searchTerm)}</div>
                <span class="word-level">${entry.level}</span>
            </div>
        </div>
    `).join('');
    
    // Update result count
    if (searchTerm) {
        const countText = `<small class="text-secondary">Tìm thấy ${filteredData.length} kết quả cho "${searchTerm}"</small>`;
        if (!document.querySelector('.search-result-count')) {
            const countDiv = document.createElement('div');
            countDiv.className = 'search-result-count text-center mb-3';
            countDiv.innerHTML = countText;
            resultsContainer.parentElement.insertBefore(countDiv, resultsContainer);
        } else {
            document.querySelector('.search-result-count').innerHTML = countText;
        }
    } else {
        const countEl = document.querySelector('.search-result-count');
        if (countEl) countEl.remove();
    }
    
    // Display pagination
    displayPagination(filteredData.length);
}

function displayPagination(totalItems) {
    const totalPages = Math.ceil(totalItems / itemsPerPage);
    const paginationContainer = document.getElementById('pagination');
    
    if (totalPages <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }
    
    let paginationHTML = '';
    
    // Previous button
    paginationHTML += `
        <button class="page-btn" onclick="changePage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>
            <i class="fas fa-chevron-left"></i>
        </button>
    `;
    
    // Page numbers
    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - 1 && i <= currentPage + 1)) {
            paginationHTML += `
                <button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="changePage(${i})">
                    ${i}
                </button>
            `;
        } else if (i === currentPage - 2 || i === currentPage + 2) {
            paginationHTML += '<span class="page-btn" disabled>...</span>';
        }
    }
    
    // Next button
    paginationHTML += `
        <button class="page-btn" onclick="changePage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>
            <i class="fas fa-chevron-right"></i>
        </button>
    `;
    
    paginationContainer.innerHTML = paginationHTML;
}

function changePage(page) {
    currentPage = page;
    displayDictionary();
    window.scrollTo({ top: 400, behavior: 'smooth' });
}

// ===================================
// SEARCH
// ===================================

function setupEventListeners() {
    const searchInput = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearSearch');
    const searchLoading = document.querySelector('.search-loading');
    let searchTimeout;
    
    // Input event with optimized debounce
    searchInput.addEventListener('input', function() {
        const value = this.value;
        
        // Show/hide clear button
        if (clearBtn) {
            clearBtn.style.display = value ? 'flex' : 'none';
        }
        
        // Show loading indicator
        if (searchLoading) {
            searchLoading.style.display = 'flex';
        }
        
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(async () => {
            currentPage = 1;
            await displayDictionary();
            
            // Hide loading
            if (searchLoading) {
                searchLoading.style.display = 'none';
            }
        }, 250);
    });
    
    // Enter key support
    searchInput.addEventListener('keypress', async function(e) {
        if (e.key === 'Enter') {
            clearTimeout(searchTimeout);
            currentPage = 1;
            await displayDictionary();
            if (searchLoading) {
                searchLoading.style.display = 'none';
            }
        }
    });
    
    // Clear button
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            searchInput.value = '';
            this.style.display = 'none';
            currentPage = 1;
            displayDictionary();
            searchInput.focus();
        });
    }

    // Apply game settings button: reinitialize game with current selections
    const applyBtn = document.getElementById('applyGameSettings');
    if (applyBtn) {
        applyBtn.addEventListener('click', function() {
            if (!gameMode) {
                alert('Hãy chọn chế độ chơi trước (Chữ Hán → Nghĩa hoặc Nghĩa → Chữ Hán).');
                return;
            }
            // If game area is hidden (user changed settings before starting), show it
            const gameArea = document.getElementById('gameArea');
            if (gameArea && gameArea.style.display !== 'block') {
                gameArea.style.display = 'block';
            }
            initializeGame();
        });
    }
}

// ===================================
// GAME
// ===================================

function startGame(mode) {
    gameMode = mode;
    
    // Hide reading game area
    const readingGameArea = document.getElementById('readingGameArea');
    if (readingGameArea) {
        readingGameArea.style.display = 'none';
    }
    
    // Get elements
    const gameTitle = document.querySelector('#games .section-header');
    const gameModes = document.querySelector('#games .row.g-4.mb-5');
    const gameArea = document.getElementById('gameArea');
    
    // Add fade out animation to title and game modes
    if (gameTitle) {
        gameTitle.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        gameTitle.style.opacity = '0';
        gameTitle.style.transform = 'translateY(-20px)';
    }
    
    if (gameModes) {
        gameModes.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        gameModes.style.opacity = '0';
        gameModes.style.transform = 'translateY(-20px)';
    }
    
    // After fade out completes, hide them and show game area
    setTimeout(() => {
        if (gameTitle) gameTitle.style.display = 'none';
        if (gameModes) gameModes.style.display = 'none';
        
        // Show game area with fade in animation
        gameArea.style.display = 'block';
        gameArea.style.opacity = '0';
        gameArea.style.transform = 'translateY(20px)';
        gameArea.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        document.getElementById('gameResults').style.display = 'none';
        
        // Trigger fade in
        setTimeout(() => {
            gameArea.style.opacity = '1';
            gameArea.style.transform = 'translateY(0)';
            
            // Initialize game without scrolling
            setTimeout(() => {
                initializeGame();
            }, 100);
        }, 50);
    }, 400);
}

async function initializeGame() {
    const scriptType = document.getElementById('gameScriptType').value;
    const level = document.getElementById('gameLevelSelect').value;
    const questionCount = parseInt(document.getElementById('questionCount').value);
    
    const dataPath = dataPaths[scriptType][level];
    
    try {
        // Button preload UX
        const applyBtn = document.getElementById('applyGameSettings');
        const card = document.querySelector('.question-card');
        const answerInputEl = document.getElementById('answerInput');
        const submitBtnEl = document.getElementById('submitBtn');
        const giveUpBtnEl = document.getElementById('giveUpBtn');
        const nextBtnEl = document.getElementById('nextBtn');

        if (applyBtn) {
            applyBtn.disabled = true;
            if (!applyBtn.dataset.originalText) {
                applyBtn.dataset.originalText = applyBtn.innerHTML;
            }
            applyBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang cập nhật';
        }

        // Start preload overlay (do NOT hide content)
        const preloadStart = performance.now();
        if (card) {
            ensureQuestionPreloadOverlay(card);
            setQuestionPreloadVisible(card, true);
            // keep inputs enabled so user sees content with wave effect
        }
        const response = await fetch(dataPath);
        const data = await response.json();
        const availableEntries = data.entries || [];
        
        // Lấy số câu thực tế (không vượt quá số câu có sẵn)
        const actualCount = Math.min(questionCount, availableEntries.length);
        // Xáo trộn ngẫu nhiên trước khi cắt theo số lượng
        gameData = shuffleArray(availableEntries).slice(0, actualCount);
        
        // Reset game state
        currentQuestion = 0;
        score = 0;
        correctAnswers = 0;
        wrongAnswers = 0;
        wrongAttempts = 0;
        
        // Update total questions display với số câu thực tế
        document.getElementById('totalQuestions').textContent = actualCount;
        
        // Update UI
        updateGameUI();

        // Ensure at least 1s preload
        const elapsed = performance.now() - preloadStart;
        const waitMs = Math.max(0, 1000 - elapsed);
        await new Promise(res => setTimeout(res, waitMs));

        showQuestion();

        // Remove overlay; keep content visible throughout
        if (card) {
            setQuestionPreloadVisible(card, false);
        }

        if (applyBtn) {
            applyBtn.disabled = false;
            applyBtn.innerHTML = applyBtn.dataset.originalText || '<i class="fas fa-sync"></i> Cập nhật';
        }
    } catch (error) {
        console.error('Error loading game data:', error);
        alert('Không thể tải dữ liệu game. Vui lòng thử lại.');
        const applyBtn = document.getElementById('applyGameSettings');
        if (applyBtn) {
            applyBtn.disabled = false;
            applyBtn.innerHTML = applyBtn.dataset.originalText || '<i class="fas fa-sync"></i> Cập nhật';
        }
    }
}

function showQuestion() {
    if (currentQuestion >= gameData.length) {
        showResults();
        return;
    }
    
    const question = gameData[currentQuestion];
    currentAnswer = question;
    wrongAttempts = 0;
    
    // Update question number
    document.getElementById('questionNumber').textContent = currentQuestion + 1;
    
    // Display question based on game mode
    if (gameMode === 'hanzi-to-meaning') {
        document.getElementById('questionText').textContent = question.hanzi;
        document.getElementById('pinyinHint').textContent = question.pinyin;
        document.getElementById('answerInput').placeholder = 'Nhập nghĩa tiếng Việt...';
    } else {
        document.getElementById('questionText').textContent = question.meaning_vi;
        document.getElementById('pinyinHint').textContent = '';
        document.getElementById('answerInput').placeholder = 'Nhập chữ Hán...';
    }
    
    // Clear input and feedback
    document.getElementById('answerInput').value = '';
    const feedbackElement = document.getElementById('feedbackMessage');
    feedbackElement.innerHTML = '';
    feedbackElement.className = 'feedback-message'; // Remove correct/wrong classes
    document.getElementById('answerInput').focus();
    
    // Reset button visibility
    document.getElementById('submitBtn').style.display = 'inline-block';
    document.getElementById('giveUpBtn').style.display = 'inline-block';
    document.getElementById('nextBtn').style.display = 'none';
    document.getElementById('answerInput').disabled = false;
}

// Helpers for question preload overlay
function ensureQuestionPreloadOverlay(card) {
    let overlay = card.querySelector('.question-preload-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'question-preload-overlay';
        card.appendChild(overlay);
    }
}

function setQuestionPreloadVisible(card, visible) {
    const overlay = card.querySelector('.question-preload-overlay');
    if (overlay) {
        overlay.style.display = visible ? 'block' : 'none';
    }
}

function submitAnswer() {
    const userAnswer = document.getElementById('answerInput').value.trim().toLowerCase();
    
    if (!userAnswer) {
        showFeedback('Vui lòng nhập câu trả lời!', 'wrong');
        return;
    }
    
    let isCorrect = false;
    
    if (gameMode === 'hanzi-to-meaning') {
        isCorrect = userAnswer === currentAnswer.meaning_vi.toLowerCase();
    } else {
        isCorrect = userAnswer === currentAnswer.hanzi.toLowerCase();
    }
    
    if (isCorrect) {
        correctAnswers++;
        // Điểm tính theo trung bình trên tổng số câu: hiển thị phần trăm
        // Cập nhật điểm tức thời = (số câu đúng / tổng số câu) * 100, làm tròn
        const total = parseInt(document.getElementById('totalQuestions').textContent) || gameData.length;
        score = Math.round((correctAnswers / total) * 100);
        showFeedback(`
            <i class="fas fa-check-circle"></i> Chính xác! 
            <br>
            <small>${currentAnswer.hanzi} (${currentAnswer.pinyin}) = ${currentAnswer.meaning_vi}</small>
        `, 'correct');
        
        updateGameUI();
        
        // Show next button instead of auto-advancing
        showNextButton();
    } else {
        wrongAnswers++;
        wrongAttempts++;
        
        // Nếu sai quá 5 lần, hiển thị đáp án và hiện nút tiếp theo
        if (wrongAttempts >= 5) {
            const correctAnswer = gameMode === 'hanzi-to-meaning' ? currentAnswer.meaning_vi : currentAnswer.hanzi;
            showFeedback(`
                <i class="fas fa-exclamation-triangle"></i> Đã sai 5 lần! Đáp án đúng là: <strong>${correctAnswer}</strong>
                <br>
                <small>${currentAnswer.hanzi} (${currentAnswer.pinyin}) = ${currentAnswer.meaning_vi}</small>
            `, 'wrong');
            
            updateGameUI();
            
            // Show next button instead of auto-advancing
            showNextButton();
        } else {
            const correctAnswer = gameMode === 'hanzi-to-meaning' ? currentAnswer.meaning_vi : currentAnswer.hanzi;
            showFeedback(`
                <i class="fas fa-times-circle"></i> Sai rồi! Thử lại nhé! (Lần ${wrongAttempts}/5)
            `, 'wrong');
            
            updateGameUI();
            
            // Clear input for retry
            document.getElementById('answerInput').value = '';
            document.getElementById('answerInput').focus();
        }
    }
}

function showFeedback(message, type) {
    const feedbackElement = document.getElementById('feedbackMessage');
    feedbackElement.innerHTML = message;
    feedbackElement.className = `feedback-message ${type}`;
}

function updateGameUI() {
    // Hiển thị điểm dạng phần trăm
    document.getElementById('gameScore').textContent = score;
    document.getElementById('correctCount').textContent = correctAnswers;
    document.getElementById('wrongCount').textContent = wrongAnswers;
}

function showResults() {
    document.getElementById('gameResults').style.display = 'flex';
    // Điểm cuối cùng là trung bình phần trăm đúng trên tổng số câu
    document.getElementById('finalScore').textContent = score;
    document.getElementById('finalCorrect').textContent = correctAnswers;
    document.getElementById('finalWrong').textContent = wrongAnswers;
}

function restartGame() {
    document.getElementById('gameResults').style.display = 'none';
    initializeGame();
}

function exitGame() {
    const gameArea = document.getElementById('gameArea');
    const gameTitle = document.querySelector('#games .section-header');
    const gameModes = document.querySelector('#games .row.g-4.mb-5');
    
    // Fade out game area
    gameArea.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    gameArea.style.opacity = '0';
    gameArea.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        gameArea.style.display = 'none';
        gameMode = null;
        
        // Show and fade in title and game modes
        if (gameTitle) {
            gameTitle.style.display = 'block';
            gameTitle.style.opacity = '0';
            gameTitle.style.transform = 'translateY(-20px)';
            gameTitle.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                gameTitle.style.opacity = '1';
                gameTitle.style.transform = 'translateY(0)';
            }, 50);
        }
        
        if (gameModes) {
            gameModes.style.display = 'flex';
            gameModes.style.opacity = '0';
            gameModes.style.transform = 'translateY(-20px)';
            gameModes.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                gameModes.style.opacity = '1';
                gameModes.style.transform = 'translateY(0)';
            }, 50);
        }
    }, 400);
}

// Add Enter key support for answer submission
document.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        const gameArea = document.getElementById('gameArea');
        if (gameArea.style.display === 'block' && document.getElementById('gameResults').style.display === 'none') {
            submitAnswer();
        }
    }
});

// Update game level options when script type changes
function updateGameLevelOptions() {
    const scriptType = document.getElementById('gameScriptType')?.value || 'simplified';
    const levelSelect = document.getElementById('gameLevelSelect');
    
    if (!levelSelect) return;
    
    levelSelect.innerHTML = '';
    
    if (scriptType === 'simplified') {
        levelSelect.innerHTML = `
            <option value="hsk1">HSK 1</option>
            <option value="hsk2">HSK 2</option>
            <option value="hsk3">HSK 3</option>
            <option value="hsk4">HSK 4</option>
            <option value="hsk5">HSK 5</option>
            <option value="hsk6">HSK 6</option>
        `;
    } else {
        levelSelect.innerHTML = `
            <option value="tocfl_a1">TOCFL A1</option>
            <option value="tocfl_a2">TOCFL A2</option>
            <option value="tocfl_b1">TOCFL B1</option>
            <option value="tocfl_b2">TOCFL B2</option>
            <option value="tocfl_c1">TOCFL C1</option>
            <option value="tocfl_c2">TOCFL C2</option>
        `;
    }
}

document.getElementById('gameScriptType')?.addEventListener('change', function() {
    updateGameLevelOptions();
});

// Cập nhật tổng số câu khi thay đổi lựa chọn số lượng câu hỏi
document.getElementById('questionCount')?.addEventListener('change', function() {
    const selected = parseInt(this.value);
    const totalSpan = document.getElementById('totalQuestions');
    // Nếu đang có dữ liệu game, cập nhật hiển thị ngay theo min(selected, gameData.length)
    const available = gameData?.length || 0;
    const actual = available ? Math.min(selected, available) : selected;
    if (totalSpan) totalSpan.textContent = actual;
});

// Give up: reveal the correct answer immediately and show next button
function giveUp() {
    if (!gameData.length || currentQuestion >= gameData.length) return;
    wrongAnswers++;
    wrongAttempts = 5;
    const correctAnswer = gameMode === 'hanzi-to-meaning' ? currentAnswer.meaning_vi : currentAnswer.hanzi;
    showFeedback(`
        <i class="fas fa-exclamation-triangle"></i> Bạn đã từ bỏ! Đáp án đúng là: <strong>${correctAnswer}</strong>
        <br>
        <small>${currentAnswer.hanzi} (${currentAnswer.pinyin}) = ${currentAnswer.meaning_vi}</small>
    `, 'wrong');
    updateGameUI();
    showNextButton();
}

// Show next button and hide submit/give up buttons
function showNextButton() {
    document.getElementById('submitBtn').style.display = 'none';
    document.getElementById('giveUpBtn').style.display = 'none';
    document.getElementById('nextBtn').style.display = 'inline-block';
    document.getElementById('answerInput').disabled = true;
}

// Move to next question
function nextQuestion() {
    const card = document.querySelector('.question-card');
    if (!card) {
        currentQuestion++;
        showQuestion();
        return;
    }
    // Animate out, then advance, then animate in
    card.classList.remove('question-transition-in');
    card.classList.add('question-transition-out');
    const handleOutEnd = () => {
        card.removeEventListener('animationend', handleOutEnd);
        currentQuestion++;
        showQuestion();
        // Animate in
        // Force reflow to restart animation
        void card.offsetWidth;
        card.classList.remove('question-transition-out');
        card.classList.add('question-transition-in');
        const handleInEnd = () => {
            card.removeEventListener('animationend', handleInEnd);
            card.classList.remove('question-transition-in');
        };
        card.addEventListener('animationend', handleInEnd);
    };
    card.addEventListener('animationend', handleOutEnd);
}

// ===================================
// UTILITY FUNCTIONS
// ===================================

function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

// Normalize text for better search (remove Vietnamese accents)
function normalizeText(text) {
    return text
        .toLowerCase()
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/đ/g, 'd')
        .replace(/Đ/g, 'd');
}

// Highlight search term in text
function highlightText(text, searchTerm) {
    if (!searchTerm) return text;
    
    const regex = new RegExp(`(${searchTerm})`, 'gi');
    return text.replace(regex, '<mark class="search-highlight">$1</mark>');
}

// Update search placeholder based on script type
function updateSearchPlaceholder() {
    const scriptType = document.getElementById('scriptType').value;
    const searchInput = document.getElementById('searchInput');
    
    if (scriptType === 'simplified') {
        searchInput.placeholder = 'Tìm trong tất cả HSK (Giản thể)...';
    } else {
        searchInput.placeholder = 'Tìm trong tất cả TOCFL (Phồn thể)...';
    }
}

// ===================================
// WORD DETAIL MODAL
// ===================================

function showWordDetail(entry) {
    const modal = document.getElementById('wordModal');
    
    // Set basic info
    document.getElementById('modalHanzi').textContent = entry.hanzi;
    document.getElementById('modalPinyin').textContent = entry.pinyin;
    document.getElementById('modalMeaning').textContent = entry.meaning_vi;
    document.getElementById('modalLevel').textContent = entry.level;
    
    // Set grammar if available
    const grammarSection = document.getElementById('modalGrammar');
    if (entry.grammar && entry.grammar.trim()) {
        document.getElementById('modalGrammarText').textContent = entry.grammar;
        grammarSection.style.display = 'block';
    } else {
        grammarSection.style.display = 'none';
    }
    
    // Set usage if available
    const usageSection = document.getElementById('modalUsage');
    if (entry.usage && entry.usage.trim()) {
        document.getElementById('modalUsageText').textContent = entry.usage;
        usageSection.style.display = 'block';
    } else {
        usageSection.style.display = 'none';
    }
    
    // Set examples if available
    const examplesSection = document.getElementById('modalExamples');
    const examplesList = document.getElementById('modalExamplesList');
    
    if (entry.examples && entry.examples.length > 0) {
        examplesList.innerHTML = entry.examples.map(ex => `
            <div class="modal-example-item">
                <div class="modal-example-hanzi">${ex.hanzi}</div>
                <div class="modal-example-pinyin">${ex.pinyin}</div>
                <div class="modal-example-meaning">${ex.meaning_vi}</div>
            </div>
        `).join('');
        examplesSection.style.display = 'block';
    } else {
        examplesSection.style.display = 'none';
    }
    
    // Show modal
    modal.style.display = 'flex';
    
    // Save focus for restoration
    lastFocusedElement = document.activeElement;
    
    // Hide scrollbar only on mobile devices (width < 768px)
    if (window.innerWidth < 768) {
        document.body.style.overflow = 'hidden';
    }
}

function closeWordModal() {
    const modal = document.getElementById('wordModal');
    const modalContent = modal.querySelector('.word-modal-content');
    
    // Add fadeout and slide down animation
    modal.style.animation = 'modalFadeOut 0.3s ease';
    modalContent.style.animation = 'modalSlideDown 0.3s ease';
    
    setTimeout(() => {
        modal.style.display = 'none';
        modal.style.animation = '';
        modalContent.style.animation = '';
        
        // Restore scrollbar (only needed if it was hidden on mobile)
        if (window.innerWidth < 768) {
            document.body.style.overflow = 'auto';
        }
        
        // Restore focus to previous element
        if (lastFocusedElement) {
            lastFocusedElement.focus();
            lastFocusedElement = null;
        }
    }, 300);
}

// Close modal when clicking outside
window.addEventListener('click', function(e) {
    const modal = document.getElementById('wordModal');
    if (e.target === modal) {
        closeWordModal();
    }
});

// Close modal with ESC key
window.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeWordModal();
    }
});

// ===================================
// READING GAME
// ===================================

let readingData = [];
let currentDialog = null;
let supportVisible = false;
let currentReadingPage = 1;
const topicsPerPage = 8;
let loadedReadingLevels = {}; // Cache for loaded reading levels {scriptType_level: data}

function startReadingGame() {
    // Hide vocabulary game area
    const gameArea = document.getElementById('gameArea');
    if (gameArea) {
        gameArea.style.display = 'none';
    }
    
    // Get elements
    const gameTitle = document.querySelector('#games .section-header');
    const gameModes = document.querySelector('#games .row.g-4.mb-5');
    const readingGameArea = document.getElementById('readingGameArea');
    
    // Add fade out animation to title and game modes
    if (gameTitle) {
        gameTitle.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        gameTitle.style.opacity = '0';
        gameTitle.style.transform = 'translateY(-20px)';
    }
    
    if (gameModes) {
        gameModes.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        gameModes.style.opacity = '0';
        gameModes.style.transform = 'translateY(-20px)';
    }
    
    // After fade out completes, hide them and show reading game area
    setTimeout(() => {
        if (gameTitle) gameTitle.style.display = 'none';
        if (gameModes) gameModes.style.display = 'none';
        
        // Show reading game area with fade in animation
        readingGameArea.style.display = 'block';
        readingGameArea.style.opacity = '0';
        readingGameArea.style.transform = 'translateY(20px)';
        readingGameArea.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        
        // Trigger fade in
        setTimeout(() => {
            readingGameArea.style.opacity = '1';
            readingGameArea.style.transform = 'translateY(0)';
            
            // Load initial reading data without scrolling
            setTimeout(() => {
                loadReadingData();
            }, 100);
        }, 50);
    }, 400);
}

function updateReadingLevelOptions() {
    const scriptType = document.getElementById('readingScriptType')?.value || 'simplified';
    const levelSelect = document.getElementById('readingLevelSelect');
    
    if (!levelSelect) return;
    
    levelSelect.innerHTML = '';
    
    if (scriptType === 'simplified') {
        levelSelect.innerHTML = `
            <option value="hsk1">HSK 1</option>
            <option value="hsk2">HSK 2</option>
            <option value="hsk3">HSK 3</option>
            <option value="hsk4">HSK 4</option>
            <option value="hsk5">HSK 5</option>
            <option value="hsk6">HSK 6</option>
        `;
    } else {
        levelSelect.innerHTML = `
            <option value="tocfl_a1">TOCFL A1</option>
            <option value="tocfl_a2">TOCFL A2</option>
            <option value="tocfl_b1">TOCFL B1</option>
            <option value="tocfl_b2">TOCFL B2</option>
            <option value="tocfl_c1">TOCFL C1</option>
            <option value="tocfl_c2">TOCFL C2</option>
        `;
    }
}

async function loadReadingData() {
    const scriptType = document.getElementById('readingScriptType').value;
    const level = document.getElementById('readingLevelSelect').value;
    
    // Show skeleton loading
    const topicsList = document.getElementById('topicsList');
    topicsList.innerHTML = `
        ${Array(8).fill(0).map(() => `
            <div class="skeleton-card">
                <div class="skeleton skeleton-avatar"></div>
                <div class="skeleton skeleton-text"></div>
                <div class="skeleton skeleton-text short"></div>
            </div>
        `).join('')}
    `;
    
    // Bắt đầu đếm thời gian loading
    const loadStartTime = Date.now();
    
    const dataPath = readingDataPaths[scriptType][level];
    
    try {
        // Check cache first
        const levelKey = `${scriptType}_${level}`;
        if (!loadedReadingLevels[levelKey]) {
            const response = await fetch(dataPath);
            const data = await response.json();
            loadedReadingLevels[levelKey] = data.dialogs || [];
        }
        
        readingData = loadedReadingLevels[levelKey];
        
        // Đảm bảo loading hiển thị ít nhất 1 giây để tránh giật
        const loadTime = Date.now() - loadStartTime;
        const minLoadTime = 1000; // 1 giây
        
        if (loadTime < minLoadTime) {
            await new Promise(resolve => setTimeout(resolve, minLoadTime - loadTime));
        }
        
        displayTopics();
    } catch (error) {
        console.error('Error loading reading data:', error);
        
        // Đảm bảo hiển thị lỗi sau 1 giây
        const loadTime = Date.now() - loadStartTime;
        const minLoadTime = 1000;
        
        if (loadTime < minLoadTime) {
            await new Promise(resolve => setTimeout(resolve, minLoadTime - loadTime));
        }
        
        document.getElementById('topicsList').innerHTML = `
            <div class="glass-card p-4 text-center">
                <i class="fas fa-exclamation-triangle" style="font-size: 3rem; color: var(--warning-color);"></i>
                <h3 class="mt-3">Không thể tải dữ liệu</h3>
                <p class="text-secondary">Vui lòng kiểm tra lại đường dẫn file JSON hoặc tạo dữ liệu đọc hiểu.</p>
            </div>
        `;
    }
}

function displayTopics() {
    const topicsList = document.getElementById('topicsList');
    
    if (!readingData || readingData.length === 0) {
        topicsList.innerHTML = `
            <div class="glass-card p-4 text-center">
                <i class="fas fa-inbox" style="font-size: 3rem; color: var(--text-secondary);"></i>
                <h3 class="mt-3">Chưa có dữ liệu</h3>
                <p class="text-secondary">Vui lòng tạo dữ liệu đọc hiểu cho cấp độ này.</p>
            </div>
        `;
        return;
    }
    
    // Calculate pagination
    const totalTopics = readingData.length;
    const totalPages = Math.ceil(totalTopics / topicsPerPage);
    const startIndex = (currentReadingPage - 1) * topicsPerPage;
    const endIndex = Math.min(startIndex + topicsPerPage, totalTopics);
    const currentPageTopics = readingData.slice(startIndex, endIndex);
    
    topicsList.innerHTML = currentPageTopics.map((dialog, index) => {
        const actualIndex = startIndex + index;
        return `
            <div class="topic-card glass-card animate-topic-card" style="animation-delay: ${index * 0.05}s" onclick="showDialog(${actualIndex})">
                <div class="topic-icon">
                    <i class="fas ${getTopicIcon(dialog.topic)}"></i>
                </div>
                <h4>${dialog.topic}</h4>
                <p>${dialog.description || ''}</p>
            </div>
        `;
    }).join('');
    
    // Add pagination controls
    if (totalPages <= 1) {
        // No pagination needed
        const readingGameArea = document.getElementById('readingGameArea');
        let paginationContainer = readingGameArea.querySelector('.reading-pagination');
        if (paginationContainer) {
            paginationContainer.innerHTML = '';
        }
    } else {
        let paginationHTML = `
            <div class="col-12">
                <div class="pagination-container mt-4">
                    <button class="page-btn" onclick="changeReadingPage(${currentReadingPage - 1})" ${currentReadingPage === 1 ? 'disabled' : ''}>
                        <i class="fas fa-chevron-left"></i>
                    </button>
        `;
        
        // Page numbers with smart display (like dictionary)
        for (let i = 1; i <= totalPages; i++) {
            if (i === 1 || i === totalPages || (i >= currentReadingPage - 1 && i <= currentReadingPage + 1)) {
                paginationHTML += `
                    <button class="page-btn ${i === currentReadingPage ? 'active' : ''}" onclick="changeReadingPage(${i})">
                        ${i}
                    </button>
                `;
            } else if (i === currentReadingPage - 2 || i === currentReadingPage + 2) {
                paginationHTML += '<span class="page-btn" disabled>...</span>';
            }
        }
        
        paginationHTML += `
                    <button class="page-btn" onclick="changeReadingPage(${currentReadingPage + 1})" ${currentReadingPage === totalPages ? 'disabled' : ''}>
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
        `;
        
        // Insert pagination after topics list
        const readingGameArea = document.getElementById('readingGameArea');
        let paginationContainer = readingGameArea.querySelector('.reading-pagination');
        if (!paginationContainer) {
            paginationContainer = document.createElement('div');
            paginationContainer.className = 'row reading-pagination';
            topicsList.parentElement.appendChild(paginationContainer);
        }
        paginationContainer.innerHTML = paginationHTML;
    }
    
    // Show topics, hide dialog
    document.getElementById('topicsList').style.display = 'grid';
    document.getElementById('dialogDisplay').style.display = 'none';
}

function changeReadingPage(page) {
    const totalPages = Math.ceil(readingData.length / topicsPerPage);
    if (page < 1 || page > totalPages) return;
    
    currentReadingPage = page;
    displayTopics();
    
    // Scroll to top of topics list
    document.getElementById('topicsList').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function getTopicIcon(topic) {
    const icons = {
        '自我介绍': 'fa-user',
        '自我介紹': 'fa-user',
        '问候': 'fa-handshake',
        '問候': 'fa-handshake',
        '购物': 'fa-shopping-cart',
        '購物': 'fa-shopping-cart',
        '餐厅': 'fa-utensils',
        '餐廳': 'fa-utensils',
        '交通': 'fa-bus',
        '学习': 'fa-graduation-cap',
        '學習': 'fa-graduation-cap',
        '工作': 'fa-briefcase',
        '家庭': 'fa-home',
        '旅游': 'fa-plane',
        '旅遊': 'fa-plane',
        '健康': 'fa-heartbeat',
        '天气': 'fa-cloud-sun',
        '天氣': 'fa-cloud-sun',
        '爱好': 'fa-palette',
        '愛好': 'fa-palette',
        '运动': 'fa-running',
        '運動': 'fa-running',
        '节日': 'fa-calendar-alt',
        '節日': 'fa-calendar-alt'
    };
    
    for (let key in icons) {
        if (topic.includes(key)) {
            return icons[key];
        }
    }
    
    return 'fa-comments';
}

function showDialog(index) {
    currentDialog = readingData[index];
    supportVisible = false;
    
    document.getElementById('dialogTitle').textContent = currentDialog.topic;
    
    // Display dialog lines
    const dialogContent = document.getElementById('dialogContent');
    dialogContent.innerHTML = currentDialog.lines.map(line => `
        <div class="dialog-line">
            ${line.speaker ? `<div class="dialog-speaker">${line.speaker}</div>` : ''}
            <div class="dialog-text">${line.text}</div>
        </div>
    `).join('');
    
    // Hide support panel initially with clean state
    const supportPanel = document.getElementById('supportPanel');
    supportPanel.classList.remove('show');
    supportPanel.style.display = 'none';
    document.getElementById('supportBtn').innerHTML = '<i class="fas fa-question-circle"></i> Hỗ trợ';
    
    // Show dialog, hide topics
    document.getElementById('topicsList').style.display = 'none';
    document.getElementById('dialogDisplay').style.display = 'block';
    
    // Hide pagination when showing dialog
    const readingGameArea = document.getElementById('readingGameArea');
    const paginationContainer = readingGameArea?.querySelector('.reading-pagination');
    if (paginationContainer) {
        paginationContainer.style.display = 'none';
    }
}

function toggleSupport() {
    supportVisible = !supportVisible;
    const supportPanel = document.getElementById('supportPanel');
    const supportBtn = document.getElementById('supportBtn');
    
    if (supportVisible) {
        // Show support
        const supportContent = document.getElementById('supportContent');
        supportContent.innerHTML = currentDialog.lines.map(line => `
            <div class="support-item">
                <div class="support-text">${line.text}</div>
                <div class="support-pinyin">${line.pinyin}</div>
                <div class="support-translation">${line.translation}</div>
            </div>
        `).join('');
        
        // First set display block, then trigger animation in next frame
        supportPanel.style.display = 'block';
        // Force reflow to ensure display change is applied
        supportPanel.offsetHeight;
        // Now add class to trigger animation
        requestAnimationFrame(() => {
            supportPanel.classList.add('show');
        });
        supportBtn.innerHTML = '<i class="fas fa-eye-slash"></i> Ẩn hỗ trợ';
    } else {
        // Hide support with animation
        supportPanel.classList.remove('show');
        supportBtn.innerHTML = '<i class="fas fa-question-circle"></i> Hỗ trợ';
        
        // Wait for animation to complete before hiding
        setTimeout(() => {
            if (!supportVisible) {
                supportPanel.style.display = 'none';
            }
        }, 400); // Match the CSS transition duration
    }
}

function backToTopics() {
    currentReadingPage = 1; // Reset to first page when going back
    displayTopics();
    
    // Show pagination again when back to topics
    const readingGameArea = document.getElementById('readingGameArea');
    const paginationContainer = readingGameArea?.querySelector('.reading-pagination');
    if (paginationContainer) {
        paginationContainer.style.display = 'block';
    }
}
function exitReadingGame() {
    const readingGameArea = document.getElementById('readingGameArea');
    const gameTitle = document.querySelector('#games .section-header');
    const gameModes = document.querySelector('#games .row.g-4.mb-5');
    
    // Fade out reading game area
    readingGameArea.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    readingGameArea.style.opacity = '0';
    readingGameArea.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
        readingGameArea.style.display = 'none';
        // Reset display and page
        currentReadingPage = 1;
        document.getElementById('topicsList').style.display = 'grid';
        document.getElementById('dialogDisplay').style.display = 'none';
        
        // Show and fade in title and game modes
        if (gameTitle) {
            gameTitle.style.display = 'block';
            gameTitle.style.opacity = '0';
            gameTitle.style.transform = 'translateY(-20px)';
            gameTitle.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                gameTitle.style.opacity = '1';
                gameTitle.style.transform = 'translateY(0)';
            }, 50);
        }
        
        if (gameModes) {
            gameModes.style.display = 'flex';
            gameModes.style.opacity = '0';
            gameModes.style.transform = 'translateY(-20px)';
            gameModes.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            
            setTimeout(() => {
                gameModes.style.opacity = '1';
                gameModes.style.transform = 'translateY(0)';
            }, 50);
        }
    }, 400);
}

// Event listeners for reading game
document.getElementById('readingScriptType')?.addEventListener('change', function() {
    updateReadingLevelOptions();
});

document.getElementById('applyReadingSettings')?.addEventListener('click', async function() {
    const btn = this;
    if (!btn.dataset.originalText) {
        btn.dataset.originalText = btn.innerHTML;
    }
    // Disable and show spinner (match vocab game UX)
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang cập nhật';

    // Load data
    await loadReadingData();

    // Restore
    btn.disabled = false;
    btn.innerHTML = btn.dataset.originalText;
});

// ===================================
// TRANSLATOR POPUP
// ===================================

let translatorDirection = 'zh-vi'; // 'zh-vi' or 'vi-zh'
let translationTimeout;
let isOnline = navigator.onLine;
let dictionaryDataLoaded = false;
let translatorChineseType = 'simplified'; // 'simplified' or 'traditional'
let translatorDictionaryData = []; // Separate dictionary for translator
let networkCheckTimeout; // debounce/show checking animation for network state

// Common Traditional Chinese characters (not in Simplified)
const traditionalChars = '繁體臺灣無還會對戰請問讓說與與聽講開關還對給給點還總與與與給與與與與與與';
// Common Simplified Chinese characters (not in Traditional)
const simplifiedChars = '简体台湾无还会对战请问让说与与听讲开关还对给给点还总与与与给与与与与与与';

// Detect if text contains Traditional or Simplified Chinese
function detectChineseType(text) {
    let traditionalCount = 0;
    let simplifiedCount = 0;
    
    for (const char of text) {
        if (traditionalChars.includes(char)) traditionalCount++;
        if (simplifiedChars.includes(char)) simplifiedCount++;
    }
    
    if (traditionalCount > simplifiedCount && traditionalCount > 0) {
        return 'traditional';
    } else if (simplifiedCount > traditionalCount && simplifiedCount > 0) {
        return 'simplified';
    }
    return null; // Cannot determine
}

// Initialize translator on page load
function initTranslator() {
    // Prevent duplicate initialization
    if (translatorInitialized) return;
    translatorInitialized = true;
    
    const toggleBtn = document.getElementById('translatorToggle');
    const translatorInput = document.getElementById('translatorInput');
    
    // Toggle popup
    toggleBtn?.addEventListener('click', function() {
        const popup = document.getElementById('translatorPopup');
        popup.classList.remove('collapsed');
        translatorInput?.focus();
        // Each time opened, show checking state briefly
        scheduleNetworkCheck(2000);
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.lang-selector')) {
            closeAllDropdowns();
        }
    });
    
    // Initialize UI to match default state
    updateLanguageIndicators();
    updateDropdownCheckmarks();
    
    // Monitor online/offline status
    window.addEventListener('online', () => {
        isOnline = true;
        // Flash checking for 2s then show result
        scheduleNetworkCheck(2000);
    });
    
    window.addEventListener('offline', () => {
        isOnline = false;
        // Flash checking for 2s then show exclamation
        scheduleNetworkCheck(2000);
    });
    
    // Initial: show checking for 2s, then reflect actual status
    isOnline = navigator.onLine;
    scheduleNetworkCheck(2000);
    
    // Auto-translate on input with debounce
    translatorInput?.addEventListener('input', function() {
        const value = this.value.trim();
        
        // Show/hide clear button
        const clearBtn = document.querySelector('.clear-input-btn');
        if (clearBtn) {
            clearBtn.style.display = value ? 'flex' : 'none';
        }
        
        // Clear previous timeout
        clearTimeout(translationTimeout);
        
        if (!value) {
            resetTranslatorOutput();
            return;
        }
        
        // Auto-detect and translate with 500ms debounce
        translationTimeout = setTimeout(() => {
            autoTranslate(value);
        }, 500);
    });
    
    // Preload dictionary data for offline use
    preloadDictionaryData();
    loadTranslatorDictionary();
}

// Small utility to check real internet reachability
async function isInternetReachable(timeoutMs = 1500) {
    try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), timeoutMs);
        // Using a tiny 204 endpoint; with mode no-cors we just need the fetch to resolve
        await fetch('https://www.gstatic.com/generate_204', {
            method: 'GET',
            cache: 'no-store',
            mode: 'no-cors',
            signal: controller.signal
        });
        clearTimeout(timer);
        return true; // Resolved => likely online
    } catch (e) {
        return false; // Fetch failed/aborted => treat as offline
    }
}

// Show spinner for a short period then set to current network state (verified)
function scheduleNetworkCheck(delayMs = 2000) {
    clearTimeout(networkCheckTimeout);
    updateTranslatorStatus('translating');
    networkCheckTimeout = setTimeout(async () => {
        const reachable = await isInternetReachable(1500);
        isOnline = reachable;
        updateTranslatorStatus(reachable ? 'online' : 'offline');
    }, delayMs);
}

function updateTranslatorStatus(status) {
    const statusEl = document.getElementById('translatorStatus');
    if (!statusEl) return;
    
    if (status === 'online') {
        statusEl.className = 'status-icon online';
        statusEl.innerHTML = '<i class="fas fa-wifi"></i>';
        statusEl.title = 'Trực tuyến';
    } else if (status === 'offline') {
        statusEl.className = 'status-icon offline';
        statusEl.innerHTML = '<i class="fas fa-exclamation"></i>';
        statusEl.title = 'Ngoại tuyến';
    } else if (status === 'translating') {
        statusEl.className = 'status-icon translating';
        statusEl.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        statusEl.title = 'Đang dịch...';
    }
}

async function autoTranslate(text) {
    if (!text || !text.trim()) {
        resetTranslatorOutput();
        return;
    }
    
    // Auto-detect language
    const isChinese = /[\u4e00-\u9fff]/.test(text);
    
    // Update direction if needed
    if (isChinese && translatorDirection === 'vi-zh') {
        translatorDirection = 'zh-vi';
        updateLanguageIndicators();
    } else if (!isChinese && translatorDirection === 'zh-vi') {
        translatorDirection = 'vi-zh';
        updateLanguageIndicators();
    }
    
    // Check LRU cache first
    const cacheKey = `${translatorDirection}:${translatorChineseType}:${text}`;
    const cachedTranslation = translatorCache.get(cacheKey);
    if (cachedTranslation) {
        displayTranslation(cachedTranslation);
        // Update status based on current network
        updateTranslatorStatus(isOnline ? 'online' : 'offline');
        return;
    }
    
    // Show translating status
    updateTranslatorStatus('translating');
    const outputEl = document.getElementById('translatorOutput');
    outputEl.className = 'translator-output translating';
    outputEl.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang dịch...';
    
    let translation = null;
    let usedOnline = false;
    
    // For Vietnamese to Chinese, ALWAYS try online first (offline won't work well)
    if (translatorDirection === 'vi-zh') {
        if (isOnline) {
            translation = await translateOnline(text, translatorDirection);
            
            // Check if translation is valid (object with text or non-empty string)
            const isValid = (typeof translation === 'object' && translation?.text) || 
                           (typeof translation === 'string' && translation.trim() && !/[\uFFFD]/.test(translation));
            
            if (isValid) {
                usedOnline = true;
            } else {
                translation = 'Cần kết nối internet.';
                usedOnline = false;
            }
        } else {
            translation = 'Cần kết nối internet.';
            usedOnline = false;
        }
    } else {
        // For Chinese to Vietnamese, try online first, fallback to offline
        if (isOnline) {
            translation = await translateOnline(text, translatorDirection);
            
            // Check if translation is valid (object with text or non-empty string)
            const isValid = (typeof translation === 'object' && translation?.text) || 
                           (typeof translation === 'string' && translation.trim() && !/[\uFFFD]/.test(translation));
            
            if (isValid) {
                usedOnline = true;
            } else {
                translation = null;
            }
        }
        
        // Fallback to offline for Chinese→Vietnamese only
        if (!translation || !usedOnline) {
            const offlineTranslation = await translateOffline(text, translatorDirection);
            if (offlineTranslation && offlineTranslation.trim()) {
                translation = offlineTranslation;
                usedOnline = false;
            }
        }
    }
    
    // Display result
    if (translation) {
        // Handle both string and object responses
        const isValidTranslation = typeof translation === 'object' 
            ? (translation.text && translation.text.trim())
            : (typeof translation === 'string' && translation.trim() && 
               !translation.includes('Không thể dịch') && 
               !translation.includes('Cần kết nối'));
        
        if (isValidTranslation) {
            translatorCache.set(cacheKey, translation);
            displayTranslation(translation);
        } else {
            displayTranslation('Không thể dịch văn bản này.');
        }
    } else {
        displayTranslation('Không thể dịch văn bản này.');
    }
    
    // Update status to reflect actual network state
    updateTranslatorStatus(usedOnline ? 'online' : 'offline');
}

async function translateOnline(text, direction) {
    try {
        // Simple translation using Google Translate (unofficial free method)
        let sourceLang, targetLang;
        if (direction === 'zh-vi') {
            sourceLang = translatorChineseType === 'simplified' ? 'zh-CN' : 'zh-TW';
            targetLang = 'vi';
        } else {
            sourceLang = 'vi';
            targetLang = translatorChineseType === 'simplified' ? 'zh-CN' : 'zh-TW';
        }
        
        // Use Google Translate unofficial API via translate.googleapis.com
        // This endpoint doesn't require API key and works from browser
        // Add dt=rm for romanization (pinyin)
        const url = `https://translate.googleapis.com/translate_a/single?client=gtx&sl=${sourceLang}&tl=${targetLang}&dt=t&dt=rm&q=${encodeURIComponent(text)}`;
        
        const response = await fetch(url);
        
        if (!response.ok) throw new Error('Translation API failed');
        
        const data = await response.json();
        
        // Parse Google Translate response format
        // Response format: [[[translated_text, original_text, ...]], ..., romanization_array]
        if (data && data[0] && Array.isArray(data[0])) {
            let translation = '';
            for (const segment of data[0]) {
                if (segment && segment[0]) {
                    translation += segment[0];
                }
            }
            
            if (translation.trim()) {
                // Check if result contains Chinese characters and get pinyin
                if (/[\u4e00-\u9fff]/.test(translation)) {
                    // Try to get pinyin from romanization data
                    let pinyin = '';
                    
                    // Google Translate response format:
                    // data[0] = [["translation", "original", null, null, ...], [null, null, "Pinyin"], ...]
                    // Pinyin is in data[0][i][2] where i > 0
                    
                    if (data[0] && Array.isArray(data[0])) {
                        for (let i = 1; i < data[0].length; i++) {
                            const segment = data[0][i];
                            if (segment && segment[2]) {
                                pinyin += segment[2] + ' ';
                            }
                        }
                    }
                    
                    pinyin = pinyin.trim();
                    
                    // Return object with both translation and pinyin
                    if (pinyin) {
                        return {
                            text: translation.trim(),
                            pinyin: pinyin
                        };
                    }
                }
                
                return translation.trim();
            }
        }
        
        return null;
    } catch (error) {
        console.error('Online translation error:', error);
        return null;
    }
}

async function translateOffline(text, direction) {
    // Ensure translator dictionary data is loaded
    if (translatorDictionaryData.length === 0) {
        await loadTranslatorDictionary();
    }
    
    if (!translatorDictionaryData || translatorDictionaryData.length === 0) {
        return null;
    }
    
    // For Chinese to Vietnamese
    if (direction === 'zh-vi') {
        return translateChineseToVietnamese(text);
    } else {
        // For Vietnamese to Chinese
        return translateVietnameseToChinese(text);
    }
}

function translateChineseToVietnamese(text) {
    if (!translatorDictionaryData || translatorDictionaryData.length === 0) {
        return 'Chưa tải dữ liệu từ điển';
    }
    
    // Detect and warn if wrong Chinese type
    const detectedType = detectChineseType(text);
    let warning = '';
    if (detectedType && detectedType !== translatorChineseType) {
        const current = translatorChineseType === 'simplified' ? 'Giản thể' : 'Phồn thể';
        const detected = detectedType === 'simplified' ? 'Giản thể' : 'Phồn thể';
        warning = `\n\n⚠️ Lưu ý: Bạn đang dịch ${current} nhưng văn bản có vẻ là ${detected}`;
    }
    
    // Strategy 1: Try to match sentence patterns and common structures
    const patterns = [
        // Subject + Verb + Object patterns
        { regex: /我(.{1,3})了/, priority: 3 },  // Tôi ... rồi
        { regex: /你(.{1,3})吗/, priority: 3 },  // Bạn ... không?
        { regex: /(.{1,2})不(.{1,2})/, priority: 2 },  // ... không ...
    ];
    
    // Process character by character with context awareness
    const characters = text.split('');
    const words = [];
    let i = 0;
    
    while (i < characters.length) {
        const char = characters[i];
        
        // Keep punctuation separately
        if (/[,.!?。，！？、；：“”‘’《》〈〉「」『』]/.test(char)) {
            words.push({ type: 'punct', value: char });
            i++;
            continue;
        }
        
        // Skip whitespace
        if (/\s/.test(char)) {
            i++;
            continue;
        }
        
        // Skip non-Chinese characters
        if (!/[\u4e00-\u9fff]/.test(char)) {
            i++;
            continue;
        }
        
        let matched = false;
        let bestMatch = null;
        let bestLen = 0;
        
        // Strategy 2: Try to match longest phrase first (up to 6 characters)
        for (let len = Math.min(6, characters.length - i); len > 0; len--) {
            const phrase = characters.slice(i, i + len).join('');
            if (/[\u4e00-\u9fff]/.test(phrase)) {
                const entry = findInDictionary(phrase);
                
                if (entry) {
                    // Prefer longer matches for better context
                    if (len > bestLen) {
                        bestMatch = entry;
                        bestLen = len;
                    }
                }
            }
        }
        
        if (bestMatch) {
            // Clean the meaning
            let meaning = bestMatch.meaning_vi;
            meaning = cleanMeaning(meaning);
            
            words.push({ type: 'word', value: meaning, length: bestLen });
            i += bestLen;
            matched = true;
        }
        
        // If no match found, skip this character
        if (!matched) {
            i++;
        }
    }
    
    // Strategy 3: Build result with intelligent spacing
    const result = buildNaturalSentence(words);
    
    return result + warning;
}

// Helper function to clean meaning
function cleanMeaning(meaning) {
    if (!meaning) return '';
    
    // Remove content in parentheses and brackets
    let cleaned = meaning.replace(/\s*\([^)]+\)/g, '');
    cleaned = cleaned.replace(/\s*\[[^\]]+\]/g, '');
    
    // Take first meaning if multiple
    if (cleaned.includes(',')) {
        cleaned = cleaned.split(',')[0].trim();
    }
    if (cleaned.includes(';')) {
        cleaned = cleaned.split(';')[0].trim();
    }
    
    return cleaned.trim();
}

// Helper function to build natural sentence
function buildNaturalSentence(words) {
    if (words.length === 0) return 'Đang dùng từ điển offline';
    
    const result = [];
    
    for (let j = 0; j < words.length; j++) {
        const word = words[j];
        const nextWord = words[j + 1];
        const prevWord = words[j - 1];
        
        if (word.type === 'punct') {
            result.push(word.value);
        } else if (word.value) {
            // Add space before word if needed
            if (result.length > 0) {
                const last = result[result.length - 1];
                // Don't add space after punctuation
                if (!/[,.!?。，！？、；：]$/.test(last)) {
                    // Smart spacing: check if words should be connected
                    const shouldConnect = shouldConnectWords(prevWord, word, nextWord);
                    if (!shouldConnect) {
                        result.push(' ');
                    }
                }
            }
            result.push(word.value);
        }
    }
    
    // Final cleanup with advanced rules
    let final = result.join('')
        .replace(/\s+/g, ' ')  // Multiple spaces to single
        .replace(/\s+([,.!?。，！？、；：])/g, '$1')  // Remove space before punctuation
        .replace(/([,.!?。，！？、；：])(?!\s|$)/g, '$1 ')  // Single space after punctuation
        .trim();
    
    // Post-processing: fix common Vietnamese grammar issues
    final = improveVietnameseGrammar(final);
    
    return final;
}

// Improve Vietnamese grammar and naturalness
function improveVietnameseGrammar(text) {
    if (!text) return text;
    
    // Fix common word order issues
    let improved = text;
    
    // Fix "rồi đã" -> "đã ... rồi"
    improved = improved.replace(/(rồi)\s+(đã)\s+([^\s]+)/gi, '$2 $3 $1');
    
    // Fix double negatives
    improved = improved.replace(/không\s+không/gi, 'không');
    
    // Fix "có thể" placement
    improved = improved.replace(/thể\s+có/gi, 'có thể');
    
    // Remove redundant words at start
    improved = improved.replace(/^(là|có|và)\s+(là|có|và)\s+/gi, '$1 ');
    
    // Capitalize first letter
    if (improved.length > 0) {
        improved = improved.charAt(0).toUpperCase() + improved.slice(1);
    }
    
    return improved;
}

// Determine if two words should be connected without space
function shouldConnectWords(prev, current, next) {
    if (!prev || !current || !prev.value || !current.value) return false;
    
    const prevVal = prev.value.toLowerCase().trim();
    const currVal = current.value.toLowerCase().trim();
    const nextVal = next?.value?.toLowerCase().trim() || '';
    
    // Connect common Vietnamese word pairs and phrases
    const connectedPairs = [
        // Negatives and modals
        ['không', 'thể'], ['không', 'biết'], ['không', 'có'],
        ['có', 'thể'], ['có', 'thể'], ['có', 'nên'],
        // Quantity and degree
        ['rất', 'nhiều'], ['rất', 'là'], ['quá', 'nhiều'],
        ['một', 'ít'], ['một', 'số'],
        // Tense and aspect markers
        ['đang', 'dùng'], ['đang', 'làm'], ['đang', 'học'],
        ['sẽ', 'là'], ['sẽ', 'có'], ['sẽ', 'đi'],
        ['đã', 'có'], ['đã', 'làm'], ['đã', 'được'],
        // Common verb phrases
        ['cần', 'phải'], ['cần', 'có'], ['muốn', 'làm'],
        ['biết', 'làm'], ['biết', 'nói'],
        // Prepositions
        ['ở', 'trong'], ['ở', 'trên'], ['tại', 'đây'],
        ['của', 'tôi'], ['của', 'bạn'],
    ];
    
    // Check direct pairs
    for (const [first, second] of connectedPairs) {
        if (prevVal === first && currVal === second) {
            return false; // Add space
        }
    }
    
    // Don't connect if both are single characters (likely separate words)
    if (prevVal.length === 1 && currVal.length === 1) {
        return false;
    }
    
    // Don't connect if current is a common standalone word
    const standaloneWords = ['và', 'hoặc', 'nhưng', 'mà', 'nên', 'thì', 'nếu'];
    if (standaloneWords.includes(currVal)) {
        return false;
    }
    
    return false; // Default: add space
}

function translateVietnameseToChinese(text) {
    if (!translatorDictionaryData || translatorDictionaryData.length === 0) {
        return 'Chưa tải dữ liệu từ điển';
    }
    
    // NOTE: Offline Vietnamese → Chinese dictionary is very limited
    // Most Vietnamese words don't have direct Chinese equivalents in HSK/TOCFL data
    // This function is mainly for reverse lookup of known Chinese words
    
    // Normalize Vietnamese text
    const normalizedText = text.toLowerCase().trim();
    
    // Try to match the whole sentence first
    const exactMatch = findInDictionaryByMeaning(normalizedText);
    if (exactMatch) {
        return exactMatch.hanzi;
    }
    
    // Try to find longest phrases first
    const words = normalizedText.split(/\s+/);
    const translations = [];
    let i = 0;
    
    while (i < words.length) {
        let found = false;
        
        // Try matching 4, 3, 2, then 1 word phrases
        for (let len = Math.min(4, words.length - i); len >= 1; len--) {
            const phrase = words.slice(i, i + len).join(' ');
            
            // Skip if only punctuation
            if (/^[,.!?。，！？\s]+$/.test(phrase)) {
                i++;
                found = true;
                break;
            }
            
            const entry = findInDictionaryByMeaning(phrase);
            if (entry) {
                translations.push(entry.hanzi);
                i += len;
                found = true;
                break;
            }
        }
        
        // If no match found for this word, skip it
        if (!found) {
            i++;
        }
    }
    
    const result = translations.join('');
    
    // If result is too short compared to input, likely not enough dictionary coverage
    if (result.length === 0) {
        return 'Dịch Việt→Trung offline chưa hỗ trợ tốt. Vui lòng dùng kết nối internet.';
    }
    
    return result;
}

function findInDictionary(hanzi) {
    // Search in translator's dictionary data
    if (!translatorDictionaryData || translatorDictionaryData.length === 0) return null;
    
    return translatorDictionaryData.find(entry => entry.hanzi === hanzi);
}

function findInDictionaryByMeaning(meaning) {
    if (!translatorDictionaryData || translatorDictionaryData.length === 0) return null;
    
    const normalized = normalizeText(meaning);
    
    // Try exact match first
    let entry = translatorDictionaryData.find(e => {
        const entryMeaning = normalizeText(e.meaning_vi);
        return entryMeaning === normalized;
    });
    
    if (entry) return entry;
    
    // Try partial match - the meaning contains the search term
    entry = translatorDictionaryData.find(e => {
        const entryMeaning = normalizeText(e.meaning_vi);
        // Split by common separators and check each meaning
        const meanings = entryMeaning.split(/[,;/]/).map(m => m.trim());
        return meanings.some(m => m === normalized || m.startsWith(normalized + ' '));
    });
    
    return entry;
}

async function preloadDictionaryData() {
    if (dictionaryDataLoaded && allScriptData.length > 0) return;
    
    try {
        // Load both simplified and traditional data
        const simplifiedPaths = Object.values(dataPaths.simplified);
        const traditionalPaths = Object.values(dataPaths.traditional);
        const allPaths = [...simplifiedPaths, ...traditionalPaths];
        
        const promises = allPaths.map(path => 
            fetch(path).then(res => res.json()).catch(() => ({ entries: [] }))
        );
        
        const results = await Promise.all(promises);
        const combinedData = results.flatMap(data => data.entries || []);
        
        // Update global dictionary if empty
        if (allScriptData.length === 0) {
            allScriptData = combinedData;
        }
        
        dictionaryDataLoaded = true;
    } catch (error) {
        console.error('Error preloading dictionary:', error);
    }
}

async function loadTranslatorDictionary() {
    try {
        // Load dictionary based on selected Chinese type
        const paths = translatorChineseType === 'simplified' 
            ? Object.values(dataPaths.simplified)
            : Object.values(dataPaths.traditional);
        
        const promises = paths.map(path => 
            fetch(path).then(res => res.json()).catch(() => ({ entries: [] }))
        );
        
        const results = await Promise.all(promises);
        translatorDictionaryData = results.flatMap(data => data.entries || []);
    } catch (error) {
        console.error('Error loading translator dictionary:', error);
        translatorDictionaryData = [];
    }
}

function displayTranslation(text) {
    const outputEl = document.getElementById('translatorOutput');
    const copyBtn = document.getElementById('copyBtn');
    
    outputEl.className = 'translator-output';
    
    // Check if text is an object with pinyin
    if (typeof text === 'object' && text.text) {
        // Display Chinese with pinyin below
        if (text.pinyin) {
            outputEl.innerHTML = `
                <div class="translation-with-pinyin">
                    <div class="translation-hanzi">${text.text}</div>
                    <div class="translation-pinyin">${text.pinyin}</div>
                </div>
            `;
        } else {
            outputEl.textContent = text.text;
        }
        
        // Enable copy button
        if (copyBtn) {
            copyBtn.disabled = false;
        }
    } else if (typeof text === 'string') {
        // Normal string display
        outputEl.textContent = text;
        
        // Enable copy button if translation is valid
        if (copyBtn) {
            if (text && text.trim() && !text.includes('Không thể dịch') && !text.includes('Cần kết nối')) {
                copyBtn.disabled = false;
            } else {
                copyBtn.disabled = true;
            }
        }
    }
}

function resetTranslatorOutput() {
    const outputEl = document.getElementById('translatorOutput');
    const copyBtn = document.getElementById('copyBtn');
    
    outputEl.className = 'translator-output empty';
    outputEl.textContent = '';
    
    if (copyBtn) {
        copyBtn.disabled = true;
    }
}

function swapLanguages() {
    // Close dropdowns immediately
    closeAllDropdowns();
    
    // Swap direction
    translatorDirection = translatorDirection === 'zh-vi' ? 'vi-zh' : 'zh-vi';
    
    // Update UI immediately
    updateLanguageIndicators();
    
    // Clear cache for new direction
    translatorCache.clear();
    
    // Swap input and output only if both have real content
    const input = document.getElementById('translatorInput');
    const output = document.getElementById('translatorOutput');
    
    // Get only the Chinese text (hanzi), not pinyin
    const hanziEl = output.querySelector('.translation-hanzi');
    const outputText = hanziEl ? hanziEl.textContent.trim() : output.textContent.trim();
    const inputText = input.value.trim();
    
    // Only swap if output has real translation (not placeholder text)
    if (outputText && outputText !== 'Bản dịch...' && 
        !outputText.includes('Không thể dịch') && 
        !outputText.includes('Cần kết nối')) {
        
        // Swap the texts (only hanzi, not pinyin)
        input.value = outputText;
        
        // Translate the new input immediately
        clearTimeout(translationTimeout);
        translationTimeout = setTimeout(() => autoTranslate(outputText), 100);
    } else {
        // Just re-translate current input with new direction
        if (inputText) {
            clearTimeout(translationTimeout);
            translationTimeout = setTimeout(() => autoTranslate(inputText), 100);
        } else {
            resetTranslatorOutput();
        }
    }
}

function updateLanguageIndicators() {
    const sourceLangText = document.getElementById('sourceLangText');
    const targetLangText = document.getElementById('targetLangText');
    const sourceIcon = document.getElementById('sourceDropdownIcon');
    const targetIcon = document.getElementById('targetDropdownIcon');
    const sourceLang = document.getElementById('sourceLang');
    const targetLang = document.getElementById('targetLang');
    
    const chineseText = translatorChineseType === 'simplified' ? '简体中文' : '繁體中文';
    const vietnameseText = 'Tiếng Việt';
    
    if (translatorDirection === 'zh-vi') {
        sourceLangText.textContent = chineseText;
        targetLangText.textContent = vietnameseText;
        sourceIcon.style.display = 'inline-block';
        targetIcon.style.display = 'none';
        sourceLang.classList.add('active');
        targetLang.classList.remove('active');
    } else {
        sourceLangText.textContent = vietnameseText;
        targetLangText.textContent = chineseText;
        sourceIcon.style.display = 'none';
        targetIcon.style.display = 'inline-block';
        sourceLang.classList.remove('active');
        targetLang.classList.add('active');
    }
}

function updateDropdownCheckmarks() {
    // Update both dropdowns
    ['sourceTypeDropdown', 'targetTypeDropdown'].forEach(dropdownId => {
        const items = document.querySelectorAll(`#${dropdownId} .dropdown-item`);
        items.forEach((item, index) => {
            const icon = item.querySelector('i');
            // index 0 = simplified, index 1 = traditional
            if ((translatorChineseType === 'simplified' && index === 0) || 
                (translatorChineseType === 'traditional' && index === 1)) {
                icon.style.visibility = 'visible';
            } else {
                icon.style.visibility = 'hidden';
            }
        });
    });
}

function toggleChineseTypeDropdown(side) {
    event?.stopPropagation(); // Prevent event bubbling
    
    const sourceDropdown = document.getElementById('sourceTypeDropdown');
    const targetDropdown = document.getElementById('targetTypeDropdown');
    
    if (side === 'source') {
        // Only show if source is Chinese
        if (translatorDirection === 'zh-vi') {
            // Ensure left alignment for source
            sourceDropdown.classList.remove('align-right');
            const isOpen = sourceDropdown.style.display === 'block';
            sourceDropdown.style.display = isOpen ? 'none' : 'block';
            // Hide the other dropdown
            targetDropdown.style.display = 'none';
        }
    } else if (side === 'target') {
        // Only show if target is Chinese
        if (translatorDirection === 'vi-zh') {
            // Ensure right alignment for target
            targetDropdown.classList.add('align-right');
            const isOpen = targetDropdown.style.display === 'block';
            targetDropdown.style.display = isOpen ? 'none' : 'block';
            // Hide the other dropdown
            sourceDropdown.style.display = 'none';
        }
    }
}

function closeAllDropdowns() {
    const sourceDropdown = document.getElementById('sourceTypeDropdown');
    const targetDropdown = document.getElementById('targetTypeDropdown');
    if (sourceDropdown) sourceDropdown.style.display = 'none';
    if (targetDropdown) targetDropdown.style.display = 'none';
}

function selectChineseType(type, side) {
    event?.stopPropagation(); // Prevent event bubbling
    
    translatorChineseType = type;
    
    // Update checkmarks in all dropdowns
    updateDropdownCheckmarks();
    
    // Update language text
    updateLanguageIndicators();
    
    // Close dropdown
    closeAllDropdowns();
    
    // Clear translator cache and reload dictionary
    translatorCache.clear();
    translatorDictionaryData = [];
    loadTranslatorDictionary();
    
    // Re-translate if there's input
    const input = document.getElementById('translatorInput');
    if (input && input.value.trim()) {
        clearTimeout(translationTimeout);
        translationTimeout = setTimeout(() => autoTranslate(input.value.trim()), 100);
    }
}

function clearTranslatorInput() {
    const input = document.getElementById('translatorInput');
    input.value = '';
    input.focus();
    
    const clearBtn = document.querySelector('.clear-input-btn');
    if (clearBtn) {
        clearBtn.style.display = 'none';
    }
    
    resetTranslatorOutput();
}

function copyTranslation() {
    const copyBtn = document.getElementById('copyBtn');
    const output = document.getElementById('translatorOutput');
    
    // Don't copy if button is disabled
    if (copyBtn.disabled) return;
    
    // Get text from output element
    let text;
    const hanziEl = output.querySelector('.translation-hanzi');
    const pinyinEl = output.querySelector('.translation-pinyin');
    
    if (hanziEl && pinyinEl) {
        // If has pinyin, copy both
        text = `${hanziEl.textContent}\n${pinyinEl.textContent}`;
    } else {
        // Otherwise copy normal text
        text = output.textContent;
    }
    
    if (!text || text === 'Bản dịch...') return;
    
    navigator.clipboard.writeText(text).then(() => {
        if (copyBtn) {
            const originalHTML = copyBtn.innerHTML;
            copyBtn.innerHTML = '<i class="fas fa-check"></i> Đã sao chép!';
            copyBtn.classList.add('copied');
            
            setTimeout(() => {
                copyBtn.innerHTML = originalHTML;
                copyBtn.classList.remove('copied');
            }, 2000);
        }
    }).catch(err => {
        console.error('Failed to copy:', err);
        alert('Không thể sao chép văn bản');
    });
}

function closeTranslator() {
    const popup = document.getElementById('translatorPopup');
    popup.classList.add('collapsed');
    
    // Clear input and output
    clearTranslatorInput();
}

// Hiển thị pinyin cho input dịch nhanh
function showPinyinForTranslatorInput() {
    const Yaniinput = document.getElementById('translatorInput');
    const pinyinOutput = document.getElementById('translatorPinyinOutput');
    if (Yaniinput && pinyinOutput) {
        const value = Yaniinput.value.trim();
        if (/^[\u4e00-\u9fff]+$/.test(value)) {
            const pinyin = getPinyinForHanzi(value);
            pinyinOutput.textContent = pinyin;
        } else {
            pinyinOutput.textContent = '';
        }
    }
}

// Gắn sự kiện input cho translatorInput
window.addEventListener('DOMContentLoaded', function() {
    const Yaniinput = document.getElementById('translatorInput');
    if (Yaniinput) {
        Yaniinput.addEventListener('input', showPinyinForTranslatorInput);
    }
});

// Hàm chuyển chữ Hán sang pinyin (ưu tiên cụm từ, sau đó từng ký tự)
function getPinyinForHanzi(hanzi) {
    let dict = translatorDictionaryData && translatorDictionaryData.length ? translatorDictionaryData : [];
    if (!dict.length) {
        Object.values(loadedLevels).forEach(arr => {
            dict = dict.concat(arr);
        });
    }
    if (!dict.length) return '';
    let pinyinArr = [];
    let i = 0;
    while (i < hanzi.length) {
        let found = false;
        for (let len = Math.min(6, hanzi.length - i); len > 0; len--) {
            let phrase = hanzi.substr(i, len);
            let entry = dict.find(e => e.hanzi === phrase);
            if (entry) {
                pinyinArr.push(entry.pinyin);
                i += len;
                found = true;
                break;
            }
        }
        if (!found) {
            let entry = dict.find(e => e.hanzi === hanzi[i]);
            if (entry) {
                pinyinArr.push(entry.pinyin);
            } else {
                pinyinArr.push(hanzi[i]);
            }
            i++;
        }
    }
    return pinyinArr.join(' ');
}

// ===================================
// EXPORT FUNCTIONS (for HTML onclick)
// ===================================

window.navigateToSection = navigateToSection;
window.changePage = changePage;
window.startGame = startGame;
window.submitAnswer = submitAnswer;
window.giveUp = giveUp;
window.nextQuestion = nextQuestion;
window.restartGame = restartGame;
window.exitGame = exitGame;
window.showWordDetail = showWordDetail;
window.closeWordModal = closeWordModal;
window.startReadingGame = startReadingGame;
window.exitReadingGame = exitReadingGame;
window.showDialog = showDialog;
window.toggleSupport = toggleSupport;
window.backToTopics = backToTopics;
window.changeReadingPage = changeReadingPage;
window.swapLanguages = swapLanguages;
window.clearTranslatorInput = clearTranslatorInput;
window.copyTranslation = copyTranslation;
window.closeTranslator = closeTranslator;
window.selectChineseType = selectChineseType;
window.toggleChineseTypeDropdown = toggleChineseTypeDropdown;
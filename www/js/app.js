// ===================================
// HANZII - Chinese Learning App
// Main JavaScript File
// ===================================

// Global Variables
let currentData = [];
let allScriptData = []; // All data for current script type (all levels combined)
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

// ===================================
// INITIALIZATION
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Hide preloader after content is loaded
    setTimeout(() => {
        const preloader = document.getElementById('preloader');
        preloader.classList.add('hidden');
    }, 1500);

    // Setup navigation
    setupNavigation();
    
    // Setup scroll to top button
    setupScrollToTop();
    
    // Setup dictionary
    setupDictionary();
    
    // Initialize level options
    updateLevelOptions();
    updateGameLevelOptions();
    
    // Setup event listeners
    setupEventListeners();
    
    // Load initial data
    loadDictionaryData();
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

function navigateToSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section-container');
    sections.forEach(section => section.classList.remove('active'));
    
    // Show target section
    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
        targetSection.classList.add('active');
        
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
// SCROLL TO TOP
// ===================================

function setupScrollToTop() {
    const scrollBtn = document.getElementById('scrollToTop');
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollBtn.classList.add('visible');
        } else {
            scrollBtn.classList.remove('visible');
        }
    });
    
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ===================================
// DICTIONARY
// ===================================

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
    
    try {
        // Load all levels for current script type
        const levelPaths = dataPaths[scriptType];
        const allPromises = Object.values(levelPaths).map(path => 
            fetch(path).then(res => res.json())
        );
        
        const allData = await Promise.all(allPromises);
        
        // Combine all entries from all levels
        allScriptData = allData.flatMap(data => data.entries || []);
        
        // Current level data for display when no search
        const currentLevelPath = levelPaths[level];
        const currentLevelResponse = await fetch(currentLevelPath);
        const currentLevelData = await currentLevelResponse.json();
        currentData = currentLevelData.entries || [];
        
        currentPage = 1;
        displayDictionary();
    } catch (error) {
        console.error('Error loading dictionary data:', error);
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

function displayDictionary() {
    const searchTerm = document.getElementById('searchInput').value.trim();
    const normalizedSearch = normalizeText(searchTerm);
    
    // Filter data based on search with normalized text
    // If searching, search ALL levels; otherwise show current level only
    let filteredData;
    if (searchTerm) {
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
    
    // Display with highlighting
    resultsContainer.innerHTML = paginatedData.map((entry, index) => `
        <div class="col-lg-3 col-md-4 col-sm-6">
            <div class="word-card" onclick='showWordDetail(${JSON.stringify(entry).replace(/'/g, "&apos;")})'>
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
        searchTimeout = setTimeout(() => {
            currentPage = 1;
            displayDictionary();
            
            // Hide loading
            if (searchLoading) {
                searchLoading.style.display = 'none';
            }
        }, 250);
    });
    
    // Enter key support
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            clearTimeout(searchTimeout);
            currentPage = 1;
            displayDictionary();
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
    
    // Show game area
    document.getElementById('gameArea').style.display = 'block';
    document.getElementById('gameResults').style.display = 'none';
    
    // Scroll to game area
    setTimeout(() => {
        document.getElementById('gameArea').scrollIntoView({ behavior: 'smooth' });
        // Initialize game after scrolling
        initializeGame();
    }, 100);
}

async function initializeGame() {
    const scriptType = document.getElementById('gameScriptType').value;
    const level = document.getElementById('gameLevelSelect').value;
    const questionCount = parseInt(document.getElementById('questionCount').value);
    
    const dataPath = dataPaths[scriptType][level];
    
    try {
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
        showQuestion();
    } catch (error) {
        console.error('Error loading game data:', error);
        alert('Không thể tải dữ liệu game. Vui lòng thử lại.');
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
    document.getElementById('gameArea').style.display = 'none';
    navigateToSection('games');
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
    currentQuestion++;
    showQuestion();
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
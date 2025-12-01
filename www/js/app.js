// ===================================
// HANZII - Chinese Learning App
// Main JavaScript File
// ===================================

// Global Variables
let currentData = [];
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
        loadDictionaryData();
    });
    
    levelSelect.addEventListener('change', function() {
        loadDictionaryData();
    });
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
    
    const dataPath = dataPaths[scriptType][level];
    
    try {
        const response = await fetch(dataPath);
        const data = await response.json();
        currentData = data.entries || [];
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
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    
    // Filter data based on search
    let filteredData = currentData;
    if (searchTerm) {
        filteredData = currentData.filter(entry => 
            entry.hanzi.toLowerCase().includes(searchTerm) ||
            entry.pinyin.toLowerCase().includes(searchTerm) ||
            entry.meaning_vi.toLowerCase().includes(searchTerm)
        );
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
                    <p class="text-secondary">Thử tìm kiếm với từ khóa khác.</p>
                </div>
            </div>
        `;
        document.getElementById('pagination').innerHTML = '';
        return;
    }
    
    resultsContainer.innerHTML = paginatedData.map(entry => `
        <div class="col-lg-3 col-md-4 col-sm-6">
            <div class="word-card">
                <div class="word-hanzi">${entry.hanzi}</div>
                <div class="word-pinyin">${entry.pinyin}</div>
                <div class="word-meaning">${entry.meaning_vi}</div>
                <span class="word-level">${entry.level}</span>
            </div>
        </div>
    `).join('');
    
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
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            currentPage = 1;
            displayDictionary();
        }, 300);
    });

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
    document.getElementById('feedbackMessage').innerHTML = '';
    document.getElementById('answerInput').focus();
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
        
        // Move to next question after delay
        setTimeout(() => {
            currentQuestion++;
            showQuestion();
        }, 2500);
    } else {
        wrongAnswers++;
        wrongAttempts++;
        
        // Nếu sai quá 5 lần, hiển thị đáp án và chuyển câu
        if (wrongAttempts >= 5) {
            const correctAnswer = gameMode === 'hanzi-to-meaning' ? currentAnswer.meaning_vi : currentAnswer.hanzi;
            showFeedback(`
                <i class="fas fa-exclamation-triangle"></i> Đã sai 5 lần! Đáp án đúng là: <strong>${correctAnswer}</strong>
                <br>
                <small>${currentAnswer.hanzi} (${currentAnswer.pinyin}) = ${currentAnswer.meaning_vi}</small>
            `, 'wrong');
            
            updateGameUI();
            
            // Move to next question after delay
            setTimeout(() => {
                currentQuestion++;
                showQuestion();
            }, 3000);
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

// Give up: reveal the correct answer immediately and advance like 5 failed attempts
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
    setTimeout(() => {
        currentQuestion++;
        showQuestion();
    }, 3000);
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

// ===================================
// EXPORT FUNCTIONS (for HTML onclick)
// ===================================

window.navigateToSection = navigateToSection;
window.changePage = changePage;
window.startGame = startGame;
window.submitAnswer = submitAnswer;
window.giveUp = giveUp;
window.restartGame = restartGame;
window.exitGame = exitGame;
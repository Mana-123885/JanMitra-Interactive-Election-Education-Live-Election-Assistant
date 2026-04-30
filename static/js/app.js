/**
 * JanMitra Web App - Core Logic
 */

class JanMitraApp {
    constructor() {
        this.config = null;
        this.profile = null;
        this.currentLang = 'en';
        this.currentScreen = null;
        
        // UI Elements
        this.sidebar = document.getElementById('sidebar');
        this.mainNav = document.getElementById('main-nav');
        this.bottomNav = document.getElementById('bottom-nav');
        this.screenContainer = document.getElementById('screen-container');
        
        this.init();
    }

    async init() {
        try {
            // 1. Fetch Config & Profile
            const [configRes, profileRes] = await Promise.all([
                fetch('/api/config'),
                fetch('/api/profile')
            ]);
            
            this.config = await configRes.json();
            this.profile = await profileRes.json();
            this.currentLang = 'en';
            
            // 2. Apply Theme
            this.applyTheme(this.profile.theme || 'dark');
            
            // 3. Initialize Sidebar
            this.renderSidebar();
            
            // 4. Start with Splash or Onboarding or Home
            if (this.profile.onboarding_done) {
                this.switchScreen('home');
            } else {
                this.switchScreen('onboarding');
            }
            
            console.log('JanMitra Initialized');
        } catch (error) {
            console.error('Initialization failed:', error);
        }
    }

    // --- NAVIGATION & ROUTING ---

    renderSidebar() {
        const navItems = [
            { id: 'home', emoji: '🏠', key: 'nav_home' },
            { id: 'learn', emoji: '📚', key: 'nav_learn' },
            { id: 'types', emoji: '🏰', key: 'nav_types' },
            { id: 'quiz', emoji: '🎯', key: 'nav_quiz' },
            { id: 'simulator', emoji: '🗳️', label: 'Polling Simulator' },
            { id: 'chat', emoji: '🤖', key: 'nav_chatbot' },
            { id: 'live', emoji: '📈', key: 'nav_live' },
            { id: 'myths', emoji: '💥', key: 'nav_myths' },
            { id: 'glossary', emoji: '📖', key: 'nav_glossary' },
            { id: 'reg', emoji: '📝', key: 'nav_reg' },
            { id: 'links', emoji: '🔗', key: 'nav_links' }
        ];

        const footerItems = [
            { id: 'profile', emoji: '👤', key: 'nav_profile' },
            { id: 'settings', emoji: '⚙️', key: 'nav_settings' }
        ];

        this.mainNav.innerHTML = navItems.map(item => this.createNavItem(item)).join('');
        this.bottomNav.innerHTML = footerItems.map(item => this.createNavItem(item)).join('');
    }

    createNavItem(item) {
        const label = item.key ? this.t(item.key) : item.label;
        return `
            <div class="nav-item" id="nav-${item.id}" onclick="app.switchScreen('${item.id}')">
                <span class="nav-emoji">${item.emoji}</span>
                <span class="nav-label">${label}</span>
            </div>
        `;
    }

    switchScreen(screenId) {
        // Update Active State in Nav
        document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
        const activeNav = document.getElementById(`nav-${screenId}`);
        if (activeNav) activeNav.classList.add('active');

        // Show/Hide Sidebar
        if (['splash', 'onboarding'].includes(screenId)) {
            this.sidebar.classList.add('hidden');
        } else {
            this.sidebar.classList.remove('hidden');
        }

        // Render Screen
        this.currentScreen = screenId;
        this.renderScreen(screenId);
        window.scrollTo(0, 0);
    }

    renderScreen(screenId) {
        this.screenContainer.innerHTML = '';
        
        switch(screenId) {
            case 'splash': this.renderSplashScreen(); break;
            case 'onboarding': this.renderOnboardingScreen(); break;
            case 'home': this.renderHomeScreen(); break;
            case 'learn': this.renderLearnScreen(); break;
            case 'types': this.renderTypesScreen(); break;
            case 'quiz': this.renderQuizScreen(); break;
            case 'simulator': this.renderSimulatorScreen(); break;
            case 'chat': this.renderChatScreen(); break;
            case 'live': this.renderLiveScreen(); break;
            case 'myths': this.renderMythScreen(); break;
            case 'glossary': this.renderGlossaryScreen(); break;
            case 'reg': this.renderRegistrationScreen(); break;
            case 'links': this.renderLinksScreen(); break;
            case 'profile': this.renderProfileScreen(); break;
            case 'settings': this.renderSettingsScreen(); break;
            default: this.renderHomeScreen();
        }
    }

    // --- HELPERS ---

    l(obj, field) {
        if (!obj) return '';
        return obj[field] || '';
    }

    t(key, params = {}) {
        let text = this.config.translations[this.currentLang][key] || key;
        for (const [k, v] of Object.entries(params)) {
            text = text.replace(`{${k}}`, v);
        }
        return text;
    }

    applyTheme(theme) {
        document.body.className = theme === 'light' ? 'light-theme' : 'dark-theme';
    }

    showToast(message, type = 'info') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = message;
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    async addXP(amount) {
        const res = await fetch('/api/xp/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ amount })
        });
        const data = await res.json();
        this.profile.xp = data.xp;
        this.showToast(`+${amount} XP Earned! 🎊`, 'success');
        return data;
    }

    // --- SCREEN RENDERERS (Placeholders for now) ---

    renderSplashScreen() {
        this.screenContainer.innerHTML = `
            <div class="splash-container">
                <div class="splash-logo">🗳️</div>
                <h1 style="font-size: 48px; margin-bottom: 10px;">${this.config.app_name}</h1>
                <p style="font-size: 20px; color: var(--text-2); mb-40">${this.t('tagline')}</p>
                <button class="btn btn-primary" onclick="app.switchScreen('onboarding')">
                    Get Started →
                </button>
            </div>
        `;
    }

    renderOnboardingScreen() {
        if (!this.obStep || this.obStep === 1) this.obStep = 2; // Skip Step 1 (Language)
        const render = () => {
            this.screenContainer.innerHTML = `
                <div class="card glass-card" style="max-width: 500px; margin: 50px auto; text-align: center; padding: 40px;">
                    ${this.obStep === 2 ? `
                        <h2>${this.t('onboarding_who')}</h2>
                        <div style="margin-top: 30px; text-align: left;">
                            <label>Name</label>
                            <input type="text" id="ob-name" class="card" style="width: 100%; margin: 8px 0 20px; background: var(--surface-2); padding: 12px; border: 1px solid var(--border); color: var(--text-1);" placeholder="Your Name">
                            <label>User Type</label>
                            <select id="ob-type" class="card" style="width: 100%; margin: 8px 0; background: var(--surface-2); padding: 12px; color: var(--text-1); border: 1px solid var(--border);">
                                <option>General Voter</option>
                                <option>First Time Voter</option>
                                <option>Student</option>
                                <option>Senior Citizen</option>
                            </select>
                            <button class="btn btn-primary" style="width: 100%; margin-top: 20px;" onclick="app.saveOnboardingStep2()">Next Step</button>
                        </div>
                    ` : `
                        <h2>${this.t('onboarding_complete')}</h2>
                        <p style="margin: 20px 0;">You're all set to begin your civic journey!</p>
                        <button class="btn btn-primary" style="width: 100%;" onclick="app.finishOnboarding()">Start My Journey</button>
                    `}
                </div>
            `;
        };
        render();
    }

    async saveOnboardingStep2() {
        const name = document.getElementById('ob-name').value || 'Voter';
        const type = document.getElementById('ob-type').value;
        this.profile.name = name;
        this.profile.user_type = type;
        await fetch('/api/profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, user_type: type })
        });
        this.obStep = 3;
        this.renderOnboardingScreen();
    }

    async finishOnboarding() {
        await fetch('/api/profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ onboarding_done: 1 })
        });
        this.profile.onboarding_done = 1;
        this.switchScreen('home');
    }

    async renderHomeScreen() {
        const level = this.profile.xp ? Math.floor(this.profile.xp / 100) + 1 : 1; // Simplified level logic
        
        this.screenContainer.innerHTML = `
            <div class="home-header" style="margin-bottom: 40px;">
                <h1 style="font-size: 32px; margin-bottom: 8px;">${this.t('welcome_greeting', { name: this.profile.name })}</h1>
                <p style="color: var(--text-2)">${this.t('profile_summary')}</p>
            </div>

            <div class="grid-3">
                <div class="card glass-card">
                    <h3>${this.t('level_label', { n: level })}</h3>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: ${(this.profile.xp % 100)}%"></div>
                    </div>
                    <p style="color: var(--text-3); font-size: 14px;">${this.t('xp_label', { xp: this.profile.xp })}</p>
                </div>
                <div class="card glass-card">
                    <h3>${this.t('streak_label', { n: this.profile.streak || 0 })}</h3>
                    <p style="font-size: 32px; margin-top: 10px;">🔥</p>
                </div>
                <div class="card glass-card">
                    <h3>${this.t('badges_label')}</h3>
                    <p style="font-size: 32px; margin-top: 10px;">🏅 🎯 🌟</p>
                </div>
            </div>

            <h2 style="margin: 40px 0 20px;">${this.t('quick_actions')}</h2>
            <div class="grid-2">
                <div class="card" onclick="app.switchScreen('learn')">
                    <h3>📚 ${this.t('nav_learn')}</h3>
                    <p style="color: var(--text-2); margin-top: 8px;">Explore the 12 stages of the election journey.</p>
                </div>
                <div class="card" onclick="app.switchScreen('quiz')">
                    <h3>🎯 ${this.t('nav_quiz')}</h3>
                    <p style="color: var(--text-2); margin-top: 8px;">Test your knowledge and earn XP!</p>
                </div>
            </div>
        `;
    }

    async renderLearnScreen() {
        const [contentRes, progressRes] = await Promise.all([
            fetch('/api/learning/content'),
            fetch('/api/learning/progress')
        ]);
        const stages = await contentRes.json();
        const progress = await progressRes.json();
        
        this.screenContainer.innerHTML = `
            <div class="screen-header">
                <h1>${this.t('learn_title')}</h1>
                <p style="color: var(--text-2)">${this.t('learn_subtitle')}</p>
            </div>
            <div class="stages-list" style="margin-top: 30px;">
                ${stages.map(stage => {
                    const isDone = progress.explored_stages.includes(stage.stage_id);
                    const color = isDone ? 'var(--success)' : stage.color;
                    return `
                        <div class="card" onclick="app.showStageDetail(${JSON.stringify(stage).replace(/"/g, '&quot;')})">
                            <div style="display: flex; align-items: center; gap: 20px;">
                                <div style="font-size: 40px;">${stage.emoji}</div>
                                <div style="flex: 1;">
                                    <h3 style="color: ${color}">Step ${stage.stage_id}: ${stage.name}</h3>
                                    <p style="color: var(--text-2); font-size: 14px; margin-top: 4px;">${stage.simple_explanation}</p>
                                </div>
                                <div class="badge" style="background: ${color}22; color: ${color}; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700;">
                                    ${isDone ? this.t('stage_done') : `+${stage.xp_reward} XP`}
                                </div>
                            </div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }

    showStageDetail(stage) {
        // Simple overlay
        const overlay = document.createElement('div');
        overlay.style = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);';
        overlay.innerHTML = `
            <div class="card glass-card" style="width: 90%; max-width: 700px; max-height: 90vh; overflow-y: auto; position: relative;">
                <button onclick="this.parentElement.parentElement.remove()" style="position: absolute; right: 20px; top: 20px; background: none; border: none; color: var(--text-1); font-size: 24px; cursor: pointer;">✕</button>
                <div style="text-align: center; margin-bottom: 30px;">
                    <div style="font-size: 80px;">${stage.emoji}</div>
                    <h2>${stage.name}</h2>
                </div>
                
                <h4 style="color: var(--primary)">Detailed Explanation</h4>
                <p style="margin: 10px 0 25px; line-height: 1.6;">${stage.detailed_explanation}</p>
                
                <h4 style="color: var(--secondary)">Why It Matters</h4>
                <p style="margin: 10px 0 25px; line-height: 1.6;">${stage.why_it_matters}</p>
                
                <div style="background: var(--surface-3); padding: 20px; border-radius: 15px; margin-bottom: 30px;">
                    <h4 style="color: var(--accent)">Common Doubt</h4>
                    <p style="font-style: italic; margin-top: 10px;"><strong>Q:</strong> ${stage.common_doubt_q}</p>
                    <p style="margin-top: 10px;"><strong>A:</strong> ${stage.common_doubt_a}</p>
                </div>

                <button class="btn btn-primary" style="width: 100%" onclick="app.completeStage(${stage.stage_id}, '${stage.name}', ${stage.xp_reward})">
                    Mark as Learned (+${stage.xp_reward} XP)
                </button>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    async completeStage(id, name, xp) {
        await fetch('/api/learning/explore', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stage_id: id, stage_name: name })
        });
        await this.addXP(xp);
        document.querySelector('[style*="z-index: 1000"]').remove();
        this.renderLearnScreen();
    }

    async renderQuizScreen() {
        const res = await fetch('/api/quiz/data');
        const flatData = await res.json();
        
        // Group by category
        const quizData = {};
        flatData.forEach(q => {
            if (!quizData[q.cat]) quizData[q.cat] = [];
            quizData[q.cat].push(q);
        });
        
        const categories = Object.keys(quizData);

        this.screenContainer.innerHTML = `
            <div class="screen-header">
                <h1>${this.t('quiz_title')}</h1>
                <p style="color: var(--text-2)">Select a category and test your knowledge!</p>
            </div>
            <div class="grid-2" style="margin-top: 30px;">
                ${categories.map(cat => `
                    <div class="card glass-card" onclick="app.startQuiz('${cat}')">
                        <h3>${cat}</h3>
                        <p style="color: var(--text-2); margin-top: 5px;">${quizData[cat].length} Questions</p>
                    </div>
                `).join('')}
            </div>
        `;
    }

    async startQuiz(category) {
        const res = await fetch('/api/quiz/data');
        const flatData = await res.json();
        const questions = flatData.filter(q => q.cat === category);
        let currentIdx = 0;
        let score = 0;

        const renderQuestion = () => {
            const q = questions[currentIdx];
            this.screenContainer.innerHTML = `
                <div class="card glass-card" style="padding: 40px; margin-top: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <p style="color: var(--text-3)">Question ${currentIdx + 1} of ${questions.length}</p>
                        <span class="badge" style="background: var(--surface-3)">${category}</span>
                    </div>
                    <h2 style="margin: 20px 0; line-height: 1.4;">${this.l(q, 'q')}</h2>
                    <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 30px;">
                        ${q.opts.map((opt, i) => {
                            const optText = q[`opts_${this.currentLang}`] ? q[`opts_${this.currentLang}`][i] : opt;
                            return `<button class="btn btn-outline" style="text-align: left; justify-content: flex-start; padding: 15px 20px;" onclick="window.checkQuizAnswer(${i})">${optText}</button>`;
                        }).join('')}
                    </div>
                </div>
            `;
        };

        window.checkQuizAnswer = async (idx) => {
            const q = questions[currentIdx];
            if (idx === q.correct) {
                score++;
                this.showToast('Correct! 🎯', 'success');
            } else {
                this.showToast(`Wrong! ${this.l(q, 'exp')}`, 'error');
            }

            if (currentIdx < questions.length - 1) {
                currentIdx++;
                renderQuestion();
            } else {
                this.finishQuiz(category, score, questions.length);
            }
        };

        renderQuestion();
    }

    async finishQuiz(category, score, total) {
        const xp = score * 10;
        await fetch('/api/quiz/save', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category, score, total, xp })
        });
        await this.addXP(xp);
        
        this.screenContainer.innerHTML = `
            <div class="card glass-card" style="text-align: center; padding: 60px; margin-top: 40px;">
                <h1 style="font-size: 48px;">${score === total ? '🎉' : '🎯'}</h1>
                <h2 style="margin: 20px 0;">Quiz Completed!</h2>
                <p style="font-size: 24px; color: var(--primary);">${this.t('quiz_score', { s: score, t: total })}</p>
                <p style="color: var(--text-2); margin-top: 10px;">${this.t('quiz_xp_earned', { xp })}</p>
                <button class="btn btn-primary" style="margin-top: 40px;" onclick="app.switchScreen('quiz')">Finish</button>
            </div>
        `;
    }

    renderTypesScreen() {
        const types = [
            { id: 'ls', emoji: '🏛️', color: 'var(--primary)' },
            { id: 'vs', emoji: '🏰', color: 'var(--accent)' },
            { id: 'rs', emoji: '📜', color: 'var(--secondary)' },
            { id: 'lb', emoji: '🏘️', color: 'var(--warning)' },
            { id: 'be', emoji: '🔄', color: 'var(--success)' }
        ];

        this.screenContainer.innerHTML = `
            <div class="screen-header">
                <h1>🏰 ${this.t('nav_types')}</h1>
                <p style="color: var(--text-2)">${this.t('learn_subtitle')}</p>
            </div>
            <div class="grid-1" style="margin-top: 30px; display: grid; gap: 15px;">
                ${types.map(type => `
                    <div class="card glass-card" style="border-left: 5px solid ${type.color};" onclick="app.showTypeDetail('${type.id}', '${type.emoji}', '${type.color}')">
                        <div style="display: flex; align-items: center; gap: 20px;">
                            <div style="font-size: 40px;">${type.emoji}</div>
                            <div style="flex: 1;">
                                <h3 style="color: ${type.color}">${this.t(`type_${type.id}_name`)}</h3>
                                <p style="color: var(--text-2); font-size: 14px; margin-top: 4px;">${this.t(`type_${type.id}_desc`)}</p>
                            </div>
                            <button class="btn btn-outline" style="border-radius: 50%; width: 40px; height: 40px; padding: 0; justify-content: center;">→</button>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    showTypeDetail(id, emoji, color) {
        const overlay = document.createElement('div');
        overlay.style = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);';
        overlay.innerHTML = `
            <div class="card glass-card" style="width: 90%; max-width: 500px; text-align: left; padding: 40px; border-top: 8px solid ${color}">
                <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                    <div style="font-size: 48px;">${emoji}</div>
                    <h2 style="color: ${color}">${this.t(`type_${id}_name`)}</h2>
                </div>
                <p style="font-size: 16px; line-height: 1.6; color: var(--text-1);">${this.t(`type_${id}_detail`)}</p>
                <button class="btn btn-primary" style="width: 100%; margin-top: 30px;" onclick="this.parentElement.parentElement.remove()">Close</button>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    renderSimulatorScreen() {
        const steps = [
            { title: "Before You Go", emoji: "🏠", desc: "Check your name on Electoral Roll, find your booth, and keep your Voter ID ready.", action: "Do you have your ID?", choices: ["Yes, I'm ready!", "No, I'll go without ID"], correct: 0, wrong: "Wait! You cannot vote without a valid ID." },
            { title: "At the Polling Station", emoji: "🏢", desc: "Identify your booth from the list outside, join the correct queue.", action: "Where do you go?", choices: ["Any booth", "My assigned booth"], correct: 1, wrong: "Each voter is assigned a specific booth." },
            { title: "Queue & Verification", emoji: "👨‍👩‍👧‍👦", desc: "First polling officer checks your name and verifies your photo ID.", action: "Present your document...", choices: ["Show ID", "Argue about the list"], correct: 0, wrong: "Cooperation is key." },
            { title: "Indelible Ink", emoji: "☝️", desc: "Second polling officer applies indelible ink to your left index finger.", action: "Extend your finger...", choices: ["Accept the ink", "Refuse the ink"], correct: 0, wrong: "The ink is mandatory to prevent multiple voting." },
            { title: "At the EVM", emoji: "🗳️", desc: "Go to the voting compartment. Press the blue button for your candidate.", action: "Cast your vote...", choices: ["Press blue button", "Take a photo"], correct: 0, wrong: "Photography is strictly prohibited." },
            { title: "VVPAT Verification", emoji: "📄", desc: "Watch the VVPAT slip for 7 seconds to confirm your vote.", action: "Verify the slip...", choices: ["Wait 7 seconds", "Leave immediately"], correct: 0, wrong: "Always verify your vote." },
            { title: "Exit", emoji: "🚪", desc: "Exit the polling station quietly. Your vote is secret.", action: "Leaving the booth...", choices: ["Tell everyone", "Keep it secret"], correct: 1, wrong: "Maintaining a secret ballot is your duty." }
        ];

        let currentStepIdx = 0;

        const renderStep = () => {
            const step = steps[currentStepIdx];
            this.screenContainer.innerHTML = `
                <div class="card glass-card" style="text-align: center; padding: 40px;">
                    <p style="color: var(--text-3)">Step ${currentStepIdx + 1} of 7</p>
                    <div class="progress-container"><div class="progress-bar" style="width: ${((currentStepIdx + 1) / 7) * 100}%"></div></div>
                    <div style="font-size: 80px; margin: 20px 0;">${step.emoji}</div>
                    <h2 style="font-size: 32px;">${step.title}</h2>
                    <p style="margin: 20px 0; font-size: 18px; line-height: 1.6;">${step.desc}</p>
                    <p style="font-weight: 700; color: var(--primary); margin-bottom: 30px;">${step.action}</p>
                    <div style="display: flex; gap: 15px; justify-content: center;">
                        ${step.choices.map((choice, i) => `
                            <button class="btn ${i === 0 ? 'btn-primary' : 'btn-outline'}" onclick="window.checkSimStep(${i})">${choice}</button>
                        `).join('')}
                    </div>
                </div>
            `;
        };

        window.checkSimStep = (idx) => {
            const step = steps[currentStepIdx];
            if (idx === step.correct) {
                this.addXP(15);
                if (currentStepIdx < steps.length - 1) {
                    currentStepIdx++;
                    renderStep();
                } else {
                    this.finishSimulator();
                }
            } else {
                alert(step.wrong);
            }
        };

        renderStep();
    }

    async finishSimulator() {
        await fetch('/api/badges/earn', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ badge_id: 'voter_ready' }) });
        this.addXP(100);
        this.showToast('Voter Ready Badge Earned! 🏅', 'success');
        this.switchScreen('home');
    }

    renderChatScreen() { 
        this.screenContainer.innerHTML = `
            <div class="screen-header">
                <h1>🤖 ${this.t('chatbot_title')}</h1>
                <p style="color: var(--text-2)">${this.t('chatbot_disclaimer')}</p>
            </div>
            <div class="card glass-card" style="height: 500px; display: flex; flex-direction: column; margin-top: 30px;">
                <div id="chat-messages" style="flex: 1; overflow-y: auto; padding: 20px; display: flex; flex-direction: column; gap: 15px;">
                    <div class="msg bot" style="background: var(--surface-3); padding: 12px 18px; border-radius: 15px; align-self: flex-start; max-width: 80%;">
                        Namaste! I am your JanMitra Assistant. How can I help you today?
                    </div>
                </div>
                <div style="padding: 20px; border-top: 1px solid var(--border); display: flex; gap: 10px;">
                    <input type="text" id="chat-input" placeholder="${this.t('chatbot_placeholder')}" style="flex: 1; background: var(--surface-2); border: 1px solid var(--border); border-radius: 12px; padding: 0 15px; color: var(--text-1);">
                    <button class="btn btn-primary" onclick="app.sendMessage()">${this.t('chatbot_send')}</button>
                </div>
            </div>
        `;
    }

    async sendMessage() {
        const input = document.getElementById('chat-input');
        const msg = input.value.trim();
        if (!msg) return;
        
        const container = document.getElementById('chat-messages');
        container.innerHTML += `<div class="msg user" style="background: var(--primary); color: white; padding: 12px 18px; border-radius: 15px; align-self: flex-end; max-width: 80%; box-shadow: 0 4px 15px rgba(168, 85, 247, 0.2);">${msg}</div>`;
        input.value = '';
        container.scrollTop = container.scrollHeight;
        
        // Show typing indicator
        const typingId = 'typing-' + Date.now();
        const typingHtml = `<div id="${typingId}" class="msg bot" style="background: var(--surface-3); padding: 12px 18px; border-radius: 15px; align-self: flex-start; max-width: 80%; font-style: italic; color: var(--text-3);">JanMitra is thinking...</div>`;
        container.insertAdjacentHTML('beforeend', typingHtml);
        container.scrollTop = container.scrollHeight;

        try {
            const res = await fetch('/api/chat/faq');
            const faqs = await res.json();
            
            let answer = "I'm sorry, I couldn't find a specific answer to that. I'm a specialized election assistant, so try asking about things like 'voter registration', 'EVM security', 'VVPAT', or 'how to find my polling booth'.";
            
            const lowerMsg = msg.toLowerCase();
            let bestMatch = null;
            let highestScore = 0;

            for (const faq of faqs) {
                let currentScore = 0;
                
                // Match keywords (highest priority)
                if (faq.keywords) {
                    faq.keywords.forEach(kw => {
                        if (lowerMsg.includes(kw.toLowerCase())) currentScore += 5;
                    });
                }
                
                // Match question words
                const qWords = faq.question.toLowerCase().split(' ');
                qWords.forEach(w => {
                    if (w.length > 3 && lowerMsg.includes(w)) currentScore += 2;
                });

                if (currentScore > highestScore) {
                    highestScore = currentScore;
                    bestMatch = faq;
                }
            }

            if (bestMatch && highestScore >= 3) {
                answer = bestMatch.answer;
            }

            // Small delay to simulate AI processing
            setTimeout(() => {
                const typingEl = document.getElementById(typingId);
                if (typingEl) typingEl.remove();
                
                container.innerHTML += `<div class="msg bot" style="background: var(--surface-3); padding: 12px 18px; border-radius: 15px; align-self: flex-start; max-width: 80%; border-left: 3px solid var(--primary); line-height: 1.5;">${answer}</div>`;
                container.scrollTop = container.scrollHeight;
            }, 800);

        } catch (err) {
            console.error('Chat error:', err);
            const typingEl = document.getElementById(typingId);
            if (typingEl) typingEl.remove();
            this.showToast('Connection to assistant failed', 'error');
        }
    }

    async renderLiveScreen() {
        const res = await fetch('/api/live-data');
        const data = await res.json();
        
        this.screenContainer.innerHTML = `
            <div class="screen-header">
                <h1>📈 ${this.t('live_title')}</h1>
                <p style="color: var(--text-2)">${this.t('live_last_updated', { t: data.last_updated })}</p>
            </div>
            <div class="live-list" style="margin-top: 30px; display: grid; gap: 20px;">
                ${data.updates.map(update => `
                    <div class="card glass-card" ${update.url ? `onclick="window.open('${update.url}', '_blank')"` : ''} style="${update.url ? 'cursor: pointer;' : ''}">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <span style="background: var(--primary); padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700;">${update.election_type}</span>
                            <span style="color: var(--text-3); font-size: 12px;">${update.date}</span>
                        </div>
                        <h3 style="margin: 12px 0 8px;">${update.state} ${update.source ? `- ${update.source}` : 'Election'}</h3>
                        <p style="color: var(--text-2); font-size: 14px; line-height: 1.5;">${update.description}</p>
                        ${update.status ? `<div style="margin-top: 10px; font-size: 12px; color: var(--text-3);">Status: <span style="color: ${update.status === 'Completed' ? 'var(--success)' : 'var(--warning)'}">${update.status}</span></div>` : ''}
                        ${update.url ? `<p style="margin-top: 10px; color: var(--primary); font-size: 12px;">Read full article ↗</p>` : ''}
                    </div>
                `).join('')}
            </div>
        `;
    }

    async renderMythScreen() {
        const res = await fetch('/api/learning/myths');
        const myths = await res.json();
        
        this.screenContainer.innerHTML = `
            <div class="screen-header">
                <h1>💥 ${this.t('myth_title')}</h1>
                <p style="color: var(--text-2)">Debunking common election misconceptions.</p>
            </div>
            <div class="grid-2" style="margin-top: 30px;">
                ${myths.map(m => `
                    <div class="card glass-card" onclick="app.showMythDetail(${JSON.stringify(m).replace(/"/g, '&quot;')})">
                        <h4 style="color: var(--error)">Myth: ${this.l(m, 'myth')}</h4>
                        <p style="margin-top: 10px; color: var(--text-2); font-size: 14px;">Click to reveal fact...</p>
                    </div>
                `).join('')}
            </div>
        `;
    }

    showMythDetail(m) {
        const overlay = document.createElement('div');
        overlay.style = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 1000; display: flex; justify-content: center; align-items: center; backdrop-filter: blur(5px);';
        overlay.innerHTML = `
            <div class="card glass-card" style="width: 90%; max-width: 500px; text-align: center; padding: 40px;">
                <h2 style="color: var(--error)">Myth</h2>
                <p style="font-size: 18px; margin: 15px 0 30px;">${this.l(m, 'myth')}</p>
                <div style="font-size: 48px;">💥</div>
                <h2 style="color: var(--success); margin-top: 30px;">Fact</h2>
                <p style="font-size: 18px; margin-top: 15px; line-height: 1.6;">${this.l(m, 'fact')}</p>
                <button class="btn btn-primary" style="width: 100%; margin-top: 40px;" onclick="this.parentElement.parentElement.remove()">I Understand</button>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    async renderGlossaryScreen() {
        const res = await fetch('/api/learning/glossary');
        const glossary = await res.json();
        
        this.screenContainer.innerHTML = `
            <div class="screen-header">
                <h1>📖 ${this.t('glossary_title')}</h1>
                <input type="text" id="glossary-search" oninput="app.searchGlossary()" placeholder="${this.t('glossary_search')}" class="card" style="width: 100%; margin-top: 20px; background: var(--surface-2); border: 1px solid var(--border); padding: 15px 20px; color: var(--text-1); border-radius: 15px;">
            </div>
            <div id="glossary-list" style="margin-top: 30px; display: grid; gap: 15px;">
                ${glossary.map(item => `
                    <div class="card glossary-item">
                        <h3>${this.l(item, 'term')}</h3>
                        <p style="color: var(--text-2); margin-top: 8px;">${this.l(item, 'definition')}</p>
                    </div>
                `).join('')}
            </div>
        `;
    }

    async searchGlossary() {
        const query = document.getElementById('glossary-search').value.toLowerCase();
        const res = await fetch('/api/learning/glossary');
        const glossary = await res.json();
        const filtered = glossary.filter(item => 
            item.term.toLowerCase().includes(query) || 
            item.definition.toLowerCase().includes(query)
        );
        
        const list = document.getElementById('glossary-list');
        list.innerHTML = filtered.map(item => `
            <div class="card glossary-item">
                <h3>${item.term}</h3>
                <p style="color: var(--text-2); margin-top: 8px;">${item.definition}</p>
            </div>
        `).join('');
    }

    async renderRegistrationScreen() {
        this.screenContainer.innerHTML = `
            <div class="screen-header">
                <h1>📝 Voter ID Registration</h1>
                <p style="color: var(--text-2)">Follow these steps to register yourself as a voter in India.</p>
            </div>
            
            <div class="registration-steps" style="margin-top: 30px; display: grid; gap: 20px;">
                <div class="card glass-card" style="display: flex; gap: 20px; align-items: flex-start;">
                    <div class="badge" style="background: var(--primary); padding: 8px 15px; border-radius: 50%; font-weight: 700;">1</div>
                    <div>
                        <h3>Check Eligibility</h3>
                        <p style="color: var(--text-2); margin-top: 5px;">You must be an Indian citizen and 18 years of age on the qualifying date (Jan 1, Apr 1, Jul 1, Oct 1).</p>
                    </div>
                </div>

                <div class="card glass-card" style="display: flex; gap: 20px; align-items: flex-start;">
                    <div class="badge" style="background: var(--secondary); padding: 8px 15px; border-radius: 50%; font-weight: 700;">2</div>
                    <div>
                        <h3>Gather Documents</h3>
                        <p style="color: var(--text-2); margin-top: 5px;">Keep a passport-sized photo, age proof (Birth certificate, 10th marksheet), and address proof (Aadhaar, Ration card, Passport) ready.</p>
                    </div>
                </div>

                <div class="card glass-card" style="display: flex; gap: 20px; align-items: flex-start;">
                    <div class="badge" style="background: var(--accent); padding: 8px 15px; border-radius: 50%; font-weight: 700;">3</div>
                    <div>
                        <h3>Fill Form 6</h3>
                        <p style="color: var(--text-2); margin-top: 5px;">Visit the <strong>voters.eci.gov.in</strong> portal or download the <strong>Voter Helpline App</strong> and select 'New Voter Registration'.</p>
                    </div>
                </div>

                <div class="card glass-card" style="display: flex; gap: 20px; align-items: flex-start;">
                    <div class="badge" style="background: var(--success); padding: 8px 15px; border-radius: 50%; font-weight: 700;">4</div>
                    <div>
                        <h3>Verification</h3>
                        <p style="color: var(--text-2); margin-top: 5px;">A Booth Level Officer (BLO) will visit your residence to verify your documents and address.</p>
                    </div>
                </div>

                <div class="card glass-card" style="display: flex; gap: 20px; align-items: flex-start;">
                    <div class="badge" style="background: var(--gold); padding: 8px 15px; border-radius: 50%; font-weight: 700;">5</div>
                    <div>
                        <h3>EPIC Generation</h3>
                        <p style="color: var(--text-2); margin-top: 5px;">Once verified, your Voter ID (EPIC) will be generated and sent via speed post.</p>
                    </div>
                </div>

                <div style="text-align: center; margin-top: 20px;">
                    <a href="https://voters.eci.gov.in" target="_blank" class="btn btn-primary" style="display: inline-block; text-decoration: none;">Register Now on NVSP Portal →</a>
                </div>
            </div>
        `;
    }

    renderLinksScreen() {
        const links = [
            { name: "Election Commission of India (ECI)", url: "https://eci.gov.in", desc: "Main website of the Election Commission." },
            { name: "Voters' Service Portal (NVSP)", url: "https://voters.eci.gov.in", desc: "Portal for registration, address change, and Voter ID downloads." },
            { name: "Electoral Search", url: "https://electoralsearch.eci.gov.in", desc: "Search your name in the Voter List across India." },
            { name: "cVigil App Portal", url: "https://cvigil.eci.gov.in", desc: "Platform to report election code violations." },
            { name: "ECI Results Portal", url: "https://results.eci.gov.in", desc: "Live election results and trends." },
            { name: "Voter Helpline (Android)", url: "https://play.google.com/store/apps/details?id=com.webcontent.voterhelpline", desc: "Official Android app for voters." }
        ];

        this.screenContainer.innerHTML = `
            <div class="screen-header">
                <h1>🔗 Official Resources</h1>
                <p style="color: var(--text-2)">Direct links to official ECI websites and portals.</p>
            </div>
            <div class="grid-2" style="margin-top: 30px;">
                ${links.map(link => `
                    <a href="${link.url}" target="_blank" style="text-decoration: none; color: inherit;">
                        <div class="card" style="height: 100%; transition: transform 0.2s; border-top: 4px solid var(--primary);">
                            <h3 style="color: var(--primary)">${link.name}</h3>
                            <p style="color: var(--text-2); margin-top: 10px; font-size: 14px;">${link.desc}</p>
                            <p style="margin-top: 15px; color: var(--text-3); font-size: 12px;">Visit Website ↗</p>
                        </div>
                    </a>
                `).join('')}
            </div>
        `;
    }

    async renderProfileScreen() {
        const badgesRes = await fetch('/api/badges');
        const earnedBadges = await badgesRes.json();
        
        // Find badge details
        const badges = this.config.badges.filter(b => earnedBadges.includes(b.id));

        this.screenContainer.innerHTML = `
            <div class="screen-header">
                <h1>👤 ${this.t('profile_title')}</h1>
            </div>
            <div class="card glass-card" style="margin-top: 30px; text-align: center;">
                <div style="font-size: 80px; margin-bottom: 10px;">👤</div>
                <h2>${this.profile.name}</h2>
                <p style="color: var(--text-2)">${this.profile.user_type}</p>
                
                <div class="grid-3" style="margin-top: 40px;">
                    <div>
                        <h4 style="color: var(--text-3)">TOTAL XP</h4>
                        <p style="font-size: 24px; font-weight: 700; color: var(--primary);">${this.profile.xp}</p>
                    </div>
                    <div>
                        <h4 style="color: var(--text-3)">STREAK</h4>
                        <p style="font-size: 24px; font-weight: 700; color: var(--secondary);">${this.profile.streak || 0} Days</p>
                    </div>
                    <div>
                        <h4 style="color: var(--text-3)">LEVEL</h4>
                        <p style="font-size: 24px; font-weight: 700; color: var(--gold);">${Math.floor(this.profile.xp / 100) + 1}</p>
                    </div>
                </div>

                <div style="margin-top: 40px; text-align: left;">
                    <h3 style="margin-bottom: 20px;">🏅 ${this.t('badges_label')}</h3>
                    <div style="display: flex; gap: 15px; flex-wrap: wrap;">
                        ${badges.map(b => `
                            <div class="card" title="${b.desc}" style="padding: 10px; width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; font-size: 30px; border-radius: 50%;">
                                ${b.emoji}
                            </div>
                        `).join('')}
                        ${badges.length === 0 ? '<p style="color: var(--text-3)">No badges earned yet. Complete quizzes to earn them!</p>' : ''}
                    </div>
                </div>
            </div>
        `;
    }

    renderSettingsScreen() {
        this.screenContainer.innerHTML = `
            <div class="screen-header">
                <h1>⚙️ ${this.t('settings_title')}</h1>
            </div>
            <div class="card" style="margin-top: 30px;">
                <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 20px; border-bottom: 1px solid var(--border);">
                    <div>
                        <h3>${this.t('settings_theme')}</h3>
                        <p style="color: var(--text-3)">Toggle dark/light mode</p>
                    </div>
                    <button class="btn btn-outline" onclick="app.toggleTheme()">
                        ${this.profile.theme === 'light' ? '🌙 Dark Mode' : '☀️ Light Mode'}
                    </button>
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 20px;">
                    <div>
                        <h3 style="color: var(--error)">${this.t('settings_reset')}</h3>
                        <p style="color: var(--text-3)">Clear all progress and data</p>
                    </div>
                    <button class="btn btn-outline" style="border-color: var(--error); color: var(--error)" onclick="app.resetData()">Reset Everything</button>
                </div>
            </div>
        `;
    }

    async toggleTheme() {
        const newTheme = this.profile.theme === 'light' ? 'dark' : 'light';
        this.profile.theme = newTheme;
        this.applyTheme(newTheme);
        await fetch('/api/profile', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ theme: newTheme })
        });
        this.renderSettingsScreen();
    }

    async changeLanguage(langCode) {
        // Feature disabled as per user request
        console.log('Language switching is disabled.');
    }

    async resetData() {
        if (confirm('Are you sure? This will delete all your progress!')) {
            await fetch('/api/reset', { method: 'POST' });
            location.reload();
        }
    }
}

const app = new JanMitraApp();

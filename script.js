// Initialize AOS (Animate On Scroll)
AOS.init({
    duration: 900,
    once: true,
    easing: 'ease-out-cubic'
});

// Interactive Neural Network Particle Canvas
const canvas = document.getElementById('neural-canvas');
if (canvas) {
    const ctx = canvas.getContext('2d');
    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const particleCount = Math.min(Math.floor(width / 15), 65);
    let mouse = { x: null, y: null, radius: 160 };

    window.addEventListener('mousemove', (e) => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
    });

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * 0.7;
            this.vy = (Math.random() - 0.5) * 0.7;
            this.radius = Math.random() * 2 + 1;
            this.color = Math.random() > 0.5 ? '#6366f1' : '#06b6d4';
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.shadowBlur = 8;
            ctx.shadowColor = this.color;
            ctx.fill();
            ctx.shadowBlur = 0;
        }

        update() {
            this.x += this.vx;
            this.y += this.vy;

            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;

            if (mouse.x && mouse.y) {
                let dx = mouse.x - this.x;
                let dy = mouse.y - this.y;
                let dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < mouse.radius) {
                    let angle = Math.atan2(dy, dx);
                    let force = (mouse.radius - dist) / mouse.radius;
                    this.x -= Math.cos(angle) * force * 2;
                    this.y -= Math.sin(angle) * force * 2;
                }
            }
        }
    }

    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    function animateParticles() {
        ctx.clearRect(0, 0, width, height);

        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();

            for (let j = i + 1; j < particles.length; j++) {
                let dx = particles[i].x - particles[j].x;
                let dy = particles[i].y - particles[j].y;
                let dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 120) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(99, 102, 241, ${1 - dist / 120})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animateParticles);
    }
    animateParticles();
}

// Dynamic Typewriter Effect for Hero Section
const typewriterElement = document.getElementById('typewriter');
if (typewriterElement) {
    const roles = [
        "AI & Machine Learning Engineer",
        "Computer Vision Specialist (YOLOv8)",
        "Data Analytics & ML Intern",
        "Python Full Stack Developer"
    ];
    let roleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;

    function type() {
        const currentRole = roles[roleIndex];
        if (isDeleting) {
            typewriterElement.textContent = currentRole.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typewriterElement.textContent = currentRole.substring(0, charIndex + 1);
            charIndex++;
        }

        let speed = isDeleting ? 35 : 75;

        if (!isDeleting && charIndex === currentRole.length) {
            speed = 2200;
            isDeleting = true;
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            roleIndex = (roleIndex + 1) % roles.length;
            speed = 350;
        }

        setTimeout(type, speed);
    }
    type();
}

// Cursor Ambient Glow Tracking
const cursorGlow = document.querySelector('.cursor-glow');
document.addEventListener('mousemove', (e) => {
    if (cursorGlow) {
        cursorGlow.style.left = e.clientX + 'px';
        cursorGlow.style.top = e.clientY + 'px';
    }
});

// Top Scroll Progress Bar & Nav Blur
const progressBar = document.getElementById('scroll-progress');
const scrollTopBtn = document.getElementById('scroll-top');
const glassNav = document.querySelector('.glass-nav');

window.addEventListener('scroll', () => {
    if (progressBar) {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    }

    if (scrollTopBtn) {
        if (window.scrollY > 400) {
            scrollTopBtn.classList.add('visible');
        } else {
            scrollTopBtn.classList.remove('visible');
        }
    }

    if (glassNav) {
        if (window.scrollY > 100) {
            glassNav.style.background = 'rgba(3, 7, 18, 0.9)';
            glassNav.style.boxShadow = '0 10px 30px rgba(0, 0, 0, 0.5)';
        } else {
            glassNav.style.background = 'rgba(3, 7, 18, 0.75)';
            glassNav.style.boxShadow = 'none';
        }
    }
});

if (scrollTopBtn) {
    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Mobile Navigation Logic
const mobileToggle = document.querySelector('.mobile-toggle');
const mobileClose = document.querySelector('.mobile-close');
const mobileNav = document.querySelector('.mobile-nav');
const mobileLinks = document.querySelectorAll('.mobile-link');

if (mobileToggle && mobileNav) {
    mobileToggle.addEventListener('click', () => {
        mobileNav.classList.add('active');
    });
}

if (mobileClose && mobileNav) {
    mobileClose.addEventListener('click', () => {
        mobileNav.classList.remove('active');
    });
}

mobileLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (mobileNav) mobileNav.classList.remove('active');
    });
});

// Copy to Clipboard Utility with Toast Alert
const copyBtns = document.querySelectorAll('.copy-btn');
const toast = document.getElementById('toast');

copyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const textToCopy = btn.getAttribute('data-copy');
        if (textToCopy) {
            navigator.clipboard.writeText(textToCopy).then(() => {
                showToast(`Copied "${textToCopy}" to clipboard!`);
            }).catch(() => {
                showToast(`Copied!`);
            });
        }
    });
});

function showToast(message) {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2800);
}

// Project Filter Tabs Logic
const filterBtns = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-full-card');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        const filter = btn.getAttribute('data-filter');

        projectCards.forEach(card => {
            const category = card.getAttribute('data-category');
            if (filter === 'all' || filter === category) {
                card.style.display = 'flex';
                card.style.opacity = '1';
            } else {
                card.style.display = 'none';
            }
        });
    });
});

// Project Detail Modals System
const modalTriggerBtns = document.querySelectorAll('.open-modal-btn');
const modals = document.querySelectorAll('.modal');
const modalCloseBtns = document.querySelectorAll('.modal-close');

modalTriggerBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const modalId = btn.getAttribute('data-modal');
        const targetModal = document.getElementById(modalId);
        if (targetModal) {
            targetModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    });
});

modalCloseBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const activeModal = btn.closest('.modal');
        if (activeModal) {
            activeModal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    });
});

modals.forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.remove('active');
            document.body.style.overflow = 'auto';
        }
    });
});

// Interactive Gallery Tabs inside Modals
const galleryTabs = document.querySelectorAll('.g-tab');
galleryTabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const parentModal = tab.closest('.modal');
        if (!parentModal) return;

        const siblings = parentModal.querySelectorAll('.g-tab');
        siblings.forEach(s => s.classList.remove('active'));
        tab.classList.add('active');

        const targetId = tab.getAttribute('data-target');
        const slides = parentModal.querySelectorAll('.g-slide');
        slides.forEach(slide => slide.classList.remove('active'));

        const targetSlide = parentModal.querySelector(`#${targetId}`);
        if (targetSlide) {
            targetSlide.classList.add('active');
        }
    });
});

// Contact Form Handler
const contactForm = document.getElementById('contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const name = document.getElementById('name').value;
        showToast(`Thank you, ${name}! Your message has been sent successfully.`);
        contactForm.reset();
    });
}

// ==========================================
// Ask Nithya's AI Chatbot Assistant Engine
// ==========================================
const aiChatBtn = document.getElementById('ai-chat-toggle');
const aiChatWindow = document.getElementById('ai-chat-window');
const chatCloseBtn = document.getElementById('chat-close-btn');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');
const suggestBtns = document.querySelectorAll('.suggest-btn');

if (aiChatBtn && aiChatWindow) {
    aiChatBtn.addEventListener('click', () => {
        aiChatWindow.classList.toggle('active');
    });
}

if (chatCloseBtn && aiChatWindow) {
    chatCloseBtn.addEventListener('click', () => {
        aiChatWindow.classList.remove('active');
    });
}

suggestBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const question = btn.textContent.trim();
        handleUserQuestion(question);
    });
});

if (chatForm) {
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = chatInput.value.trim();
        if (text) {
            handleUserQuestion(text);
            chatInput.value = '';
        }
    });
}

function handleUserQuestion(query) {
    appendMessage(query, 'user');
    const response = getAiResponse(query.toLowerCase());

    setTimeout(() => {
        appendMessage(response, 'bot');
    }, 400);
}

function appendMessage(text, sender) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    msgDiv.innerHTML = text;
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getAiResponse(q) {
    if (q.includes('fine') || q.includes('email') || q.includes('anpr') || q.includes('gate') || q.includes('violation')) {
        return "🚨 <strong>Gate ANPR & E-Fine Invoice System</strong>:<br>When level crossing gate barriers are closed, vehicles attempting to cross bend under the gate trigger ANPR OCR. The captured license plate queries the registry email ID and automatically dispatches an E-Fine invoice to pay!";
    }
    if (q.includes('udid') || q.includes('voice') || q.includes('disabled') || q.includes('driver') || q.includes('accept') || q.includes('reject') || q.includes('portal')) {
        return "🚌 <strong>4-Role Smart Bus Portals</strong>:<br>1. <strong>Passenger</strong>: Live GPS Map & 3-Color Crowd Indicator (🟢 Seats Available, 🟡 Light Crowd, 🔴 Overcrowded)<br>2. <strong>Disabled Person</strong>: UDID Card login & pyttsx3 voice navigation request<br>3. <strong>Driver</strong>: Live pickup request Accept/Confirm or Reject console<br>4. <strong>Admin</strong>: Fleet management Analytics";
    }
    if (q.includes('pre-check') || q.includes('mechanical') || q.includes('train part') || q.includes('fault') || q.includes('pre-departure') || q.includes('locopilot')) {
        return "🚂 <strong>Train Mechanical Pre-Inspection & Locopilot EAR</strong>:<br>Scans train mechanical components (brakes, couplers) before departure and alerts mobile before start! Also monitors train driver (Locopilot) Eye Aspect Ratio (EAR) for drowsiness!";
    }
    if (q.includes('calendar') || q.includes('date') || q.includes('gold') || q.includes('plotly')) {
        return "💰 <strong>Gold Rate Calendar Predictor</strong>:<br>Pick any target date on the Streamlit calendar date-picker to forecast per-gram gold rates powered by degree-3 Polynomial Regression and Plotly trend graphs!";
    }
    if (q.includes('video') || q.includes('reel') || q.includes('demo') || q.includes('screen')) {
        return "🖼️ <strong>Live Project Image Reels</strong>:<br>Hover over any project box to watch output image reels cycle automatically! Click <strong>'Architecture & Module Outputs'</strong> to explore the full architecture diagram and module outputs!";
    }
    if (q.includes('arch') || q.includes('diagram') || q.includes('module') || q.includes('output') || q.includes('screenshot')) {
        return "🏗️ Each project includes an <strong>Architecture Diagram Flowchart</strong> & <strong>Module Outputs</strong>!<br>Click on any project's <strong>'Architecture & Module Outputs'</strong> button to explore!";
    }
    if (q.includes('intern') || q.includes('experience') || q.includes('cognifyz') || q.includes('nlc') || q.includes('full stack') || q.includes('fullstack')) {
        return "💼 <strong>Nithyasri's Internships</strong>:<br>1. <strong>ML Intern @ NLC India Ltd</strong> (Time-Series & Forecasting)<br>2. <strong>Data Analysis Intern @ Cognifyz Technologies</strong> (EDA & Business Intelligence)<br>3. <strong>Python Full Stack Intern</strong> (Web Apps, Flask/FastAPI, Databases)";
    }
    if (q.includes('nptel') || q.includes('certif') || q.includes('cloud') || q.includes('nlp') || q.includes('language processing')) {
        return "📜 <strong>Certifications & NPTEL Courses</strong>:<br>• <strong>NPTEL Cloud Computing</strong><br>• <strong>NPTEL Natural Language Processing (NLP)</strong><br>• <strong>NPTEL Python Programming</strong> (86% Elite)<br>• Gen AI in Data Analytics<br>• English Typewriting Junior (First Class with Distinction)";
    }
    if (q.includes('tech') || q.includes('stack') || q.includes('tool') || q.includes('language') || q.includes('library')) {
        return "🛠️ <strong>Technology Stack</strong>:<br>• <strong>Languages</strong>: Python, SQL, HTML, CSS, JS<br>• <strong>ML, Vision & NLP</strong>: YOLOv8, OpenCV, Scikit-learn, XGBoost, Random Forest, MediaPipe, DeepSORT, DeepLabV3, NLP, Speech AI (Whisper)<br>• <strong>Frameworks & Cloud</strong>: FastAPI, Streamlit, Flask, Firebase, MySQL, MongoDB";
    }
    if (q.includes('cgpa') || q.includes('college') || q.includes('education') || q.includes('degree')) {
        return "🎓 Nithyasri is pursuing B.Tech in <strong>AI & Data Science</strong> at <strong>Velammal Engineering College, Chennai</strong> (2023–2027) with an <strong>8.07 CGPA</strong>!";
    }
    if (q.includes('project') || q.includes('work') || q.includes('yolo') || q.includes('smartrail') || q.includes('bus') || q.includes('flood') || q.includes('gold')) {
        return "🚀 <strong>AI & Vision Projects</strong>:<br>1. <strong>SmartRailShield</strong> (Pre-Check, Track YOLO, ANPR E-Fine, Locopilot EAR)<br>2. <strong>Tamil Nadu Smart Bus</strong> (4 Portals: Passenger, Disabled UDID/Voice, Driver Accept/Reject, Admin)<br>3. <strong>AI Flood Rescue System</strong> (FastAPI, DeepLabV3, MediaPipe, DeepSORT, Whisper)<br>4. <strong>Gold Rate Prediction</strong> (Polynomial Regression, Calendar Date Picker, Plotly)";
    }
    if (q.includes('award') || q.includes('achievement') || q.includes('prize') || q.includes('hackathon')) {
        return "🏆 <strong>Key Recognition</strong>:<br>• <strong>2nd Prize</strong> in Paper Presentation at Jeppiaar Institute (*Accident Hotspot Prediction*)<br>• <strong>Top 25 out of 150 Teams</strong> in State Hackathon<br>• International Hackathon Finalist at Vel Tech";
    }
    if (q.includes('contact') || q.includes('email') || q.includes('phone') || q.includes('hire') || q.includes('reach')) {
        return "📫 Reach Nithyasri via:<br>📧 <strong>nithyasri482006sri@gmail.com</strong><br>📱 <strong>+91 9363606782</strong><br>🔗 <a href='https://linkedin.com/in/nithyasri-r-03a5932a6' target='_blank' style='color:#6366f1;'>LinkedIn Profile</a>";
    }
    return "😊 Nithyasri is an AI/ML Engineer skilled in Python Full Stack, YOLOv8, Data Analytics, and Cloud/NLP. Feel free to ask about her <strong>Gate E-Fine Email Engine</strong>, <strong>4-Portal Bus System</strong>, <strong>Train Pre-Inspection</strong>, or <strong>Gold Calendar Predictor</strong>!";
}

// ==========================================
// Project Card Hover Image Slideshow Engine
// ==========================================
const slideshowContainers = document.querySelectorAll('.project-hover-slideshow');

const projectModuleTitles = {
    smartrail: [
        "Module 1/4: Train Mechanical Pre-Check",
        "Module 2/4: Railway Track Obstacle Scan",
        "Module 3/4: Gate Violation ANPR & E-Fine",
        "Module 4/4: Locopilot Drowsiness Monitor"
    ],
    smartbus: [
        "1. Passenger Live Map & Crowd Badge",
        "2. Disabled UDID & Voice Navigation",
        "3. Driver Pickup Accept / Reject Console",
        "4. Admin Fleet Master Dashboard"
    ],
    flood: [
        "Module 1/4: DeepLabV3 Water Segmentation",
        "Module 2/4: Pose Distress Tracking (DeepSORT)",
        "Module 3/4: Face Recognition Matching",
        "Module 4/4: Whisper Speech & Folium Map"
    ],
    gold: [
        "Module 1/4: Historical Gold Price EDA",
        "Module 2/4: Polynomial Regression Fitting",
        "Module 3/4: Streamlit Calendar Date Picker",
        "Module 4/4: Plotly Interactive Trends"
    ]
};

slideshowContainers.forEach(container => {
    const slides = container.querySelectorAll('.reel-slide');
    const dots = container.querySelectorAll('.slideshow-dots .dot');
    const statusText = container.querySelector('.slideshow-status');
    const slideshowKey = container.getAttribute('data-slideshow');
    
    if (!slides.length) return;

    let currentIndex = 0;
    let timer = null;

    const moduleTitles = projectModuleTitles[slideshowKey] || [
        "Module 1: Output Preview",
        "Module 2: Feature Detection",
        "Module 3: System Result",
        "Module 4: Dashboard & UI"
    ];

    function showSlide(index) {
        slides.forEach((s, i) => {
            s.classList.toggle('active', i === index);
        });
        dots.forEach((d, i) => {
            d.classList.toggle('active', i === index);
        });
        if (statusText && moduleTitles[index]) {
            statusText.textContent = moduleTitles[index];
        }
    }

    function startCycle() {
        if (timer) clearInterval(timer);
        timer = setInterval(() => {
            currentIndex = (currentIndex + 1) % slides.length;
            showSlide(currentIndex);
        }, 1500);
    }

    function stopCycle() {
        if (timer) {
            clearInterval(timer);
            timer = null;
        }
        currentIndex = 0;
        showSlide(0);
    }

    container.addEventListener('mouseenter', startCycle);
    container.addEventListener('mouseleave', stopCycle);

    const parentCard = container.closest('.project-full-card');
    if (parentCard) {
        parentCard.addEventListener('mouseenter', () => {
            if (!timer) startCycle();
        });
        parentCard.addEventListener('mouseleave', stopCycle);
    }

    // Cursor-driven slide scrub: move cursor across viewport to switch slides
    const viewport = container.querySelector('.slideshow-viewport');
    if (viewport) {
        viewport.addEventListener('mousemove', (e) => {
            const rect = viewport.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const idx = Math.min(slides.length - 1, Math.max(0, Math.floor((x / rect.width) * slides.length)));
            if (idx !== currentIndex) {
                currentIndex = idx;
                showSlide(currentIndex);
            }
        });

        viewport.addEventListener('touchmove', (e) => {
            const touch = e.touches[0];
            if (!touch) return;
            const rect = viewport.getBoundingClientRect();
            const x = touch.clientX - rect.left;
            const idx = Math.min(slides.length - 1, Math.max(0, Math.floor((x / rect.width) * slides.length)));
            if (idx !== currentIndex) {
                currentIndex = idx;
                showSlide(currentIndex);
            }
        }, { passive: true });
    }
});

// Pause videos on modal close
function pauseModalVideos(modal) {
    if (!modal) return;
    const videos = modal.querySelectorAll('video');
    videos.forEach(v => v.pause());
}

modalCloseBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const activeModal = btn.closest('.modal');
        pauseModalVideos(activeModal);
    });
});

modals.forEach(modal => {
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            pauseModalVideos(modal);
        }
    });
});

// Dedicated Video Lightbox Modal Controller
const openVideoBtns = document.querySelectorAll('.open-video-modal-btn');
const videoModal = document.getElementById('modal-video-player');
const videoElement = document.getElementById('global-video-element');
const videoSourceTag = document.getElementById('video-source-tag');
const videoPlayerTitle = document.getElementById('video-player-title');
const videoFallbackNotice = document.getElementById('video-fallback-notice');
const closeVideoBtns = document.querySelectorAll('.close-video-modal, .close-video-modal-btn');

openVideoBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const videoTitle = btn.getAttribute('data-video-title') || 'Project Video Output Demo';
        const videoSrc = btn.getAttribute('data-video-src');
        const videoPoster = btn.getAttribute('data-video-poster');

        if (videoPlayerTitle) videoPlayerTitle.textContent = videoTitle;
        
        if (videoElement) {
            videoElement.src = videoSrc;
            if (videoSourceTag) videoSourceTag.src = videoSrc;
            if (videoPoster) videoElement.poster = videoPoster;

            videoElement.style.display = 'block';
            if (videoFallbackNotice) videoFallbackNotice.style.display = 'none';

            videoElement.onerror = () => {
                videoElement.style.display = 'none';
                if (videoFallbackNotice) videoFallbackNotice.style.display = 'flex';
            };

            videoElement.oncanplay = () => {
                videoElement.style.display = 'block';
                if (videoFallbackNotice) videoFallbackNotice.style.display = 'none';
            };

            videoElement.load();
        }

        if (videoModal) {
            videoModal.classList.add('active');
            document.body.style.overflow = 'hidden';
            if (videoElement) {
                videoElement.play().catch(() => {
                    // Auto-play muted fallback if blocked by browser policy
                });
            }
        }
    });
});

closeVideoBtns.forEach(btn => {
    btn.addEventListener('click', closeVideoLightbox);
});

if (videoModal) {
    videoModal.addEventListener('click', (e) => {
        if (e.target === videoModal) closeVideoLightbox();
    });
}

function closeVideoLightbox() {
    if (videoElement) {
        videoElement.pause();
        videoElement.currentTime = 0;
    }
    if (videoModal) videoModal.classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Dedicated Certificate Lightbox Viewer Controller
const openCertBtns = document.querySelectorAll('.open-cert-modal-btn');
const certModal = document.getElementById('modal-cert-viewer');
const certViewerTitle = document.getElementById('cert-viewer-title');
const certViewerIssuer = document.getElementById('cert-viewer-issuer');
const certViewerDate = document.getElementById('cert-viewer-date');
const certViewerImg = document.getElementById('cert-viewer-img');
const certFallbackCard = document.getElementById('cert-fallback-card');
const fallbackCertName = document.getElementById('fallback-cert-name');
const fallbackCertOrg = document.getElementById('fallback-cert-org');
const certDownloadBtn = document.getElementById('cert-download-btn');
const closeCertBtns = document.querySelectorAll('.close-cert-modal, .close-cert-modal-btn');

openCertBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const certTitle = btn.getAttribute('data-cert-title') || 'Official Certificate Proof';
        const certIssuer = btn.getAttribute('data-cert-issuer') || 'Verified Credential';
        const certDate = btn.getAttribute('data-cert-date') || 'Verified Record';
        const certImg = btn.getAttribute('data-cert-img');

        if (certViewerTitle) certViewerTitle.textContent = certTitle;
        if (certViewerIssuer) certViewerIssuer.textContent = `Issuer: ${certIssuer}`;
        if (certViewerDate) certViewerDate.innerHTML = `<i class="fas fa-calendar-check"></i> ${certDate}`;
        if (fallbackCertName) fallbackCertName.textContent = certTitle;
        if (fallbackCertOrg) fallbackCertOrg.textContent = `Issued by ${certIssuer}`;

        if (certViewerImg) {
            certViewerImg.style.display = 'block';
            if (certFallbackCard) certFallbackCard.style.display = 'none';
            certViewerImg.src = certImg;
            
            certViewerImg.onload = () => {
                certViewerImg.style.display = 'block';
                if (certFallbackCard) certFallbackCard.style.display = 'none';
            };

            certViewerImg.onerror = () => {
                certViewerImg.style.display = 'none';
                if (certFallbackCard) certFallbackCard.style.display = 'flex';
            };
        }

        if (certDownloadBtn) {
            certDownloadBtn.href = certImg;
        }

        if (certModal) {
            certModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        }
    });
});

closeCertBtns.forEach(btn => {
    btn.addEventListener('click', closeCertLightbox);
});

if (certModal) {
    certModal.addEventListener('click', (e) => {
        if (e.target === certModal) closeCertLightbox();
    });
}

function closeCertLightbox() {
    if (certModal) certModal.classList.remove('active');
    document.body.style.overflow = 'auto';
}
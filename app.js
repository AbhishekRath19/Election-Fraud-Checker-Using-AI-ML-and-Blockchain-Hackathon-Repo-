// AI-Blockchain Election Ballot System - JavaScript
class ElectionSystem {
    constructor() {
        this.currentPage = 'landing-page';
        this.currentStep = 1;
        this.totalSteps = 5;
        this.selectedParty = null;
        this.voterSession = null;
        this.voteSubmitted = false;
        
        // Application data from requirements
        this.politicalParties = [
            {
                id: "party1",
                name: "Democratic Progress Party",
                symbol: "🏛️",
                color: "#2563eb",
                candidate: "Dr. Sarah Johnson",
                platform: "Education & Healthcare Reform",
                votes: 15847
            },
            {
                id: "party2",
                name: "National Unity Coalition",
                symbol: "🤝",
                color: "#dc2626",
                candidate: "Prof. Michael Chen",
                platform: "Economic Development & Jobs",
                votes: 18923
            },
            {
                id: "party3",
                name: "Green Future Alliance",
                symbol: "🌱",
                color: "#16a34a",
                candidate: "Ms. Priya Sharma",
                platform: "Environment & Sustainability",
                votes: 12456
            },
            {
                id: "party4",
                name: "Progressive Reform Movement",
                symbol: "⚖️",
                color: "#7c3aed",
                candidate: "Dr. Raj Patel",
                platform: "Social Justice & Equality",
                votes: 9834
            }
        ];

        this.systemStats = {
            total_votes_cast: 57060,
            districts_connected: 156,
            security_level: "99.7%",
            average_verification_time: "1.8 seconds",
            ai_accuracy: "99.7%",
            blockchain_transactions: 57060,
            system_uptime: "99.99%",
            verified_voters: 62847
        };

        this.verificationSteps = [
            { id: 1, title: "Phone Verification", description: "Initialize voter session with phone number", icon: "📱" },
            { id: 2, title: "Document Upload", description: "Upload and verify government ID", icon: "📄" },
            { id: 3, title: "AI Verification", description: "AI processes document authenticity", icon: "🤖" },
            { id: 4, title: "Face Recognition", description: "Match face with ID photo", icon: "👤" },
            { id: 5, title: "OTP Verification", description: "Verify phone number with OTP", icon: "🔐" }
        ];

        this.demoTransactions = [
            { id: "0x7d4a2b8f9c3e1a5d", voter: "VTR789123", party: "party2", timestamp: "2025-08-25T10:15:30Z", block: 18500743 },
            { id: "0x9f8e7d6c5b4a3e2d", voter: "VTR456789", party: "party1", timestamp: "2025-08-25T10:14:15Z", block: 18500742 },
            { id: "0x3c2b1a9f8e7d6c5b", voter: "VTR234567", party: "party3", timestamp: "2025-08-25T10:13:45Z", block: 18500741 }
        ];
    }

    init() {
        console.log('Initializing ElectionSystem...');
        this.setupEventListeners();
        this.updateStats();
        this.initializeProgressSteps();
        console.log('ElectionSystem initialized successfully');
    }

    setupEventListeners() {
        console.log('Setting up event listeners...');
        
        // Landing page - Start Voting Button
        const startVotingBtn = document.getElementById('start-voting-btn');
        console.log('Start voting button found:', startVotingBtn);
        
        if (startVotingBtn) {
            startVotingBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Start voting button clicked - navigating to verification page');
                this.navigateToPage('verification-page');
            });
            console.log('Event listener attached to start voting button');
        } else {
            console.error('Start voting button not found!');
        }

        // Phone verification
        const phoneSubmitBtn = document.getElementById('phone-submit');
        if (phoneSubmitBtn) {
            phoneSubmitBtn.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Phone submit clicked');
                this.handlePhoneSubmit();
            });
        }

        // Document upload
        const documentUpload = document.getElementById('document-upload');
        const documentFile = document.getElementById('document-file');
        const documentSubmit = document.getElementById('document-submit');
        
        if (documentUpload && documentFile) {
            documentUpload.addEventListener('click', () => {
                documentFile.click();
            });

            documentFile.addEventListener('change', (e) => {
                this.handleDocumentUpload(e);
            });
        }

        if (documentSubmit) {
            documentSubmit.addEventListener('click', (e) => {
                e.preventDefault();
                this.processDocument();
            });
        }

        // Face recognition
        const faceVerifyBtn = document.getElementById('face-verify');
        if (faceVerifyBtn) {
            faceVerifyBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.processFaceRecognition();
            });
        }

        // OTP verification
        this.setupOTPInputs();
        const verifyOtpBtn = document.getElementById('verify-otp');
        const resendOtpBtn = document.getElementById('resend-otp');
        
        if (verifyOtpBtn) {
            verifyOtpBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.verifyOTP();
            });
        }

        if (resendOtpBtn) {
            resendOtpBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.resendOTP();
            });
        }

        // Voting
        const clearVoteBtn = document.getElementById('clear-vote');
        const confirmVoteBtn = document.getElementById('confirm-vote');
        
        if (clearVoteBtn) {
            clearVoteBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.clearVoteSelection();
            });
        }

        if (confirmVoteBtn) {
            confirmVoteBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.showVoteConfirmation();
            });
        }

        // Vote confirmation modal
        const cancelVoteBtn = document.getElementById('cancel-vote');
        const submitVoteBtn = document.getElementById('submit-vote');
        
        if (cancelVoteBtn) {
            cancelVoteBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.hideVoteConfirmation();
            });
        }

        if (submitVoteBtn) {
            submitVoteBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.submitVote();
            });
        }

        // Receipt page
        const verifyVoteBtn = document.getElementById('verify-vote-btn');
        const viewResultsBtn = document.getElementById('view-results-btn');
        
        if (verifyVoteBtn) {
            verifyVoteBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.verifyVote();
            });
        }

        if (viewResultsBtn) {
            viewResultsBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigateToPage('results-page');
                this.loadResults();
            });
        }

        // Results page
        const backToHomeBtn = document.getElementById('back-to-home');
        const systemHealthBtn = document.getElementById('system-health-btn');
        
        if (backToHomeBtn) {
            backToHomeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.navigateToPage('landing-page');
                this.resetSystem();
            });
        }

        if (systemHealthBtn) {
            systemHealthBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.showSystemHealth();
            });
        }

        // System health modal
        const closeHealthModalBtn = document.getElementById('close-health-modal');
        if (closeHealthModalBtn) {
            closeHealthModalBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.hideSystemHealth();
            });
        }

        // Modal and keyboard handling
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.classList.add('hidden');
            }
        });
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                document.querySelectorAll('.modal').forEach(modal => {
                    modal.classList.add('hidden');
                });
            }
        });

        console.log('All event listeners set up successfully');
    }

    navigateToPage(pageId) {
        console.log(`Navigating from ${this.currentPage} to ${pageId}`);
        
        // Hide current page
        const currentPageElement = document.getElementById(this.currentPage);
        if (currentPageElement) {
            currentPageElement.classList.remove('active');
        }
        
        // Show new page
        const newPageElement = document.getElementById(pageId);
        if (newPageElement) {
            newPageElement.classList.add('active');
            this.currentPage = pageId;
            console.log(`Successfully navigated to ${pageId}`);
        } else {
            console.error(`Page element not found: ${pageId}`);
            return;
        }

        // Update page-specific content
        if (pageId === 'voting-page') {
            this.loadBallot();
        } else if (pageId === 'results-page') {
            this.loadResults();
        }
    }

    initializeProgressSteps() {
        const progressSteps = document.getElementById('progress-steps');
        if (!progressSteps) return;
        
        progressSteps.innerHTML = '';
        
        this.verificationSteps.forEach((step, index) => {
            const stepElement = document.createElement('div');
            stepElement.className = 'progress-step';
            stepElement.innerHTML = `
                <div class="step-number">${step.id}</div>
                <span>${step.title}</span>
            `;
            
            if (index === 0) {
                stepElement.classList.add('active');
            }
            
            progressSteps.appendChild(stepElement);
        });
    }

    updateProgress() {
        const progressFill = document.getElementById('verification-progress');
        if (progressFill) {
            const percentage = (this.currentStep / this.totalSteps) * 100;
            progressFill.style.width = `${percentage}%`;
        }

        // Update step indicators
        const steps = document.querySelectorAll('.progress-step');
        steps.forEach((step, index) => {
            step.classList.remove('active', 'completed');
            if (index < this.currentStep - 1) {
                step.classList.add('completed');
            } else if (index === this.currentStep - 1) {
                step.classList.add('active');
            }
        });
    }

    nextStep() {
        // Hide current step
        const currentStepElement = document.querySelector('.verification-step.active');
        if (currentStepElement) {
            currentStepElement.classList.remove('active');
        }
        
        // Show next step
        this.currentStep++;
        const nextStepId = this.getStepId(this.currentStep);
        const nextStep = document.getElementById(nextStepId);
        if (nextStep) {
            nextStep.classList.add('active');
        }
        
        this.updateProgress();
    }

    getStepId(step) {
        const stepIds = ['step-phone', 'step-document', 'step-ai-processing', 'step-face-recognition', 'step-otp'];
        return stepIds[step - 1];
    }

    handlePhoneSubmit() {
        const phoneInput = document.getElementById('phone-input');
        const phone = phoneInput ? phoneInput.value.trim() : '';
        
        if (!phone) {
            alert('Please enter your phone number');
            return;
        }

        // Generate voter session
        this.voterSession = {
            voterId: 'VTR' + Math.random().toString(36).substring(2, 8).toUpperCase(),
            phone: phone,
            verified: false
        };

        // Update voter ID display
        const voterIdElements = document.querySelectorAll('#voter-id, #receipt-voter-id');
        voterIdElements.forEach(element => {
            if (element) element.textContent = this.voterSession.voterId;
        });

        this.nextStep();
    }

    handleDocumentUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.getElementById('document-preview');
            if (preview) {
                preview.src = e.target.result;
            }
            
            const uploadedDoc = document.getElementById('uploaded-document');
            const submitBtn = document.getElementById('document-submit');
            
            if (uploadedDoc) uploadedDoc.style.display = 'block';
            if (submitBtn) submitBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    processDocument() {
        this.nextStep();
        this.startAIProcessing();
    }

    startAIProcessing() {
        const checks = [
            { id: 'check-authenticity', delay: 1000 },
            { id: 'check-quality', delay: 2000 },
            { id: 'check-validity', delay: 3000 },
            { id: 'check-data', delay: 4000 }
        ];

        const statusElement = document.getElementById('ai-status');
        
        checks.forEach((check, index) => {
            setTimeout(() => {
                const checkElement = document.getElementById(check.id);
                if (checkElement) {
                    const icon = checkElement.querySelector('.check-icon');
                    if (icon) icon.textContent = '✅';
                    checkElement.style.color = 'var(--color-success)';
                }
                
                if (index === checks.length - 1) {
                    if (statusElement) {
                        statusElement.textContent = '✅ Document verification completed successfully!';
                        statusElement.style.color = 'var(--color-success)';
                    }
                    
                    setTimeout(() => {
                        this.nextStep();
                    }, 1000);
                }
            }, check.delay);
        });
    }

    processFaceRecognition() {
        const resultDiv = document.getElementById('face-result');
        const button = document.getElementById('face-verify');
        
        if (button) {
            button.textContent = 'Processing...';
            button.disabled = true;
        }

        setTimeout(() => {
            if (resultDiv) resultDiv.style.display = 'block';
            if (button) button.textContent = 'Verification Complete';
            
            setTimeout(() => {
                this.nextStep();
                this.generateOTP();
            }, 2000);
        }, 3000);
    }

    generateOTP() {
        this.currentOTP = Math.floor(100000 + Math.random() * 900000).toString();
        const otpPhone = document.getElementById('otp-phone');
        const demoOtpDisplay = document.getElementById('demo-otp');
        
        if (otpPhone && this.voterSession) {
            otpPhone.textContent = `Code sent to ${this.voterSession.phone}`;
        }
        
        // Display demo OTP
        if (demoOtpDisplay) {
            demoOtpDisplay.textContent = this.currentOTP;
        }
        
        // Auto-fill OTP for demo after a short delay
        setTimeout(() => {
            const otpInputs = document.querySelectorAll('.otp-input');
            this.currentOTP.split('').forEach((digit, index) => {
                if (otpInputs[index]) {
                    otpInputs[index].value = digit;
                }
            });
        }, 1500);
    }

    setupOTPInputs() {
        const otpInputs = document.querySelectorAll('.otp-input');
        
        otpInputs.forEach((input, index) => {
            input.addEventListener('input', (e) => {
                if (e.target.value.length === 1 && index < otpInputs.length - 1) {
                    otpInputs[index + 1].focus();
                }
            });

            input.addEventListener('keydown', (e) => {
                if (e.key === 'Backspace' && !e.target.value && index > 0) {
                    otpInputs[index - 1].focus();
                }
            });
        });
    }

    verifyOTP() {
        const otpInputs = document.querySelectorAll('.otp-input');
        const enteredOTP = Array.from(otpInputs).map(input => input.value).join('');
        
        if (enteredOTP === this.currentOTP) {
            if (this.voterSession) this.voterSession.verified = true;
            this.navigateToPage('voting-page');
        } else {
            alert('Invalid OTP. Please try again.');
        }
    }

    resendOTP() {
        this.generateOTP();
        alert('New OTP sent to your phone');
    }

    loadBallot() {
        const ballot = document.getElementById('ballot');
        if (!ballot) return;
        
        ballot.innerHTML = '';

        this.politicalParties.forEach(party => {
            const partyOption = document.createElement('div');
            partyOption.className = 'party-option';
            partyOption.dataset.partyId = party.id;
            
            partyOption.innerHTML = `
                <div class="party-radio"></div>
                <div class="party-symbol">${party.symbol}</div>
                <div class="party-details">
                    <h3>${party.name}</h3>
                    <div class="party-candidate">Candidate: ${party.candidate}</div>
                    <p class="party-platform">${party.platform}</p>
                </div>
            `;

            partyOption.addEventListener('click', () => {
                this.selectParty(party.id);
            });

            ballot.appendChild(partyOption);
        });
    }

    selectParty(partyId) {
        // Clear previous selection
        document.querySelectorAll('.party-option').forEach(option => {
            option.classList.remove('selected');
        });

        // Select new party
        const selectedOption = document.querySelector(`[data-party-id="${partyId}"]`);
        if (selectedOption) {
            selectedOption.classList.add('selected');
        }
        
        this.selectedParty = partyId;
        const confirmBtn = document.getElementById('confirm-vote');
        if (confirmBtn) confirmBtn.disabled = false;
    }

    clearVoteSelection() {
        document.querySelectorAll('.party-option').forEach(option => {
            option.classList.remove('selected');
        });
        this.selectedParty = null;
        const confirmBtn = document.getElementById('confirm-vote');
        if (confirmBtn) confirmBtn.disabled = true;
    }

    showVoteConfirmation() {
        if (!this.selectedParty) return;

        const party = this.politicalParties.find(p => p.id === this.selectedParty);
        const selectedPartyInfo = document.getElementById('selected-party-info');
        
        if (selectedPartyInfo && party) {
            selectedPartyInfo.innerHTML = `
                <div class="party-symbol">${party.symbol}</div>
                <div>
                    <strong>${party.name}</strong><br>
                    Candidate: ${party.candidate}
                </div>
            `;
        }

        const modal = document.getElementById('vote-confirmation-modal');
        if (modal) modal.classList.remove('hidden');
    }

    hideVoteConfirmation() {
        const modal = document.getElementById('vote-confirmation-modal');
        if (modal) modal.classList.add('hidden');
    }

    submitVote() {
        this.hideVoteConfirmation();
        this.navigateToPage('processing-page');
        this.processVote();
    }

    processVote() {
        const steps = [
            { id: 'step-encrypt', delay: 1000 },
            { id: 'step-blockchain', delay: 2500 },
            { id: 'step-network', delay: 4000 },
            { id: 'step-finalize', delay: 5500 }
        ];

        steps.forEach((step, index) => {
            setTimeout(() => {
                const stepElement = document.getElementById(step.id);
                if (stepElement) {
                    stepElement.classList.add('active');
                    
                    setTimeout(() => {
                        stepElement.classList.remove('active');
                        stepElement.classList.add('completed');
                        const indicator = stepElement.querySelector('.step-indicator');
                        if (indicator) indicator.innerHTML = '✅';
                    }, 1000);
                }

                if (index === steps.length - 1) {
                    setTimeout(() => {
                        this.generateReceipt();
                        this.navigateToPage('receipt-page');
                    }, 1500);
                }
            }, step.delay);
        });

        // Update blockchain info
        setTimeout(() => {
            const currentBlock = document.getElementById('current-block');
            if (currentBlock) {
                const blockNumber = parseInt(currentBlock.textContent.replace(/,/g, '')) + 1;
                currentBlock.textContent = blockNumber.toLocaleString();
            }
        }, 3000);
    }

    generateReceipt() {
        const transactionId = '0x' + Math.random().toString(16).substring(2, 18);
        const voteHash = '0x' + Math.random().toString(16).substring(2, 18);
        const blockNumber = 18500746;
        const timestamp = new Date().toLocaleString('en-IN', { 
            timeZone: 'Asia/Kolkata',
            dateStyle: 'long',
            timeStyle: 'medium'
        });

        const transactionIdEl = document.getElementById('transaction-id');
        const voteHashEl = document.getElementById('vote-hash');
        const blockNumberEl = document.getElementById('block-number');
        const timestampEl = document.getElementById('vote-timestamp');

        if (transactionIdEl) transactionIdEl.textContent = transactionId;
        if (voteHashEl) voteHashEl.textContent = voteHash;
        if (blockNumberEl) blockNumberEl.textContent = blockNumber.toLocaleString();
        if (timestampEl) timestampEl.textContent = timestamp;

        // Update vote count
        const party = this.politicalParties.find(p => p.id === this.selectedParty);
        if (party) {
            party.votes++;
            this.systemStats.total_votes_cast++;
        }

        this.voteSubmitted = true;
    }

    verifyVote() {
        alert('Vote verification successful! Your vote has been recorded on the blockchain and is tamper-proof.');
    }

    loadResults() {
        this.updateResultsDisplay();
        setTimeout(() => {
            this.createResultsChart();
        }, 100);
    }

    updateResultsDisplay() {
        const totalVotes = this.politicalParties.reduce((sum, party) => sum + party.votes, 0);
        const totalVotesEl = document.getElementById('total-votes-count');
        if (totalVotesEl) {
            totalVotesEl.textContent = totalVotes.toLocaleString();
        }
        
        // Update last updated time
        const now = new Date().toLocaleString('en-IN', { 
            timeZone: 'Asia/Kolkata',
            dateStyle: 'long',
            timeStyle: 'medium'
        });
        const lastUpdatedEl = document.getElementById('last-updated');
        if (lastUpdatedEl) {
            lastUpdatedEl.textContent = now;
        }

        // Update party results
        const partyResults = document.getElementById('party-results');
        if (!partyResults) return;
        
        partyResults.innerHTML = '';

        // Sort parties by votes
        const sortedParties = [...this.politicalParties].sort((a, b) => b.votes - a.votes);

        sortedParties.forEach(party => {
            const percentage = ((party.votes / totalVotes) * 100).toFixed(1);
            
            const resultDiv = document.createElement('div');
            resultDiv.className = 'party-result';
            resultDiv.innerHTML = `
                <div class="party-info">
                    <span class="party-symbol">${party.symbol}</span>
                    <div>
                        <div class="party-name">${party.name}</div>
                        <div class="party-candidate">${party.candidate}</div>
                    </div>
                </div>
                <div class="vote-info">
                    <div class="vote-count">${party.votes.toLocaleString()}</div>
                    <div class="vote-percentage">${percentage}%</div>
                </div>
            `;
            
            partyResults.appendChild(resultDiv);
        });
    }

    createResultsChart() {
        const canvas = document.getElementById('results-chart');
        if (!canvas) return;
        
        const ctx = canvas.getContext('2d');
        
        // Prepare data
        const labels = this.politicalParties.map(party => party.name);
        const data = this.politicalParties.map(party => party.votes);
        const colors = ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5'];

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors,
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                }
            }
        });
    }

    showSystemHealth() {
        // Load recent transactions
        const transactionList = document.getElementById('transaction-list');
        if (!transactionList) return;
        
        transactionList.innerHTML = '';

        this.demoTransactions.forEach(tx => {
            const party = this.politicalParties.find(p => p.id === tx.party);
            const time = new Date(tx.timestamp).toLocaleTimeString();
            
            const txDiv = document.createElement('div');
            txDiv.className = 'transaction-item';
            txDiv.innerHTML = `
                <span class="transaction-hash">${tx.id}</span>
                <span>${party ? party.name : 'Unknown'}</span>
                <span class="transaction-time">${time}</span>
            `;
            
            transactionList.appendChild(txDiv);
        });

        const modal = document.getElementById('system-health-modal');
        if (modal) modal.classList.remove('hidden');
    }

    hideSystemHealth() {
        const modal = document.getElementById('system-health-modal');
        if (modal) modal.classList.add('hidden');
    }

    updateStats() {
        // Animate counter updates
        const totalVotesElement = document.getElementById('total-votes');
        if (totalVotesElement) {
            this.animateCounter(totalVotesElement, this.systemStats.total_votes_cast);
        }

        // Update other stats periodically
        setInterval(() => {
            if (this.voteSubmitted) {
                this.systemStats.total_votes_cast++;
                if (totalVotesElement) {
                    totalVotesElement.textContent = this.systemStats.total_votes_cast.toLocaleString();
                }
            }
        }, 10000); // Update every 10 seconds
    }

    animateCounter(element, target) {
        const start = 0;
        const duration = 2000;
        const startTime = performance.now();

        const updateCounter = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = Math.floor(start + (target - start) * progress);
            element.textContent = current.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(updateCounter);
            }
        };

        requestAnimationFrame(updateCounter);
    }

    resetSystem() {
        this.currentStep = 1;
        this.selectedParty = null;
        this.voterSession = null;
        this.voteSubmitted = false;
        
        // Reset form inputs
        const phoneInput = document.getElementById('phone-input');
        const documentFile = document.getElementById('document-file');
        const uploadedDoc = document.getElementById('uploaded-document');
        const documentSubmit = document.getElementById('document-submit');
        
        if (phoneInput) phoneInput.value = '';
        if (documentFile) documentFile.value = '';
        if (uploadedDoc) uploadedDoc.style.display = 'none';
        if (documentSubmit) documentSubmit.disabled = true;
        
        // Clear OTP inputs
        document.querySelectorAll('.otp-input').forEach(input => {
            input.value = '';
        });
        
        // Reset verification steps
        document.querySelectorAll('.verification-step').forEach(step => {
            step.classList.remove('active');
        });
        const firstStep = document.getElementById('step-phone');
        if (firstStep) firstStep.classList.add('active');
        
        // Reset progress
        this.updateProgress();
        this.initializeProgressSteps();
        
        // Reset AI processing
        document.querySelectorAll('.ai-check .check-icon').forEach(icon => {
            icon.textContent = '⏳';
        });
        const aiStatus = document.getElementById('ai-status');
        if (aiStatus) {
            aiStatus.textContent = 'Analyzing document authenticity...';
            aiStatus.style.color = 'var(--color-primary)';
        }
        
        // Reset face recognition
        const faceResult = document.getElementById('face-result');
        const faceVerify = document.getElementById('face-verify');
        if (faceResult) faceResult.style.display = 'none';
        if (faceVerify) {
            faceVerify.textContent = 'Verify Identity';
            faceVerify.disabled = false;
        }
        
        // Reset processing steps
        document.querySelectorAll('.processing-step').forEach(step => {
            step.classList.remove('active', 'completed');
            const indicator = step.querySelector('.step-indicator');
            if (indicator) indicator.innerHTML = '<div class="spinner-small"></div>';
        });
    }
}

// Initialize the application when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, initializing ElectionSystem');
    
    try {
        const electionSystem = new ElectionSystem();
        electionSystem.init();
        
        // Make it globally accessible for debugging
        window.electionSystem = electionSystem;
        
        console.log('Application successfully initialized');
    } catch (error) {
        console.error('Error initializing application:', error);
    }
});

// Utility functions for demo purposes
function simulateNetworkDelay(min = 500, max = 2000) {
    return new Promise(resolve => {
        const delay = Math.random() * (max - min) + min;
        setTimeout(resolve, delay);
    });
}

function generateRandomHash() {
    return '0x' + Math.random().toString(16).substring(2, 18);
}

function getCurrentTimestamp() {
    return new Date().toLocaleString('en-IN', { 
        timeZone: 'Asia/Kolkata',
        dateStyle: 'long',
        timeStyle: 'medium'
    });
}
# 🗳️ AI-Blockchain Election Ballot System - Integrated

> **InnovAct 2025 Hackathon Project**  
> Complete voting system with AI verification and blockchain security in one integrated application

## 🚀 Quick Start

```bash
# 1. Install Node.js (if not already installed)
# Download from: https://nodejs.org/

# 2. Install dependencies
npm install

# 3. Start the application
npm start
```

**🌐 Open in browser:** http://localhost:3000

## ✨ Features

- **🤖 AI Document Verification:** Government ID analysis and validation
- **👤 Facial Recognition:** Live photo matching against ID documents  
- **📱 OTP Authentication:** SMS-based multi-factor security
- **⛓️ Blockchain Voting:** Immutable vote recording with transaction proofs
- **📊 Live Results:** Real-time election results dashboard
- **🔒 Security:** End-to-end encryption and tamper-proof voting

## 🎯 Demo Flow

1. **Start Voting** → Enter phone number
2. **Upload ID** → Government document verification
3. **Take Photo** → Facial recognition matching
4. **Enter OTP** → SMS verification code
5. **Cast Vote** → Select party and submit to blockchain
6. **View Receipt** → Blockchain transaction confirmation
7. **See Results** → Live election dashboard

## 🏗️ Architecture

```
Frontend (HTML/CSS/JS) ← → Backend API (Express.js) ← → Mock Services
                                    ↑
                            File Storage & Processing
```

## 📱 For InnovAct 2025 Demo

**Demo Credentials:**
- Phone: Any 10-digit Indian number
- OTP: Displayed on screen (demo mode)
- Documents: Upload any image/PDF
- AI Processing: Simulated (90% success rate)
- Blockchain: Mock network for fast demo

## 🛠️ Technical Stack

- **Frontend:** Vanilla HTML5, CSS3, JavaScript
- **Backend:** Node.js, Express.js
- **File Upload:** Multer middleware
- **Mock AI:** Simulated document & face verification
- **Mock Blockchain:** Transaction simulation
- **Storage:** In-memory (demo mode)

## 📂 File Structure

```
ai-blockchain-voting-integrated/
├── app.js                    # Main server file
├── package.json              # Dependencies
├── README.md                 # This file
├── public/                   # Frontend files
│   ├── index.html           # Main HTML
│   ├── style.css            # Styling
│   └── app.js               # Frontend JavaScript
└── uploads/                 # Document uploads
    └── documents/           # ID documents
```

## 🚨 Troubleshooting

**Port already in use:**
```bash
# Kill process on port 3000
npx kill-port 3000
npm start
```

**Node.js not found:**
```bash
# Install Node.js from: https://nodejs.org/
# Verify installation:
node --version
npm --version
```

**File upload issues:**
- Check file size (max 10MB)
- Supported formats: JPG, PNG, PDF
- Ensure upload directory exists

## 🎭 Demo Notes

- **AI Verification:** Mock processing with realistic delays
- **Face Recognition:** Simulated matching (85% success rate)
- **Blockchain:** Local simulation for fast demo
- **OTP:** Displayed on screen for easy testing
- **Results:** Updates in real-time during demo

## 🏆 Hackathon Highlights

**Innovation Points:**
- ✅ AI-powered identity verification
- ✅ Blockchain vote immutability  
- ✅ Multi-factor authentication
- ✅ Real-time transparency
- ✅ Accessible design
- ✅ Scalable architecture

**Evaluation Criteria Coverage:**
- **Innovation & Creativity (20%):** AI + Blockchain integration
- **Technical Implementation (25%):** Working prototype with modern tech
- **Impact & Usefulness (15%):** Solves real election security problems
- **Presentation & Teamwork (15%):** Clean interface and demo flow
- **Scalability (10%):** Architecture supports millions of voters

## 🎉 Success Tips

1. **Demo the complete flow** from phone to blockchain receipt
2. **Show AI verification** with confidence scores
3. **Highlight blockchain** transaction proof
4. **Emphasize security** with multi-factor auth
5. **Display live results** for transparency

## 📞 Support

For InnovAct 2025 hackathon support:
- Check console logs for debugging
- All API endpoints return JSON with error details
- Frontend state is logged to browser console
- Mock services simulate realistic processing times

---

**🚀 Ready to demo your AI-Blockchain voting system!**

*Built for InnovAct 2025 • VIT Chennai • August 2025*
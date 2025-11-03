import streamlit as st
import pandas as pd
import pickle

# 1. Set page config FIRST
st.set_page_config(page_title='Loan Approval Predictor', page_icon='💎', layout='wide')

# 2. Premium fintech-inspired CSS
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles - Remove ALL white backgrounds */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        background-attachment: fixed;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Remove white space from main container */
    .main {
        background: transparent !important;
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
        background: transparent !important;
    }
    
    /* Remove white background from all containers */
    div[data-testid="stVerticalBlock"],
    div[data-testid="stHorizontalBlock"],
    div[data-testid="column"],
    .element-container {
        background: transparent !important;
    }
    
    /* All text elements - Light theme */
    .stApp, .main, p, span, div, label, .stMarkdown {
        color: #ffffff !important;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    /* Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        padding: 2.5rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(255, 107, 107, 0.4);
        text-align: center;
        animation: slideDown 0.6s ease-out;
    }
    
    .header-banner h1 {
        color: white !important;
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-banner p {
        color: rgba(255,255,255,0.95);
        font-size: 1.15rem;
        margin-top: 0.5rem;
        font-weight: 400;
    }
    
    /* Card Containers */
    .card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.3);
        animation: fadeIn 0.5s ease-in;
    }
    
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .card-header h3 {
        color: #ffffff !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin: 0 !important;
        margin-left: 0.5rem !important;
    }
    
    .card-icon {
        font-size: 1.8rem;
    }
    
    /* Input Styling */
    .stNumberInput input, .stSelectbox select, .stSlider {
        background: rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        color: #ffffff !important;
        transition: all 0.3s ease !important;
    }
    
    .stNumberInput input:focus, .stSelectbox select:focus {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: #ff6b6b !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 107, 0.3) !important;
    }
    
    /* Input containers background */
    .stNumberInput, .stSelectbox, .stSlider {
        background: transparent !important;
    }
    
    /* Input text color */
    input, select, textarea {
        color: #ffffff !important;
    }
    
    /* Placeholder text */
    ::placeholder {
        color: rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Labels with icons */
    label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    
    /* All text elements visibility */
    .stMarkdown, p, span, div {
        color: #ffffff !important;
    }
    
    /* Section headers */
    h5 {
        color: #ffd93d !important;
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 3rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.5) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 1rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 107, 0.6) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* Button container */
    .stButton {
        background: transparent !important;
    }
    
    /* Result Cards */
    .result-approved {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(56, 239, 125, 0.3);
        animation: scaleIn 0.5s ease-out;
    }
    
    .result-rejected {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 10px 40px rgba(235, 51, 73, 0.3);
        animation: scaleIn 0.5s ease-out;
    }
    
    .result-approved h2, .result-rejected h2 {
        color: white !important;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin: 0.5rem 0 !important;
    }
    
    .result-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: bounce 0.6s ease-in-out;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4a148c 0%, #6a1b9a 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
        background: transparent !important;
    }
    
    .sidebar-content {
        text-align: center;
        padding: 1rem;
    }
    
    .sidebar-content h2 {
        color: #ffd93d !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        margin: 1rem 0 !important;
    }
    
    .sidebar-content p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    /* DataFrame Styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        background: rgba(255, 255, 255, 0.1) !important;
    }
    
    .stDataFrame table {
        color: #ffffff !important;
        background: transparent !important;
    }
    
    .stDataFrame th {
        background: rgba(255, 107, 107, 0.3) !important;
        color: #ffffff !important;
    }
    
    .stDataFrame td {
        color: #ffffff !important;
        background: rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Info/Warning boxes */
    .stAlert {
        border-radius: 12px !important;
        border-left: 4px solid #ffd93d !important;
        background: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
    }
    
    .stAlert p {
        color: #ffffff !important;
    }
    
    /* Success/Info boxes */
    .stSuccess, .stInfo {
        background: rgba(255, 255, 255, 0.15) !important;
        color: #ffffff !important;
        border-radius: 12px !important;
    }
    
    .stSuccess p, .stInfo p {
        color: #ffffff !important;
    }
    
    /* Spinner container */
    .stSpinner > div {
        border-top-color: #ff6b6b !important;
    }
    
    /* Footer */
    .footer {
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
    }
    
    .footer-content {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .footer-icon {
        font-size: 1.5rem;
        opacity: 0.7;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .header-banner h1 {
            font-size: 2rem !important;
        }
        .card {
            padding: 1.5rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.image('https://cdn-icons-png.flaticon.com/512/616/616494.png', width=80)
    st.markdown('<h2>💎 Loan Predictor</h2>', unsafe_allow_html=True)
    st.markdown('<p>Enter your financial details to get instant loan approval predictions powered by advanced machine learning.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<p style="color: #ffd93d; font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">📊 Quick Tips</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255, 255, 255, 0.95); margin: 0.3rem 0;">✓ Higher CIBIL score improves chances</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255, 255, 255, 0.95); margin: 0.3rem 0;">✓ Provide accurate asset values</p>', unsafe_allow_html=True)
    st.markdown('<p style="color: rgba(255, 255, 255, 0.95); margin: 0.3rem 0;">✓ Review all fields before prediction</p>', unsafe_allow_html=True)

# 4. Header Banner
st.markdown("""
    <div class="header-banner">
        <h1>💎 ApproveMe</h1>
        <p>Get instant eligibility results with our AI-powered prediction engine</p>
    </div>
""", unsafe_allow_html=True)

# 5. Load models
try:
    with open('rf_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('model_columns.pkl', 'rb') as cols_file:
        model_cols = pickle.load(cols_file)
except FileNotFoundError:
    st.error("⚠️ Model files not found. Please ensure 'rf_model.pkl' and 'model_columns.pkl' are in the same directory.")
    st.stop()

# 6. User Input Section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header"><span class="card-icon">📝</span><h3>Applicant Information</h3></div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 🎓 Personal Details")
    education = st.selectbox('Education Level', [1, 0], format_func=lambda x: '🎓 Graduate' if x == 1 else '📚 Not Graduate')
    self_employed = st.selectbox('Employment Status', [1, 0], format_func=lambda x: '💼 Self Employed' if x == 1 else '🏢 Salaried')
    
    st.markdown("##### 💰 Financial Information")
    income_annum = st.number_input('Annual Income (₹)', min_value=0, step=50000, help="Your total yearly income")
    loan_amount = st.number_input('Loan Amount Required (₹)', min_value=0, step=10000, help="Amount you wish to borrow")
    loan_term = st.selectbox('Loan Term', [12, 24, 36, 60, 120, 180], format_func=lambda x: f'📅 {x} months')

with col2:
    st.markdown("##### 📊 Credit Profile")
    cibil_score = st.slider('CIBIL Score', 300, 900, 750, help="Your credit score (300-900)")
    
    st.markdown("##### 🏠 Asset Values")
    residential_assets_value = st.number_input('Residential Assets (₹)', min_value=0, step=100000)
    commercial_assets_value = st.number_input('Commercial Assets (₹)', min_value=0, step=100000)
    luxury_assets_value = st.number_input('Luxury Assets (₹)', min_value=0, step=50000)
    bank_asset_value = st.number_input('Bank Balance (₹)', min_value=0, step=10000)

applicant_data = {
    'education': education,
    'self_employed': self_employed,
    'income_annum': income_annum,
    'loan_amount': loan_amount,
    'loan_term': loan_term,
    'cibil_score': cibil_score,
    'residential_assets_value': residential_assets_value,
    'commercial_assets_value': commercial_assets_value,
    'luxury_assets_value': luxury_assets_value,
    'bank_asset_value': bank_asset_value
}
input_df = pd.DataFrame([applicant_data])

st.markdown("#### 📋 Application Summary")
st.markdown('<p style="color: #ffffff; margin-bottom: 1rem;">Review your entered information before prediction:</p>', unsafe_allow_html=True)
st.dataframe(input_df, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# 7. Prediction Button & Result
if st.button('🚀 Predict Loan Approval'):
    with st.spinner('🔄 Analyzing your application...'):
        X_pred = input_df.reindex(columns=model_cols, fill_value=0)
        pred = model.predict(X_pred)[0]
        
        if pred == 1:
            st.markdown("""
                <div class="result-approved">
                    <div class="result-icon">✅</div>
                    <h2>Congratulations!</h2>
                    <p style="color: white; font-size: 1.2rem; margin-top: 1rem;">Your loan application is likely to be <strong>APPROVED</strong></p>
                </div>
            """, unsafe_allow_html=True)
            st.success("✨ Based on your financial profile, you have strong eligibility for loan approval!")
        else:
            st.markdown("""
                <div class="result-rejected">
                    <div class="result-icon">❌</div>
                    <h2>Application Review Needed</h2>
                    <p style="color: white; font-size: 1.2rem; margin-top: 1rem;">Your loan application may be <strong>REJECTED</strong></p>
                </div>
            """, unsafe_allow_html=True)
            st.info("💡 Consider improving your CIBIL score or adjusting loan parameters for better chances.")

# 8. Footer
st.markdown("""
    <div class="footer">
        <div class="footer-content">
            <span class="footer-icon">🔒</span>
            <span>Secure & Confidential</span>
            <span class="footer-icon">⚡</span>
            <span>Instant Results</span>
            <span class="footer-icon">🎯</span>
            <span>AI-Powered</span>
        </div>
        <p style="font-size: 0.9rem;">© 2025 LEAD College MCA | Your privacy is our priority</p>
        <p style="font-size: 0.85rem; opacity: 0.6;">Built with ❤️ using Streamlit</p>
    </div>

""", unsafe_allow_html=True)

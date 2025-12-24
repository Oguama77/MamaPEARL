# MamaPEARL (Preeclampsia Early Alert and Response Lab)

This project is a conversational AI system that predicts the risk of **late-onset preeclampsia** using clinical and laboratory data. It integrates a machine learning model with a natural language interface to make healthcare insights more accessible and proactive for expecting mothers. Find the web application ([here](https://preview--pearl-ai-whispers-form.lovable.app/chat))

## Project Description

Preeclampsia is a life-threatening pregnancy complication that is often detected late. This solution uses a Random Forest classifier trained on clinical variables such as blood pressure, kidney and liver function, urine protein levels, and other biomarkers to assess the likelihood of developing preeclampsia.

Users interact with the system via a chatbot that accepts natural language descriptions of lab test results and returns an instant risk assessment. It also provides personalized maternal health information based on risk scores.

## Key Files

New to the project? Start here:

- **[Documentation](docs/project_overview.pdf)** - Detailed explanation of the research and methodology
- **[main.py](main.py)** - Application entry point
- **[app/routes/](app/routes/routes.py)** - API endpoints for predictions and data processing
- **[app/models/](app/models/train_model.ipynb)** - Model training notebook
- **Core Prediction Components:**
  - **[app/services/agent_service.py](app/services/agent_service.py)** - Conversational AI integration (LLM calls and prompts)
  - **[app/services/variable_service.py](app/services/variable_service.py)** - Converts conversational input to model-ready format
  - **[app/services/image_service.py](app/services/image_service.py)** - Extracts clinical data from uploaded images
  - **[app/routes/prediction.py](app/routes/prediction.py)** - Direct prediction endpoint for structured form input
- **[Sample Requests](docs/sample_requests.md)** - API usage examples
- **[requirements.txt](requirements.txt)** - Project dependencies

## Key Features

- **Conversational AI**: Accepts free-text inputs like "My blood pressure is 140/90 and creatinine is 1.2"  
- **Machine Learning Model**: Trained using a Random Forest classifier with 0.97 accuracy and 0.90 AUC  
- **Medical Data Handling**: Accepts over 25 lab and clinical variables from blood and urine tests  
- **Deployment**: Frontend hosted on **Vercel**, backend API deployed on **Render**  
- **Scalability Plan**: Future integration with **mobile apps** and **wearable devices** (e.g. smartwatches) for real-time monitoring and alerting  


## Dataset

The model was trained on clinical data referenced from the paper:  
> *"Prediction model development of late-onset preeclampsia using machine learning-based methods"* ([Jhee et al., 2019](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0221202))

## Project Structure
```
MamaPEARL/
│   .gitignore              # Git ignore rules 
│   main.py                 # Application entry point - runs the FastAPI server
│   README.md               # Project documentation and setup instructions
│   requirements.txt        # Python dependencies
│   
├── app/
│   │   main.py            # FastAPI app instance and route registration
│   │   __init__.py        # Makes app a Python package
│   │   
│   ├── core/
│   │   ├── config.py      # Application configuration and environment variables
│   │   └── __init__.py
│   │       
│   ├── models/
│   │   ├── call_model.py       # Functions to load and call the ML model
│   │   ├── model.pkl           # Trained preeclampsia prediction model
│   │   ├── scaler.pkl          # Data scaler for normalizing input features
│   │   ├── train_model.ipynb   # Jupyter notebook for model training/experimentation
│   │   ├── train_model.py      # Model training script
│   │   └── __init__.py
│   │
│   ├── routes/
│   │   ├── chat.py            # Conversational AI endpoints
│   │   ├── image.py           # Image upload and processing endpoints
│   │   ├── prediction.py      # Direct prediction endpoint for structured form input
│   │   ├── routes.py          # Route aggregation/organization
│   │   ├── variables.py       # Variable normalization endpoints
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── requests.py        # Pydantic models for request/response validation
│   │   └── __init__.py
│   │
│   ├── services/
│   │   ├── agent_service.py      # Conversational AI logic (LLM calls and prompts)
│   │   ├── image_service.py      # Extracts clinical data from uploaded images
│   │   ├── variable_service.py   # Converts conversational input to model-ready format
│   │   └── __init__.py
│   │
│   └── utils/
│       ├── helpers.py        # Utility functions and helper methods
│       └── __init__.py
│
├── docs/
│   ├── project_overview.pdf   # Detailed research documentation and methodology
│   ├── sample_lab_test.png    # Example lab test image for testing
│   └── sample_requests.md     # API usage examples and request formats
│
└── tests/
    ├── endpoint_test_report.json    # Detailed test results in JSON format
    ├── endpoint_test_summary.md     # Human-readable test summary
    └── test_endpoints.py            # API endpoint test suite
```

## Installation

````bash
# Clone the repository
git clone https://github.com/Oguama77/MamaPEARL.git
cd MamaPEARL

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows Command Prompt:
venv\Scripts\activate.bat

# On Windows PowerShell:
venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt
````



# MamaPEARL
Late-onset preeclampsia prediction agent

This project is a conversational AI system that predicts the risk of **late-onset preeclampsia** using clinical and laboratory data. It integrates a machine learning model with a natural language interface to make healthcare insights more accessible and proactive for expecting mothers. Find the web application ([here](https://preview--pearl-ai-whispers-form.lovable.app/chat))

---

## Project Description

Preeclampsia is a life-threatening pregnancy complication often detected late. This solution uses a Random Forest classifier trained on clinical variables such as blood pressure, kidney and liver function, urine protein levels, and other biomarkers to assess the likelihood of developing preeclampsia.

Users interact with the system via a chatbot that accepts natural language descriptions of lab test results and returns an instant risk assessment.

---

## Key Features

- **Conversational AI**: Accepts free-text inputs like "My blood pressure is 140/90 and creatinine is 1.2"  
- **Machine Learning Model**: Trained using a Random Forest classifier with 0.97 accuracy and 0.90 AUC  
- **Medical Data Handling**: Accepts over 25 lab and clinical variables from blood and urine tests  
- **Deployment**: Frontend hosted on **Vercel**, backend API deployed on **Render**  
- **Scalability Plan**: Future integration with **mobile apps** and **wearable devices** (e.g. smartwatches) for real-time monitoring and alerting  

---

## Dataset

The model was trained on clinical data referenced from the paper:  
> *"Prediction model development of late-onset preeclampsia using machine learning-based methods"* ([PLOS ONE, 2019](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0221202))

### Sample Features:
- Gestational age  
- Blood pressure (SBP, DBP)  
- Serum creatinine, albumin, uric acid  
- Liver enzymes (ALT, AST, ALP)  
- Urine albumin-to-creatinine ratio  
- Fundal height, maternal weight, haemoglobin  

---

## Model Performance

| Metric         | Score     |
|----------------|-----------|
| Accuracy       | 0.97      |
| AUC Score      | 0.90      |
| Inference Time | < 1 sec   |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/preeclampsia-ai.git
cd preeclampsia-ai

# Create virtual environment and install requirements
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt


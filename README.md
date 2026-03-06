# WorkflowIQ

**WorkflowIQ** is a machine learning powered task prioritization system that intelligently ranks tasks based on urgency, importance, and deadline proximity.

Instead of relying on static to-do lists, WorkflowIQ predicts a **priority score** for each task and automatically determines what should be done first.

This project explores how **machine learning models can be integrated with backend APIs and simple user interfaces to solve real productivity problems.**



# Problem Statement

Most task management tools treat every task equally or rely on manual sorting.

In real life, priorities constantly change because of:

* approaching deadlines
* urgency of the task
* overall importance
* limited available time

Managing this manually becomes inefficient when multiple tasks compete for attention.

WorkflowIQ attempts to **automate task prioritization using machine learning.**

---

# Solution

WorkflowIQ converts real-world task attributes into machine learning features and uses a **Random Forest model** to predict task priority.

The predicted score is then used to rank tasks dynamically so users can focus on the most impactful work first.

---

# System Architecture

```
User Task Input
       ↓
Feature Engineering
(deadline, urgency, importance)
       ↓
Random Forest Model
       ↓
Priority Score Prediction
       ↓
FastAPI Backend
       ↓
Streamlit Frontend
       ↓
Ranked Task Output
```

---

# Tech Stack

### Machine Learning

* Scikit-learn
* Random Forest Algorithm
* Feature Engineering

### Backend

* Python
* FastAPI

### Frontend

* Streamlit

### Deployment

* Render (Backend API)
* Streamlit Cloud (Frontend)

### Version Control

* Git
* GitHub

---

# Machine Learning Approach

The model learns how different task attributes influence priority levels.

Features used include:

* **deadline proximity**
* **urgency level**
* **importance score**

These features are used to train a **Random Forest model**, which predicts a **priority score** for each task.

Random Forest was chosen because it performs well on structured data and handles feature interactions effectively.


# Example Workflow

1. User enters a task with deadline, urgency, and importance.
2. The system converts inputs into machine learning features.
3. The trained model predicts a **priority score**.
4. Tasks are ranked automatically based on predicted scores.



# Example API Usage

Endpoint

```
POST /predict-priority
```

Example Request

```json
{
  "task": "Submit project report",
  "deadline_days": 1,
  "urgency": 3,
  "importance": 4
}
```

Example Response

```json
{
  "task": "Submit project report",
  "priority_score": 0.92,
  "rank": 1
}
```

# Project Structure

```
workflowiq/
│
├── backend/
│   ├── main.py
│   ├── model.pkl
│   └── feature_engineering.py
│
├── frontend/
│   └── app.py
│
├── dataset/
│   └── task_data.csv
│
├── requirements.txt
│
└── README.md
```
# Future Improvements

* add task history learning
* integrate calendar APIs
* improve UI dashboard
* deploy full production pipeline


#Building WorkflowIQ helped me understand:

1. how to translate real-world logic into machine learning features
2. how to integrate ML models into backend APIs
3. how to build simple interfaces for ML-powered systems

---

# Author

Nandini 

Machine Learning + Backend enthusiast building practical AI systems.


import keyword
import os
import joblib
import numpy as np
import pandas as pd
from datetime import datetime,date
from typing import Optional
from scipy.sparse import csr_matrix,hstack

class TaskPriorityPredictor:
    def __init__(self):
        self.model=None
        self.vectorizer=None
        self.model_path=r"C:\Users\nandi\OneDrive\Desktop\WorkflowIQ\object\training_model.pkl"
        self.vectorizer_path=r"C:\Users\nandi\OneDrive\Desktop\WorkflowIQ\object\Tfidf_Vectorizer.pkl"
        self.load_model()

    def load_model(self):
        try:
            if os.path.exists(self.model_path):
                self.model=joblib.load(self.model_path)
                print("ML model loaded successfully!")

            else:
                print(f"Model not found in {self.model_path}")
                self.model=None
            if os.path.exists(self.vectorizer_path):
                self.vectorizer = joblib.load(self.vectorizer_path)
                print("Vectorizer loaded successfully!")
            else:
                print(f"Vectorizer not found in {self.vectorizer_path}")
                self.vectorizer = None
            

        except:
            pass

    def deadline_to_importance(self,deadline:Optional[date])-> int:
        # If deadline accidentally comes as string → convert
        if isinstance(deadline, str):
            try:
                deadline = datetime.fromisoformat(deadline).date()
            except Exception:
                return 0

    # If deadline is datetime → convert to date
        if isinstance(deadline, datetime):
            deadline = deadline.date()

            days_remaining=(deadline-date.today()).days

            if days_remaining <=0:
                return 4 #high urgency
        #deadline may be today or overdue if return negative
            elif days_remaining == 1:
                return 3 #urgent but deadline is tommorow
            elif days_remaining <= 7:
                return 2 
        #high priority,deadline will be this week
            elif days_remaining <= 30:
                return 1
            #low priority,deadline will be until this month
            else:
                return 0
            #low urgency

    def category_to_importance(self,category:str)->int:
        cate_lower=category.lower()
        if cate_lower in ['work','career','academic']:
            return 3
        #maximum importance
        elif cate_lower == 'personal':
            return 2
        #moderate importance
        else:
            return 1
        #low importance

    #Main priority predictor
    def priority_predictor(
            self,
            title:str,
            deadline:Optional[date],
            category:str
        ) ->tuple[str,float]:
        if self.model or self.vectorizer is None:
            return self._rule_based_prediction(title,deadline,category),0.5
            #will return high,urgent,low with 50% confidence

        
        deadline_importance=self.deadline_to_importance(deadline)

        category_importance=self.category_to_importance(category)

        title_feature=self.vectorizer.transform([title])

        structured_features=np.array([deadline_importance,category_importance])

        combined_features=hstack([title_feature,csr_matrix(structured_features)])
            #hstack will align both of these horizontaly in an array
            #csr_matrix will convert structured_features into the same structure as of title_features
            
            
        

    #Final Part
        try:
            prediction=self.model.predict(combined_features)[0]

            confidence=self.model.predict_proba(combined_features)[0].max()#will return the highest probability among all
            return prediction,confidence
        except Exception as e:
            print(f"Prediction error{e}")
            return self._rule_based_prediction(title,category,deadline),0.5
        
    #Rule Based Fallback
    def _rule_based_prediction(
        self,
        title:str,
        deadline:Optional[date],
        category:str
    )->str:
    #it is backup prediction method used if ml model crashes

        deadline_urgency=self.deadline_to_importance(deadline)
        if deadline_urgency==4:
            return "urgent"
        elif deadline_urgency==3:
            return "urgent"
        elif deadline_urgency==2:
            return "high"
        elif deadline_urgency==1:
            return "moderate"
        else:
            return "low"
        
urgent_keywords=['urgent','asap','critical','emergency','immediately']
high_keywords=['important','priority','deadline','due']
def get_priority(title):
    title_lower=title.lower()

    if any(keyword in title_lower for keyword in urgent_keywords):
        return "urgent"
    elif any(keyword in title_lower for keyword in  high_keywords):
        return "high"

def category_get(category):
    if category.lower() in ['work','academic','career']:
        return "moderate"
    
    else:
        return "low"
    
#Global Instance & simple instance
predictor=TaskPriorityPredictor()

def predict_priority(
        title:str,
        deadline:Optional[date],
        category:str
)->str:
    priority,confidence=predictor.priority_predictor(title,deadline,category)
    print(f"Prediction:{priority}(confidence:{confidence:.2%})")

    return priority
    
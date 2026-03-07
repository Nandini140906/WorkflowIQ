import requests

BASE_URL = "https://workflowiq-hw99.onrender.com"
# ── Auth ──────────────────────────────────────────────────────────────────────

def signup(name, email, password):
    """POST /api/signup — body: {name, email, password}"""
    try:
        r = requests.post(f"{BASE_URL}/api/signup", json={
            "name": name, "email": email, "password": password
        })
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"signup error: {e}")
        return None


def login(email, password):
    
    try:
        r = requests.post(f"{BASE_URL}/api/login", json={
            "email": email, "password": password
        })
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"login error: {e}")
        return None


# ── Users ─────────────────────────────────────────────────────────────────────

def get_user(user_id):
    """GET /api/user/{user_id} — returns {id, name, email, created_at}"""
    try:
        # NOTE: backend route is /user/ (singular) — users_routers.py line 8
        r = requests.get(f"{BASE_URL}/api/user/{user_id}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"get_user error: {e}")
        return None


# ── Tasks ─────────────────────────────────────────────────────────────────────

def create_task(user_id, title, category, deadline):
    
    try:
        r = requests.post(f"{BASE_URL}/api/tasks", json={
            "title": title,
            "category": category,
            "deadline": f"{deadline}T00:00:00"  # backend expects datetime not date
        }, params={"user_id": user_id})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"create_task error: {e}")
        return None


def get_tasks(user_id, skip=0, limit=100):
    """GET /api/tasks?user_id={user_id}&skip={skip}&limit={limit}"""
    try:
        r = requests.get(f"{BASE_URL}/api/tasks", params={
            "user_id": user_id, "skip": skip, "limit": limit
        })
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"get_tasks error: {e}")
        return []


def update_task(task_id, user_id, status=None, title=None, category=None, deadline=None, priority=None):
    body = {}
    if status   is not None: body["status"]   = status
    if title    is not None: body["title"]    = title
    if category is not None: body["category"] = category
    if deadline is not None: body["deadline"] = deadline
    if priority is not None: body["priority"] = priority
    try:
        r = requests.put(f"{BASE_URL}/api/tasks/{task_id}", json=body,
                         params={"user_id": user_id})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"update_task error: {e}")
        return None


def delete_task(task_id, user_id):
    try:
        # singular /task/ — this is how the backend actually defines it
        r = requests.delete(f"{BASE_URL}/api/task/{task_id}",
                            params={"user_id": user_id})
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"delete_task error: {e}")
        return False


# ── Workflows ─────────────────────────────────────────────────────────────────

def create_workflow(user_id, name, description=""):
    
    try:
        r = requests.post(f"{BASE_URL}/api/workflow", json={
            "name": name, "description": description
        }, params={"user_id": user_id})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"create_workflow error: {e}")
        return None


def get_workflows(user_id):
    """GET /api/workflows?user_id={user_id}"""
    try:
        r = requests.get(f"{BASE_URL}/api/workflows", params={"user_id": user_id})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"get_workflows error: {e}")
        return []


def update_workflow(workflow_id, user_id, name=None, description=None):
    
    body = {}
    if name        is not None: body["name"]        = name
    if description is not None: body["description"] = description
    try:
        r = requests.put(f"{BASE_URL}/api/workflow/{workflow_id}", json=body,
                         params={"user_id": user_id})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"update_workflow error: {e}")
        return None


def delete_workflow(workflow_id, user_id):
    """
    DELETE /api/workflow/{workflow_id}
    NOTE: route is /workflow/ (singular)
    """
    try:
        r = requests.delete(f"{BASE_URL}/api/workflow/{workflow_id}",
                            params={"user_id": user_id})
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"delete_workflow error: {e}")
        return False


# ── Productivity Logs ─────────────────────────────────────────────────────────

def create_log(user_id, task_id, time_spent, date=None):
    
    body = {"task_id": task_id, "time_spent": time_spent}
    if date:
        body["date"] = date
    try:
        r = requests.post(f"{BASE_URL}/api/logs", json=body,
                          params={"user_id": user_id})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"create_log error: {e}")
        return None


def get_logs_for_task(task_id, user_id):
    """GET /api/logs/task/{task_id}?user_id={user_id}"""
    try:
        r = requests.get(f"{BASE_URL}/api/logs/task/{task_id}",
                         params={"user_id": user_id})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"get_logs error: {e}")
        return []


def delete_log(log_id, user_id):
    
    try:
        r = requests.delete(f"{BASE_URL}/api/log/{log_id}",
                            params={"user_id": user_id})
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"delete_log error: {e}")
        return False


# ── ML Prediction ─────────────────────────────────────────────────────────────

def predict_priority(title, category, deadline=None):
    
    try:
        body = {"title": title, "category": category}
        if deadline:
            body["deadline"] = str(deadline)
        r = requests.post(f"{BASE_URL}/api/predict_priority", json=body)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"predict_priority error: {e}")
        return None

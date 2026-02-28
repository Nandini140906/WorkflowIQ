import requests

BASE_URL = "http://localhost:8000/api"


# ── Auth ──────────────────────────────────────────────────────────────────────

def signup(name, email, password):
    """POST /api/signup — body: {name, email, password}"""
    try:
        r = requests.post(f"{BASE_URL}/signup", json={
            "name": name, "email": email, "password": password
        })
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"signup error: {e}")
        return None


def login(email, password):
    """
    POST /api/login — body: {email, password}
    Returns: {access_token, token_type}
    NOTE: backend Token schema only returns access_token + token_type.
    user_id and name are NOT in the login response — we fetch them separately.
    """
    try:
        r = requests.post(f"{BASE_URL}/login", json={
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
        r = requests.get(f"{BASE_URL}/user/{user_id}")
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"get_user error: {e}")
        return None


# ── Tasks ─────────────────────────────────────────────────────────────────────

def create_task(user_id, title, category, deadline):
    """
    POST /api/tasks?user_id={user_id}
    Body: {title, category, deadline}
    TaskCreate schema only has: title, category, deadline, workflow_id
    description and status are NOT in TaskCreate — don't send them
    deadline must be a datetime string e.g. "2026-03-01T00:00:00"
    """
    try:
        r = requests.post(f"{BASE_URL}/tasks", json={
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
        r = requests.get(f"{BASE_URL}/tasks", params={
            "user_id": user_id, "skip": skip, "limit": limit
        })
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"get_tasks error: {e}")
        return []


def update_task(task_id, user_id, status=None, title=None, category=None, deadline=None, priority=None):
    """
    PUT /api/tasks/{task_id}?user_id={user_id}
    Body: TaskUpdate — all fields optional: title, description, category,
          deadline, priority, status, workflow_id
    """
    body = {}
    if status   is not None: body["status"]   = status
    if title    is not None: body["title"]    = title
    if category is not None: body["category"] = category
    if deadline is not None: body["deadline"] = deadline
    if priority is not None: body["priority"] = priority
    try:
        r = requests.put(f"{BASE_URL}/tasks/{task_id}", json=body,
                         params={"user_id": user_id})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"update_task error: {e}")
        return None


def delete_task(task_id, user_id):
    """
    DELETE /api/task/{task_id}?user_id={user_id}
    NOTE: backend route is /task/ (singular) — tasks_routers.py line 49
    """
    try:
        # singular /task/ — this is how the backend actually defines it
        r = requests.delete(f"{BASE_URL}/task/{task_id}",
                            params={"user_id": user_id})
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"delete_task error: {e}")
        return False


# ── Workflows ─────────────────────────────────────────────────────────────────

def create_workflow(user_id, name, description=""):
    """
    POST /api/workflow?user_id={user_id}
    Body: WorkflowCreate — {name, description}
    NOTE: WorkflowCreate has no steps field — backend schema doesn't support it
    NOTE: backend route is /workflow (singular) — workflow_routers.py line 9
    user_id passed as query param (backend signature: user_id:int)
    """
    try:
        r = requests.post(f"{BASE_URL}/workflow", json={
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
        r = requests.get(f"{BASE_URL}/workflows", params={"user_id": user_id})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"get_workflows error: {e}")
        return []


def update_workflow(workflow_id, user_id, name=None, description=None):
    """
    PUT /api/workflow/{workflow_id}
    Body: WorkflowUpdate — {name, description} both optional
    NOTE: route is /workflow/ (singular)
    """
    body = {}
    if name        is not None: body["name"]        = name
    if description is not None: body["description"] = description
    try:
        r = requests.put(f"{BASE_URL}/workflow/{workflow_id}", json=body,
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
        r = requests.delete(f"{BASE_URL}/workflow/{workflow_id}",
                            params={"user_id": user_id})
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"delete_workflow error: {e}")
        return False


# ── Productivity Logs ─────────────────────────────────────────────────────────

def create_log(user_id, task_id, time_spent, date=None):
    """
    POST /api/logs?user_id={user_id}
    Body: ProductivityLogCreate — {time_spent, task_id, date}
    NOTE: field is time_spent (not hours_spent) — schemas.py line 105
    """
    body = {"task_id": task_id, "time_spent": time_spent}
    if date:
        body["date"] = date
    try:
        r = requests.post(f"{BASE_URL}/logs", json=body,
                          params={"user_id": user_id})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"create_log error: {e}")
        return None


def get_logs_for_task(task_id, user_id):
    """GET /api/logs/task/{task_id}?user_id={user_id}"""
    try:
        r = requests.get(f"{BASE_URL}/logs/task/{task_id}",
                         params={"user_id": user_id})
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"get_logs error: {e}")
        return []


def delete_log(log_id, user_id):
    """
    DELETE /api/log/{log_id}
    NOTE: route is /log/ (singular) — log_routers.py line 40
    """
    try:
        r = requests.delete(f"{BASE_URL}/log/{log_id}",
                            params={"user_id": user_id})
        r.raise_for_status()
        return True
    except Exception as e:
        print(f"delete_log error: {e}")
        return False


# ── ML Prediction ─────────────────────────────────────────────────────────────

def predict_priority(title, category, deadline=None):
    """
    POST /api/predict_priority  (underscore — prediction_routers.py line 7)
    Body: {title, category, deadline}
    Returns: {priority, confidence}
    NOTE: no auth required
    """
    try:
        body = {"title": title, "category": category}
        if deadline:
            body["deadline"] = str(deadline)
        r = requests.post(f"{BASE_URL}/predict_priority", json=body)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"predict_priority error: {e}")
        return None

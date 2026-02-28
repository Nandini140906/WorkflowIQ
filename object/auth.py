# app/auth.py
"""
AUTHENTICATION MODULE
Handles password hashing and JWT token generation/verification
"""

from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import hashlib
# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secret-key-change-this-in-production-use-openssl-rand-hex-32"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 60 minutes


def hash_password(password: str) -> str:
    """
    Hash a plain text password
    
    Args:
        password: Plain text password from user
    
    Returns:
        Hashed password string
    """
    password_bytes=hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(password_bytes)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against hashed password
    
    Args:
        plain_password: Password user typed
        hashed_password: Hashed password from database
    
    Returns:
        True if passwords match, False otherwise
    """
    password_bytes=hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.verify(password_bytes, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create JWT access token
    
    Args:
        data: Dictionary to encode in token (user_id, email, etc.)
        expires_delta: Optional custom expiration time
    
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """
    Decode JWT token and return payload
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload dict if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
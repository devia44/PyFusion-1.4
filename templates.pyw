# -*- coding: utf-8 -*-
"""
Управление шаблонами кода с предупреждением о несохраненных изменениях
"""

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText


class TemplateManager(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.templates = self._get_templates()
        self.setup_ui()
        
    def _get_templates(self):
        """Получение всех шаблонов"""
        return {
            "python": '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module description
"""

import os
import sys
from pathlib import Path

def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
''',
            "flask": '''from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return {"message": "Hello, World!"}

@app.route('/api/data')
def get_data():
    return jsonify({"status": "success", "data": []})

@app.route('/api/data', methods=['POST'])
def create_data():
    data = request.get_json()
    return jsonify({"status": "created", "data": data}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
''',
            "fastapi": '''from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

app = FastAPI(title="API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    tax: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.now)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/")
async def get_items(skip: int = 0, limit: int = 10):
    return {"items": [], "skip": skip, "limit": limit}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}

@app.post("/items/")
async def create_item(item: Item):
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}
''',
            "html": '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #333;
            margin-bottom: 20px;
        }
        
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background 0.3s;
        }
        
        button:hover {
            background: #5a67d8;
        }
        
        .card {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello, World!</h1>
        
        <div class="card">
            <h2>Card Title</h2>
            <p>This is a sample card component.</p>
            <button onclick="handleClick()">Click me</button>
        </div>
    </div>
    
    <script>
        function handleClick() {
            alert('Button clicked!');
        }
        
        console.log('Page loaded successfully');
    </script>
</body>
</html>
''',
            "react": '''import React, { useState, useEffect, useCallback, useMemo } from 'react';

interface Props {
    title?: string;
    initialCount?: number;
    onCountChange?: (count: number) => void;
}

interface Item {
    id: number;
    name: string;
}

const Component: React.FC<Props> = ({ 
    title = "Default Title", 
    initialCount = 0,
    onCountChange 
}) => {
    const [count, setCount] = useState(initialCount);
    const [items, setItems] = useState<Item[]>([]);
    const [loading, setLoading] = useState(false);
    
    useEffect(() => {
        console.log('Component mounted');
        fetchItems();
        
        return () => {
            console.log('Component unmounted');
        };
    }, []);
    
    useEffect(() => {
        onCountChange?.(count);
    }, [count, onCountChange]);
    
    const fetchItems = async () => {
        setLoading(true);
        try {
            const response = await fetch('/api/items');
            const data = await response.json();
            setItems(data);
        } catch (error) {
            console.error('Failed to fetch items:', error);
        } finally {
            setLoading(false);
        }
    };
    
    const handleIncrement = useCallback(() => {
        setCount(prev => prev + 1);
    }, []);
    
    const handleDecrement = useCallback(() => {
        setCount(prev => Math.max(0, prev - 1));
    }, []);
    
    const totalItems = useMemo(() => items.length, [items]);
    
    return (
        <div className="component">
            <h1>{title}</h1>
            
            <div className="counter">
                <p>Count: {count}</p>
                <button onClick={handleIncrement}>+</button>
                <button onClick={handleDecrement}>-</button>
            </div>
            
            <div className="items">
                <h2>Items ({totalItems})</h2>
                {loading ? (
                    <p>Loading...</p>
                ) : (
                    <ul>
                        {items.map(item => (
                            <li key={item.id}>{item.name}</li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
};

export default Component;
''',
            "react_tsx": '''import React from 'react';

interface Props {
    children: React.ReactNode;
    className?: string;
}

export const Container: React.FC<Props> = ({ children, className = '' }) => {
    return (
        <div className={`container ${className}`}>
            {children}
        </div>
    );
};

export const Button: React.FC<{
    onClick?: () => void;
    variant?: 'primary' | 'secondary' | 'danger';
    children: React.ReactNode;
    disabled?: boolean;
}> = ({ onClick, variant = 'primary', children, disabled = false }) => {
    const baseClass = 'px-4 py-2 rounded font-semibold transition-colors';
    const variants = {
        primary: 'bg-blue-500 hover:bg-blue-600 text-white',
        secondary: 'bg-gray-500 hover:bg-gray-600 text-white',
        danger: 'bg-red-500 hover:bg-red-600 text-white'
    };
    
    return (
        <button
            onClick={onClick}
            disabled={disabled}
            className={`${baseClass} ${variants[variant]} ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
            {children}
        </button>
    );
};
''',
            "vue": '''<template>
  <div class="component">
    <h1>{{ title }}</h1>
    
    <div class="counter">
      <p>Count: {{ count }}</p>
      <button @click="increment">+</button>
      <button @click="decrement">-</button>
    </div>
    
    <div class="items" v-if="!loading">
      <h2>Items ({{ items.length }})</h2>
      <ul>
        <li v-for="item in items" :key="item.id">
          {{ item.name }}
        </li>
      </ul>
    </div>
    <p v-else>Loading...</p>
  </div>
</template>

<script>
export default {
  name: 'Component',
  props: {
    title: {
      type: String,
      default: 'Default Title'
    },
    initialCount: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      count: this.initialCount,
      items: [],
      loading: false
    }
  },
  mounted() {
    this.fetchItems()
  },
  methods: {
    async fetchItems() {
      this.loading = true
      try {
        const response = await fetch('/api/items')
        this.items = await response.json()
      } catch (error) {
        console.error('Failed to fetch items:', error)
      } finally {
        this.loading = false
      }
    },
    increment() {
      this.count++
      this.$emit('count-change', this.count)
    },
    decrement() {
      if (this.count > 0) {
        this.count--
        this.$emit('count-change', this.count)
      }
    }
  }
}
</script>

<style scoped>
.component {
  padding: 20px;
}

.counter {
  margin: 20px 0;
}

.counter button {
  margin: 0 5px;
  padding: 5px 15px;
  cursor: pointer;
}

.items ul {
  list-style: none;
  padding: 0;
}

.items li {
  padding: 5px 0;
  border-bottom: 1px solid #eee;
}
</style>
''',
            "docker": '''FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD python -c "import sys; sys.exit(0)"

CMD ["python", "app.py"]
''',
            "docker_compose": '''version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/app
    depends_on:
      - db
      - redis
    volumes:
      - ./uploads:/app/uploads
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./static:/static:ro
    depends_on:
      - app
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
''',
            "gitignore": '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
env/
venv/
.venv/
ENV/
env.bak/
venv.bak/
pythonenv*

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.coverage
htmlcov/
.tox/
.pytest_cache/
hypothesis/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# Environment variables
.env
.env.local
.env.*.local

# Logs
*.log
logs/
*.pid

# Database
*.db
*.sqlite
*.sqlite3

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
*.tmp

# Project specific
instance/
.webassets-cache
uploads/
media/

# Secrets
*.pem
*.key
*.crt
secrets.yml
config/secrets.yml
''',
            "bash": '''#!/bin/bash

set -euo pipefail

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Configuration
APP_NAME="myapp"
LOG_FILE="./${APP_NAME}.log"
PID_FILE="./${APP_NAME}.pid"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" >> "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [WARN] $1" >> "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" >> "$LOG_FILE"
}

check_dependencies() {
    local deps=("python3" "pip3")
    for dep in "${deps[@]}"; do
        if ! command -v "$dep" &> /dev/null; then
            log_error "$dep is not installed"
            return 1
        fi
    done
    return 0
}

setup_environment() {
    if [ ! -d "venv" ]; then
        log_info "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    log_info "Installing dependencies..."
    pip install -r requirements.txt
}

start_app() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            log_warn "Application is already running (PID: $pid)"
            return 1
        fi
    fi
    
    log_info "Starting $APP_NAME..."
    nohup python app.py > /dev/null 2>&1 &
    echo $! > "$PID_FILE"
    log_info "Started with PID: $!"
}

stop_app() {
    if [ ! -f "$PID_FILE" ]; then
        log_warn "PID file not found"
        return 1
    fi
    
    local pid=$(cat "$PID_FILE")
    if kill -0 "$pid" 2>/dev/null; then
        log_info "Stopping $APP_NAME (PID: $pid)..."
        kill "$pid"
        rm "$PID_FILE"
        log_info "Stopped"
    else
        log_warn "Process not running"
        rm "$PID_FILE"
    fi
}

status_app() {
    if [ -f "$PID_FILE" ]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            log_info "$APP_NAME is running (PID: $pid)"
            return 0
        fi
    fi
    log_info "$APP_NAME is not running"
    return 1
}

cleanup() {
    log_info "Cleaning up..."
    rm -rf __pycache__ *.pyc .pytest_cache
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
}

# Main execution
main() {
    case "${1:-}" in
        start)
            check_dependencies && start_app
            ;;
        stop)
            stop_app
            ;;
        restart)
            stop_app
            sleep 2
            start_app
            ;;
        status)
            status_app
            ;;
        setup)
            setup_environment
            ;;
        clean)
            cleanup
            ;;
        logs)
            tail -f "$LOG_FILE"
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|status|setup|clean|logs}"
            exit 1
            ;;
    esac
}

# Trap Ctrl+C
trap 'log_info "Script interrupted"; exit 130' INT

main "$@"
''',
            "css": '''/* Reset and base styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --success-color: #48bb78;
    --danger-color: #f56565;
    --warning-color: #ed8936;
    --text-color: #2d3748;
    --text-light: #718096;
    --bg-color: #f7fafc;
    --border-color: #e2e8f0;
    --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
    --radius: 8px;
    --transition: all 0.3s ease;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--bg-color);
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    margin-bottom: 1rem;
    font-weight: 600;
    line-height: 1.2;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.75rem; }

p {
    margin-bottom: 1rem;
}

a {
    color: var(--primary-color);
    text-decoration: none;
    transition: var(--transition);
}

a:hover {
    color: var(--secondary-color);
}

/* Layout */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

.flex {
    display: flex;
    gap: 20px;
}

.flex-center {
    display: flex;
    align-items: center;
    justify-content: center;
}

.grid {
    display: grid;
    gap: 20px;
}

.grid-2 {
    grid-template-columns: repeat(2, 1fr);
}

.grid-3 {
    grid-template-columns: repeat(3, 1fr);
}

/* Components */
.card {
    background: white;
    border-radius: var(--radius);
    padding: 20px;
    box-shadow: var(--shadow);
    transition: var(--transition);
}

.card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
}

.btn {
    display: inline-block;
    padding: 10px 20px;
    border: none;
    border-radius: var(--radius);
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: var(--transition);
    text-align: center;
}

.btn-primary {
    background: var(--primary-color);
    color: white;
}

.btn-primary:hover {
    background: var(--secondary-color);
}

.btn-success {
    background: var(--success-color);
    color: white;
}

.btn-danger {
    background: var(--danger-color);
    color: white;
}

.btn-outline {
    background: transparent;
    border: 2px solid var(--primary-color);
    color: var(--primary-color);
}

.btn-outline:hover {
    background: var(--primary-color);
    color: white;
}

/* Form elements */
input, textarea, select {
    width: 100%;
    padding: 10px 15px;
    border: 1px solid var(--border-color);
    border-radius: var(--radius);
    font-size: 16px;
    transition: var(--transition);
}

input:focus, textarea:focus, select:focus {
    outline: none;
    border-color: var(--primary-color);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group {
    margin-bottom: 20px;
}

.form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
}

/* Utilities */
.text-center { text-align: center; }
.text-right { text-align: right; }
.text-muted { color: var(--text-light); }

.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }

.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }

.p-1 { padding: 0.5rem; }
.p-2 { padding: 1rem; }
.p-3 { padding: 1.5rem; }
.p-4 { padding: 2rem; }

/* Responsive */
@media (max-width: 768px) {
    .grid-2, .grid-3 {
        grid-template-columns: 1fr;
    }
    
    .flex {
        flex-direction: column;
    }
    
    h1 { font-size: 2rem; }
    h2 { font-size: 1.75rem; }
    h3 { font-size: 1.5rem; }
}

/* Animations */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeIn 0.5s ease;
}

/* Loading spinner */
.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid var(--border-color);
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
''',
            "javascript": '''// Utility functions
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// Event handling
class EventEmitter {
    constructor() {
        this.events = {};
    }
    
    on(event, callback) {
        if (!this.events[event]) {
            this.events[event] = [];
        }
        this.events[event].push(callback);
    }
    
    emit(event, data) {
        if (this.events[event]) {
            this.events[event].forEach(callback => callback(data));
        }
    }
    
    off(event, callback) {
        if (this.events[event]) {
            this.events[event] = this.events[event].filter(cb => cb !== callback);
        }
    }
}

// HTTP client
class HttpClient {
    constructor(baseURL = '') {
        this.baseURL = baseURL;
    }
    
    async request(method, url, data = null) {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(this.baseURL + url, options);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Request failed:', error);
            throw error;
        }
    }
    
    get(url) { return this.request('GET', url); }
    post(url, data) { return this.request('POST', url, data); }
    put(url, data) { return this.request('PUT', url, data); }
    delete(url) { return this.request('DELETE', url); }
}

// State management
class Store extends EventEmitter {
    constructor(initialState = {}) {
        super();
        this.state = initialState;
    }
    
    getState() {
        return { ...this.state };
    }
    
    setState(newState) {
        const oldState = { ...this.state };
        this.state = { ...this.state, ...newState };
        this.emit('change', { oldState, newState: this.state });
    }
}

// Component base class
class Component {
    constructor(element) {
        this.element = element;
        this.state = {};
    }
    
    setState(newState) {
        this.state = { ...this.state, ...newState };
        this.render();
    }
    
    render() {
        // Override in subclass
    }
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Local storage wrapper
const storage = {
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch {
            return defaultValue;
        }
    },
    
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch {
            return false;
        }
    },
    
    remove(key) {
        localStorage.removeItem(key);
    },
    
    clear() {
        localStorage.clear();
    }
};

// Date formatting
function formatDate(date, format = 'YYYY-MM-DD') {
    const d = new Date(date);
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    const hours = String(d.getHours()).padStart(2, '0');
    const minutes = String(d.getMinutes()).padStart(2, '0');
    const seconds = String(d.getSeconds()).padStart(2, '0');
    
    return format
        .replace('YYYY', year)
        .replace('MM', month)
        .replace('DD', day)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        EventEmitter,
        HttpClient,
        Store,
        Component,
        debounce,
        throttle,
        storage,
        formatDate
    };
}
''',
            "typescript": '''// Types and interfaces
export interface User {
    id: number;
    name: string;
    email: string;
    role: UserRole;
    createdAt: Date;
    updatedAt: Date;
}

export enum UserRole {
    ADMIN = 'admin',
    USER = 'user',
    GUEST = 'guest'
}

export interface ApiResponse<T> {
    success: boolean;
    data?: T;
    error?: string;
    timestamp: Date;
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    page: number;
    pageSize: number;
    totalPages: number;
}

export type Nullable<T> = T | null;
export type Optional<T> = T | undefined;
export type DeepPartial<T> = {
    [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Utility types
export type AsyncFunction<T = any> = (...args: any[]) => Promise<T>;
export type SyncFunction<T = any> = (...args: any[]) => T;
export type EventHandler<T = any> = (event: T) => void;

// Base classes
export abstract class BaseEntity {
    id: number;
    createdAt: Date;
    updatedAt: Date;
    
    constructor(data: Partial<BaseEntity> = {}) {
        this.id = data.id ?? 0;
        this.createdAt = data.createdAt ?? new Date();
        this.updatedAt = data.updatedAt ?? new Date();
    }
    
    abstract validate(): boolean;
    abstract toJSON(): Record<string, any>;
}

export class Result<T, E = Error> {
    private constructor(
        private readonly _isSuccess: boolean,
        private readonly _value?: T,
        private readonly _error?: E
    ) {}
    
    static ok<T, E = Error>(value: T): Result<T, E> {
        return new Result<T, E>(true, value);
    }
    
    static fail<T, E = Error>(error: E): Result<T, E> {
        return new Result<T, E>(false, undefined, error);
    }
    
    get isSuccess(): boolean {
        return this._isSuccess;
    }
    
    get isFailure(): boolean {
        return !this._isSuccess;
    }
    
    get value(): T {
        if (!this._isSuccess) {
            throw new Error('Cannot get value from failed result');
        }
        return this._value!;
    }
    
    get error(): E {
        if (this._isSuccess) {
            throw new Error('Cannot get error from successful result');
        }
        return this._error!;
    }
    
    map<U>(fn: (value: T) => U): Result<U, E> {
        if (this._isSuccess) {
            return Result.ok(fn(this._value!));
        }
        return Result.fail(this._error!);
    }
    
    flatMap<U>(fn: (value: T) => Result<U, E>): Result<U, E> {
        if (this._isSuccess) {
            return fn(this._value!);
        }
        return Result.fail(this._error!);
    }
    
    match<U>(onSuccess: (value: T) => U, onFailure: (error: E) => U): U {
        return this._isSuccess ? onSuccess(this._value!) : onFailure(this._error!);
    }
}

// Generic repository pattern
export interface Repository<T extends BaseEntity> {
    findById(id: number): Promise<Result<T>>;
    findAll(): Promise<Result<T[]>>;
    create(entity: Omit<T, 'id' | 'createdAt' | 'updatedAt'>): Promise<Result<T>>;
    update(id: number, entity: Partial<T>): Promise<Result<T>>;
    delete(id: number): Promise<Result<boolean>>;
}

// Service base class
export abstract class BaseService<T extends BaseEntity> {
    protected abstract repository: Repository<T>;
    
    async getById(id: number): Promise<Result<T>> {
        return this.repository.findById(id);
    }
    
    async getAll(): Promise<Result<T[]>> {
        return this.repository.findAll();
    }
    
    async create(data: Omit<T, 'id' | 'createdAt' | 'updatedAt'>): Promise<Result<T>> {
        return this.repository.create(data);
    }
    
    async update(id: number, data: Partial<T>): Promise<Result<T>> {
        return this.repository.update(id, data);
    }
    
    async delete(id: number): Promise<Result<boolean>> {
        return this.repository.delete(id);
    }
}

// Decorators
export function logMethod(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    
    descriptor.value = function(...args: any[]) {
        console.log(`Calling ${propertyKey} with args:`, args);
        const result = originalMethod.apply(this, args);
        console.log(`Method ${propertyKey} returned:`, result);
        return result;
    };
    
    return descriptor;
}

export function measure(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    
    descriptor.value = async function(...args: any[]) {
        const start = performance.now();
        const result = await originalMethod.apply(this, args);
        const end = performance.now();
        console.log(`${propertyKey} took ${end - start}ms`);
        return result;
    };
    
    return descriptor;
}

// Event bus
export class EventBus {
    private handlers: Map<string, Set<EventHandler>> = new Map();
    
    on(event: string, handler: EventHandler): void {
        if (!this.handlers.has(event)) {
            this.handlers.set(event, new Set());
        }
        this.handlers.get(event)!.add(handler);
    }
    
    off(event: string, handler: EventHandler): void {
        this.handlers.get(event)?.delete(handler);
    }
    
    emit(event: string, data?: any): void {
        this.handlers.get(event)?.forEach(handler => handler(data));
    }
    
    once(event: string, handler: EventHandler): void {
        const onceHandler = (data: any) => {
            handler(data);
            this.off(event, onceHandler);
        };
        this.on(event, onceHandler);
    }
}

// Configuration
export interface AppConfig {
    apiUrl: string;
    environment: 'development' | 'staging' | 'production';
    version: string;
    features: Record<string, boolean>;
}

export class Config {
    private static instance: Config;
    private config: AppConfig;
    
    private constructor() {
        this.config = {
            apiUrl: process.env.API_URL || 'http://localhost:3000',
            environment: (process.env.NODE_ENV as any) || 'development',
            version: '1.0.0',
            features: {}
        };
    }
    
    static getInstance(): Config {
        if (!Config.instance) {
            Config.instance = new Config();
        }
        return Config.instance;
    }
    
    get<K extends keyof AppConfig>(key: K): AppConfig[K] {
        return this.config[key];
    }
    
    set<K extends keyof AppConfig>(key: K, value: AppConfig[K]): void {
        this.config[key] = value;
    }
    
    isFeatureEnabled(feature: string): boolean {
        return this.config.features[feature] ?? false;
    }
}
''',
        }
    
    def setup_ui(self):
        """Настройка интерфейса с расположением кода справа"""
        # Title
        title = ttk.Label(self, text=self.app.i18n.get("templates.title"),
                         font=('TkDefaultFont', 14, 'bold'))
        title.pack(pady=15)
        
        # Main container - split left and right
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - template list
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="Select Template:",
                 font=('TkDefaultFont', 10, 'bold')).pack(anchor=tk.W, pady=5)
        
        # Template list with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.template_listbox = tk.Listbox(list_frame, bg='#1e1e1e', fg='#d4d4d4',
                                           selectbackground='#264f78', height=20)
        self.template_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL,
                                  command=self.template_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.template_listbox.config(yscrollcommand=scrollbar.set)
        
        # Populate list
        template_names = {
            "python": "Python Script",
            "flask": "Flask Application",
            "fastapi": "FastAPI Application",
            "html": "HTML5 Page",
            "react": "React Component (TS)",
            "react_tsx": "React TSX Components",
            "vue": "Vue Component",
            "docker": "Dockerfile",
            "docker_compose": "Docker Compose",
            "gitignore": ".gitignore",
            "bash": "Bash Script",
            "css": "CSS Stylesheet",
            "javascript": "JavaScript Utilities",
            "typescript": "TypeScript Types & Utils",
        }
        
        for key, name in template_names.items():
            if key in self.templates:
                self.template_listbox.insert(tk.END, name)
        
        self.template_keys = [k for k in template_names.keys() if k in self.templates]
        
        # Bind selection
        self.template_listbox.bind('<<ListboxSelect>>', self.on_template_select)
        
        # Buttons
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text=self.app.i18n.get("templates.insert"),
                  command=self.insert_template, style="success.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Copy", 
                  command=self.copy_template).pack(side=tk.LEFT, padx=5)
        
        # Right panel - code preview
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=2)
        
        ttk.Label(right_frame, text="Preview:",
                 font=('TkDefaultFont', 10, 'bold')).pack(anchor=tk.W, pady=5)
        
        self.preview_text = ScrolledText(right_frame, bg='#1e1e1e', fg='#d4d4d4',
                                        font=("Consolas", 10), wrap=tk.NONE)
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        
        # Horizontal scrollbar for preview
        h_scrollbar = ttk.Scrollbar(right_frame, orient=tk.HORIZONTAL,
                                    command=self.preview_text.xview)
        h_scrollbar.pack(fill=tk.X)
        self.preview_text.config(xscrollcommand=h_scrollbar.set)
        
        # Info label
        self.info_label = ttk.Label(self, text="", foreground="gray")
        self.info_label.pack(pady=5)
    
    def on_template_select(self, event=None):
        """Выбор шаблона"""
        selection = self.template_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        if idx < len(self.template_keys):
            key = self.template_keys[idx]
            template = self.templates.get(key, "")
            
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, template)
            
            # Update info
            lines = len(template.split('\n'))
            chars = len(template)
            self.info_label.config(text=f"Lines: {lines} | Characters: {chars}")
    
    def check_unsaved_changes(self):
        """Проверка несохраненных изменений"""
        if hasattr(self.app, 'editor') and hasattr(self.app.editor, 'current_file'):
            if self.app.editor.current_file is None:
                content = self.app.editor.text.get(1.0, tk.END).strip()
                if content:
                    return True
            else:
                # Check if modified
                try:
                    with open(self.app.editor.current_file, 'r', encoding='utf-8') as f:
                        saved_content = f.read().strip()
                    current_content = self.app.editor.text.get(1.0, tk.END).strip()
                    if saved_content != current_content:
                        return True
                except:
                    pass
        return False
    
    def insert_template(self):
        """Вставка шаблона с предупреждением"""
        selection = self.template_listbox.curselection()
        if not selection:
            messagebox.showinfo("Info", "Select a template first")
            return
        
        # Check for unsaved changes
        if self.check_unsaved_changes():
            response = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes in the editor.\n\n"
                "Do you want to save before inserting the template?\n\n"
                "• Yes - Save and insert template\n"
                "• No - Insert without saving (changes will be lost)\n"
                "• Cancel - Don't insert template"
            )
            
            if response is None:  # Cancel
                return
            elif response:  # Yes
                if hasattr(self.app, 'editor'):
                    self.app.editor.save_file()
        
        # Insert template
        idx = selection[0]
        if idx < len(self.template_keys):
            key = self.template_keys[idx]
            template = self.templates.get(key, "")
            
            if hasattr(self.app, 'editor') and hasattr(self.app.editor, 'text'):
                # Ask if replace or append
                current_content = self.app.editor.text.get(1.0, tk.END).strip()
                if current_content:
                    action = messagebox.askyesno(
                        "Insert Template",
                        "Editor already has content.\n\n"
                        "Yes - Replace all content\n"
                        "No - Append to end"
                    )
                    
                    if action:  # Replace
                        self.app.editor.text.delete(1.0, tk.END)
                        self.app.editor.text.insert(1.0, template)
                    else:  # Append
                        self.app.editor.text.insert(tk.END, "\n\n" + template)
                else:
                    self.app.editor.text.insert(1.0, template)
                
                if hasattr(self.app, 'set_status'):
                    self.app.set_status(f"Template '{self.template_listbox.get(idx)}' inserted")
    
    def copy_template(self):
        """Копирование шаблона в буфер обмена"""
        selection = self.template_listbox.curselection()
        if not selection:
            return
        
        idx = selection[0]
        if idx < len(self.template_keys):
            key = self.template_keys[idx]
            template = self.templates.get(key, "")
            
            self.clipboard_clear()
            self.clipboard_append(template)
            
            if hasattr(self.app, 'set_status'):
                self.app.set_status(f"Template '{self.template_listbox.get(idx)}' copied to clipboard")
            
            self.info_label.config(text="Template copied to clipboard!")
            self.after(2000, lambda: self.info_label.config(text=""))
    
    def update_texts(self):
        """Обновление текстов при смене языка"""
        pass

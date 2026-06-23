// API 基础 URL
const API_BASE = '';

// 当前选中的 Agent
let currentAgent = 'code-generator';

// DOM 元素
const elements = {
    // 导航
    navItems: document.querySelectorAll('.nav-item'),
    tabContents: document.querySelectorAll('.tab-content'),
    
    // Agent
    agentBtns: document.querySelectorAll('.agent-btn'),
    taskInput: document.getElementById('task-input'),
    codeInput: document.getElementById('code-input'),
    contentInput: document.getElementById('content-input'),
    codeInputGroup: document.getElementById('code-input-group'),
    contentInputGroup: document.getElementById('content-input-group'),
    executeBtn: document.getElementById('execute-btn'),
    agentOutput: document.getElementById('agent-output'),
    
    // 任务
    taskTitle: document.getElementById('task-title'),
    taskDesc: document.getElementById('task-desc'),
    createTaskBtn: document.getElementById('create-task-btn'),
    taskList: document.getElementById('task-list'),
    
    // 项目
    projectName: document.getElementById('project-name'),
    projectDesc: document.getElementById('project-desc'),
    createProjectBtn: document.getElementById('create-project-btn'),
    projectList: document.getElementById('project-list'),
    
    // 健康状态
    healthDb: document.getElementById('health-db'),
    healthRedis: document.getElementById('health-redis'),
    healthQdrant: document.getElementById('health-qdrant'),
    healthLlm: document.getElementById('health-llm'),
    refreshHealthBtn: document.getElementById('refresh-health-btn'),
    
    // 状态栏
    dbStatus: document.getElementById('db-status'),
    redisStatus: document.getElementById('redis-status'),
    qdrantStatus: document.getElementById('qdrant-status'),
    llmStatus: document.getElementById('llm-status'),
    
    // 加载和通知
    loadingOverlay: document.getElementById('loading-overlay'),
    notification: document.getElementById('notification')
};

// 工具函数
function showLoading() {
    elements.loadingOverlay.classList.add('active');
}

function hideLoading() {
    elements.loadingOverlay.classList.remove('active');
}

function showNotification(message, type = 'success') {
    elements.notification.textContent = message;
    elements.notification.className = `notification ${type} show`;
    setTimeout(() => {
        elements.notification.classList.remove('show');
    }, 3000);
}

async function fetchAPI(url, options = {}) {
    try {
        const response = await fetch(API_BASE + url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || data.detail || '请求失败');
        }
        return data;
    } catch (error) {
        throw error;
    }
}

// 导航切换
function initNavigation() {
    elements.navItems.forEach(item => {
        item.addEventListener('click', () => {
            const tab = item.dataset.tab;
            
            // 更新导航状态
            elements.navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            
            // 更新内容区域
            elements.tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(`${tab}-tab`).classList.add('active');
            
            // 刷新数据
            if (tab === 'tasks') {
                loadTasks();
            } else if (tab === 'projects') {
                loadProjects();
            } else if (tab === 'health') {
                checkHealth();
            }
        });
    });
}

// Agent 选择
function initAgentSelector() {
    elements.agentBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const agent = btn.dataset.agent;
            currentAgent = agent;
            
            // 更新按钮状态
            elements.agentBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            
            // 显示/隐藏额外输入区域
            elements.codeInputGroup.style.display = agent === 'code-reviewer' ? 'block' : 'none';
            elements.contentInputGroup.style.display = agent === 'document-writer' ? 'block' : 'none';
            
            // 更新占位符
            if (agent === 'code-generator') {
                elements.taskInput.placeholder = '请描述您需要生成的代码功能...';
            } else if (agent === 'code-reviewer') {
                elements.taskInput.placeholder = '请描述审查要求...';
            } else if (agent === 'document-writer') {
                elements.taskInput.placeholder = '请输入文档主题...';
            }
        });
    });
}

// 执行 Agent 任务
async function executeAgentTask() {
    const task = elements.taskInput.value.trim();
    if (!task) {
        showNotification('请输入任务描述', 'error');
        return;
    }
    
    let context = {};
    if (currentAgent === 'code-reviewer') {
        const code = elements.codeInput.value.trim();
        if (!code) {
            showNotification('请输入需要审查的代码', 'error');
            return;
        }
        context = { code };
    } else if (currentAgent === 'document-writer') {
        const content = elements.contentInput.value.trim();
        context = { content };
    }
    
    showLoading();
    elements.agentOutput.innerHTML = '<p class="output-placeholder">正在执行...</p>';
    
    try {
        let url = '';
        if (currentAgent === 'code-generator') {
            url = '/agent/code/generate';
        } else if (currentAgent === 'code-reviewer') {
            url = '/agent/code/review';
        } else if (currentAgent === 'document-writer') {
            url = '/agent/document/write';
        }
        
        const result = await fetchAPI(url, {
            method: 'POST',
            body: JSON.stringify({ task, context })
        });
        
        const statusClass = result.status === 'completed' ? 'success' : 'error';
        elements.agentOutput.innerHTML = `<pre class="output-result ${statusClass}">${result.result}</pre>`;
        showNotification('任务执行成功');
    } catch (error) {
        elements.agentOutput.innerHTML = `<pre class="output-result error">${error.message}</pre>`;
        showNotification(error.message, 'error');
    } finally {
        hideLoading();
    }
}

// 任务管理
async function loadTasks() {
    try {
        const tasks = await fetchAPI('/tasks/');
        renderTaskList(tasks);
    } catch (error) {
        elements.taskList.innerHTML = `<p class="list-placeholder">${error.message}</p>`;
    }
}

function renderTaskList(tasks) {
    if (!tasks || tasks.length === 0) {
        elements.taskList.innerHTML = '<p class="list-placeholder">暂无任务</p>';
        return;
    }
    
    elements.taskList.innerHTML = tasks.map(task => `
        <div class="task-card">
            <div class="card-info">
                <h4>${task.title}</h4>
                <p>${task.description || '无描述'}</p>
                <small>创建时间: ${new Date(task.created_at).toLocaleString()}</small>
            </div>
            <div class="card-actions">
                <span class="card-status ${task.status === 'completed' ? 'completed' : ''}">${task.status}</span>
                <button class="btn-delete" onclick="deleteTask(${task.id})">删除</button>
            </div>
        </div>
    `).join('');
}

async function createTask() {
    const title = elements.taskTitle.value.trim();
    if (!title) {
        showNotification('请输入任务标题', 'error');
        return;
    }
    
    showLoading();
    try {
        await fetchAPI('/tasks/', {
            method: 'POST',
            body: JSON.stringify({
                title,
                description: elements.taskDesc.value.trim()
            })
        });
        showNotification('任务创建成功');
        elements.taskTitle.value = '';
        elements.taskDesc.value = '';
        loadTasks();
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function deleteTask(id) {
    showLoading();
    try {
        await fetchAPI(`/tasks/${id}`, { method: 'DELETE' });
        showNotification('任务删除成功');
        loadTasks();
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        hideLoading();
    }
}

// 项目管理
async function loadProjects() {
    try {
        const projects = await fetchAPI('/projects/');
        renderProjectList(projects);
    } catch (error) {
        elements.projectList.innerHTML = `<p class="list-placeholder">${error.message}</p>`;
    }
}

function renderProjectList(projects) {
    if (!projects || projects.length === 0) {
        elements.projectList.innerHTML = '<p class="list-placeholder">暂无项目</p>';
        return;
    }
    
    elements.projectList.innerHTML = projects.map(project => `
        <div class="project-card">
            <div class="card-info">
                <h4>${project.name}</h4>
                <p>${project.description || '无描述'}</p>
                <small>创建时间: ${new Date(project.created_at).toLocaleString()}</small>
            </div>
            <div class="card-actions">
                <button class="btn-delete" onclick="deleteProject(${project.id})">删除</button>
            </div>
        </div>
    `).join('');
}

async function createProject() {
    const name = elements.projectName.value.trim();
    if (!name) {
        showNotification('请输入项目名称', 'error');
        return;
    }
    
    showLoading();
    try {
        await fetchAPI('/projects/', {
            method: 'POST',
            body: JSON.stringify({
                name,
                description: elements.projectDesc.value.trim()
            })
        });
        showNotification('项目创建成功');
        elements.projectName.value = '';
        elements.projectDesc.value = '';
        loadProjects();
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function deleteProject(id) {
    showLoading();
    try {
        await fetchAPI(`/projects/${id}`, { method: 'DELETE' });
        showNotification('项目删除成功');
        loadProjects();
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        hideLoading();
    }
}

// 健康检查
async function checkHealth() {
    try {
        const health = await fetchAPI('/health');
        
        // 更新健康状态面板
        updateHealthStatus('health-db', health.database);
        updateHealthStatus('health-redis', health.redis);
        updateHealthStatus('health-qdrant', health.qdrant);
        updateHealthStatus('health-llm', health.llm);
        
        // 更新顶部状态栏
        updateStatusBar('db-status', health.database);
        updateStatusBar('redis-status', health.redis);
        updateStatusBar('qdrant-status', health.qdrant);
        updateStatusBar('llm-status', health.llm);
    } catch (error) {
        showNotification('健康检查失败', 'error');
    }
}

function updateHealthStatus(elementId, status) {
    const element = document.getElementById(elementId);
    const isAvailable = status === 'available';
    element.textContent = isAvailable ? '正常运行' : status;
    element.className = `health-status ${isAvailable ? 'available' : 'unavailable'}`;
}

function updateStatusBar(elementId, status) {
    const element = document.getElementById(elementId);
    const dot = element.querySelector('.status-dot');
    const isAvailable = status === 'available';
    dot.className = `status-dot ${isAvailable ? 'available' : 'unavailable'}`;
}

// 初始化
function init() {
    initNavigation();
    initAgentSelector();
    
    // 绑定事件
    elements.executeBtn.addEventListener('click', executeAgentTask);
    elements.createTaskBtn.addEventListener('click', createTask);
    elements.createProjectBtn.addEventListener('click', createProject);
    elements.refreshHealthBtn.addEventListener('click', checkHealth);
    
    // 初始健康检查
    checkHealth();
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', init);
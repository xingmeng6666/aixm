<template>
  <div class="app-container">
    <h1>🔥 Multi-Agent Automation Platform</h1>
    
    <div class="task-form">
      <h2>Submit a New Task</h2>
      <div class="form-group">
        <input 
          v-model="taskInput" 
          type="text" 
          placeholder="e.g., Research AI news, summarize it, and tweet about it" 
          class="input-box"
          @keyup.enter="submitTask"
        />
        <button @click="submitTask" :disabled="isSubmitting || !taskInput.trim()" class="btn">
          {{ isSubmitting ? 'Submitting...' : 'Run Agent Workflow' }}
        </button>
      </div>
    </div>

    <div class="task-list">
      <h2>Recent Tasks (Auto-refreshing)</h2>
      <button @click="fetchTasks" class="btn btn-small">Refresh Now</button>
      
      <div v-if="loading" class="loading">Loading tasks...</div>
      <div v-else-if="tasks.length === 0" class="no-tasks">No tasks found. Submit one above!</div>
      
      <div v-for="task in tasks" :key="task.id" class="task-card">
        <div class="task-header">
          <span class="task-id">Task #{{ task.id }}</span>
          <span :class="['status-badge', task.status]">{{ task.status }}</span>
        </div>
        <div class="task-body">
          <p><strong>Input:</strong> {{ task.payload?.input || JSON.stringify(task.payload) }}</p>
          
          <div v-if="task.result" class="task-result">
            <h4>Workflow Result:</h4>
            <div class="result-stats">
              <span class="stat"><strong>Approved:</strong> {{ task.result.is_approved ? '✅ Yes' : '❌ No' }}</span>
              <span class="stat"><strong>Revisions:</strong> {{ task.result.revision_count }}</span>
            </div>
            
            <div class="code-block">
              <h5>Plan:</h5>
              <pre>{{ task.result.plan }}</pre>
              
              <h5>Execution Result:</h5>
              <pre>{{ task.result.execution_result }}</pre>
              
              <template v-if="task.result.review_feedback">
                <h5>Reviewer Feedback:</h5>
                <pre class="feedback">{{ task.result.review_feedback }}</pre>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const tasks = ref([])
const taskInput = ref('')
const isSubmitting = ref(false)
const loading = ref(true)
let pollInterval = null

const fetchTasks = async () => {
  try {
    const response = await fetch('/api/v1/tasks/')
    if (response.ok) {
      tasks.value = await response.json()
    }
  } catch (error) {
    console.error('Failed to fetch tasks:', error)
  } finally {
    loading.value = false
  }
}

const submitTask = async () => {
  if (!taskInput.value.trim()) return
  
  isSubmitting.value = true
  try {
    await fetch('/api/v1/tasks/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        task_type: 'langgraph_flow',
        payload: { input: taskInput.value }
      })
    })
    taskInput.value = ''
    await fetchTasks()
  } catch (error) {
    console.error('Failed to submit task:', error)
  } finally {
    isSubmitting.value = false
  }
}

onMounted(() => {
  fetchTasks()
  // Poll every 3 seconds if there are active tasks
  pollInterval = setInterval(() => {
    if (tasks.value.some(t => ['pending', 'processing'].includes(t.status))) {
      fetchTasks()
    }
  }, 3000)
})

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval)
})
</script>

<style scoped>
.app-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  color: #333;
}

h1, h2, h4, h5 {
  color: #2c3e50;
  margin-top: 0;
}

.task-form {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  margin-bottom: 2rem;
  border: 1px solid #e9ecef;
}

.form-group {
  display: flex;
  gap: 1rem;
}

.input-box {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  background: #0d6efd;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  transition: background 0.2s;
}

.btn:hover { background: #0b5ed7; }
.btn:disabled { background: #6ea8fe; cursor: not-allowed; }

.btn-small {
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
  background: #6c757d;
  margin-bottom: 1rem;
}
.btn-small:hover { background: #5c636a; }

.task-card {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f1f3f5;
}

.task-id {
  font-weight: bold;
  color: #495057;
  font-size: 1.1rem;
}

.status-badge {
  padding: 0.35rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-badge.pending { background: #fff3cd; color: #856404; }
.status-badge.processing { background: #cce5ff; color: #004085; }
.status-badge.completed { background: #d1e7dd; color: #0f5132; }
.status-badge.failed { background: #f8d7da; color: #842029; }

.result-stats {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.code-block {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 6px;
  border: 1px solid #e9ecef;
}

.code-block pre {
  margin: 0 0 1rem 0;
  font-size: 0.9rem;
  white-space: pre-wrap;
  color: #212529;
}

.code-block pre.feedback {
  color: #dc3545;
}

.no-tasks, .loading {
  text-align: center;
  color: #6c757d;
  padding: 2rem;
  font-style: italic;
}
</style>

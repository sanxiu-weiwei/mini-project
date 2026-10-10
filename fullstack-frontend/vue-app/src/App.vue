<template>
  <div style="padding: 20px;">
    <h1>我的全栈用户列表（增删查）</h1>

    <!-- 增：添加用户表单 -->
    <div style="margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 8px; width: 80%;">
      <h3>添加新用户</h3>
      <el-input v-model="newUser.username" placeholder="用户名" style="width: 200px; margin-right: 10px;" />
      <el-input v-model="newUser.password" placeholder="密码" type="password" style="width: 200px; margin-right: 10px;" />
      <el-button type="primary" @click="addUser">添加</el-button>
    </div>

    <!-- 查 和 删 表格 -->
    <el-table :data="users" style="width: 80%;" border>
      <el-table-column prop="id" label="ID" width="100" />
      <el-table-column prop="username" label="用户名" width="200" />
      <el-table-column prop="created_at" label="创建时间" />
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button type="danger" size="small" @click="deleteUser(scope.row.id)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const users = ref<any[]>([])
const newUser = ref({ username: '', password: '' })

// 查
const fetchUsers = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/users')
    users.value = response.data.users
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

// 增
const addUser = async () => {
  if (!newUser.value.username || !newUser.value.password) {
    ElMessage.warning('用户名和密码不能为空！')
    return
  }
  try {
    await axios.post('http://127.0.0.1:8000/users', newUser.value)
    ElMessage.success('添加成功！')
    newUser.value.username = ''
    newUser.value.password = ''
    fetchUsers()
  } catch (error) {
    ElMessage.error('添加失败！')
  }
}

// 删
const deleteUser = async (id: number) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/users/${id}`)
    ElMessage.success('删除成功！')
    fetchUsers() // 重新刷新表格
  } catch (error) {
    ElMessage.error('删除失败！')
  }
}

onMounted(() => {
  fetchUsers()
})
</script>
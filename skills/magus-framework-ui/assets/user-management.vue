<template>
  <div p-4 gap-4 flex flex-col h-full min-h-0>
    <MgSearch @search="searchData">
      <template #search>
        <el-form-item label="名称">
          <el-input v-model.trim="search.name" clearable />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="search.status" clearable>
            <el-option label="激活" value="active" />
            <el-option label="禁用" value="inactive" />
          </el-select>
        </el-form-item>
      </template>
      <template #buttons>
        <el-button type="primary" @click="searchData">查询</el-button>
      </template>
    </MgSearch>

    <!-- 工具栏：包含新增、删除等操作 -->
    <MgToolbar
      :select-length="selectedUsers.length"
      @event-handle="handleToolbarEvent"
    />

    <!-- 用户表格：展示用户列表，支持分页、选择、编辑、删除 -->
    <div flex-1 min-h-0>
      <MgTable
        :data="userList"
        :total="total"
        :current-page="currentPage"
        :page-size="pageSize"
        @paging-change="loadUserData"
        @selection-change="handleSelectionChange"
      >
        <!-- 显示列：选择、用户名、邮箱、角色等 -->
        <el-table-column type="selection" width="55" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="role" label="角色">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'primary'">
              {{ row.role === "admin" ? "管理员" : "普通用户" }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="{ row }">
            <el-switch
              v-model="row.status"
              :active-value="'active'"
              :inactive-value="'inactive'"
              @change="handleStatusChange(row)"
            />
          </template>
        </el-table-column>
        <!-- 操作列：编辑、删除按钮 -->
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <MgButton type="primary" size="small" @click="handleEdit(row)">
              编辑
            </MgButton>
            <MgButton type="danger" size="small" @click="handleDelete(row)">
              删除
            </MgButton>
          </template>
        </el-table-column>
      </MgTable>
    </div>

    <!-- 编辑对话框：用于新增或编辑用户 -->
    <MgDialog v-model="editDialogVisible" title="编辑用户" width="500px">
      <el-form
        ref="formRef"
        :model="formData"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item prop="username" label="用户名">
          <el-input v-model="formData.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item prop="email" label="邮箱">
          <el-input
            v-model="formData.email"
            type="email"
            placeholder="请输入邮箱"
          />
        </el-form-item>
        <el-form-item prop="role" label="角色">
          <el-select v-model="formData.role">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-switch
            v-model="formData.status"
            :active-value="'active'"
            :inactive-value="'inactive'"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <MgButton @click="editDialogVisible = false">取消</MgButton>
        <MgButton type="primary" :loading="submitting" @click="handleSubmit">
          保存
        </MgButton>
      </template>
    </MgDialog>
  </div>
</template>

<script setup lang="ts">
import type { FormInstance, FormItemRule } from "element-plus";

// 获取用户管理的API方法
interface User {
  id: string;
  username: string;
  email?: string;
  role?: string;
  status?: string;
}

const search = ref<{ name: string; status: string }>({
  name: "",
  status: "",
});

const searchData = () => {
  console.log(search.value);
};

// 表单引用
const formRef = ref<FormInstance>();

// 状态管理
const userList = ref<User[]>([]);
const selectedUsers = ref<User[]>([]);
const total = ref(0);
const currentPage = ref(1);
const pageSize = ref(10);
const editDialogVisible = ref(false);
const submitting = ref(false);
const isEditing = ref(false);
const editingUserId = ref<number | string | null>(null);

// 表单数据
const formData = reactive({
  username: "",
  email: "",
  role: "user" as "admin" | "user",
  status: "active" as "active" | "inactive",
});

// 表单验证规则
const formRules: Record<string, FormItemRule[]> = {
  username: [
    { required: true, message: "请输入用户名", trigger: "blur" },
    { min: 3, max: 20, message: "长度在 3 到 20 个字符", trigger: "blur" },
  ],
  email: [
    { required: true, message: "请输入邮箱", trigger: "blur" },
    { type: "email" as any, message: "请输入正确的邮箱地址", trigger: "blur" },
  ],
};

// 加载用户数据
const loadUserData = async () => {
  console.log("加载用户数据");
  // 调用查询接口
  userList.value = [
    {
      id: "1",
      username: "张三",
      email: "zhangsan@example.com",
      role: "admin",
      status: "active",
    },
    {
      id: "2",
      username: "李四",
      email: "lisi@example.com",
      role: "user",
      status: "active",
    },
    {
      id: "3",
      username: "王五",
      email: "wangwu@example.com",
      role: "user",
      status: "inactive",
    },
    {
      id: "4",
      username: "赵六",
      email: "zhaoliu@example.com",
      role: "admin",
      status: "active",
    },
    {
      id: "5",
      username: "孙七",
      email: "sunqi@example.com",
      role: "user",
      status: "active",
    },
    {
      id: "6",
      username: "周八",
      email: "zhouba@example.com",
      role: "user",
      status: "inactive",
    },
    {
      id: "7",
      username: "吴九",
      email: "wujiu@example.com",
      role: "admin",
      status: "active",
    },
    {
      id: "8",
      username: "郑十",
      email: "zhengshi@example.com",
      role: "user",
      status: "active",
    },
  ];
};

// 处理选择变化
const handleSelectionChange = (selection: User[]) => {
  selectedUsers.value = selection;
};

// 处理工具栏事件
const handleToolbarEvent = (code: string) => {
  if (code === "add") {
    // 新增用户
    isEditing.value = false;
    editingUserId.value = null;
    formData.username = "";
    formData.email = "";
    formData.role = "user";
    formData.status = "active";
    editDialogVisible.value = true;
  } else if (code === "batchDelete") {
    // 批量删除
    handleBatchDelete();
  }
};

// 批量删除
const handleBatchDelete = async () => {
  if (selectedUsers.value.length === 0) {
    ElMessage.warning("请先选择要删除的用户");
    return;
  }
  // 调用删除接口
};

// 编辑用户
const handleEdit = (row: User) => {
  console.log("编辑用户", row);
  isEditing.value = true;
  editingUserId.value = row.id;
  formData.username = row.username;
  formData.email = row.email;
  formData.role = row.role;
  formData.status = row.status;
  editDialogVisible.value = true;
};

// 删除用户
const handleDelete = async (row: User) => {
  console.log("删除用户", row);
  // 调用删除接口
};

// 处理状态变化
const handleStatusChange = async (row: User) => {
  console.log("处理状态变化", row);
  // 调用更新接口
};

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;
  const valid = await formRef.value.validate();
  console.log("表单校验", valid);
  // 调用新增接口
};

// 初始加载
onMounted(() => {
  loadUserData();
});
</script>

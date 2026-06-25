<template>
  <div class="flex h-full min-h-0 flex-col">
    <el-form ref="formRef" class="max-w-[720px]" :model="formData" :rules="formRules" label-width="120px">
      <el-form-item label="资源编码" prop="code">
        <el-input
          v-model.trim="formData.code"
          :disabled="isEdit"
          maxlength="50"
          placeholder="请输入资源编码"
          show-word-limit
        />
      </el-form-item>

      <el-form-item label="资源名称" prop="name">
        <el-input v-model.trim="formData.name" maxlength="100" placeholder="请输入资源名称" show-word-limit />
      </el-form-item>

      <el-form-item label="状态" prop="state">
        <el-radio-group v-model="formData.state">
          <el-radio label="enabled">启用</el-radio>
          <el-radio label="disabled">停用</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="备注" prop="remark">
        <el-input
          v-model.trim="formData.remark"
          type="textarea"
          :rows="4"
          maxlength="500"
          placeholder="请输入备注"
          show-word-limit
        />
      </el-form-item>
    </el-form>

    <div class="h-[40px] py-4 pl-[120px]">
      <el-button v-if="showReset" @click="onReset">重置</el-button>
      <el-button v-if="showCancel" @click="onCancel">取消</el-button>
      <el-button type="primary" :loading="submitLoading" @click="onConfirm">确认</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useVModel } from '@vueuse/core'
import type { FormInstance, FormRules } from 'element-plus'
import type { XxxSaveReq } from '@/api/xxx/types'

defineOptions({ name: 'XxxForm' })

const props = withDefaults(
  defineProps<{
    modelValue?: Partial<XxxSaveReq>
    isEdit?: boolean
    showCancel?: boolean
    showReset?: boolean
    submitLoading?: boolean
  }>(),
  {
    modelValue: () => ({}),
    isEdit: false,
    showCancel: false,
    showReset: false,
    submitLoading: false,
  }
)

const emit = defineEmits<{
  'update:modelValue': [Partial<XxxSaveReq>]
  confirm: [XxxSaveReq]
  cancel: []
}>()

const defaultForm = (): XxxSaveReq => ({
  name: '',
  code: '',
  state: 'enabled',
  remark: '',
})

const formData = useVModel(props, 'modelValue', emit, {
  passive: true,
  defaultValue: defaultForm(),
})

const formRef = ref<FormInstance>()

const formRules: FormRules<XxxSaveReq> = {
  code: [
    { required: true, message: '请输入资源编码', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' },
  ],
  name: [
    { required: true, message: '请输入资源名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' },
  ],
  state: [{ required: true, message: '请选择状态', trigger: 'change' }],
  remark: [{ max: 500, message: '长度不能超过 500 个字符', trigger: 'blur' }],
}

const onConfirm = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  emit('confirm', { ...defaultForm(), ...formData.value })
}

const onReset = () => {
  formData.value = defaultForm()
  formRef.value?.clearValidate()
}

const onCancel = () => {
  emit('cancel')
}
</script>

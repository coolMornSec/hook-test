<template>
  <MgBackWrap title="新增资源">
    <XxxForm
      :submit-loading="submitLoading"
      show-cancel
      show-reset
      @confirm="onConfirm"
      @cancel="onCancel"
    />
  </MgBackWrap>
</template>

<script setup lang="ts">
import XxxApi, { type XxxSaveReq } from "@/api/xxx.api";
import XxxForm from "./components/XxxForm.vue";

defineOptions({ name: "XxxAdd" });

const router = useRouter();
const submitLoading = ref(false);

const onConfirm = async (data: XxxSaveReq) => {
  submitLoading.value = true;
  try {
    await XxxApi.create(data);
    ElMessage.success("保存成功");
    router.back();
  } finally {
    submitLoading.value = false;
  }
};

const onCancel = () => {
  router.back();
};
</script>

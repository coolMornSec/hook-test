<template>
  <!-- 使用 MgLayout 组件 -->
  <MgLayout>
    <!-- aside 区 -->
    <template #aside>
      <!-- 树组件 -->
      <MgTree
        :data="treeData"
        :is-need-expand="true"
        :is-need-reload="true"
        :is-need-search="true"
        :icon-list="['wenjianjia1', 'bumenyongneng']"
        highlight
        default-expand-all
        node-key="nodeId"
        @node-click="handleTreeNodeClick"
      ></MgTree>
    </template>
    <!-- header 区 -->
    <template #header>
      <!-- 搜索组件 -->
      <MgSearch @search="onSearch">
        <template #search>
          <el-form-item label="搜索条件 1">
            <el-input
              v-model.trim="search.keyword"
              clearable
              placeholder="搜索条件 1"
            ></el-input>
          </el-form-item>
          <el-form-item label="搜索条件 2">
            <el-select
              v-model="search.state"
              placeholder="搜索条件 2"
              clearable
            >
              <!-- 下拉选项 -->
            </el-select>
          </el-form-item>
        </template>
      </MgSearch>
    </template>
    <!-- main 区 -->
    <template #main>
      <!-- 工具栏 (可选) -->
      <MgToolbar :select-length="multipleSelection.length">
        <MgButton type="primary"> 新增 </MgButton>
        <MgButton type="danger" @click="deleteRows(multipleSelection)">
          批量删除
        </MgButton>
        <MgButton> 其他工具按钮 </MgButton>
      </MgToolbar>

      <!-- 数据表格, 根据是否需要分页设置 hide-page 属性 -->
      <Mg-Table
        :page-size="page.size"
        :current-page="page.page"
        :hide-page="false"
        :data="tableData"
        :total="total"
        @paging-change="queryData"
        @select="handleSelectionChange"
        @select-all="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column type="index" label="#" width="55" />
        <el-table-column
          label="名称"
          prop="name"
          min-width="160"
          show-overflow-tooltip
        />
        <!-- 其他列 -->
        <!-- 操作列 -->
        <el-table-column
          :label="$t('global.action.operation')"
          width="390"
          fixed="right"
        >
          <template #default="{ row }">
            <MgButton type="danger" @click="deleteRows([row])">删除</MgButton>
          </template>
        </el-table-column>
      </Mg-Table>
    </template>
  </MgLayout>
</template>

<script setup lang="ts">
const { queryXxxList, deleteXxx } = useXxxApi();

const treeData = ref([]);
const search = reactive({
  keyword: "",
  state: "",
});

const page = reactive({
  page: 1,
  size: 10,
});

const tableData = ref([]);
const total = ref(0);
const multipleSelection = ref([]);
const queryData = async () => {
  await queryXxxList({
    ...search,
    page: page.page,
    size: page.size,
  }).then((res) => {
    tableData.value = res.records;
    total.value = res.total;
  });
};

const handleSelectionChange = (val) => {
  multipleSelection.value = val;
};

const handleTreeNodeClick = (node) => {
  console.log(node);
};

const confirmDelete = useConfirm();

const deleteRows = async (rows) => {
  await confirmDelete(async () => {
    const ids = rows.map((row) => row.id);
    await deleteXxx(ids);
    await queryData();
  });
};

const onSearch = async () => {
  // 处理搜索操作
  await queryData();
};

onMounted(async () => {
  await queryData();
});
</script>

<style scoped lang="scss"></style>

import { useAxios } from '@magustek/framework-core'
import type { XxxDTO, XxxPageReq, XxxSaveReq } from '@/api/xxx/types'

const url = '/magus-service/xxx'
const { get, post } = useAxios()

export default {
  page: (params: XxxPageReq) => post<MgPageResponse<XxxDTO>>(`${url}/page`, params),
  findOne: (id: string) => get<MgDataResponse<XxxDTO>>(`${url}/find-by-id/${id}`),
  create: (data: XxxSaveReq) => post<MgBaseResponse>(`${url}/create`, data),
  update: (data: XxxSaveReq) => post<MgBaseResponse>(`${url}/update`, data),
  delete: (ids: string[]) => post<MgBaseResponse>(`${url}/delete`, ids),
}

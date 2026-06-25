export interface XxxPageReq extends MgPageReq {
  name?: string
  state?: string
}

export interface XxxSaveReq {
  id?: string
  name: string
  code: string
  state: string
  remark?: string
}

export interface XxxDTO {
  id: string
  name: string
  code: string
  state: string
  remark?: string
}

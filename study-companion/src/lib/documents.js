import api from "./api";

export async function listDocuments(notebookId) {
  const { data } = await api.get(`/notebooks/${notebookId}/documents/`);
  return data;
}

export async function uploadDocument(notebookId, file, title) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("title", title || file.name);

  const { data } = await api.post(`/notebooks/${notebookId}/documents/`, formData,);
  return data;
}

export async function deleteDocument(notebookId, documentId) {
  await api.delete(`/notebooks/${notebookId}/documents/${documentId}/`);
}
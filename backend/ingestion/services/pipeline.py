from notebooks.models import Document, Chunk
from ingestion.services.pdf_parser import extract_text_by_page
from ingestion.services.chunker import chunk_pages
from ingestion.services.embedder import embed_chunks


def process_document(document_id: int) -> None:
    try:
        document = Document.objects.get(id=document_id)

        document.status = Document.Status.PROCESSING
        document.save()

        pages_data = extract_text_by_page(document.file.path)
        chunks = chunk_pages(pages_data)
        chunks = embed_chunks(chunks)
        chunk_objects = []

        for chunk in chunks:
            chunk_objects.append(
                Chunk(
                    notebook=document.notebook,
                    document=document,
                    content=chunk["content"],
                    embedding=chunk["embedding"],
                    page_number=chunk["page_number"],
                    chunk_index=chunk["chunk_index"],
                    section_title=chunk["section_title"],
                )
            )
        Chunk.objects.bulk_create(chunk_objects)

        document.status = Document.Status.READY
        document.save()

    except Document.DoesNotExist:
        return None
    except Exception as e:
        document.status = Document.Status.FAILED
        document.save()
        raise

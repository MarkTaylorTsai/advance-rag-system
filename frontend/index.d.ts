import { SvelteComponentTyped } from 'svelte';

/** Components */
export class KnowledgeBase extends SvelteComponentTyped<{
    selectedId?: string;
    onSelect?: (id: string) => void;
}> {}

export class DocumentSettings extends SvelteComponentTyped<{
    config: any;
    onSave: (newConfig: any) => void;
}> {}

/** API Interfaces */
export interface RAGFile {
    id: string;
    filename: string;
    status: 'processed' | 'processing' | 'error';
    meta?: Record<string, any>;
}

export interface KnowledgeItem {
    id: string;
    name: string;
    description: string;
    file_ids: string[];
}

/** API Namespaces */
export namespace RetrievalAPI {
    /** Fetches the status of a file processing task */
    function getFileStatus(
        id: string
    ): Promise<{ status: string; progress: number }>;

    /** Triggers a web search or URL crawl for RAG context */
    function processWebUrl(url: string): Promise<{ file_id: string }>;

    /** Retrieves relevant chunks for a given query (RAG search) */
    function queryRAG(query: string, collection_id?: string): Promise<any[]>;
}

export namespace KnowledgeAPI {
    /** Returns all available knowledge bases */
    function getKnowledgeBases(): Promise<KnowledgeItem[]>;

    /** Creates a new knowledge collection */
    function createKnowledge(data: {
        name: string;
        description: string;
    }): Promise<KnowledgeItem>;

    /** Adds a file to a specific knowledge base */
    function addFileToKnowledge(knowledgeId: string, fileId: string): Promise<void>;
}

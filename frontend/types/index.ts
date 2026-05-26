export interface RepoResponse {
  id: string;
  owner: string;
  repo_name: string;
  status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  architecture_summary?: string;
  created_at: string;
  last_queried_at: string;
}

export interface Citation {
  file_path: string;
  text_snippet: string;
}

export interface QueryResponse {
  answer: string;
  citations: Citation[];
}

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: Citation[];
  isLoading?: boolean;
}

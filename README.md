# llm-rag

#### Description

llm-rag is a project focused on optimizing retrieval and generation tasks, utilizing advanced RAG (Retrieval-Augmented Generation) techniques to enhance the quality of information retrieval and answer generation. Through query rewriting, HyDE (Hypothetical Document Embeddings), hierarchical indexing, router-based tool selection, retrieval optimization, and re-ranking steps, it achieves efficient information retrieval and precise answer generation.

Advanced RAG technology has been proven to be a very effective technology to improve the ability of  LLM to  deal with Natural Language tasks, such as working as a chatbot.In our work,we first leverage Advanced RAG to complete a digital circuit automatic design task, specifically automatically generating whole code of an 8-bit processor with hardware description language. The workflow is shown in Figure*.

#### Software Architecture

This project adopts a modular design with the following main components:
- **Query Rewrite**: Rewrites user queries to improve recall rates.
- **HyDE Query Transformation**: Uses LLM to generate hypothetical documents to aid in retrieval.
- **Hierarchical Indexing**: Constructs multi-level indexes to optimize retrieval efficiency.
- **Router for Tool Selection**: Dynamically selects the most suitable retrieval tools or information sources based on user queries.
- **Advanced Retrieval Strategies**: Includes automatic merged retrieval, hybrid search strategies, etc.
- **Re-ranking**: Re-ranks retrieved results to enhance relevance.
![图片1](https://github.com/user-attachments/assets/3b7a8049-4a04-4420-bd2e-e7730739f2d6)

#### Installation

1. Ensure you have Python 3.x installed.
2. Install the required dependencies using pip:
3. shell
   pip install -r requirements.txt
3.Configure database connections or other external services as needed.

#### Contribution

Fork this repository.
Create a new branch (named feat_your_feature).
Make your code changes and commit them to the new branch.
Create a Pull Request for review and merging.

#### RAG Optimization Details

Query Rewrite: Improves recall rates by rewriting queries.
HyDE Query Transformation: Generates hypothetical documents based on LLM knowledge to improve retrieval accuracy.
Hierarchical Indexing: Builds a three-level index structure (e.g., [2048, 512, 128]) and uses AutoMergeRetriever to automatically merge child nodes back to parent nodes during retrieval.
Router for Tool Selection: Matches queries with descriptions of retrieval tools via Selector to dynamically choose the best tool.
Advanced Retrieval Strategies: Combines vector-based retrieval with BM25 retrieval and uses the Reciprocal Rank Fusion (RRF) algorithm for preliminary ranking.
Re-ranking: Utilizes SentenceTransformerRerank to re-rank retrieved results, ensuring that highly relevant content is prioritized.

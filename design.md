# Design

## Main App requirements
1. News-Catalog is a Desktop app (Possibly enhanced to web app)
2. Newses are gathered from many websites
3. Newses are presented in simple way - only text
4. Newses can be filtered be website, author, topic, keywords, date
5. There are tags assigned to newses based on their content
6. Newses can be marked by user as interesting/not interesting
7. Newses probability to be interesting for specific user is evaluated - based on that only possibly interesting newses are recommended to user, but he/she can see all newses
8. **Initial Scraping**: On the first run (empty database), the system should only fetch articles from the last 2 days to avoid overloading.

## Architecture: Data Abstraction Layer
To ensure the UI remains decoupled from the storage implementation, the project uses an **Interface-based Abstraction Layer**:
1. **Interfaces**: Define standard protocols (e.g., `NewsRepository`) for data access.
2. **Implementation**: Specific handlers (like `MongoDBHandler`) implement these interfaces.
3. **Frontend**: Streamlit interacts only with the interfaces, allowing for easy swapping of the underlying database (e.g., to PostgreSQL or a Mock DB for testing).

## Development flow
Gitflow will be used. Main branch contains only released code. Develop branch contains code that is being developed currently. Feature branches are merged to develop. There is no need of using release branches.

## Technologies used
* **Core**: Python
* **Scraping**: Scrapy
* **Storage**: MongoDB (accessed via Abstraction Layer)
* **UI**: Streamlit
* **Data Processing**: Pandas

## Project Progress & Roadmap

### Phase 1: Foundation (Scrapy & MongoDB)
- [x] Specify Scraped Data Structure in `items.py`.
- [x] Create Scrapy spider for WP.
- [x] Create initial `MongoDBHandler`.
- [x] Create pipeline to connect spider and database with watermark logic.
- [x] Implement duplicate removal in pipeline.

### Phase 2: Dependency Management (uv)
- [x] Initialize project with `uv`.
- [x] Migrate `requirements.txt` to `pyproject.toml` managed by `uv`.
- [x] Set up `uv` lockfile and environment.

### Phase 3: Decoupling & Abstraction
- [ ] Define Python Protocols/Interfaces for Data Access (Repository Pattern).
- [ ] Refactor `MongoDBHandler` to implement these interfaces.
- [ ] Update Streamlit to use the Interface instead of `MongoDBHandler` directly.

### Phase 4: Scalability & Performance
- [ ] Implement Pagination in the Interface and MongoDB implementation.
- [ ] Update UI to load data lazily/in chunks.
- [ ] Separate scraping process from UI startup (background/scheduled tasks).

### Phase 5: Enhancements
- [ ] Implement AI-based tagging/topic extraction.
- [ ] Implement user preference evaluation (Recommendation system).
- [ ] Expand scraping to multiple news websites.
* [x] add [Dependency Injector](https://python-dependency-injector.ets-labs.org/)
  * [x] common tests
    * [x] rm common tests
  * [x] global wiring
* [x] async migrations (alembic+asyncpg) -> no way! won't fix!
* [ ] reorganize src/ structure
* implement
  * file storage classes with tests
    * FS
      * [ ] implementation
      * [ ] tests
    * S3
      * [ ] implementation
      * [ ] tests
  * data storage classes
    * PostgreSQL DAO (alembic, SQLAlchemy-core, asyncpg)
      * Books
        * [x] implementation
        * [ ] tests
      * Tags
        * [ ] implementation
        * [ ] tests
      * m2m
        * [ ] implementation
        * [ ] tests
    * InMemoryStub DAO
      * [ ] implementation
      * [ ] tests
  * Repositories
    * Books
      * [ ] implementation
      * [ ] tests
    * Tags
      * [ ] implementation
      * [ ] tests
* [ ] Data Mappers
* try events
  * [ ] Event storming
  * [ ] Event sourcing
  * [ ] Event Driven Architecture
    * [ ] message bus 
      * [ ] local pub-sub
      * [ ] any MQ
* DTO ?
  * xml
    * [ ] input
    * [ ] output
  * json
    * [ ] input
    * [ ] output
  * yaml
    * [ ] input
    * [ ] output
* [ ] Helm charts
* [ ] migrate to litestar
* [ ] HTMX

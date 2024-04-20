## REST API views MUST be here
## MUST NOT import anything outside, except global/common/utils/domain.DTO/domain.interface
### Dependency injection

* group by framework
```
rest/
    fastapi/
        app.py
        ...
    aiohttp/
        app.py
        ...
    litestar/
        app.py
        ...
```

* group by (framework, content-type)
```
rest/
    fastapi/
        app.py
        json/
        xml/
        yaml/
        etc/
    aiohttp/
        app.py
        json/
        xml/
        yaml/
        etc/
    litestar/
        app.py
        json/
        xml/
        yaml/
        etc/
```

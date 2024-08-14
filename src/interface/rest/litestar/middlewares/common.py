def path_to_route_name(app, path):
    app, handler, path, params = app.asgi_router.handle_routing(path, 'OPTIONS')
    return list(handler.paths)[0]

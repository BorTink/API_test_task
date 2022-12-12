from app.forum import views

# настраиваем пути, которые будут вести к нашей странице
def setup_routes(app):
    app.router.add_post('/new', views.new_user)
    app.router.add_get('/select', views.select_user)
    app.router.add_put('/edit', views.edit_user)
    app.router.add_get('/get_list', views.get_list)
    app.router.add_put('/deactivate', views.deactivate_user)
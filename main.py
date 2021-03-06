from bottle import error, get, post, redirect, request, response, route, run, static_file, template
import os
import utils


# Static Routes
@get("/js/<filepath:re:.*\.js>")
def js(filepath):
    return static_file(filepath, root="./js")


@get("/css/<filepath:re:.*\.css>")
def css(filepath):
    return static_file(filepath, root="./css")


@get("/images/<filepath:re:.*\.(jpg|png|gif|ico|svg)>")
def img(filepath):
    return static_file(filepath, root="./images")


@route('/home')
def index():
    sectionTemplate = "./templates/home.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@route('/')
def handle_root_url():
    redirect("/home")


@route('/browse/<order>')
def load_shows(order):
    list_shows = [utils.getJsonFromFile(show_id) for show_id in utils.AVAILABE_SHOWS]
    if order == "name":
        list_shows.sort(key=lambda x: x["name"])
    if order == "ratings":
        list_shows.sort(key=lambda x: x["rating"]["average"], reverse=True)
    sectionTemplate = "./templates/browse.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                    sectionData=list_shows)


@route('/browse')
def handle_root_url():
    redirect("/browse/name")


@route('/show/<show_id>')
def browse_show(show_id):
    show = utils.getJsonFromFile(int(show_id))
    if any(show):
        sectionTemplate = "./templates/show.tpl"
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                        sectionData=show)
    else:
        response.status = 404
        sectionTemplate = "./templates/404.tpl"
        return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                        sectionData=show)


@route('/ajax/show/<show_id>')
def browse_show(show_id):
    show = utils.getJsonFromFile(int(show_id))
    return template("./templates/show.tpl", result=show)


@route('/show/<show_id>/episode/<episode_id>')
def show_episode(show_id, episode_id):
    show = utils.getJsonFromFile(int(show_id))
    for episode in show['_embedded']['episodes']:
        if episode["id"] == int(episode_id):
            sectionTemplate = "./templates/episode.tpl"
            return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                            sectionData=episode)
        else:
            response.status = 404
            sectionTemplate = "./templates/404.tpl"
            return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate,
                            sectionData=episode)


@route('/ajax/show/<show_id>/episode/<episode_id>')
def show_episode(show_id, episode_id):
    show = utils.getJsonFromFile(int(show_id))
    for episode in show['_embedded']['episodes']:
        if episode["id"] == int(episode_id):
            return template("./templates/episode.tpl", result=episode)


@route('/search')
def search():
    sectionTemplate = "./templates/search.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


@post('/search')
def search_result():
    sectionTemplate = "./templates/search_result.tpl"
    query = request.forms.get('q')

    result = []
    list_shows = [utils.getJsonFromFile(id) for id in utils.AVAILABE_SHOWS]
    # i = 0

    for show in list_shows:
        # search functionality according the name of the show

        # if query in show["name"]:
        #   while i <= len(show["_embedded"]["episodes"])-1:
        #       show_result = {"showid": show["id"], "episodeid": show["_embedded"]["episodes"][i]["id"],
        #                      "text": show["name"] + ": " + show["_embedded"]["episodes"][i]["name"]}
        #       result.append(show_result)
        #       i += 1
        for episode in show["_embedded"]["episodes"]:
            if query in episode["name"] or (episode["summary"] is not None and query in episode["summary"]):
                episode_result = {"showid": show["id"], "episodeid": episode["id"],
                                  "text": show["name"] + ": " + episode["name"]}
                result.append(episode_result)

    result.sort(key=lambda x: x["text"])
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, query=query,
                    sectionData={}, results=result)


@error(404)
def error404(error):
    sectionTemplate = "./templates/404.tpl"
    return template("./pages/index.html", version=utils.getVersion(), sectionTemplate=sectionTemplate, sectionData={})


def main():
    run(host='localhost', port=os.environ.get('PORT', 7000))
    # run(host='0.0.0.0', port=os.environ.get('PORT', 5000))


if __name__ == "__main__":
    main()

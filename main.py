from fasthtml.common import *
from datetime import datetime


db = database("data/articles.db")
articles = db.t.articles

# create the article table if it doesn't exists
if articles not in db.t:
    articles.create(id=int, title=str, subtitle=str, content=str,
                    created_at=datetime, pk="id")


# add tailwind css
headers = (Script(src="https://cdn.tailwindcss.com"),)

# load app and dataclass
app = FastHTML(hdrs=(headers))

# footer tag
footer_tag = Footer(
    Div(
        P(" © The Daily Planet"),
        cls="container mx-auto flex flex-col justify-between items-center py-12"),
    cls="bg-gray-800 text-white mt-16 ",
)

# header tag
header_tag = Header(
    Nav(
        Div(A(Img(src="", cls="rounded-md w-4"), href="/")),
        H2(A("The Daily Planet", href="/", cls="text-2xl font-medium text-zinc-800")),

        Button("Add New Post", cls="bg-purple-700 px-3 py-3 rounded-md text-white font-medium",
               hx_get="/articles/create/", hx_target="main", hx_swap="outerHTML"),
        cls="flex bg-gray-50 border border-gray-200 items-center justify-between px-8 py-4",),
    Div(
        A("Home", href="/"), cls="px-6 py-4 border-b border-gray-200 text-purple-700 font-medium text-underline"),)


# index page
@app.get("/")
def home():
    if articles.count == 0:
        return (header_tag,
                Main(
                    Div(
                        H1("No Article Found", cls='text-2xl'),
                        cls="py-4 px-4 mb-[20rem]"
                    ), cls="main"
                ),
                footer_tag,
                )
    # list to hold our articles
    arts = []
    for art in articles.rows:
        article_id = art["id"]
        img_src = art.get("img", f"https://picsum.photos/id/{article_id+10}/300"
                          )
        title = art['title']
        subtitle = art['subtitle']
        created_at = art['created_at']
        a = Article(
            Img(src=img_src,

                cls="w-full h-48 object-cover"
                ),
            Div(H3(
                A(title, href=f"/articles/{article_id}",
                  cls="text-purple-700 text-2xl"),
                cls="text-l font-medium text-gray-900"),
                P(subtitle,
                  cls="text-gray-700"),
                P(created_at, cls="text-gray-700 text-md py-3"),
                cls="pt-4 px-2"),
            cls="bg-white shadow-md rounded-lg overflow-hidden"
        )
        arts.append(a)
    # returns a lists of articles if it exists
    return (
        header_tag,
        Main(
            Div(*arts, cls="grid grid-cols-4 gap-4 px-6"),
            cls="main"),
        footer_tag,
    )

# route to view a single article by id


@app.get("/articles/{article_id}")
def get_article(article_id: int):
    if articles.count == 0:
        return (header_tag,
                Main(
                    Div(
                        H1("No Article Found", cls='text-2xl'),
                        cls="py-4 px-4 mb-[20rem]"
                    ),
                    cls="main"),
                footer_tag,
                )

    article = articles[article_id]
    img_src = f"https://picsum.photos/id/{article_id+10}/600"
    print(article.get("title"))
    return (header_tag,
            Main(
                Article(
                    H1(article.get("title"), cls="text-3xl font-bold pb-4"),
                    H4(article.get("subtitle"), cls="pb-4"),
                    Img(src=img_src, cls="w-full h-48 object-cover"
                        ),
                    P(article.get("content"), cls="pt-6"),
                    cls="mt-2 m-auto px-80"
                ),
                cls="main"
            ), footer_tag,
            )
# route to post article


@app.post("/articles/create/")
def create_article(title: str, subtitle: str, content: str):
    a_id = articles.count + 1
    articles.insert(
        {"id": a_id, "title": title, "subtitle": subtitle, "content": content})
    return RedirectResponse("/", status_code=302)


# route to view page for adding article
@app.get("/articles/create/")
def get_article():
    sect = Section(
        Form(
            Div(
                Label("Title", title="title",
                      cls="block text-sm font-medium text-gray-700"),
                Input(name="title", id="title", required=true,
                      cls="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm h-10 px-2"),
            ),
            Div(Label("subtitle", title="subtitle",
                      cls="block text-sm font-medium text-gray-700"),
                Input(name="subtitle", id="subtitle", required=true,
                      cls="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm h-10 px-2")),
            Div(
                Label("content", title="content",
                      cls="block text-sm font-medium text-gray-700"),
                Textarea(name="content", id="content", required=true,
                         cls="mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm h-36 px-4 py-4  "), contenteditable=true),
            Div(
                Button(
                    "Create Post", type="submit", cls="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                ),
            ),
            action='/articles/create/', method='post',
            cls="max-w-md mx-auto space-y-6 pt-6 pb-32"),
    )
    return (sect)


# run the fasthtml server
serve()

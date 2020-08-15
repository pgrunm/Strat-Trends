from errbot import BotPlugin, webhook


class WebhookExample(BotPlugin):

    # Basic Webhook for new article. Just for demo purposes.
    @webhook('/new_article/<name>/<url>/')
    def new_article(self, request, name, url):
        return f"New article with title {name} is available at: {url}"

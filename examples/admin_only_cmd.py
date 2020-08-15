from errbot import BotPlugin, arg_botcmd, botcmd, logging, webhook


@botcmd
def example_command(self, msg, args, admin_only=True):
    # Just a simple example to show how admin only commands work.
    self.warn_admins('Warning, something really bad happened!')

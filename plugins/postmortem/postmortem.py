from errbot import BotPlugin, botcmd, arg_botcmd, webhook, logging
import sqlite3


class Postmortem(BotPlugin):
    """
    A plugin to create and view postmortems.
    """

    def activate(self):
        """
        Triggers on plugin activation

        You should delete it if you're not using it to override any default behaviour
        """
        super(Postmortem, self).activate()

        # Create the postmortem database
        # Create a database connection and a cursor for executing commands.
        conn = sqlite3.connect('postmortem.db')
        c = conn.cursor()

        try:
            # Create database with tables
            c.executescript('''
            CREATE TABLE "Sources" (
            "source_id"	INTEGER,
            "url"	TEXT, 
            "last_access_timestamp"	TEXT, 
            "http_status_code"	INTEGER, 
            PRIMARY KEY("source_id"));
            
            CREATE TABLE "Postmortems" (
            "content"	TEXT,
            "fk_source_id"	INTEGER,
            "postmortem_id" INTEGER,
            FOREIGN KEY("fk_source_id") REFERENCES "Sources"("source_id"),
            PRIMARY KEY("postmortem_id"));
            ''')

            # close the database connection
            conn.commit()

        except sqlite3.OperationalError as oe:
            self.log.error(f'Error occured while creating database: {oe}')
        conn.close()

    def deactivate(self):
        """
        Triggers on plugin deactivation

        You should delete it if you're not using it to override any default behaviour
        """
        super(Postmortem, self).deactivate()

    def get_configuration_template(self):
        """
        Defines the configuration structure this plugin supports

        You should delete it if your plugin doesn't use any configuration like this
        """
        return {'EXAMPLE_KEY_1': "Example value",
                'EXAMPLE_KEY_2': ["Example", "Value"]
                }

    def check_configuration(self, configuration):
        """
        Triggers when the configuration is checked, shortly before activation

        Raise a errbot.ValidationException in case of an error

        You should delete it if you're not using it to override any default behaviour
        """

        super(Postmortem, self).check_configuration(configuration)

    def callback_connect(self):
        """
        Triggers when bot is connected

        You should delete it if you're not using it to override any default behaviour
        """
        pass

    def callback_message(self, message):
        """
        Triggered for every received message that isn't coming from the bot itself

        You should delete it if you're not using it to override any default behaviour
        """
        pass

    def callback_botmessage(self, message):
        """
        Triggered for every message that comes from the bot itself

        You should delete it if you're not using it to override any default behaviour
        """
        pass

    @arg_botcmd('name', type=str)
    @arg_botcmd('--favorite-number', type=int, unpack_args=False)
    def hello(self, message, args):
        """
        A command which says hello to someone.

        If you include --favorite-number, it will also tell you their
        favorite number.
        """
        if args.favorite_number is None:
            return f'Hello {args.name}.'
        else:
            return f'Hello {args.name}, I hear your favorite number is {args.favorite_number}.'

    # Own functions

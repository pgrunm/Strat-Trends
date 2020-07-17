import sqlite3

import certifi
import urllib3
from errbot import BotPlugin, arg_botcmd, botcmd, logging, webhook


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
        try:
            Postmortem.create_postmortem_database()
        except sqlite3.OperationalError as oe:
            self.log.error(f'Error while creating the database: {oe}')

        # Create variables for execution statements etc.
        self.conn = sqlite3.connect('postmortem.db', check_same_thread=False)
        self.c = self.conn.cursor()

    def deactivate(self):
        """
        Triggers on plugin deactivation

        You should delete it if you're not using it to override any default behaviour
        """
        self.conn.close()
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
    @staticmethod
    def create_postmortem_database():
        # Create the postmortem database
        # Create a database connection and a cursor for executing commands.
        conn = sqlite3.connect('postmortem.db')
        c = conn.cursor()

        try:
            # Create database with tables
            c.executescript('''
            CREATE TABLE "Sources" (
            "source_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
            "url"	TEXT,
            "last_access_timestamp"	TEXT,
            "http_status_code"	INTEGER,
            PRIMARY KEY("source_id"));  

            CREATE TABLE "Postmortems" (
            "content"	TEXT,
            "fk_source_id"	INTEGER,
            "postmortem_id"	INTEGER PRIMARY KEY AUTOINCREMENT,
            FOREIGN KEY("fk_source_id") REFERENCES "Sources"("source_id"));
            ''')

            # close the database connection
            conn.commit()

        except sqlite3.OperationalError as oe:
            raise sqlite3.OperationalError(
                f'Error occured while creating database: {oe}')
        conn.close()

    # Feed related commands
    @botcmd
    def feeds(self, msg, args):
        """
        A command to display all current feeds. Alias for /feed list
        """
        self.log.debug(
            'Called the feeds commands and calling feeds_list function.')
        # Call the /feed list function and return it's values.
        return self.feed_list(msg, args)

    @botcmd
    def feed_list(self, msg, args):
        """
        A command to display all current feeds.
        """
        self.c.execute('select source_id, url from Sources;')

        # Fetch all rows
        query = self.c.fetchall()
        self.log.debug(f'Query returned: {query}')
        query_string = 'Currently subscribed feeds:'

        # Build a string to return
        for source_id, url in query:
            query_string += f'ID {source_id}: URL {url}\n'

        self.log.debug(f'Query string value is {query_string}')
        return query_string

    @botcmd
    def feed_add(self, msg, args):
        """
        Command allows to add new feeds.
        """
        self.log.debug(f'Arguments are: {args}.')
        url = urllib3.util.parse_url(args)
        if url.host == None:
            return f'Please use /feed add <URL> to add a new feed.'

        # Check if url is already in database
        self.c.execute(
            'SELECT DISTINCT URL FROM SOURCES WHERE url=?', (url.host,))
        result = self.c.fetchone()

        if result != None:
            self.log.warning(f'Url {url.host} already in database')
            return f'URL {url.host} is already saved to database. Feel free to add a different one.'
        elif self.c != None:
            # Try to retrieve the url
            http = urllib3.PoolManager(
                timeout=3.0, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
            try:
                response = http.request('GET', args)
            except urllib3.exceptions.MaxRetryError as read_err:
                self.log.critical(
                    f'Could not access url {url} while adding it, error: {read_err}')
            # SSL Error
            except urllib3.exceptions.SSLError as tls_err:
                self.log.critical(f'TLS verification error occure: {tls_err}')
            if response.status == 200:
                # Insert a row of data: url, last_access, http_status_code
                try:
                    # Null works with auto increment
                    self.c.execute(
                        f"INSERT INTO Sources VALUES (NULL, '{args}', 'Unknown', 200)")
                    # Save (commit) the changes
                    self.conn.commit()
                except sqlite3.Error as sqlite_error:
                    self.log.error(
                        f'Error while saving to database: {sqlite_error}')
                else:
                    self.log.info(f'Successfully saved {args} to database.')
                    return f'URL {args} saved to database.'

    @ botcmd
    def feed_delete(self):
        """
        Command allows to remove feeds.
        """
        pass

#!/usr/bin/env python

import twitter
import time

class Tweet:

    def __init__(self):
        self.consumer_keyflag    = "1234"
        self.consumer_secretflag = "1234"
        self.access_keyflag      = "1234"
        self.access_secretflag   = "1234"
        self.encoding            = None
        self.api  = twitter.Api(self.consumer_keyflag, self.consumer_secretflag, self.access_keyflag, self.access_secretflag, self.encoding)
        self.user = self.api.GetUser(screen_name="SlowConcert")
        print "--> myTwitter: Init ok with username " + self.user.name

    def post(self, message):
        message = message + "\nPlayed on " + str(time.ctime())
        try:
            status = self.api.PostUpdate(message)
        except UnicodeDecodeError:
            print "Your message could not be encoded.  Perhaps it contains non-ASCII characters? "
            print "Try explicitly specifying the encoding with the --encoding flag"
            sys.exit(2)
        print "--> " + status.user.name + " just posted:\n" + message

    def post_fake(self, message):
        message = message + "\nPlayed on " + str(time.ctime())
        print "--> FAKE: " + self.user.name + " just posted:\n" + message

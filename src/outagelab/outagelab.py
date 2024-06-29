"""Main module."""

import http.client
import time
import threading

import requests

account = None

def init(application, environment, api_key, host=None):

    def getresponse(self, *k, **kw):
        res = _getresponse(self, *k, **kw)

        if self.host in host:
            return res

        try:
            print(self.host, res.status)
            global account
            acct = account
            if acct == None:
                print("no account")
                return res

            app = None
            for a in acct.get("applications", []):
                if a["id"] == application:
                    app = a

            if app == None:
                print("no app")
                return res

            env = None
            for e in app.get("environments", []):
                if e["id"] == environment and e["enabled"]:
                    env = e

            if env == None:
                print("no env")
                return res

            rule = None
            for r in app.get("rules", []):
                if self.host == r["host"] and r["enabled"]:
                    rule = r

            if rule == None:
                print("no rule")
                return res

            print(f"rule status: {rule["status"]} delay: {rule["duration"]}")

            if rule["status"]:
                res.status = rule["status"]
                res.reason = http.client.responses.get(rule["status"], "Unknown")

            if rule["duration"]:
                time.sleep(rule["duration"])

            return res
        except Exception as e:
            print(f"outagelab interceptor error: {e}")
            pass
        finally:
            return res


    _getresponse = http.client.HTTPConnection.getresponse
    http.client.HTTPConnection.getresponse = getresponse

    def _poll():
        global account
        while True:
            try:
                res = requests.post(host + "/api/datapage", headers={
                    "x-api-key": api_key
                })
                account = res.json()
            except Exception as e:
                print(e)
                account = None
            time.sleep(5)

    threading.Thread(target=_poll, daemon=True).start()

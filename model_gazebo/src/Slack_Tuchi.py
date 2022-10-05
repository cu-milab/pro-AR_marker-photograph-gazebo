# -- coding: utf-8 --
import sys
sys.path.append("/home/milab/.local/lib/python3.5/site-packages")

import slackweb

def Tuchi(i):
    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")

    # 何らかの処理
    slack.notify(text= str(i))

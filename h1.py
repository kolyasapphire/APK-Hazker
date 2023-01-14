#!/usr/bin/env python
# coding: utf-8

import requests
import json

query_url = "https://hackerone.com/programs/search?query=type:hackerone&sort=published_at:descending&page={page}"

scope_query = """
    query($handle: String!) {
      team(handle: $handle) {
        structured_scopes() {
          edges {
            node {
              asset_identifier,
              asset_type,
              eligible_for_bounty,
              max_severity,
            }
          }
        }
      }
    }
"""

def hackerone_to_list():
    targets = {
        'android': [],
        'androidnobounty': [],
    }
    page = 1
    with requests.Session() as session:
        while True:
            r = session.get(query_url.format(page=page))
            page += 1
            if r.status_code != 200:
                break
            print('got programs page')
            resp = json.loads(r.text)
            for program in resp['results']:
                r = session.get("https://hackerone.com{program}".format(
                    program=program['url']),
                    headers={'Accept': 'application/json'})
                if r.status_code != 200:
                    print('unable to retreive %s', program['name'])
                    continue

                resp = json.loads(r.text)
                query = json.dumps({'query': scope_query,
                                    'variables': {'handle': resp['handle']}})
                r = session.post("https://hackerone.com/graphql",
                                 data=query,
                                 headers={'content-type': 'application/json'})
                scope_resp = json.loads(r.text)
                print('got ' + resp['handle'])

                for e in scope_resp['data']['team']['structured_scopes']['edges']:
                    if e['node']['asset_type'] == 'GOOGLE_PLAY_APP_ID' and e['node']['max_severity']  != 'none':
                        domain = e['node']['asset_identifier']
                        if e['node']['eligible_for_bounty']:
                            targets['android'].append(domain)
                        else:
                            targets['androidnobounty'].append(domain)
    return targets


if __name__ == "__main__":
    targets = hackerone_to_list()
    with open('output/playids/android.txt', 'w+') as f:
        f.write('\n'.join(targets['android']))
    with open('output/playids/androidnobounty.txt', 'w+') as f:
        f.write('\n'.join(targets['androidnobounty']))
    print('done with h1')
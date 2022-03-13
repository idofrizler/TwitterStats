import json, codecs
from pprint import pprint
from collections import defaultdict

TWITTER_DATA_PATH = '<YOUR_EXTRACTED_TWITTER_ARCHIVE_PATH>'
PREFIX = u'window.YTD.ad_impressions.part0 = '

with codecs.open(TWITTER_DATA_PATH + 'data\\ad-impressions.js', encoding='utf-8') as f:
    data = f.read()[len(PREFIX):] 
    d = json.loads(data)

targeting = defaultdict(int)
advertisers = defaultdict(int)
total_ads = 0

for ad in d:
    ad_impressions = ad['ad']['adsUserData']['adImpressions']['impressions']
    total_ads += len(ad_impressions)
    for ad_data in ad_impressions:
        advertisers[ad_data.get('advertiserInfo', {}).get('screenName', 'N/A')] += 1
        for criterion in ad_data.get('matchedTargetingCriteria', []):
            targeting_type = criterion['targetingType']
            val = criterion.get('targetingValue', 'N/A') if targeting_type != 'Tailored audience CRM lookalike targeting' else 'N/A'
            targeting[(targeting_type, val)] += 1
            
sorted_advertisers = sorted(advertisers.items(), key=lambda x: x[1], reverse=True)
sorted_targeting = sorted(targeting.items(), key=lambda x: x[1], reverse=True)

print('Total ads: {}'.format(total_ads))
print('Total distinct advertisers: {}'.format(len(advertisers.keys())))
print()
print('Top advertisers: ')
pprint(sorted_advertisers[:20])
print()
print('Top matching criteria: ')
pprint(sorted_targeting[:40])
print()

top_interests = [c for c in sorted_targeting if c[0][0] == 'Interests'][:10]
top_keywords = [c for c in sorted_targeting if c[0][0] == 'Keywords'][:10]
top_look_alikes = [c for c in sorted_targeting if c[0][0] == 'Follower look-alikes'][:10]
top_conversation_topics = [c for c in sorted_targeting if c[0][0] == 'Conversation topics'][:10]

print('Top interests: ')
pprint(top_interests)
print()
print('Top keywords: ')
pprint(top_keywords)
print()
print('Top look alikes: ')
pprint(top_look_alikes)
print()
print('Top conversation topics: ')
pprint(top_conversation_topics)
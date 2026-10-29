#!/usr/bin/env python3
"""Fetch publicly available deal RSS; reported prices are NOT retailer-verified."""
import json,re,html,urllib.request,xml.etree.ElementTree as ET,datetime,pathlib
ROOT=pathlib.Path(__file__).parent
FEEDS={
 'Slickdeals Frontpage':'https://slickdeals.net/newsearch.php?mode=frontpage&searcharea=deals&searchin=first&rss=1',
 'Slickdeals Hot Deals':'https://slickdeals.net/newsearch.php?searchin=first&forumchoice%5B%5D=9&rss=1',
 'Slickdeals Freebies':'https://slickdeals.net/newsearch.php?searchin=first&forumchoice%5B%5D=54&rss=1',
}
KEYWORDS={
 'Kitchen Appliances':r'\b(air fryer|blender|mixer|toaster|microwave|dishwasher|espresso|coffee maker|kettle|instant pot|rice cooker|refrigerator|freezer|oven|cookware|vacuum sealer)\b',
 'Furniture':r'\b(sofa|couch|sectional|desk|dresser|bookshelf|bookcase|bed frame|nightstand|dining table|chair|recliner|mattress|cabinet|sideboard|furniture)\b',
 'Electronics':r'\b(tv|television|monitor|laptop|tablet|ipad|iphone|headphones|earbuds|speaker|router|camera|smart home|ssd|gaming|computer|projector|security camera)\b',
 'Home Goods':r'\b(rug|curtain|bedding|pillow|blanket|lamp|lighting|storage|organizer|decor|décor|towel|vacuum|cleaner|mop|humidifier|fan|sheets|comforter|kitchen|bathroom|home|patio|garden|christmas)\b',
}
def classify(title,source):
 if 'freebie' in source.lower() or re.search(r'\b(freebie|free sample|completely free|free after rebate|100% off)\b',title,re.I):return 'Freebies'
 for cat,pattern in KEYWORDS.items():
  if re.search(pattern,title,re.I):return cat
 return None

def load_feed(source,url):
 req=urllib.request.Request(url,headers={'User-Agent':'DealRadarPersonal/1.0 (RSS reader)'})
 with urllib.request.urlopen(req,timeout=18) as response: raw=response.read(3_000_000)
 root=ET.fromstring(raw)
 result=[]
 for item in root.findall('.//item')[:120]:
  title=html.unescape(' '.join((item.findtext('title') or '').split()))
  category=classify(title,source)
  if not category:continue
  link=(item.findtext('link') or '').strip()
  if not link.startswith('https://'):continue
  prices=re.findall(r'(?<!\w)\$([\d,]+(?:\.\d{1,2})?)',title)
  price=float(prices[0].replace(',','')) if prices else None
  if price is not None and price>100000:price=None
  in_store=bool(re.search(r'in.store|pickup only|ymmv|clearance',title,re.I))
  result.append({'id':link,'title':title,'store':'Reported on '+source,'source':source,'category':category,'channel':'in-store' if in_store else 'online','location':'Store varies — verify locally' if in_store else '', 'price':price,'original':0,'url':link,'status':'unverified','notes':'Community-reported deal; price, stock and eligibility not verified.','created':int(datetime.datetime.now(datetime.timezone.utc).timestamp()*1000)})
 return result

def main():
 all_deals=[];errors=[]
 for source,url in FEEDS.items():
  try:
   deals=load_feed(source,url);all_deals.extend(deals);print(source,len(deals))
  except Exception as exc:errors.append(f'{source}: {exc}')
 # Preserve last successful dataset on complete failure.
 if not all_deals:
  print('No feeds succeeded; existing deals.json preserved',errors)
  return
 unique=list({d['id']:d for d in all_deals}.values())
 payload={'updated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_type':'community-reported RSS','errors':errors,'deals':unique}
 (ROOT/'deals.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
 print('Saved',len(unique),'deals',errors)
if __name__=='__main__':main()

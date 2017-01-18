import json
import urllib

url = "https://www.youtube.com/watch?v=34Na4j8AVgA"
api_url = "https://count.donreach.com/?url=" + url

response = urllib.urlopen(api_url).read()
data = json.loads(response)
print data

total_shares = data['total']
google_shares = data['shares']['google']
facebook_shares = data['shares']['facebook']
linkedin_shares = data['shares']['linkedin']
pinterest_shares = data['shares']['pinterest']

print 'total shares' , total_shares
print 'google_shares' , google_shares
print 'facebook_shares' , facebook_shares
print 'linkedin shares' , linkedin_shares
print 'pinterest shares' , pinterest_shares

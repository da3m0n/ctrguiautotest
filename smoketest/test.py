import makeHTML
import RSS

t = makeHTML.Part()

pageTitle = 'Mimsy Were the Borogoves'
mimsyLink = t.addPart('a', content="Mimsy Were the Borogoves",
                             attributes={'href': 'http://www.hoboes.com/Mimsy/'})

pageHead = t.addPart('head')
pageHead.addPart('title', content=pageTitle)
pageHead.addPart(makeHTML.styleSheet('stylesheet'))

pageBody = t.addPart('body')
pageBody = makeHTML.body(pageTitle)
pageBody.addPart(content="This is an RSS feed from " + mimsyLink.make() + ".")
pageBody.addPiece(makeHTML.headline("Latest Headlines from Mimsy"))

feed = RSS.TrackingChannel()
feed.parse('http://www.hoboes.com/Mimsy/?RSS')

entries = makeHTML.part("dl")
for article in feed.listItems():
    articleURL = article[0]
    articleData = feed.getItem(article)
    articleTitle = articleData.get((RSS.ns.rss10, 'title'))
    articleDescription = articleData.get((RSS.ns.rss10, 'description'))
    articleLink = makeHTML.part('a', content=articleTitle, attributes={'href': articleURL})
    entryTitle = makeHTML.part("dt", content=articleLink)
    entryText = makeHTML.part("dd", content=articleDescription)
    entries.addPieces([entryTitle, entryText])

pageBody.addPiece(entries)

fullPage = makeHTML.page([pageHead, pageBody])
fullPage.make()

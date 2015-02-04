var utils = (function () {

    function loadXMLDoc(filename) {
        var xhttp;

        if (window.ActiveXObject) {
            xhttp = new ActiveXObject("Msxml2.XMLHTTP");
        }
        else {
            xhttp = new XMLHttpRequest();
        }

        try {
            xhttp.open("GET", filename, false);
            xhttp.responseType = "msxml-document"
        } catch (err) {
            console.log("Missing file: " + filename);
        }
        xhttp.send("");

        return {
            response: xhttp.responseXML,
            responseType: xhttp.responseType,
            status: xhttp.status
        };
    }

    function getResult(filename) {
        var xml = loadXMLDoc(filename);

        if (xml.status == 404) {
            return false;
        }
        return xml;

    }

    function displayResult(xml, xsl, elementId) {
        var xsl = loadXMLDoc(xsl);
        // code for IE
        var xsltProcessor = new XSLTProcessor();
        if(xml.response === 'undefined'){
            console.log('XML needs to be loaded...');
        }
        if (xml) {
            xsltProcessor.importStylesheet(xsl.response);
            var resultDocument = xsltProcessor.transformToFragment(xml.response, document);
            document.getElementById(elementId).appendChild(resultDocument);
        } else {
            var p = document.createElement('div')
            document.getElementById(elementId).appendChild(p);
        }

    }

    function getSortedTestDates(file) {
        var xml = loadXMLDoc(file),
            xmldoc = xml.response,
            testDateTags = xmldoc.getElementsByTagName('testDate'),
            dates = [];

        for (var i = 0; i < testDateTags.length; i++) {
            var sortDate = testDateTags.item(i).attributes[1].nodeValue,
                date = testDateTags.item(i).attributes[0].nodeValue;

            dates.push({'sortDate': sortDate, 'date': date});
        }

        dates.sort(function (a, b) {
            return b.sortDate - a.sortDate;
        });

        return dates;
    }

    function loadNewResults(date) {
        displayResult(date, 'results.xsl', 'tests');
    }

    function loadAndDisplayPage(allTests, testDates) {

        var sortedDates = getSortedTestDates("logs/testDates.xml");
        var data = getResult(testDates);
        displayResult(data, "dates2.xsl", "dates");

        for (var testi in allTests) {
            var test = allTests[testi];
            var latest = sortedDates[0];

            var newDate = latest.date.split(' ').join('_');
            var newDateXml = newDate + '.xml';
            var data = getResult("logs/" + newDate + "/" + test.dir + "/" + newDateXml);
            if (data) {
                displayResult(data, test.xslDoc, test.name);
            }
        }
    }

    function click(e) {
        var date = $(this).attr('href');
        e.preventDefault();
        $('#tests').empty();
        utils.loadNewResults(utils.getResult(date));
    }

    return {
        displayResult: displayResult,
        getSortedTestDates: getSortedTestDates,
        getResult: getResult,
        loadNewResults:loadNewResults,
        loadAndDisplayPage: loadAndDisplayPage
    };
})();
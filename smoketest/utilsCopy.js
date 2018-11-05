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
        if (xml) {
            xsltProcessor.importStylesheet(xsl.response);
            var resultDocument = xsltProcessor.transformToFragment(xml.response, document);
            document.getElementById(elementId).appendChild(resultDocument);
        } else {
            var p = document.createElement('div');
            document.getElementById(elementId).appendChild(p);
        }

    }

    function getIpAddresses(file) {
        var xml = loadXMLDoc(file),
            xmlDoc = xml.response,
            addressTags = xmlDoc.getElementsByTagName('ipAddress'),
            ipAddresses = [];

        for (var i = 0; i < addressTags.length; i++) {
            ipAddresses.push(addressTags[i].innerHTML);
        }

        return ipAddresses;
    }


    function getSortedTestDates(file) {
        var xml = loadXMLDoc(file),
            xmldoc = xml.response,
            testDateTags = xmldoc.getElementsByTagName('testDate'),
            dates = [];

        for (var i = 0; i < testDateTags.length; i++) {
            var sortDate = testDateTags.item(i).attributes[1].value,
                date = testDateTags.item(i).attributes[0].value;

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

    function loadAndDisplayPage(allTests, testDates, ipAddresses) {

        var sortedDates = getSortedTestDates(testDates);
        var data = getResult(testDates);
        displayResult(data, "dates2.xsl", "dates");

        var count = 0;
        for (var testi in allTests) {
            var test = allTests[testi];
            var latest = sortedDates[0];

            var newDate = latest.date.split(' ').join('_');
            var newDateXml = newDate + '.xml';
            // var data = getResult(test.xslDoc);

            var data = getResult("logs/" + newDate + "/" + test.dir + "/" + ipAddresses[count] + "/" + newDateXml);
            // var data = getResult("logs/" + newDate + "/" + test.dir);
            if (data) {
                displayResult(data, test.xslDoc, test.name);
            }
            count++;
        }

        for (var i = 0; i < ipAddresses.length; i++) {
            var address = ipAddresses[i];

        }
    }

    function findNode(node, searchName) {
        for(var index in node.children) {
            if(node.children[index].nodeName === searchName) {
                return node.children[index];
            }
        }
    }

    function doCountResults (node) {
        var msgs = [];
        for (var i = 0; i < node.children.length; i++) {
            var c = node.children[i];
            if (c.localName === 'error') {
                var msg = c.getAttribute('msg');
                if (msg !== '-') {
                    msgs.push(msg)
                }
            }
            console.log();
        }
        return {total: 1, errors: msgs.length > 0 ? 1 : 0, msg:msgs};
    }
    function getOverallResult() {
        var ipAddresses = getIpAddresses('ipAddresses.xml');
        var sortedDates = getSortedTestDates("logs/smoketestDates.xml");
        var result = [];
        var htmlResult = '<div>';

        // date -> test -> ip -> {total, errors}
        var res = {};
        sortedDates.forEach(function (date) {
            res[date.date] = res[date.date] || {};
            var dateMap = res[date.date];
            var newDate = date.date.split(' ').join('_');
            var newDateXml = date.date.split(' ').join('_') + '.xml';
            ipAddresses.forEach(function (ipAddress) {
                var xmlFile = "logs/" + newDate + "/" + 'smoketest' + "/" + ipAddress + "/" + newDateXml;
                var data = getResult(xmlFile);
                if (data) {
                    var node = findNode(data.response.children[0], 'errorCount');
                    var tests =  data.response.children[0];

                    for (var i = 0; i< tests.children.length; i++) {
                        var test = tests.children[i];
                        if (test.localName === 'testScreen') {
                            var testName = test.getAttribute('testScreen');
                            var screenMap = dateMap[testName] = dateMap[testName] || {};
                            screenMap[ipAddress] = doCountResults(test);

                        }

                    }
                    var pass = node.getAttribute('errorCount') === "1";
                    result.push(pass);
                }

            });
        });
        console.log("res", res);

        for (var dt in res) {
            let dayErrors = 0;
            let dayTotal = 0;
            var htmlTest = '';
            for (var test in res[dt]) {
                // htmlTest += '<h2>' + test+ '</h2>';
                for (var ip in res[dt][test]) {
                    htmlTest += '<h3>' + ip;

                    let result = res[dt][test][ip];
                    dayErrors += result.errors;
                    dayTotal += result.total;
                    if (result.errors) {
                        htmlTest += " Error"
                    }
                    else {
                        htmlTest += " Ok"
                    }
                    htmlTest +=  '</h3>'
                }
            }
            htmlResult += '<h1>' + dt + ' ' + dayErrors + '/' + dayTotal + '</h1>';
            htmlResult += htmlTest;

        }
        htmlResult += '</div>';

        return htmlResult;
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
        loadAndDisplayPage: loadAndDisplayPage,
        getIpAddresses: getIpAddresses,
        getOverallResult: getOverallResult
    };
})();
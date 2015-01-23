var utils = (function () {

            function loadXMLDoc(filename) {
                var xhttp;

                if (window.ActiveXObject) {
                    xhttp = new ActiveXObject("Msxml2.XMLHTTP");
                }
                else {
                    xhttp = new XMLHttpRequest();
                }
                xhttp.open("GET", filename, false);
                try {
                    xhttp.responseType = "msxml-document"
                } catch (err) {
                    console.log("Missing file");
                } // Helping IE11
                xhttp.send("");
//                return xhttp.responseXML;

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

            function displayResult(xml, xsl, elementId, hideIfNotPresent) {
                var xsl = loadXMLDoc(xsl);
                // code for IE
                    var xsltProcessor = new XSLTProcessor();
                    if (xml) {
                        xsltProcessor.importStylesheet(xsl.response);
                        var resultDocument = xsltProcessor.transformToFragment(xml.response, document);
                        document.getElementById(elementId).appendChild(resultDocument);
                    } else {
                        var p = document.createElement('div')
                        document.getElementById(elementId).appendChild(p);
                    }

            }

            function getLatestTest(file) {
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

            return {
                displayResult: displayResult,
                getLatestTest: getLatestTest,
                getResult: getResult
            };
        })();
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
                } // Helping IE11
                xhttp.send("");
//                return xhttp.responseXML;

                return {
                    response: xhttp.responseXML,
                    responseType: xhttp.responseType
                };
            }

            function displayResult(filename, xsl, elementId) {
                var xml = loadXMLDoc(filename),
                        xsl = loadXMLDoc(xsl);
                // code for IE
                if (window.ActiveXObject || xml.responseType === "msxml-document") {
                    document.getElementById(elementId).innerHTML = xml.response.transformNode(xsl.response);
                }
                // code for Chrome, Firefox, Opera, etc.
                else if (document.implementation && document.implementation.createDocument) {
                    var xsltProcessor = new XSLTProcessor();
                    xsltProcessor.importStylesheet(xsl.response);
                    var resultDocument = xsltProcessor.transformToFragment(xml.response, document);
                    document.getElementById(elementId).appendChild(resultDocument);
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
                getLatestTest: getLatestTest
            };
        })();
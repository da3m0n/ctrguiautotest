//goog.require();

let utils = (function () {

    function loadXMLDoc(filename) {
        return loadDoc(filename,"msxml-document")
    }

    function loadDoc(filename, type) {
        let xhttp;

        if (window.ActiveXObject) {
            xhttp = new ActiveXObject("Msxml2.XMLHTTP");
        }
        else {
            xhttp = new XMLHttpRequest();
        }

        try {
            xhttp.open("GET", filename, false);
            if (type) {
                xhttp.responseType = type;
             }
        } catch (err) {
            console.log("Missing file: " + filename);
        }
        xhttp.send("");

        return {
            response: xhttp.responseXML ? xhttp.responseXML : xhttp.responseText,
            responseType: xhttp.responseType,
            status: xhttp.status
        };
    }

    function getResult(filename) {
        let xml = loadXMLDoc(filename);

        if (xml.status === 404) {
            return false;
        }
        return xml;

    }

    function displayXMLResult(xml, xsl, elementId) {
        var xsl = loadXMLDoc(xsl);
        // code for IE
        let xsltProcessor = new XSLTProcessor();
        if (xml) {
            xsltProcessor.importStylesheet(xsl.response);
            let resultDocument = xsltProcessor.transformToFragment(xml.response, document);
            document.getElementById(elementId).appendChild(resultDocument);
        } else {
            let p = document.createElement('div');
            document.getElementById(elementId).appendChild(p);
        }

    }

    function getIpAddresses(file) {
        let xml = loadXMLDoc(file),
            xmlDoc = xml.response,
            addressTags = xmlDoc.getElementsByTagName('ipAddress'),
            ipAddresses = [];

        for (let i = 0; i < addressTags.length; i++) {
            ipAddresses.push(addressTags[i].innerHTML);
        }

        return ipAddresses;
    }

    let removeEmptyItemsFromArr = (arr) => {
        var newArr = [];

        for(var a in arr) {
            if(arr[a] !== "") {
                newArr.push(arr[a]);
            }
        }
        return newArr;
    }
    var monthMap = {
        'January' : 0,
        'February' : 1,
        'March': 2,
        'April' : 3,
        'May' : 4,
        'June': 5,
        'July': 6,
        'August': 7,
        'September': 8,
        'October': 9,
        'November': 10,
        'December': 11};

    let parseDate = (dStr) => {
        let parts = dStr.split('_');
        return new Date(parseInt(parts[2]), monthMap[parts[1]], parseInt(parts[0])).getTime();
    }

    let getTestRunInfo = (data) => {
        let runInfo = [];
        let runArrays = {};

        if(data !== undefined) {
            let splitDates = data.response.split('\n');
            let newDatesArr = removeEmptyItemsFromArr(splitDates);
            let runNumberArr = [];

            for (let d in newDatesArr) {
                let date = newDatesArr[d].split('/')[0];
                let runNumber = newDatesArr[d].split('/')[1];

                let runs = runArrays[date] = runArrays[date] || [];
                if (runs.length === 0) {
                    runInfo.push({date, runs})
                }
                runs.push (runNumber);
            }
        }
        runInfo.forEach(function (info) {
            info.runs.sort(function (x, y) {
                return parseInt(y) - parseInt(x);
            });

        })

        runInfo.sort(function (x, y) {
            return parseDate(y.date) - parseDate(x.date);
        });
        return runInfo;
    }

    function loadNewResults(date) {
        displayXMLResult("logs/smoketestDatesOrig.xml", 'results.xsl', 'tests');
//        display
    }

    function loadAndDisplayPage(allTests, testRunInfo) {

        let dates = [];

        let rootEle = document.getElementById('accordion');
        console.log('rootEle', rootEle);

        var count = 0;

        testRunInfo.forEach(function(obj){
            let defaultPanelEle = document.createElement("div");
            defaultPanelEle.setAttribute('class', 'panel panel-default');

            let panelHeadingEle = document.createElement("div");
            panelHeadingEle.setAttribute('class', 'panel-heading');

            let panelTitleEle = document.createElement("h4");
            panelTitleEle.setAttribute('class', 'panel-title');

            let anchorEle = document.createElement("a");
            anchorEle.setAttribute('data-toggle', 'collapse');
            anchorEle.setAttribute('data-parent', '#accordion');
            anchorEle.setAttribute('href', '#collapse' + count);

            let bodyPanelContainer = document.createElement('div');
            bodyPanelContainer.setAttribute('id', 'collapse' + count);
            bodyPanelContainer.setAttribute('class', 'panel-collapse');
            bodyPanelContainer.setAttribute('class', 'collapse');
            bodyPanelContainer.setAttribute('class', 'in');

            let tempEle = document.createElement('p');
            tempEle.innerHTML = 'HTML stands for HyperText Markup Language. HTML is the standard markup language for describing the structure of web pages.';

            defaultPanelEle.appendChild(panelHeadingEle);
            panelHeadingEle.appendChild(panelTitleEle);

            anchorEle.innerHTML = obj.date;
            panelTitleEle.appendChild(anchorEle);

            let panelBodyEle = document.createElement('div');
            panelBodyEle.setAttribute('class', 'panel-body');

            panelBodyEle.appendChild(tempEle);

            defaultPanelEle.appendChild(bodyPanelContainer);
            bodyPanelContainer.appendChild(panelBodyEle);




//            let ulEle = document.createElement('ul');
//            obj.runs.forEach(function(run) {
//                console.log('run', run);
//                let liEle = document.createElement('li');
//                liEle.innerHTML = run;
//
//                let numRunPanel = document.createElement('div');
//                numRunPanel.setAttribute('id', 'collapse' + count);
//                numRunPanel.setAttribute('data-parent', '#accordion');
//                numRunPanel.setAttribute('class', 'panel-collapse collapse in');
//
////                defaultPanelEle.appendChild(numRunPanel);
////                let runEle = document.createElement('div');
////                runEle.setAttribute('class', 'runNumber');
//
////                panelBodyEle.innerHTML = run;
////                defaultPanelEle.appendChild(panelBodyEle);
//            })

            dates.push(obj.date);

            rootEle.appendChild(defaultPanelEle);
            count++;
        });

//        let doc = loadDoc("logs/smoketestDates2.xml");
//        displayXMLResult(doc, "dates2.xsl", "dates");
    }

    function findNode(node, searchName) {
        for(let index in node.children) {
            if(node.children[index].nodeName === searchName) {
                return node.children[index];
            }
        }
    }

    function doCountResults (node) {
        let msgs = [];
        for (let i = 0; i < node.children.length; i++) {
            let c = node.children[i];
            if (c.localName === 'error') {
                let msg = c.getAttribute('msg');
                if (msg !== '-') {
                    msgs.push(msg)
                }
            }
            console.log();
        }
        return {total: 1, errors: msgs.length > 0 ? 1 : 0, msg:msgs};
    }

    function getOverallResult(runInfo) {
        let result = [];
        let htmlResult = '<div>';

        runInfo.forEach(function (obj) {
//            console.log('q', obj);


        });
        htmlResult += "<h1> This is a test" + "</h1>";
        htmlResult += "</div>";

        return htmlResult;

    }

    function getOverallResult2(runInfo) {
//        let sortedDates = getSortedTestDates("logs/runDates.txt");

//        let sortedDates = readTextFile("logs/runDates.txt");


        let result = [];
        let htmlResult = '<div>';

        // date -> test -> ip -> {total, errors}
        let res = {};
        sortedDates.forEach(function (date) {
            res[date.date] = res[date.date] || {};
            let dateMap = res[date.date];
            let newDate = date.date.split(' ').join('_');
            let newDateXml = date.date.split(' ').join('_') + '.xml';
            let ipAddresses = getIpAddresses('ipAddresses.xml');
            ipAddresses.forEach(function (ipAddress) {
                let xmlFile = date.outputDir + "/" + ipAddress + "/" + newDateXml;
                let data = getResult(xmlFile);
                console.log("xml", data);
                if (data) {
                    let node = findNode(data.response.children[0], 'errorCount');
                    let tests =  data.response.children[0];

                    for (let i = 0; i< tests.children.length; i++) {
                        let test = tests.children[i];
                        if (test.localName === 'testScreen') {
                            let testName = test.getAttribute('testScreen');
                            let screenMap = dateMap[testName] = dateMap[testName] || {};
                            screenMap[ipAddress] = doCountResults(test);
                        }
                    }
                    let pass = node.getAttribute('errorCount') === "1";
                    result.push(pass);
                }
            });
        });
        console.log("res", res);

        for (let dt in res) {
            let dayErrors = 0;
            let dayTotal = 0;
            let htmlTest = '';
            for (let test in res[dt]) {
                // htmlTest += '<h2>' + test+ '</h2>';

                for (let ip in res[dt][test]) {
                    console.log("dt", res[dt][test][ip])
                    let result = res[dt][test][ip];
                    dayErrors += result.errors;
                    dayTotal += result.total;

                    if (result.errors) {
                        htmlTest += '<h5>' + ip;
                        htmlTest += " " + test + " Error"
                        htmlTest +=  '</h5>'
                    }
                }
            }
            htmlResult += '<h1>' + dt + ' ' + dayErrors + '/' + dayTotal + '</h1>';
            htmlResult += htmlTest;

        }
        htmlResult += '</div>';

        return htmlResult;
    }

    function click(e) {
        let date = $(this).attr('href');
        e.preventDefault();
        $('#tests').empty();
        utils.loadNewResults(utils.getResult(date));
    }

    return {
//        displayXMLResult: displayXMLResult,
//        getSortedTestDates: getSortedTestDates,
        getResult: getResult,
        loadNewResults:loadNewResults,
        loadAndDisplayPage: loadAndDisplayPage,
        getIpAddresses: getIpAddresses,
        getOverallResult: getOverallResult,
        getTestRunInfo: getTestRunInfo,
        loadDoc: loadDoc
    };
})();
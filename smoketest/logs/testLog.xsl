<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <!--<div id="resultsContainer">-->
        <!--test-->
        <!--</div>-->

        <div id="header">
            <div class="container4">
                <div class="container3">
                    <div class="container2">
                        <div class="container1">
                            <div class="col1">Test Screen</div>
                            <div class="col2">Test Name</div>
                            <div class="col3">Result</div>
                            <div class="col4">Reason</div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div class="items">
            <div class="container4">
                <div class="container3">
                    <div class="container2">
                        <div class="container1">
                            <div class="col1">
                                <xsl:for-each select="smoketests/testName">
                                    <xsl:value-of select="@testName"/>
                                </xsl:for-each>
                            </div>
                            <div class="col2">Test Name</div>
                            <div class="col3">Result</div>
                            <div class="col4">Reason</div>
                        </div>
                    </div>
                </div>

            </div>
        </div>

        <div id="footer">footer</div>

        <br/>
        <div id="resultsTable">
            <table border="1">
                <tr bgcolor="#9acd32">
                    <th>Test Screen</th>
                    <th>Test Name</th>
                    <th>Result</th>
                    <th>Reason</th>
                </tr>
                <xsl:for-each select="smoketests/testScreen">
                    <tr>
                        <td>
                            <xsl:value-of select="@testScreen"/>
                        </td>
                        <td>
                            <xsl:value-of select="error/@testName"/>
                        </td>
                        <td>
                            <xsl:choose>
                                <xsl:when test="string-length(error/@msg) > 0">
                                    Fail
                                </xsl:when>
                                <xsl:otherwise>
                                    Pass
                                </xsl:otherwise>
                            </xsl:choose>
                        </td>
                        <td>
                            <xsl:value-of select="error/@msg"/>
                        </td>
                    </tr>
                </xsl:for-each>

            </table>
        </div>
    </xsl:template>
</xsl:stylesheet>
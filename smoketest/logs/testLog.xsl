<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <!--<div id="resultsContainer">-->
        <!--test-->
        <!--</div>-->

        <div id="resultsTable">
            <table border="1">
                <tr>
                    <th>Test Screen</th>
                    <th>Test Name</th>
                    <th>Result</th>
                    <th>Reason</th>
                </tr>
                <xsl:for-each select="smoketests/testScreen">
                    <tr>
                        <td class="testScreenName">
                            <xsl:value-of select="@testScreen"/>
                        </td>
                        <td>
                            <!--<xsl:value-of select="error/@testName"/>-->
                            <ul>
                                <xsl:for-each select="error">
                                    <li>
                                        <div class="testName">
                                            <xsl:choose>
                                                <xsl:when test="string-length(@msg) > 1">
                                                    <span class="fail">
                                                        <xsl:value-of select="@testName"/>
                                                    </span>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <span class="pass"><xsl:value-of select="@testName"/></span>
                                                </xsl:otherwise>
                                            </xsl:choose>

                                        </div>
                                    </li>
                                </xsl:for-each>
                            </ul>

                        </td>
                        <td>
                            <ul>
                                <xsl:for-each select="error">
                                    <li>
                                        <div class="testName">
                                            <xsl:choose>
                                                <xsl:when test="string-length(@msg) > 1">
                                                    <span class="fail">Fail</span>
                                                </xsl:when>
                                                <xsl:otherwise>
                                                    <span class="pass">Pass</span>
                                                </xsl:otherwise>
                                            </xsl:choose>

                                        </div>
                                    </li>
                                </xsl:for-each>
                            </ul>
                        </td>
                        <td>
                            <ul>
                                <xsl:for-each select="error">
                                    <li>
                                        <div class="testName">
                                            <xsl:value-of select="@msg"/>
                                        </div>
                                    </li>
                                </xsl:for-each>
                            </ul>

                        </td>
                    </tr>
                </xsl:for-each>

            </table>
        </div>
        <!--<div id="footer">footer</div>-->

    </xsl:template>
</xsl:stylesheet>
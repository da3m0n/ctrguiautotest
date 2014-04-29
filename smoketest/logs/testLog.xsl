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
                            <ul>
                                <xsl:for-each select="error">
                                    <xsl:choose>
                                        <xsl:when test="string-length(@msg) > 1">
                                            <li class="fail">
                                                <xsl:value-of select="@testName"/>
                                            </li>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <li class="pass">
                                                <xsl:value-of select="@testName"/>
                                            </li>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>
                            </ul>

                        </td>
                        <td>
                            <ul>
                                <xsl:for-each select="error">
                                    <xsl:choose>
                                        <xsl:when test="string-length(@msg) > 1">
                                            <li class="fail">Fail</li>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <li class="pass">Pass</li>
                                        </xsl:otherwise>
                                    </xsl:choose>
                                </xsl:for-each>
                            </ul>
                        </td>
                        <td>
                            <ul>
                                <xsl:for-each select="error">
                                    <xsl:choose>
                                        <xsl:when test="string-length(@msg) > 1">
                                            <li class="fail">
                                                <xsl:value-of select="@msg"/>
                                            </li>
                                        </xsl:when>
                                        <xsl:otherwise>
                                            <li class="pass">
                                                <xsl:value-of select="@msg"/>
                                            </li>
                                        </xsl:otherwise>
                                    </xsl:choose>
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
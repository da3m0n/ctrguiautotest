<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <!--<div id="resultsContainer">-->
        <!--test-->
        <!--</div>-->


        <div id="datesContainer">
            <div class="heading">Tests Dates</div>
            <div id="dates">
                <xsl:for-each select="resultsFiles/testDate">
                <ul>
                    <li><xsl:value-of select="@date"></xsl:value-of></li>
                    <li>
                        <ul>
                            <li><a href=""><xsl:value-of select="fileName/@file"></xsl:value-of></a></li>
                            <xsl:for-each select="screenshots/screenshot">
                                <li><a href=""><xsl:value-of select="@error"></xsl:value-of></a></li>
                            </xsl:for-each>
                        </ul>

                    </li>
                </ul>
                </xsl:for-each>
            </div>
        </div>
        <!--<div id="footer">footer</div>-->

    </xsl:template>
</xsl:stylesheet>
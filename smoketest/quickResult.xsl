<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <xsl:for-each select="resultsFiles/testDate">
            <xsl:value-of select="errors/@totalErrors"/>

            <!--@todo add a new xml file to return just the last result-->
            <!--<xsl:choose>-->
            <!--<xsl:when test="errors/@totalErrors &gt; 0">-->
            <!--<h1>Fail</h1>-->
            <!--</xsl:when>-->
            <!--<xsl:otherwise>-->
            <!--<h1>Pass</h1>-->
            <!--</xsl:otherwise>-->
            <!--</xsl:choose>-->
        </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>

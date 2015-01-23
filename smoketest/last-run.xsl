<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <h5>Last test run at
            <xsl:value-of select="tests/allTestsStart/@allTestsStart"></xsl:value-of>
            <xsl:choose>
                <xsl:when test="@allTestsStart != ''">Nothing here</xsl:when>
                <xsl:otherwise>test run</xsl:otherwise>
            </xsl:choose>
        </h5>
    </xsl:template>
</xsl:stylesheet>

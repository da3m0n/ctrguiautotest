<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <div class="progress">
            <xsl:variable name="totalScreenCount">
                <xsl:value-of select="tests/totalScreens/@totalScreenCount"></xsl:value-of>
            </xsl:variable>
            <xsl:variable name="totalTestsCount">
                <xsl:value-of select="tests/totalTestCount/@totalTestCount"></xsl:value-of>
            </xsl:variable>
            <xsl:variable name="coveragePercentage">
                <xsl:value-of select="tests/coveragePercentage/@coveragePercentage"></xsl:value-of>
            </xsl:variable>

            <div class="progress-bar" role="progressbar" aria-valuenow="{$totalTestsCount}" aria-valuemin="0"
                 aria-valuemax="{$totalScreenCount}"
                 style="width: {$coveragePercentage};">
                <xsl:value-of select="tests/coveragePercentage/@coveragePercentage"></xsl:value-of>
            </div>
        </div>

    </xsl:template>
</xsl:stylesheet>
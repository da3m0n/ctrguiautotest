<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <div class="progress">
            <xsl:element name="a">
                <xsl:attribute name="href">
                    <xsl:value-of select="fileName/@fileurl"/>

                </xsl:attribute>
                <xsl:attribute name="class">datesListener
                    <!--<xsl:value-of select="@date"/>-->
                </xsl:attribute>
                <xsl:value-of select="fileName/@file"/>
            </xsl:element>


            <xsl:variable name="TotalScreenCount">
                <xsl:value-of select="smoketests/totalTestCount/@totalTestCount"></xsl:value-of>
            </xsl:variable>
            <div class="progress-bar" role="progressbar" aria-valuenow="60" aria-valuemin="0"
                 aria-valuemax="{$TotalScreenCount}"
                 style="width: 10%;">
                <xsl:value-of select="smoketests/totalTestCount/@totalScreenCount"></xsl:value-of>

            </div>
        </div>

        <div>
            <xsl:value-of select="smoketests/totalTestCount/@totalTestCount"></xsl:value-of>
            of
            <xsl:value-of select="smoketests/totalScreens/@totalScreens"></xsl:value-of>
        </div>

    </xsl:template>
</xsl:stylesheet>
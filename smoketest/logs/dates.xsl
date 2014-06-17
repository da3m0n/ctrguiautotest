<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <div class="row">
            <h3>
                Dates
            </h3>
        </div>

        <div class="panel-group" id="accordion">
            <xsl:for-each select="resultsFiles/testDate">
                <div class="panel panel-default">
                    <div class="panel-heading">

                        <h4 class="panel-title">
                            <a data-toggle="collapse" data-parent="#accordion" href="#{generate-id(@date)}">
                                <xsl:value-of select="@date"></xsl:value-of>
                            </a>
                        </h4>
                    </div>
                    <div id="{generate-id(@date)}" class="panel-collapse collapse">
                        <div class="panel-body artifacts">
                            <ul>
                                <li>
                                    <!--<xsl:variable name="test">-->
                                        <!--<xsl:value-of select="fileName/@file"></xsl:value-of>-->
                                    <!--</xsl:variable>-->
                                    <!--<a href="{@date}/$test">-->
                                        <!--<xsl:value-of select="fileName/@file"></xsl:value-of>-->
                                    <!--</a>-->
                                    <xsl:element name="a">
                                        <xsl:attribute name="href">
                                            <xsl:value-of select="fileName/@file"/>
                                        </xsl:attribute>
                                        <xsl:value-of select="fileName/@file"/>
                                    </xsl:element>

                                </li>
                                <xsl:for-each select="screenshots/screenshot">
                                    <li>
                                        <xsl:element name="a">
                                            <xsl:attribute name="href">
                                                <xsl:value-of select="@url"/>
                                            </xsl:attribute>
                                            <xsl:value-of select="@error"/>
                                        </xsl:element>
                                        <!--<a href="{@date}">-->
                                            <!--<xsl:value-of select="@error"></xsl:value-of>-->
                                        <!--</a>-->
                                    </li>
                                </xsl:for-each>
                            </ul>
                        </div>
                    </div>
                </div>
            </xsl:for-each>
        </div>
    </xsl:template>
</xsl:stylesheet>
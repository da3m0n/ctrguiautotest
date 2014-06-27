<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <div class="row">
            <h3>
                Dates
            </h3>
        </div>

        <!--<xsl:for-each select="resultsFiles/testDate">-->
        <!--<div id="test">blah-->
                <!--<xsl:value-of select="@sortDate"></xsl:value-of>-->
        <!--</div>-->

        <!--</xsl:for-each>-->

        <div class="panel-group" id="accordion">
            <xsl:for-each select="resultsFiles/testDate">
            <xsl:sort select="@sortDate" data-type="number" order="descending"/>
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
                                    <xsl:element name="a">
                                        <xsl:attribute name="href">
                                            <xsl:value-of select="fileName/@fileurl"/>
                                        </xsl:attribute>
                                        <xsl:attribute name="class">clicktest
                                            <!--<xsl:value-of select="@date"/>-->
                                        </xsl:attribute>
                                        <xsl:value-of select="fileName/@file"/>
                                    </xsl:element>

                                </li>
                                <xsl:for-each select="screenshots/screenshot">
                                    <li>
                                        <xsl:element name="a">
                                            <xsl:attribute name="href">
                                                <xsl:value-of select="@imageurl"/>
                                            </xsl:attribute>
                                        <xsl:attribute name="data-lightbox">
                                            <xsl:value-of select="@error"/>
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
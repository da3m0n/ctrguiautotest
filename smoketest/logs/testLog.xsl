<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <body>
                <table border="1">
                    <tr bgcolor="#9acd32">
                        <th style="text-align:left">Test Name</th>
                        <th style="text-align:left">Heading 1</th>
                    </tr>
                    <xsl:for-each select="smoketests/testName">
                        <tr>
                            <td>
                                <xsl:value-of select="@testName"/>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <xsl:value-of select="startTime/@name"/>
                            </td>
                        </tr>
                    </xsl:for-each>

                </table>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
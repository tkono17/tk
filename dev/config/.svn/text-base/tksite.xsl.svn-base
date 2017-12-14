<xsl:stylesheet 
   xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
   version="1.0">

  <xsl:output method="html" encoding="UTF-8"/>

  <xsl:param name="site-top"></xsl:param>

  <xsl:template match="@*|node()">
    <xsl:copy>
      <xsl:apply-templates select="@*|node()"/>
    </xsl:copy>
  </xsl:template>

  <xsl:template match="html">
    <html>
      <xsl:apply-templates/>
    </html>
  </xsl:template>

  <xsl:template match="head">
    <head>
      <link>
	<xsl:attribute name="rel">stylesheet</xsl:attribute>
	<xsl:attribute name="type">text/css</xsl:attribute>
	<xsl:attribute name="href"><xsl:value-of select="$site-top"/>/utils/tkstyle.css</xsl:attribute>
      </link>
      <script>
	<xsl:attribute name="type">text/javascript</xsl:attribute>
	<xsl:attribute name="src"><xsl:value-of select="$site-top"/>/utils/jquery.js</xsl:attribute>
      </script>
      <xsl:apply-templates/>
    </head>
  </xsl:template>

  <xsl:template match="body">
    <body>
      <div class="fullpage">
	<div class="header">
	  <h2><xsl:value-of select="../head/title"/></h2>
	</div>
	<div class="menu">
	</div>
	<xsl:apply-templates/>
	<div class="footer">
	</div>
      </div>
    </body>
  </xsl:template>

</xsl:stylesheet>


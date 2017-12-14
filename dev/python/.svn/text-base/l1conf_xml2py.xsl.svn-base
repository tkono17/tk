<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:op="http://www.w3.org/TR/xquery-functions"
  xmlns:fo="http://www.w3.org/1999/XSL/Format"
  xmlns="http://www.w3.org/1999/xhtml">

  <xsl:output method="xml" encoding="ISO-8859-1"/>

  <xsl:template match="/">
tm = TriggerPythonConfig('hlt.xml', 'lvl1.xml')
    <xsl:apply-templates select="//TriggerThreshold"/>
  </xsl:template>

  <xsl:template match="TriggerThreshold">
tm.addLvl1Threshold('<xsl:value-of select="@name"/>')
  </xsl:template>
  
  <xsl:template match="TriggerThresholdValue">
  </xsl:template>

</xsl:stylesheet>

<?xml version="1.0" encoding="UTF-8"?>
  <xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:oe="http://schemas.dmtf.org/ovf/environment/1">
    <xsl:output method="text" indent="no"/>
    <xsl:template match="/">
    <xsl:for-each select="oe:Environment/oe:PropertySection/oe:Property">
      <xsl:text>export ovf_</xsl:text>
      <xsl:value-of select="@oe:key"/>
      <xsl:text>=&quot;</xsl:text>
      <xsl:value-of select="@oe:value"/>
      <xsl:text>&quot;&#xa;</xsl:text>
    </xsl:for-each>
  </xsl:template>
</xsl:stylesheet>

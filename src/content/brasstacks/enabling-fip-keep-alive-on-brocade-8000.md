---
title: "Enabling FIP Keep Alive on Brocade 8000"
pubDate: 2011-06-24
postedAt: "08:38 AM"
description: "I received a question from a colleague in Singapore yesterday asking about the D bit in FIP FKA_ADV_Period Descriptor. Apparently, a customer was wondering if it could be changed from “one” to \"zero\" on a Brocade 8000 switch. A portion of the customer's email is shown below: The Discovery Advertisement..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2011/06/enabling-fip-keep-alive-on-brocade-8000.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250912181305/https://brasstacksblog.typepad.com/brass-tacks/2011/06/enabling-fip-keep-alive-on-brocade-8000.html"
pdf: "/brasstacks/enabling-fip-keep-alive-on-brocade-8000/enabling-fip-keep-alive-on-brocade-8000.pdf"
comments: []
---

<p>I received a question from a colleague in Singapore yesterday asking about the D bit in FIP&#0160;FKA_ADV_Period Descriptor.&#0160; Apparently, a customer was wondering if it could be changed from “one” to &quot;zero&quot;&#0160;on a Brocade 8000 switch.</p>
<p>A portion of the customer&#39;s email is shown below:</p>
<p><span style="color: #0060bf;"><em>The Discovery Advertisement frame received from the switch has the “D” bit set to 1. This seems to be disabling the FIP Keep Alive frames.&#0160; We would like to have these Keep Alive frames. What can we do to modify the current behavior?</em></span></p>
<p><span style="color: #0060bf;"><em>FYI, according to the standard</em></span></p>
<p><span style="color: #0060bf;"><em><a href="http://www.t11.org/ftp/t11/pub/fc/bb-5/09-056v5.pdf%20Table%2041%20FIP%20FKA_ADV_Period%20descriptor%20format">http://www.t11.org/ftp/t11/pub/fc/bb-5/09-056v5.pdf Table 41 FIP FKA_ADV_Period descriptor format</a></em></span></p>
<p><span style="color: #0060bf;"><em>7.8.6.3.13 FIP FKA_ADV_Period descriptor</em><em></em></span></p>
<p><span style="color: #0060bf;"><em>D: the value of the D bit shall be administratively configurable on FCFs. The D bit shall be set to zero unless administratively set to one. VE_Port capable FCF-MACs shall ignore the value of the D bit provided in received Discovery Advertisements. ENode MACs shall process the value of the D bit provided in received Discovery Advertisements.</em><em></em></span></p>
<p><span style="color: #0060bf;"><em>When the D bit is set to zero, the receiving ENode MAC shall verify periodic reception of Discovery Advertisements and shall transmit periodic ENode FIP Keep Alive and VN_Port FIP Keep Alive frames as specified in 7.8.5.2. The VF_Port capable FCF-MAC shall verify periodic reception of ENode FIP Keep Alive and VN_Port FIP Keep Alive frames as specified in 7.8.5.2.</em></span></p>
<p>My response was:</p>
<p>Hi, you can display the FIP configuration settings by using the “<strong>fcoe --fipcfgshow</strong>” command.</p>
<p><span style="color: #0000bf;">----Example----</span></p>
<p><span style="color: #0000bf;">Elara_IOP05472_AG:admin&gt; <strong>fcoe --fipcfgshow</strong></span></p>
<p><span style="color: #0000bf;">FIP Unsolicited Advertisement Interval = 8</span></p>
<p><span style="color: #0000bf;"><strong>FIP Keep Alive Timeout Disabled.</strong></span></p>
<p><span style="color: #0000bf;">========================================</span></p>
<p><span style="color: #0000bf;">VLAN&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; fcmap</span></p>
<p><span style="color: #0000bf;">========================================</span></p>
<p><span style="color: #0000bf;">1002&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; 0x0efc00 [Default fcmap]</span></p>
<p><span style="color: #0000bf;">========================================</span></p>
<p><span style="color: #0000bf;">Elara_IOP05472_AG:admin&gt;</span></p>
<p><span style="color: #0000bf;">&#0160;--------</span></p>
<p>You can configure the FIP FKA-adv-period (shown above as <strong>FIP Keep Alive Timeout Disabled.</strong>) using the “<strong>fcoe --fipcfg -advinterval &lt;value&gt;</strong>&quot; command.</p>
<p><span style="color: #0000bf;">----Example----&#0160;</span></p>
<p><span style="color: #0000bf;">Elara_IOP05472_AG:admin&gt; <strong>fcoe --fipcfg -advintvl 8</strong></span></p>
<p><span style="color: #0000bf;">FIP Unsolicited Advertisement Interval is set to = 8</span></p>
<p><span style="color: #0000bf;">Elara_IOP05472_AG:admin&gt; <strong>fcoe --fipcfgshow</strong></span></p>
<p><span style="color: #0000bf;">FIP Unsolicited Advertisement Interval = 8</span></p>
<p><span style="color: #0000bf;"><strong>FIP Keep Alive Timeout Enabled. FKA_ADV_PERIOD = 8</strong></span></p>
<p><span style="color: #0000bf;">========================================</span></p>
<p><span style="color: #0000bf;">VLAN&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; fcmap</span></p>
<p><span style="color: #0000bf;">========================================</span></p>
<p><span style="color: #0000bf;">1002&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160;&#0160; 0x0efc00 [Default fcmap]</span></p>
<p><span style="color: #0000bf;">========================================</span></p>
<p><span style="color: #0000bf;">Elara_IOP05472_AG:admin&gt;</span></p>
<p><span style="color: #0000bf;">--------&#0160;</span></p>
<p>Thanks for reading!</p>

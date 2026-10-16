---
title: "FC/FCoE Connectivity options as of 11/3/2011"
pubDate: 2011-10-27
postedAt: "01:04 PM"
description: "Well…we’ve been talking about it since EMC World in May and on November 3rd EMC will officially release support for a Director Class Multi-Hop FCoE solution! More specifically, we will be adding the Cisco Nexus 7000 and FCoE support for the Cisco MDS 95xx to the November EMC Support Matrix..."
originalUrl: "https://brasstacksblog.typepad.com/brass-tacks/2011/10/fcfcoe-connectivity-options-as-of-1132011.html"
sources:
  - label: "Post and comments"
    url: "https://web.archive.org/web/20250913031128/https://brasstacksblog.typepad.com/brass-tacks/2011/10/fcfcoe-connectivity-options-as-of-1132011.html"
pdf: "/brasstacks/fcfcoe-connectivity-options-as-of-1132011/fcfcoe-connectivity-options-as-of-1132011.pdf"
comments:
  - author: "Victorforde"
    date: "10/28/2011 at 04:39 AM"
    html: |-
      <p>Great resource, thanks!  </p>
  - author: "Juan Tarrío (BRCD)"
    date: "01/11/2012 at 05:09 AM"
    html: |-
      <p>Just a comment: The Brocade DCX cannot be configured in AG mode. I see it in a couple of the configurations you&#39;re listing so I though I&#39;d point it out. Otherwise, this is a great resource, thanks for putting it together! :)</p>
  - author: "Erik Smith"
    date: "01/11/2012 at 09:52 AM"
    html: |-
      <p>Hi Juan, thanks for pointing that out!  I&#39;ve updated the graphics.</p>
      <p>Erik </p>
---

<p>Well…we’ve been talking about it since EMC World in May and&#0160;on November 3rd EMC will officially release support for a Director Class Multi-Hop FCoE solution!&#0160; More specifically, we will be adding the Cisco Nexus 7000 and FCoE support for the Cisco MDS 95xx to the November EMC Support Matrix (ESM).&#0160; We are also adding a case study to the EMC FCoE TechBook that will provide step-by-step installation instructions for a couple of different deployment options.&#0160; I’ll provide a link to the updated techbook once it’s posted.&#0160;</p>
<h2>Configuration rules</h2>
<p>The following configuration rules were used to create the topology diagrams.&#0160; If there is a discrepancy between the diagrams and the configuration rules, the configuration rules take precedence:</p>
<ol>
<li>The Nexus 2232 requires a connection to a Nexus 5000 in order to function.</li>
<li>The Nexus 2232 does not support native Fibre Channel ports.</li>
<li>The Nexus 4001i requires a connection to a Nexus 5000 in order to support FCoE.</li>
<li>The Nexus 4001i does not support native Fibre Channel ports.</li>
<li>The Nexus 7000 does not support native Fibre Channel ports.</li>
<li>The Fibre Channel ports on the Nexus 5000 cannot be used for end device connectivity while the switch is in NPV mode.</li>
<li>FC-SW interoperability between Brocade and Cisco is not supported.&#0160; When attaching a Brocade switch to a Cisco FCF and vice versa, either NPV mode must be used on the Cisco switch or AG mode must be used on the Brocade switch.</li>
<li>The Fibre Channel ports on the Brocade 8000 cannot be used for end device connectivity while the switch is in NPV mode.</li>
<li>All host connectivity to the UCS 6100 is via FCoE.</li>
<li>The Fibre Channel ports on the UCS 6100 cannot be used for end device connectivity while the switch is in NPV mode.</li>
<li>The UCS 6100 does not currently provide an FC zoning interface.&#0160; As a result, when the 6100 is running in FC-SW mode, it must be connected to another Cisco switch that is also running in switch mode.</li>
<li>Cascading switches that are running in NPV / AG mode is not supported.</li>
<li>The Nexus 4001i does not support external VN_Port connections</li>
<li><span style="color: #ff4040;">As of November 3rd 2011, EMC supports FCoE on the Nexus 7000&#0160;and MDS.</span></li>
<li>Storage ports cannot be connected to the Nexus 5000 while it is running in NPV mode.</li>
<li>The Brocade 8000 and DCX do not support VE_Ports</li>
<li>Cisco UCS does not currently support VE_Ports.</li>
<li>FCoE NPV uplinks between Cisco and Brocade switches are not supported.</li>
</ol>
<h2>Supported connectivity options:</h2>
<p>The supported connectivity options have been broken down into several categories with each category focusing on the connectivity options for a particular connectivity component.&#0160; The categories are:</p>
<ol>
<li>Configurations specific to Nexus 5000</li>
<li>Configurations specific to Nexus 2000</li>
<li>Configurations specific to Nexus 4001i</li>
<li>Configurations specific to Nexus 6100</li>
<li>Configurations specific to Nexus 7000</li>
<li>Configurations specific to MDS 95xx</li>
<li>Configurations specific to Brocade 8000 / DCX</li>
</ol>
<h3>Configurations specific to Nexus 5000:</h3>
<h3><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c015436736842970c.jpg" style="display: inline;"></a><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c0162fbf5437a970d.jpg" style="display: inline;"></a><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c01676059ee2c970b.jpg" style="display: inline;"></a><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c0162ff652b8d970d.jpg" style="display: inline;"><img alt="One" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0162ff652b8d970d image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c0162ff652b8d970d.jpg" title="One" /></a><br /><br /><em>Configurations specific to Nexus 2000:</em></h3>
<h3><em><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c0162fbf53ef6970d.jpg" style="display: inline;"><img alt="Two" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0162fbf53ef6970d image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c0162fbf53ef6970d.jpg" title="Two" /></a><br /></em><em>Configurations specific to Nexus 4001i:</em></h3>
<h3><em><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c0162fbf53f62970d.jpg" style="display: inline;"><img alt="Three" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0162fbf53f62970d image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c0162fbf53f62970d.jpg" title="Three" /></a><br /></em><em>Configurations specific to 6100:</em></h3>
<p><em><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c015436b426d7970c.jpg" style="display: inline;"><img alt="Four" border="0" class="asset  asset-image at-xid-6a013487ed263f970c015436b426d7970c image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c015436b426d7970c.jpg" title="Four" /></a><br /></em><em>Configurations specific to 7000:</em></p>
<h3><em><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c015436736f79970c.jpg" style="display: inline;"><img alt="Five" border="0" class="asset  asset-image at-xid-6a013487ed263f970c015436736f79970c image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c015436736f79970c.jpg" title="Five" /></a><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c0153929fcece970b.jpg" style="display: inline;"><br /></a></em><em>Configurations specific to MDS 95xx:</em></h3>
<h3><em><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c015436736c45970c.jpg" style="display: inline;"><img alt="Six" border="0" class="asset  asset-image at-xid-6a013487ed263f970c015436736c45970c image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c015436736c45970c.jpg" title="Six" /></a><br /></em><em>Configurations specific to Brocade 8000 / DCX:</em></h3>
<p><em><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c0162fbf541ed970d.jpg" style="display: inline;"></a></em></p>
<p><em><a href="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c0168e55ac102970c.jpg" style="display: inline;"><img alt="Seven" border="0" class="asset  asset-image at-xid-6a013487ed263f970c0168e55ac102970c image-full" src="/brasstacks/fcfcoe-connectivity-options-as-of-1132011/6a013487ed263f970c0168e55ac102970c.jpg" title="Seven" /></a><br /></em></p>
<p><em>Thanks for reading!</em></p>
<p><em>&#0160;Note: This post was updated on 11/7/2011 to correct one of the 6100 topologies.</em></p>
